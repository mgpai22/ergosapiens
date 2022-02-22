from fastapi import FastAPI
import json
from dotenv import load_dotenv
import os

load_dotenv()
hashFileCmd = os.getenv("HASHFILECMD")


def data_file():  # Function to load in the data.json file
    with open('hash.json', 'r+') as file:
        return json.load(file)


def data_file1():  # Function to load in the hash.json file
    with open('hashRL.json') as file:
        return json.load(file)


def write(new_data, filename):  # function that appends data to the specified file
    with open(filename, "r") as file1:
        data = json.load(file1)
        data.append(new_data)
    with open(filename, "w") as file1:
        # Sets file's current position at offset.
        file1.seek(0)
        json.dump(data, file1, indent=4)


def clear(x):  # function to clear file and add square brackets
    dict1 = []
    out_file = open(x, "w")

    json.dump(dict1, out_file, indent=6)

    out_file.close()


def loop(limit, offset):
    if offset > 0:
        if limit > len(data_file()) - offset:
            limit = len(data_file()) - offset
    if limit > len(data_file()):
        limit = len(data_file())
    if offset > len(data_file()) - 2:
        offset = len(data_file()) - 1
        limit = 1
    for x in range(limit):
        y = data_file()[x + offset]
        write(y, 'hashRL.json')


app = FastAPI()


@app.get("/" + str(hashFileCmd))
def hash(offset: int = 0, limit: int = 1000000):
    clear("hashRL.json")
    loop(limit, offset)
    return data_file1()
