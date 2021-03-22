from my_lib import Wallet

adress_list = {
    "antoine": "JDLvmPFK7Aai41RxAsciv862AUa9va4ANFFkJ23fXJZg",      # 1
    "zak": "5MrzFo5omy6wYgi2oMLFZJ5rjfGXSxokhhVeC7kULVRE",          # 2
    "sylvain": "HWjHxcSdwBB9thkLCtiVfqiy5iAr25Y2x1bEJXhaCDPKs"      # 3
}

w = Wallet(public_key_path="/app/keys/1_public.pem",
           private_key_path="/app/keys/1_private.pem",
           connection_host="localhost",
           connection_port=8000)

request_transaction = w.send_token(adress_list["zak"], 12)
w.send_token(adress_list["zak"], 11)
w.send_token(adress_list["zak"], 10)

print("res", w.check_transaction(request_transaction.transaction))


if __name__ == "__main__":
    pass
