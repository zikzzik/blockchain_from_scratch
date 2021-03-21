from .Transaction import Transaction
import pickle
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class TransactionRequest:

    def __init__(self, transaction: Transaction, public_key: RSA._RSAobj):
        self.transaction = transaction
        self.public_key = public_key
        self.signature = None

    def sign_transaction(self, private_key: RSA._RSAobj):
        hasher = SHA256.new(f"{self.transaction}".encode())
        signer = PKCS1_v1_5.new(private_key)
        self.signature = signer.sign(hasher)
        return self

    def is_valid_signature(self):
        if self.signature is None:
            return False
        hasher = SHA256.new(f"{self.transaction}".encode())
        checker = PKCS1_v1_5.new(self.public_key)
        return checker.verify(hasher, self.signature)


    def get_transaction(self):
        return self.transaction