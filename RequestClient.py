from ibapi.client import EClient
import queue

class RequestClient(EClient):
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
            print("An error occurred")

        return nextValidId