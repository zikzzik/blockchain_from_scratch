import threading
import my_lib
from my_lib import Block, Transaction
from datetime import datetime

if __name__ == "__main__":
    lock = threading.Lock()
    genesis_hash = "05b5196940816a718ae765c735c7be4cc437a005a633c3219a6c13cfb9d06e7f"
    bloc1_hash = "000a18ee3d4a4229016502b4bb6702b3147095000cd2595f980458cd0bae76fd"
    bloc2_hash = "000718d70f5e1cd3aab56a80b096953ece34859822e577dad6c1bd78e7a83ad1"
    block_size = 3
    difficulty = 3

    bc = my_lib.Blockchain(lock, block_size=3)

    # bloc 1
    ts = int(datetime.timestamp(datetime(2000, 5, 1, 12, 12)))
    b = Block(index=1, previous_hash=genesis_hash, block_size=3, timestamp=ts)
    b.add_transaction(Transaction("antoine", "zak", 100, ts))
    b.add_transaction(Transaction("sylvain", "antoine", 200, ts))
    b.add_transaction(Transaction("zak", "sylvain", 300, ts))
    b.set_nonce(1687)

    bc.block_list.append(b)

    print(bc.is_valid_blockchain(3))

    # bloc 2
    ts = int(datetime.timestamp(datetime(2000, 6, 1, 12, 12)))
    b = Block(index=2, previous_hash=bloc1_hash, block_size=3, timestamp=ts)
    b.add_transaction(Transaction("zak", "sylvain", 10000, ts))
    b.add_transaction(Transaction("antoine", "zak", 5000, ts))
    b.add_transaction(Transaction("zak", "antoine", 30, ts))
    b.set_nonce(643)
    bc.block_list.append(b)


    print(bc.is_valid_blockchain(3))

    print(bc.is_valid_transaction(Transaction("antoine", "zak", 1)))
    print(bc.is_valid_transaction(Transaction("antoine", "zak", 999999999)))
    print(bc.is_valid_transaction(Transaction("toto", "zak", 10)))

