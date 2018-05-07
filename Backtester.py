from datetime import date
from SectorRotationStrategy import SectorRotationStrategy
from PandasRepo import PandasRepo
from Asset import Asset
from OrderGenerator import OrderGenerator
from typing import List
from pandas import Timestamp

class Backtester:
    def __init__(self,
                 openingBalance,
                 startDate : date,
                 endDate : date):
        self._openingBalance = openingBalance
        self._startDate = startDate
        self._endDate = endDate
        self._benchmarkSymbol = 'SPY'

    def Run(self):
        # TODO: calculate sharpe ratio too as follows:
        # df['daily_ret'] = df['Close'].pct_change();
        # df['excess_daily_ret'] = df['daily_ret'] - 0.05/252
        # sharpe = np.sqrt(252) * df['excess_daily_ret'].mean() / df['excess_daily_ret'].std()
        repo = PandasRepo()
        df = repo.GetData(self._benchmarkSymbol)
        tradingDays = [row[1].to_pydatetime().date() for row in df.index]
        startIdx = tradingDays.index(self._startDate)
        idx = startIdx

        currentPortfolio = SectorRotationStrategy(self._openingBalance, tradingDays[idx]).GetTargetPortfolio()
        portfolioValue = self.PortfolioValue(currentPortfolio)
        cash = self._openingBalance - portfolioValue

        while(tradingDays[idx] <= self._endDate and idx < len(tradingDays)):
            totalValue = cash
            if (len(currentPortfolio) > 0):
                self.UpdatePrices(currentPortfolio, repo, tradingDays[idx])
                portfolioValue = self.PortfolioValue(currentPortfolio)
                totalValue += portfolioValue
            print(tradingDays[idx], ":  ", totalValue)

            # Rebalance if due
            if idx % 7 == 0:
                targetPortfolio = SectorRotationStrategy(totalValue, tradingDays[idx]).GetTargetPortfolio()
                orders = OrderGenerator().MakeOrders(currentPortfolio, targetPortfolio)
                cash += sum(o.Proceeds() for o in orders)
                currentPortfolio = targetPortfolio
            idx += 1

    def PortfolioValue(self, portfolio : List[Asset]):
        return sum(a.Value for a in portfolio)

    def UpdatePrices(self, portfolio: List[Asset], repo : PandasRepo, day : date):
        for asset in portfolio:
            data = repo.GetData(asset._symbol)
            price = data.loc[(asset._symbol, Timestamp(day))]['Close']
            asset._sharePrice = price