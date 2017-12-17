
# Std Lib
from collections import defaultdict
from csv import DictReader

# Third-pary
from boto3 import client
from botocore.exceptions import EndpointConnectionError
from pandas import DataFrame, Series
import requests as r


class UserPageTimeAggregator():

    def __init__(self):
        self.data = {}

    def add_stat(self, stat):
        """Add statistic data to the lookup, keyed by user_id"""
        user_dict = self.data.get(stat["user_id"])
        if not user_dict:
            user_dict = defaultdict(lambda: 0)
            user_dict["user_id"] = stat["user_id"]
            self.data[stat["user_id"]] = user_dict
        user_dict[stat["path"]] += stat["length"]

    def add_csv(self, csv):
        """Takes any iterable that DictReader can handle
        and aggregates data in the expected shape."""
        for row in DictReader(csv):
            self.add_stat(row)


class S3DataLoader():
    """Uses requests to load S3 csv files as boto3 still
    doesn't support streaming responses by line:
    https://github.com/boto/botocore/pull/1055
    """

    def __init__(self, region, bucket):
        self.bucket = bucket
        self.region = region
        self.s3 = client('s3', region)

    def list(self):
        """Return a list of objects in the bucket.
        @todo: Paging if required
        """
        try:
            objects = self.s3.list_objects(Bucket=self.bucket)
        except EndpointConnectionError as e:
            raise ValueError("Unable to connect; bad bucket or region")
        return [o["Key"] for o in objects["Contents"]]

    def load(self):
        """Loop through files in the bucket, generating a stream
        handle for each."""
        for key in self.list():
            res = r.get(self.__construct_url(key), stream=True)
            if res.encoding is None:
                res.encoding = 'utf-8'
            yield res.iter_lines(decode_unicode=True)

    def __construct_url(self, key):
        return "https://s3-{}.amazonaws.com/{}/{}".format(
            self.region, self.bucket, key)