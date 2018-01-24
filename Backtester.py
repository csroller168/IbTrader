from datetime import date
from SectorRotationStrategy import SectorRotationStrategy
from GoogleRepo import GoogleRepo
from Asset import Asset
from OrderGenerator import OrderGenerator
from typing import List

class Backtester:
    def __init__(self,
                 openingBalance,
                 startDate : date,
                 endDate : date):
        self._openingBalance = openingBalance
        self._startDate = startDate
        self._endDate = endDate

    def Run(self):
        repo = GoogleRepo()
        repo.GetData("SPY")
        prices = repo.ClosingPrices("SPY")
        tradingDays = list(prices.keys())
        startIdx = tradingDays.index(self._startDate)
        idx = startIdx

        cash = self._openingBalance
        currentPortfolio = []
        totalValue = cash

        # TODO: rebalance every 7 days, update portfolio asset values each day (helper function in Asset - maybe new portfolio class)
        while(tradingDays[idx] <= self._endDate and idx < len(tradingDays)):
            totalValue = cash
            if (len(currentPortfolio) > 0):
                totalValue += self.PortfolioValue(currentPortfolio)
            print(tradingDays[idx], ":  ", totalValue)
            targetPortfolio = SectorRotationStrategy(totalValue, tradingDays[idx]).GetTargetPortfolio()
            orders = OrderGenerator().MakeOrders(currentPortfolio, targetPortfolio)
            cash += sum(o.Proceeds() for o in orders)
            currentPortfolio = targetPortfolio
            idx += 1

    def PortfolioValue(self, portfolio : List[Asset]):
        return sum(a.Value for a in portfolio)