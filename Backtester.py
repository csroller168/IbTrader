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
            if idx % 5 == 0:
                targetPortfolio = SectorRotationStrategy(totalValue, tradingDays[idx]).GetTargetPortfolio()
                orders = OrderGenerator().MakeOrders(currentPortfolio, targetPortfolio)
                cash += sum(o.Proceeds() for o in orders)
                currentPortfolio = targetPortfolio
            idx += 1

    def PortfolioValue(self, portfolio : List[Asset]):
        return sum(a.Value for a in portfolio)

    def UpdatePrices(self, portfolio: List[Asset], repo : GoogleRepo, day : date):
        for asset in portfolio:
            asset._sharePrice = repo.ClosingPrices(asset._symbol)[day]