from datetime import datetime, timedelta
import os
import os.path
import pandas as pd
import pandas_datareader.data as web

class PandasRepo:
    def __init__(self):
        self._dataFileFormat = os.path.dirname(os.path.abspath(__file__)) + "/data/{}.dat"
        self._dfEmpty = pd.DataFrame(columns=['Close', 'High', 'Low', 'Open', 'Volume'])
        self._localCache = {}
        pass

    def GetData(self, symbol:str, startDate: datetime, endDate: datetime):
        dfCached = self.GetDataFromCache(symbol)
        if not dfCached.empty:
            return dfCached

        dfNew = self.GetDataFromWeb(symbol, startDate, endDate)
        self.CacheData(dfNew, symbol)
        return dfNew

        #dateToBeginPull = startDate
        #if not dfCached.empty:
        #    dateToBeginPull = dfCached.index[-1][1].to_pydatetime() + timedelta(days=1)

        #dfNew = self.GetDataFromWeb(symbol, dateToBeginPull, endDate)
        #df = dfNew
        #if not dfCached.empty:
        #    df = pd.concat([dfCached, dfNew])
        #self.CacheData(df, symbol)
        #return df

    def GetDataFromCache(self, symbol:str):
        if symbol in self._localCache:
            return self._localCache[symbol]
        df = self._dfEmpty
        filename = self._dataFileFormat.format(symbol)
        if os.path.exists(filename):
            df = pd.read_pickle(filename)
            self._localCache[symbol] = df
        return df

    def GetDataFromWeb(self, symbol:str, startDate:datetime, endDate:datetime):
        df = self._dfEmpty
        try:
            df = web.DataReader(symbol, 'morningstar', startDate, endDate)
            df.dropna()
            df['Close'].ffill()
            df = df.reset_index(level=[0])
        except:
            pass
        return df

    def CacheData(self, df, symbol:str):
        self._localCache[symbol] = df
        filename = self._dataFileFormat.format(symbol)
        df.to_pickle(filename)
        return