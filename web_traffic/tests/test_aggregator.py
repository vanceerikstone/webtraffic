from web_traffic import UserPageTimeAggregator
import os
import unittest
import sys

sys.path.append("..")

class AggregatorTestCase(unittest.TestCase):

    def test_add_csv(self):
        agg = UserPageTimeAggregator()
        dir = os.path.dirname(__file__)
        with open(os.path.join(dir, 'sample_data.csv')) as f:
            agg.add_csv(f)

        assert agg.data[378]["/"] == 16


if __name__ == "__main__":
    unittest.main()
