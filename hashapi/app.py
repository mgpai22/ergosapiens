from flask import Flask, json
from hashlib import blake2b
from flask_cors import CORS, cross_origin
import json
import os
import random
from dotenv import load_dotenv
import os

load_dotenv()
hashCmd = os.getenv("HASHCMD")


def write(new_data, filename="hash.json"):  # function that appends data to the specified file
    with open(filename, "r") as file1:
        data = json.load(file1)
        data.append(new_data)
    with open(filename, "w") as file1:
        # Sets file's current position at offset.
        file1.seek(0)
        json.dump(data, file1, indent=4)


def hasher():  # This function returns a hash
    for x in range(1):
        name = 'ErgoSapien #' + str(random.randint(0, 1000))  # This is the thing that is hashed
        # essentially hashing ErgoSapien # + 'insert a random number between -1 and 1001'
        msg = bytes(name, encoding='utf8')  # name is converted into bytes
        salt1 = os.urandom(blake2b.SALT_SIZE)  # a random salt is selected; salts randomize the hash
        h1 = blake2b(salt=salt1)  # provides the salt to the hashing algo
        h1.update(msg)  # hashes the name which is in bytes
        blakeHash = h1.hexdigest()  # returns the encoded data in hexadecimal format
        lastSeven = blakeHash[-7:]  # gives the last seven digits

        return lastSeven  # returns the last seven digits of the hash


# The rest of the code is slightly modified version of the defaults provided with flask


api = Flask(__name__)
# The cors stuff is there to make this api compatible with javascript
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'


@api.route('/' + str(hashCmd), methods=['GET'])
def get_companies():
    hash = {"Hash": hasher()}  # formats the hash into json
    write(hash)  # writes the formatted hash into hash.json
    return hash  # returns the hash to the website that only shows the one hash


if __name__ == '__main__':
    api.run(host='0.0.0.0')  # Runs the site on local computer with the default port
