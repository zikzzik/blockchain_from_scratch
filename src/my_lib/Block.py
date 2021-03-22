from hashlib import sha256
import time
from .Transaction import Transaction
from copy import deepcopy
from merkletools import MerkleTools


class Block:
    def __init__(self, index: int, previous_hash: str, block_size: int, nonce: int = 0, timestamp: float = None):
        self.index = index
        self.transaction_list = []
        self.block_size = block_size
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = int(time.time()) if timestamp is None else timestamp

    def add_transaction(self, transaction: Transaction):
        assert transaction.timestamp is not None
        assert len(self.transaction_list) <= self.block_size, "Try to add a transaction in full block"

        if len(self.transaction_list) < self.block_size:
            self.transaction_list.append(transaction)

    def hash(self):
        str_transaction_for_hash = "_".join([el.str_for_hash() for el in self.transaction_list])
        str_to_hash = f"{self.index}_{str_transaction_for_hash}_{self.previous_hash}_{self.nonce}_{self.timestamp}"
        return sha256(str_to_hash.encode()).hexdigest()

    def set_nonce(self, nonce: int):
        self.nonce = nonce

    def is_correct(self, difficulty: int):
        return self.hash()[:difficulty] == "0" * difficulty

    def get_index(self):
        return self.index

    def copy_for_mining(self):
        return deepcopy(self)

    def get_transaction_list(self, receiver=None, sender=None):
        assert not (receiver is not None and sender is not None)
        if receiver is not None:
            return [el for el in self.transaction_list if el.receiver == receiver]
        elif sender is not None:
            return [el for el in self.transaction_list if el.sender == sender]
        else:
            return self.transaction_list

    def is_full_transaction(self):
        return len(self.transaction_list) == self.block_size

    def get_merkle_root(self):
        tree = MerkleTools(hash_type="SHA256")
        tree.add_leaf([str(el) for el in self.transaction_list], True)
        tree.make_tree()
        return tree

    def merkle_root_calculation(self):
        self.merkle_root = self.get_merkle_root().get_merkle_root()

    def __str__(self):
        return f"hash {self.hash}"

    def get_transaction_position(self, transaction: Transaction):
        for pos, registred_transaction in enumerate(self.transaction_list):
            if transaction == registred_transaction:
                return pos
        assert False, "ERROR Transaction not found in block"
