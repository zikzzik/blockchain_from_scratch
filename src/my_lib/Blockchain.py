from .Block import Block


class Blockchain:

    def __init__(self, lock, block_size=3):
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
                raise ValueError
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
                res += f"  - {transaction['sender']} -> {transaction['receiver']} : {transaction['mount']} tokens\n"
            res += "\n"
        return res

    def check_valid_operation(self, sender, mount):
        # @todo vérifie si l'envoyeur à les fonds suffisant
        pass

    def create_genesis_block(self):
        # @todo ajouter hash valid genesis
        genesis_bloc = Block(index=0, previous_hash="Hello world", block_size=self.block_size)
        genesis_bloc.add_transaction("admin", "zak", 6000)
        genesis_bloc.add_transaction("admin", "antoine", 5000)
        genesis_bloc.add_transaction("admin", "sylvain", 4000)

        return genesis_bloc

