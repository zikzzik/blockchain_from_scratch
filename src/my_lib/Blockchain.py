from .Block import Block
from .Transaction import Transaction
import time
from datetime import datetime


class Blockchain:
    def __init__(self, lock, block_size=1):
        self.lock = lock
        self.block_list = []
        self.block_size = block_size
        self.block_list.append(self.create_genesis_block())

    def add_block(self, block):
        self.lock.acquire()
        try:
            if self.get_idx_last_block() + 1 == block.get_index():
                self.block_list.append(block)
            else:
                raise ValueError("Can't add a block with index inferior")
        finally:
            self.lock.release()

    def get_block_list(self):
        return self.block_list

    def get_idx_last_block(self):
        if len(self.block_list) == 0:
            return -1
        return self.block_list[-1].get_index()

    def __str__(self):
        res = "Contain blockchain : \n"
        for block in self.block_list:
            res += f" * block idx : {block.get_index()}\n"
            for transaction in block.get_transaction_list():
                res += f"  - {transaction.sender} -> {transaction.receiver} : {transaction.mount} tokens\n"
            res += "\n"
        return res

    def check_valid_operation(self, sender, mount):
        # @todo vérifie si l'envoyeur à les fonds suffisant
        pass

    def create_genesis_block(self):
        # Set up manually
        ts = int(datetime.timestamp(datetime(1998, 6, 9, 22, 46)))
        genesis_bloc = Block(index=0, previous_hash="Hello world", block_size=self.block_size, timestamp=ts)
        genesis_bloc.add_transaction(Transaction("admin", "zak", 6000, ts))
        genesis_bloc.add_transaction(Transaction("admin", "antoine", 5000, ts))
        genesis_bloc.add_transaction(Transaction("admin", "sylvain", 4000, ts))
        genesis_bloc.set_nonce(1)

        return genesis_bloc

    def is_valid_blockchain(self, difficulty: int):
        if len(self.block_list) == 0:
            return False

        if len(self.block_list) == 1:
            # For the first block, we select difficulty 1 because this is a particular block
            return self.block_list[0].is_correct(difficulty=1)

        previous_block = self.block_list[0]
        for block in self.block_list[1:]:
            if (
                block.is_correct(difficulty=difficulty) is False
                or previous_block.hash() != block.previous_hash
                or previous_block.index + 1 != block.index
            ):
                return False
            previous_block = block
        return True

    def is_valid_transaction(self, transaction: Transaction):
        if transaction.mount <= 0:
            return False

        sender_sold = 0
        for block in self.block_list:
            for receive_transaction in block.get_transaction_list(receiver=transaction.sender):
                sender_sold += receive_transaction.mount
            for sender_transaction in block.get_transaction_list(sender=transaction.sender):
                sender_sold -= sender_transaction.mount
        return sender_sold > transaction.mount

    def is_transaction_register(self, transaction: Transaction):
        for block in self.block_list:
            for register_transaction in block.get_transaction_list():
                if register_transaction == transaction:
                    return True
        return False
