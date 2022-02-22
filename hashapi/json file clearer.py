import json

print("type the file name to clear")

x = input()


def clear(x):
    dict1 = []
    out_file = open(x, "w")

    json.dump(dict1, out_file, indent=6)

    out_file.close()


clear(x)

print("All Done!")
