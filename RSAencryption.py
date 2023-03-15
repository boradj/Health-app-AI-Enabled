from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

# Function to generate key and store it file


def storeKey():
    key = RSA.generate(1024)
    private_key = key.export_key('PEM')
    public_key = key.publickey().exportKey('PEM')

    with open("PrivateKey.pem", "wb") as key_file:
        key_file.write(private_key)

    with open("PublicKey.pem", "wb") as key_file1:
        key_file1.write(public_key)

# Function to assign key to variable for encryption of database


def encryptkey():
    PublicKey = open("PublicKey.pem", "rb").read()
    RSA_public_key = RSA.importKey(PublicKey)
    RSA_public_key = PKCS1_OAEP.new(RSA_public_key)
    return RSA_public_key

# Function to assign key to variable for decryption of database


def decryptkey():
    PrivateKey = open("PrivateKey.pem", "rb").read()
    RSA_private_key = RSA.importKey(PrivateKey)
    RSA_private_key = PKCS1_OAEP.new(RSA_private_key)
    return RSA_private_key


# Function for encryption of data from SQL

def encryption(file=""):

    RSA_public_key = encryptkey()

    # TO acess a database file

    with open(file, "rb") as rfile:

        # Read the content of file and store it

        dataG = rfile.read()

    # Encryption of data

    encrypted_filedata = RSA_public_key.encrypt(dataG)
    with open(file, "wb") as wfile:

        # write the content of file and store it

        wfile.write(encrypted_filedata)


def decryption(file=""):

    RSA_private_key = decryptkey()

    # TO acess a database file

    with open(file, "rb") as rfile:

        # Read the content of file and store it

        dataG = rfile.read()
        #dataS = dataG.decode()

    # decrption of data

    key = RSA_private_key.decrypt(dataG)
    with open("file2.key", "wb") as file2:
        file2.write(key)
    return key


def encrypt(file, key):

    cipher = AES.new(key, AES.MODE_ECB)

    with open(file, "rb") as rfile:

        # Read the content of file and store it

        data = rfile.read()

        #dataS = str.encode(dataG)
    ciphertext = cipher.encrypt(data)
    #encrypted_data = ciphertext, tag, nonce
    with open(file, "wb") as file1:
        file1.write(ciphertext)

#file1, ciphertext, tag, nonce


def decrypt(file, key):
    with open(file, "rb") as rfile:

        # Read the content of file and store it

        ciphertext = rfile.read()
    decipher = AES.new(key, AES.MODE_ECB)
    plaintext = decipher.decrypt(ciphertext)

    with open(file, "wb") as file:
        file.write(plaintext)


def encryptionfile():
    key = decryption("file2.key")
    encrypt("users.db", key)
    encryption("file2.key")


def decryptionfile():
    key = decryption("file2.key")
    decrypt("users.db", key)
    encryption("file2.key")


# encryptionfile()
# decryptionfile()

# Used the function to store key for encryption


# storeKey()
# encryption("file2.key")
#key = decryption("file2.key")
# print(key)
# encryption('file2.key')
