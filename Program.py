from IbRepo import IbRepo
from time import sleep


if __name__ == '__main__':
    app = IbRepo("127.0.0.1", 4002, 168)
    app.init_error()
    app.placeSampleOrder()
    sleep(5)
    # request a contract rather than build one (test with msft)
    app.disconnect()