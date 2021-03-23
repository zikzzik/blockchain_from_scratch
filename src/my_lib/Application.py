from .Wallet import Wallet
from datetime import datetime
from time import time


address_list = {
    "antoine": "FiLz2wYz1kXuisZg1koWDhZhrekhD7GSgNLRevXH5b5U",      # 1
    "zak": "5MrzFo5omy6wYgi2oMLFZJ5rjfGXSxokhhVeC7kULVRE",          # 2
    "sylvain": "HWjHxcSdwBB9thkLCtiVfqiy5iAr25Y2x1bEJXhaCDPKs"      # 3
}


class Application:

    def __init__(self):

        choice = int(input("1. Generate key\n2. Load keys\n"))
        if choice == 1:
            self.command_generate_keys()
        else:
            self.command_load_keys(False)

        self.command_connect_minor()
        self.wallet = Wallet(self.private_key_path,
                             self.public_key_path,
                             self.connection_host,
                             self.connection_port)

    def run(self):
        command_dict = {
            0: self.command_view_address,
            1: self.command_sold,
            2: self.command_send_transaction,
            3: self.command_check_transaction,
            4: self.command_load_keys,
            5: self.command_generate_keys,
            6: self.command_connect_minor,
        }
        while True:
            cmd = int(input(
                """
0. view address
1. view sold
2. send tokens
3. check transaction
4. load keys
5. generate new keys 
6. set connection minor
Choice :
                """
            ))
            if cmd in command_dict:
                command_dict[cmd]()
            else:
                print("Good bye !")

    def command_sold(self):
        print("Solde :", self.wallet.get_sold())

    def command_load_keys(self, reload_wallet=True):
        self.private_key_path = str(input("private key path :\n"))
        self.public_key_path = str(input("public key path :\n"))
        if reload_wallet:
            self.wallet = Wallet(self.private_key_path,
                                 self.public_key_path,
                                 self.connection_host,
                                 self.connection_port)

    def command_send_transaction(self):
        receiver, mount, ts = self.ask_transaction_information()
        self.wallet.send_token(receiver, mount, ts)

    def command_check_transaction(self):
        receiver, mount, ts = self.ask_transaction_information()
        res = self.wallet.check_transaction(receiver, mount, ts)
        if res:
            print("Transaction exist")
        else:
            print("Transaction not found")

    def command_generate_keys(self):
        self.private_key_path = str(input("private key path :\n"))
        self.public_key_path = str(input("public key path :\n"))
        Wallet.create_key(self.public_key_path, self.private_key_path)
        print("new key created")
    
    def command_connect_minor(self):
        self.connection_host = str(input("minor host :\n"))
        self.connection_port = int(input("minor port :\n"))

    def ask_transaction_information(self):
        mount = float(input("mount :\n"))
        receiver = str(input(f"address or contact {address_list.keys()}: \n"))
        if receiver in address_list:
            receiver = address_list[receiver]

        str_ts = input("Datetime jj/mm/AA hh:mm:ss (default is current):\n")
        ts = int(time()) if str_ts == "" else round(datetime.strptime(str_ts, '%d/%m/%y %H:%M:%S').timestamp())
        return receiver, mount, ts

    def command_view_address(self):
        print("address :", self.wallet.address)


# /app/keys/1_private.pem
# /app/keys/1_public.pem