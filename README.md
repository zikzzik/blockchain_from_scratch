# blockchain_from_scratch

## Installation

Installer docker et docker-compose (Linux, Windows, Mac)


## Get starting

``` bash
    cd docker
    cp .env.dist .env
```

Don't modify the .env
Paste the keys send by mail /keys/

``` bash
   docker-compose build
   docker-compose up -d
```

## Start mining

Enter the container :
```bash
  docker exec -it blockchain bash
```
Launch the first miner :  
```bash
    python3 /app/src/main_miner.py
```
Launch the second miner :  
```bash
    python3 /app/src/second_miner.py
```
Launch the third miner :  
```bash
    python3 /app/src/third_miner.py
```

## Software wallet
Use the wallet:  
``` bash
    python3 /app/src/wallet_application.py
```

Basic arg:
  - load key : 2 
  - private key : /app/keys/1_private.pem
  - public key path : /app/keys/1_public.pem
  - minor host : localhost
  - minor port : 8000