from my_lib import Miner


if __name__ == "__main__":

    m = Miner(host="localhost", port=8000)
    m.start_mine()

# TODO Code pas beau / devra être lancé dans un thread
# b = Block(index=1, previous_hash="None", block_size=10, nonce=0, timestamp=None)

# ts = int(datetime.timestamp(datetime(2000, 6, 1, 12, 12)))
# b = Block(
#     index=2,
#     previous_hash="000a18ee3d4a4229016502b4bb6702b3147095000cd2595f980458cd0bae76fd",
#     block_size=3,
#     timestamp=ts,
# )
# b.add_transaction(Transaction("zak", "sylvain", 10000, ts))
# b.add_transaction(Transaction("antoine", "zak", 5000, ts))
# b.add_transaction(Transaction("zak", "antoine", 30, ts))
#
# self.mine_block(b)
# print(self.blockchain)
