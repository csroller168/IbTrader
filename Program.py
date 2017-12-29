from IbRepo import IbRepo

if __name__ == '__main__':
    app = IbRepo("127.0.0.1", 4002, 168)
    next_id = app.next_valid_id()
    app.placeSampleOrder()
    print(next_id)
    app.disconnect()