from hashlib import sha256
import time
from .Transaction import Transaction
from copy import deepcopy
from merkletools import MerkleTools


class Block:
    def __init__(self, index: int, previous_hash: str, block_size: int, nonce: int = 0, timestamp: float = None,
                 minor_address: str = None, reward: int = 1):
        self.index = index
        self.transaction_list = []
        self.block_size = block_size
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = int(time.time()) if timestamp is None else timestamp
        self.minor_address = minor_address
        self.reward = reward

        self.add_transaction(Transaction("SYSTEM", self.minor_address, self.reward, self.timestamp))

    def add_transaction(self, transaction: Transaction):
        """Method use to add a transaction in the block

        Args:
            transaction:

        Returns:

        """
        assert transaction.timestamp is not None
        assert len(self.transaction_list) <= self.block_size, "Try to add a transaction in full block"

        if len(self.transaction_list) < self.block_size:
            self.transaction_list.append(transaction)

    def hash(self):
        """Method use to hash a block

        Returns:
            The hash value (str)
        """
        str_transaction_for_hash = "_".join([el.str_for_hash() for el in self.transaction_list])
        str_to_hash = f"{self.index}_{str_transaction_for_hash}_{self.previous_hash}_{self.nonce}_{self.timestamp}"
        return sha256(str_to_hash.encode()).hexdigest()

    def set_nonce(self, nonce: int):
        """ Setter

        Args:
            nonce:

        Returns:

        """
        self.nonce = nonce

    def is_correct(self, difficulty: int):
        """ Methode use to check if the block have a good hash depending of the difficulties

        Args:
            difficulty:

        Returns:

        """
        return self.hash()[:difficulty] == "0" * difficulty

    def get_index(self):
        """ Getter

        Returns:

        """
        return self.index

    def copy_for_mining(self):
        """

        Returns:

        """
        return deepcopy(self)

    def get_transaction_list(self, receiver=None, sender=None):
        """Method use to get the transaction list with filter

        Args:
            receiver: filter on receiver
            sender:  filter on sender

        Returns:

        """
        assert not (receiver is not None and sender is not None)
        if receiver is not None:
            return [el for el in self.transaction_list if el.receiver == receiver]
        elif sender is not None:
            return [el for el in self.transaction_list if el.sender == sender]
        else:
            return self.transaction_list

    def is_full_transaction(self):
        """ Mesthod use to check is the block is full of transaction

        Returns:

        """
        return len(self.transaction_list) == self.block_size

    def get_merkle_tree(self):
        """Methode use to build the merkle tree on transaction

        Returns:

        """
        tree = MerkleTools(hash_type="SHA256")
        tree.add_leaf([str(el) for el in self.transaction_list], True)
        tree.make_tree()
        return tree

    def merkle_root_calculation(self):
        """ Methode use to extract the root from the merkle tree of transaction

        Returns:

        """
        self.merkle_root = self.get_merkle_tree().get_merkle_root()

    def __str__(self):
        return f"hash {self.hash}"

    def get_transaction_position(self, transaction: Transaction):
        """ Method use to get the transaction position in a block

        Args:
            transaction:

        Returns:

        """
        for pos, registred_transaction in enumerate(self.transaction_list):
            if transaction == registred_transaction:
                return pos
        assert False, "ERROR Transaction not found in block"
