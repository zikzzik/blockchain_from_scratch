from hashlib import sha256
import time
from copy import deepcopy


class Block:

    def __init__(self, index, previous_hash, size_max, nonce=0, timestamp=None):
        self.index = index
        self.transaction_list = []
        self.size_max = size_max
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = int(time.time()) if timestamp is None else timestamp

    def add_transaction(self, timestamp, sender, receiver, mount):
        if len(self.transaction_list) < self.size_max:
            self.transaction_list.append((timestamp, sender, receiver, mount))

    def hash(self):
        str_to_hash = f"{self.index}_{self.transaction_list}_{self.previous_hash}_{self.nonce}_{self.timestamp}"
        return sha256(str_to_hash.encode()).hexdigest()

    def set_nonce(self, nonce):
        self.nonce = nonce

    def is_correct(self, difficulty):
        return self.hash()[:difficulty] == "0" * difficulty

    def get_index(self):
        return self.index

    def copy(self):
        return deepcopy(self)