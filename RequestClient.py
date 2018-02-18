from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from Asset import Asset
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

        if self.wrapper.is_error():
            print("An error occurred")

        return nextValidId

    def get_cash_value(self):
        rid = self.next_valid_id()
        print("Getting next valid ID from the server... ")
        cash_store = self.wrapper.init_cash_store()
        self.reqAccountSummary(rid, "All", "TotalCashValue")

        ## Try and get next valid ID
        MAX_WAIT_SECONDS = 10

        try:
            cashValue = cash_store.get(timeout=MAX_WAIT_SECONDS)
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")
            cashValue = 0

        if self.wrapper.is_error():
            print("An error occurred")

        return cashValue

    def get_current_portfolio(self):
        porfolio_store = self.wrapper.init_positions()
        getComplete = self.wrapper.init_positionEnd()
        print("Getting current portfolio from the server... ")
        self.reqPositions()

        ## Try and get next valid ID
        MAX_WAIT_SECONDS = 10

        try:
            done = getComplete.get(timeout=MAX_WAIT_SECONDS)
            positions = porfolio_store
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")
            positions = None

        if self.wrapper.is_error():
            print("An error occurred")

        return positions

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

        if self.wrapper.is_error():
            print("An error occurred")

        return response

    def placeOrder(self, type, shares, symbol):
        oid = self.next_valid_id()

        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "ARCA"
        contract.primaryExchange = "ARCA"

        order = Order()
        order.action = type
        order.orderType = "MKT"
        order.totalQuantity = shares

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