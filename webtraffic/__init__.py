
# Std Lib
from collections import defaultdict
from csv import DictReader
from logging import getLogger

# Third-pary
from pandas import DataFrame
import requests as r
import xmltodict

LOG = getLogger(__name__)


class UserPageTimeAggregator():
    """Take statistic data and aggregate it across paths, per user.
    This could probably be done in one fell swoop with pandas, but
    streaming the files in seemed more memory-safe and I am not
    familiar enough with pandas facilities for that yet.

    @todo: Worry about the aggregate data set approaching memory limits
    """

    def __init__(self):
        self.data = {}

    def add_stat(self, stat):
        """Add statistic data to the lookup, keyed by user_id"""
        user_dict = self.data.get(stat["user_id"])
        if not user_dict:
            user_dict = defaultdict(lambda: 0)
            self.data[stat["user_id"]] = user_dict
        user_dict[stat["path"]] += int(stat["length"])

    def add_csv(self, csv):
        """Takes any iterable that DictReader can handle
        and aggregates data in the expected shape.
        """
        for row in DictReader(csv):
            self.add_stat(row)

    def dump_csv(self):
        """Dump a csv containing all path columns, with
        aggregate time-on-page as values, one row per user_id
        """
        df = DataFrame(self.data).transpose()
        df = df.fillna(0)
        df = df.rename_axis("user_id")
        df.index = df.index.astype(int)
        df.sort_index(inplace=True)
        return df.to_csv()


class S3DataLoader():
    """Uses requests to load S3 csv files as boto3 still
    doesn't support streaming responses by line:
    https://github.com/boto/botocore/pull/1055
    Also it requires valid credentials even for public
    bucket access.
    """

    def __init__(self, region, bucket):
        self.bucket = bucket
        self.region = region

    def list(self):
        """Return a list of objects in the bucket.
        @todo: Pagination if later required
        """
        url = self.__construct_bucket_url()
        try:
            res = r.get(url, timeout=5)
            res.raise_for_status()
        except r.HttpError as e:
            LOG.debug(repr(e))
            raise ValueError("Bucket not found or unavailable")
        except r.ConnectionError as e:
            LOG.debug(repr(e))
            raise ValueError("Unable to connect; bad bucket or region")
        try:
            objects = xmltodict.parse(res.text)
        except Exception as e:
            LOG.debug(repr(e))
            raise ValueError("Bad XML response received from bucket request")

        return [o["Key"] for o in objects["ListBucketResult"]["Contents"]]

    def load(self):
        """Loop through files in the bucket, generating an
        iterable stream for each."""
        for key in self.list():

            if not key.endswith(".csv"):
                LOG.info("Skipping key: {}".format(key))
                continue

            url = self.__construct_url(key)
            LOG.info("Requesting file at: {}".format(url))
            res = r.get(url, stream=True)
            if res.encoding is None:
                res.encoding = 'utf-8'
            yield res.iter_lines(decode_unicode=True)

    def __construct_url(self, key):
        return self.__construct_bucket_url() + "/{}".format(key)

    def __construct_bucket_url(self):
        if self.region == "us-east-1":
            url = "https://s3.amazonaws.com/{}".format(
                self.bucket)
        else:
            url = "https://s3-{}.amazonaws.com/{}".format(
                self.region, self.bucket)
        return url
