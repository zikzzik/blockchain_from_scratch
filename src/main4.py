import my_lib
import time
from my_lib import Miner

if __name__ == "__main__":

    b = my_lib.Block(index=1, previous_hash="None", size_max=10, nonce=0, timestamp=None)

    b.add_transaction(timestamp=time.time(), sender="Moi", receiver="Toi", mount=5)
    b.add_transaction(timestamp=time.time(), sender="Moi", receiver="Toi", mount=8)
    b.add_transaction(timestamp=time.time(), sender="Moi", receiver="Toi", mount=9)
    # print(b.transaction_list)
    # print(b.hash())

    # b.set_nonce(nonce=12)
    # print(b.hash())
    # nonce = 0
    # while True:
    #     if nonce % 1000 == 0:
    #         print(nonce)
    #
    #     b.set_nonce(nonce)
    #     nonce += 1
    #
    #     if b.is_correct(difficulty=4):
    #         print(b.hash())
    #         break
    #
    # print(b.__dict__)

    m = Miner(host="localhost", port=8000, difficulty=1)
    m.mine_block(block=b.copy_for_mining())

    b2 = my_lib.Block(index=2, previous_hash="None", size_max=10, nonce=0, timestamp=None)
    b2.add_transaction(timestamp=time.time(), sender="Moi", receiver="Toi", mount=9)

    m.mine_block(block=b2.copy_for_mining())

    time.sleep(10)
    print(m.blockchain.block_list)
    pass

