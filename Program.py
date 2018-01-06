from IbRepo import IbRepo
from time import sleep


if __name__ == '__main__':
    app = IbRepo("127.0.0.1", 4002, 168)
    app.init_error()
    app.placeSampleOrder()
    sleep(10)
    # initialize a queue for the response in the wrapper, similar to the get valid id call
    app.disconnect()