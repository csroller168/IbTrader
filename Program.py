from IbRepo import IbRepo
from time import sleep
from SectorRotationStrategy import SectorRotationStrategy
from OrderGenerator import OrderGenerator
from datetime import date
from Backtester import Backtester
from datetime import date


if __name__ == '__main__':
    Backtester(100000, date(2017, 1, 3), date(2017, 12, 29)).Run()

    # maybe make this take an argument that signals what action to perform

    # app = IbRepo("127.0.0.1", 4002, 168)
    # app.init_error()
    # app.placeSampleOrder()
    # sleep(5)
    # # request a contract rather than build one (test with msft)
    # app.disconnect()