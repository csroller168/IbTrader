from datetime import datetime, timedelta
import os
import os.path
import pandas as pd
import pandas_datareader.data as web

class PandasRepo:
    def __init__(self):
        self._dataFileFormat = os.path.dirname(os.path.abspath(__file__)) + "/data/{}.dat"
        self._dfEmpty = pd.DataFrame(columns=['Symbol', 'Close', 'High', 'Low', 'Open', 'Volume'])
        self._localCache = {}
        pass

    def GetData(self, symbol:str, startDate: datetime, endDate: datetime):
        df = self.GetDataFromCache(symbol)
        reqStartDt = startDate
        reqEndDt = endDate

        if (not df.empty):
            cacheStartDt = df.index[0].to_pydatetime()
            cacheEndDt = df.index[-1].to_pydatetime()
            if(endDate >= cacheStartDt and endDate <= cacheEndDt):
                reqEndDt = cacheStartDt
            if (startDate >= cacheStartDt and startDate <= cacheEndDt):
                reqStartDt = cacheEndDt

        if (reqStartDt <= reqEndDt):
            dfNew = self.GetDataFromWeb(symbol, reqStartDt, reqEndDt)
            df = pd.concat([df,dfNew]).drop_duplicates().sort_index()
            self.CacheData(df, symbol)

        return df

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