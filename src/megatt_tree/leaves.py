import csv
from pandas import DataFrame

LEAVES_PATH = "leaves.csv"
TREE_PATH = "tree.csv"

PARENT = {}
LENGTH = {}

ROOT = 4250
ROOT_NAME = "cellular organisms"

def leaves():
    print("Loading leaves file")
    with open(LEAVES_PATH) as f:
        reader = csv.reader(f)
        next(reader) # csv header
        leaves = [*reader]

    print("Loading tree")
    with open(TREE_PATH) as f:
        reader = csv.reader(f)
        next(reader) # csv header
        for parent, child, length in reader:
            PARENT[child] = parent
            LENGTH[child] = float(length)

    for leaf_sci, leaf_colloq in leaves:
        if leaf_sci not in PARENT:
            print(f"{leaf_sci} not found")
            continue

        node = leaf_sci
        path = [[node, 0]]

        while node != ROOT_NAME:
            path.append([PARENT[node], LENGTH[node]])
            node = PARENT[node]

        df = DataFrame(path, columns=[leaf_colloq, "spans"])

        offset = ROOT - df["spans"].sum()
        df["mya"] = df["spans"].cumsum() + offset
        del df["spans"]
        df = df.iloc[::-1]

        leaf_file = leaf_colloq.replace(" ", "-").lower()
        df.to_csv(f"out/{leaf_file}.csv", index=False)
