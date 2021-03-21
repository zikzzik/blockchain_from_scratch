import hashlib
from bitcoinaddress import Wallet as BitcoinWallet

# base58 alphabet
alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def sha256(string: str):
    """Return a sha256 hash of a string

    Args:
            string:

    Returns:

    """
    encoded_string = string.encode()
    byte_array = bytearray(encoded_string)
    m = hashlib.sha256()
    m.update(byte_array)
    return m.hexdigest()


def b58encode(hex_string):
    """

    Args:
            hex_string:

    Returns:

    """
    num = int(hex_string, 16)
    encode = ""
    base_count = len(alphabet)
    while num > 0:
        num, res = divmod(num, base_count)
        encode = alphabet[res] + encode
    return encode


def b58decode(v):
    """

    Args:
        v:

    Returns:

    """
    if not isinstance(v, str):
        v = v.decode("ascii")
    decimal = 0
    for char in v:
        decimal = decimal * 58 + alphabet.index(char)
    return hex(decimal)[2:]  # (remove "0x" prefix)


def private_key_to_wif(private_key):
    """

    Args:
        private_key:

    Returns:

    """
    priv_add_x80 = "80" + private_key
    first_sha256 = sha256(priv_add_x80)
    second_sha256 = sha256(first_sha256)
    first_4_bytes = second_sha256[0:8]
    resulting_hex = priv_add_x80 + first_4_bytes
    result_wif = b58encode(resulting_hex)
    return result_wif


def wif_to_private_key(wif):
    """

    Args:
        wif:

    Returns:

    """
    if not wif_checksum(wif):
        raise Exception("The WIF is not correct (does not pass checksum)")
    byte_str = b58decode(wif)
    byte_str_drop_last_4bytes = byte_str[0:-8]
    byte_str_drop_first_byte = byte_str_drop_last_4bytes[2:]
    return byte_str_drop_first_byte


def wif_checksum(wif):
    """Returns True if the WIF is positive to the checksum, False otherwise

    Args:
        wif:

    Returns:

    """
    byte_str = b58decode(wif)
    byte_str_drop_last_4bytes = byte_str[0:-8]
    sha_256_1 = sha256(byte_str_drop_last_4bytes)
    sha_256_2 = sha256(sha_256_1)
    first_4_bytes = sha_256_2[0:8]
    last_4_bytes_WIF = byte_str[-8:]
    bytes_check = False
    if first_4_bytes == last_4_bytes_WIF:
        bytes_check = True
    check_sum = False
    if bytes_check and byte_str[0:2] == "80":
        check_sum = True
    return check_sum
