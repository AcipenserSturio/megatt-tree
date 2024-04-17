import csv
from pandas import DataFrame

LEAVES_PATH = "leaves.csv"
TREE_PATH = "tree.csv"

TREE = {}

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
            TREE[child] = parent, length

    for leaf_sci, leaf_colloq in leaves:
        if leaf_sci not in TREE:
            # print(f"{leaf_sci} not found in tree")
            continue

        path = []
        node = leaf_sci

        while node != "cellular organisms":
            path.append([node, float(TREE[node][1])]) # node name, length
            node = TREE[node][0] # go to parent

        path.append(["cellular organisms", 0])

        df = DataFrame(path, columns=[leaf_colloq, "spans"])

        offset = 4250 - df["spans"].sum()
        df["mya"] = df["spans"].cumsum() + offset
        del df["spans"]
        df = df.iloc[::-1]


        leaf_file = leaf_colloq.replace(" ", "-").lower()
        df.to_csv(f"out/{leaf_file}.csv", index=False)

        print(offset, leaf_colloq, sep=",")
