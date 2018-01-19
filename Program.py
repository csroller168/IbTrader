from IbRepo import IbRepo
from time import sleep
from SectorRotationStrategy import SectorRotationStrategy
from OrderGenerator import OrderGenerator
from datetime import date


if __name__ == '__main__':
    strategy = SectorRotationStrategy(100000, date(2018,1,8))
    portfolio = strategy.GetTargetPortfolio()
    orders = OrderGenerator().MakeOrders([], portfolio)
    print(orders)

    # maybe make this take an argument that signals what action to perform

    # app = IbRepo("127.0.0.1", 4002, 168)
    # app.init_error()
    # app.placeSampleOrder()
    # sleep(5)
    # # request a contract rather than build one (test with msft)
    # app.disconnect()