from my_lib import Miner


if __name__ == "__main__":

    m = Miner(host="localhost", port=8000)
    m.start_mine()
