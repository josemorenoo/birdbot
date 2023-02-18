import os
import sys

from datetime import datetime
from Historic_Crypto import HistoricalData

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "report_parser")))


class Prices:
    def __init__(self, token):
        self.token = token
        self.pair = "{}-USD".format(self.token)

    def _stringify_datetime(self, dt):
        if int(dt.month) < 10:
            month = f"0{dt.month}"
        else:
            month = dt.month
        if int(dt.day) < 10:
            day = f"0{dt.day}"
        else:
            day = dt.day

        return "{}-{}-{}".format(dt.year, month, day)

    def get_token_price_from_coinbase(self, start_date, end_date, interval_sec=300):
        """returns a dataframe containing price data for a given token
        given that Coinbase the price stored somewhere.
        Returns a dataframe:

        time                 low    high    open     close    volume
        2021-12-22 00:05:00  2.3866  2.4054  2.4042  2.3884   61175.067550
        2021-12-22 00:10:00  2.3843  2.4003  2.3901  2.3987   51876.207316
        2021-12-22 00:15:00  2.3903  2.3997  2.3993  2.3975   44646.627470
        2021-12-22 00:20:00  2.3930  2.4088  2.3976  2.4049   45447.516436
        2021-12-22 00:25:00  2.4004  2.4091  2.4044  2.4070   22489.383224

        Args:
            startDate (datetime)
            endDate (datetime)
            interval_sec (int, optional): The time interval width in seconds of each price sample. Defaults to 300.
        """

        def _stringify_datetime(dt):
            return datetime.strftime(dt, "%Y-%m-%d-%H-%M")

        start_date_str = _stringify_datetime(start_date)
        if end_date:
            end_date_str = _stringify_datetime(end_date)

        usd_pair_df = HistoricalData(
            self.pair, interval_sec, start_date_str, end_date_str
        ).retrieve_data()

        print("\nFound data for {}:".format(self.pair))
        print(usd_pair_df.head())
        return usd_pair_df


if __name__ == "__main__":
    c = Prices(token="ROSE")
    start = datetime(2023, 1, 23)
    end = datetime(2023, 1, 24)
    # d_str = d.strftime("%Y-%m-%d")
    data = c.get_token_price_df(start, end)
    print(data)
    # print(data.loc[d_str])
