from my_lib import Miner


if __name__ == "__main__":

    m = Miner(host="localhost", port=8000, public_key_path="/app/keys/minor_1_public.pem")
    m.start_mine()

