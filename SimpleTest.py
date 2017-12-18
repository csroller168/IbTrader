# TODOs:
# refactor into separate classes

from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from threading import Thread
import queue

class TestWrapper(EWrapper):

    ## error handling code
    def init_error(self):
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None

        return None

    def is_error(self):
        an_error_if=not self._my_errors.empty()
        return an_error_if

    def error(self, id, errorCode, errorString):
        ## Overriden method
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)

    def init_valid_id(self):
        id_queue = queue.Queue()
        self._id_queue = id_queue
        return id_queue

    def nextValidId(self, id_from_server):
        self._id_queue.put(id_from_server)

    def Close(self):
        pass

class TestClient(EClient):
    """
    The client method
    We don't override native methods, but instead call them from our own wrappers
    """
    def __init__(self, wrapper):
        ## Set up with a wrapper inside
        EClient.__init__(self, wrapper)

    def next_valid_id(self):
        id_store = self.wrapper.init_valid_id()
        print("Getting next valid ID from the server... ")
        self.reqIds(1)

        ## Try and get next valid ID
        MAX_WAIT_SECONDS = 10

        try:
            nextValidId = id_store.get(timeout=MAX_WAIT_SECONDS)
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")
            nextValidId = None

        while self.wrapper.is_error():
            print(self.get_error())

        return nextValidId

class TestApp(TestWrapper, TestClient):
    def __init__(self, ipaddress, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)

        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)

        self.init_error()


if __name__ == '__main__':
    ##
    ## Check that the port is the same as on the Gateway
    ## ipaddress is 127.0.0.1 if one same machine, clientid is arbitrary

    app = TestApp("127.0.0.1", 4002, 168)

    next_id = app.next_valid_id()

    print(next_id)

    app.disconnect()