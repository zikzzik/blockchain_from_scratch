from hashlib import sha256
from .Transaction import Transaction
from merkletools import MerkleTools

class MerkleProof:
    
    def __init__(self, root: str = None, hash_list: list = None, not_found=False):

        self.root = root
        self.hash_list = hash_list
        self.not_found = not_found

    def is_in_merkle_root(self, transaction: Transaction):
        if self.not_found:
            print("Transaction not found")
            return False
        return MerkleTools().validate_proof(self.hash_list,
                                            sha256(str(transaction).encode()).hexdigest(),
                                            self.root)
