"""Extract csv files of known shape from an S3 bucket and parse them into an
aggregate format.
"""

# Std Lib
import argparse

# local/library specific
from web_traffic.web_traffic import S3DataLoader, UserPageTimeAggregator


def setup():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("bucket", help="Name of the S3 bucket",
                   metavar="my-bucket")
    p.add_argument("region", help="Region in which bucket can be accessed",
                   metavar="us-west-2")
    p.add_argument("--list", "-l", help="List the contents of the bucket; do "
                   "not process them", action="store_true")
    p.add_argument("--yes", "-y", help="Yes to all prompts, good for "
                   "non-interactive execution", action="store_true")
    p.add_argument("--output", "-o", help="Path to write csv; stdout "
                   "otherwise")

    return p.parse_args()


def main():
    args = setup()
    loader = S3DataLoader(args.region, args.bucket)
    aggregator = UserPageTimeAggregator()
    if args.list:
        print("Found files:")
        for f in loader.list():
            print("  {}".format(f))
    for csv in loader.load():
        aggregator.add_csv(csv)


if __name__ == "__main__":
    main()
