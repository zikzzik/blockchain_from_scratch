from my_lib import Miner


if __name__ == "__main__":
    Miner(host="localhost", port=8002, connection_host="localhost", connection_port=8000,
          public_key_path="/app/keys/minor_3_public.pem")

