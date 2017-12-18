"""Extract csv files of known shape from an S3 bucket and parse them into an
aggregate format.
"""

# Std Lib
import argparse
import logging
import sys

# local/library specific
from webtraffic import S3DataLoader, UserPageTimeAggregator

LOG = logging.getLogger(__name__)

def setup():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("bucket", help="Name of the S3 bucket",
                   metavar="my-bucket")
    p.add_argument("region", help="Region in which bucket can be accessed",
                   metavar="us-west-2")
    p.add_argument("--list", "-l", help="List the contents of the bucket; do "
                   "not process them", action="store_true")
    p.add_argument("--output", "-o", help="Path to write csv; stdout "
                   "otherwise")
    p.add_argument("--verbosity", "-v", help="Increase log messages; may be specified "
                   "multiple times", action="count")

    args = p.parse_args()

    verbosity = 4 if args.verbosity > 4 else args.verbosity
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=levels[verbosity])
    
    return args


def main():
    args = setup()
    loader = S3DataLoader(args.region, args.bucket)
    aggregator = UserPageTimeAggregator()
    if args.list:
        print("Found files:")
        for f in loader.list():
            print("  {}".format(f))
        sys.exit(0)

    for csv in loader.load():
        aggregator.add_csv(csv)

    output_data = aggregator.dump_csv()
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_data)

    else:
        print(output_data)


if __name__ == "__main__":
    main()
