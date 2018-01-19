from Order import Order
from Asset import Asset

class OrderGenerator:
    def MakeOrders(self, currentPortfolio, targetPortfolio):
        orders = []
        for currentAsset in currentPortfolio:
            # if exists in target, buy/sell to get to target
            tgtAssetArray = [a for a in targetPortfolio if a._symbol == currentAsset._symbol]
            if len(tgtAssetArray) > 0:
                symbol = tgtAssetArray[0]._symbol
                price = tgtAssetArray[0]._sharePrice
                numShares = tgtAssetArray[0]._numShares - currentAsset._numShares
                if numShares > 0:
                    orders.append(Order("Buy", Asset(symbol, price, numShares)))
                elif numShares < 0:
                    orders.append(Order("Sell", Asset(symbol, price, -numShares)))
            else:
                # else, sell all
                orders.append(Order("Sell", currentAsset))
        for targetAsset in targetPortfolio:
            # if not exists in current, buy all
            if not any([a for a in currentPortfolio if a._symbol == targetAsset._symbol]):
                orders.append(Order("Buy", targetAsset))

        return orders