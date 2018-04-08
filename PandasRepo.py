import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta
import os.path
#from os.path import dirname, abspath

# todos:
# save data file to local data directory (not home)

class PandasRepo:
    def __init__(self):
        self._dataFileFormat = "/Users/dennis/data/{}.dat"
        self._dfEmpty = pd.DataFrame(columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        self._startDate = datetime(2018,4,2)
        pass

    def ClosingPrices(self, symbol:str):
        dfCached = self.ReadCachedData(symbol)
        dateToBeginPull = self._startDate
        if not dfCached.empty:
            dateToBeginPull = dfCached.index[-1][1].to_pydatetime() + timedelta(days=1)

        dfNew = self.GetRecentPrices(symbol, dateToBeginPull)
        df = pd.concat([dfCached, dfNew])
        self.WriteCachedData(df, symbol)
        return df

    def ReadCachedData(self, symbol:str):
        filename = self._dataFileFormat.format(symbol)
        df = self._dfEmpty
        if os.path.exists(filename):
            df = pd.read_pickle(filename)
        return df

    def GetRecentPrices(self, symbol:str, startDate:datetime):
        df = self._dfEmpty
        try:
            df = web.DataReader(symbol, 'morningstar', startDate, datetime.today())
        except:
            pass

        return df

    def WriteCachedData(self, df, symbol:str):
        filename = self._dataFileFormat.format(symbol)
        df.to_pickle(filename)
        return