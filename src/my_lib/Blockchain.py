from .Block import Block
import threading


class Blockchain:

    def __init__(self):
        self.lock = threading.Lock()
        self.blockchain = []
        self.add_block(Block(0, "genèse", 10, 0))

    def add_block(self, block):
        self.lock.acquire()
        try:
            if self.get_idx_last_block() + 1 == block.get_index():
                self.blockchain.append(block)
            else:
                raise ValueError
        finally:
            self.lock.release()

    def get_blockchain(self):
        return self.blockchain

    def get_idx_last_block(self):
        if len(self.blockchain) == 0:
            return -1
        return self.blockchain[-1].get_index()