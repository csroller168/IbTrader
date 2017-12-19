from IbRepo import IbRepo

if __name__ == '__main__':
    ##
    ## Check that the port is the same as on the Gateway
    ## ipaddress is 127.0.0.1 if one same machine, clientid is arbitrary

    app = IbRepo("127.0.0.1", 4002, 168)

    next_id = app.next_valid_id()

    print(next_id)

    app.disconnect()