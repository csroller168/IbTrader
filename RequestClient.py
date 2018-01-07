from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
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

    def request_matching_symbols(self, symbol):
        rid = self.next_valid_id()
        queue = self.wrapper.init_match_symbols()
        self.reqMatchingSymbols(rid, symbol)
        MAX_WAIT_SECONDS = 10
        try:
            response =  queue.get(timeout=MAX_WAIT_SECONDS)
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")
            response = None

        while self.wrapper.is_error():
            print("An error occurred")

        return response

    def placeSampleOrder(self):
        oid = self.next_valid_id()

        contract = Contract()
        contract.symbol = "MSFT"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = "ISLAND"

        order = Order()
        order.action = "BUY"
        order.orderType = "MKT"
        order.totalQuantity = 5

        queue = self.wrapper.init_order_status()
        self.placeOrder(oid, contract, order)
        MAX_WAIT_SECONDS = 10
        try:
            queue.get(timeout=MAX_WAIT_SECONDS)
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")

        if self.wrapper.is_error():
            print("An error occurred")
        pass