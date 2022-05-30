from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from dotenv import load_dotenv
from hashlib import blake2b
import os
import sqlFunctions

load_dotenv()
hashcmd = os.getenv("HASHCMD")
hashFileCmd = os.getenv("HASHFILECMD")


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


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlFunctions.createHashTable()
sqlFunctions.createHashTableTest()


@app.get("/" + str(hashcmd))
def getHash():
    hash = hasher()
    sqlFunctions.writeToHash(hash)
    hashData = {"Hash": hash}
    return hashData


@app.get("/{hashFileCmd}/{hash_to_check}")
async def checkValidity(hash_to_check: str):
    validity = sqlFunctions.validateHash(hash_to_check)
    return {"Validity": validity}


@app.get("/thash")
def getHashTest():
    hash = hasher()
    sqlFunctions.writeToHashTest(hash)
    hashData = {"Hash": hash}
    return hashData


@app.get("/test/{hashFileCmd}/{hash_to_check}")
async def checkValidityTest(hash_to_check: str):
    validity = sqlFunctions.validateHashTest(hash_to_check)
    return {"Validity": validity}


@app.get("/{test_hash_to_add}")
async def addHashTest(test_hash_to_add: str):
    try:
        sqlFunctions.writeToHashTest(test_hash_to_add)
        return {"Status": "successful"}
    except Exception as e:
        pass
    return {"Status": "unsuccessful"}
