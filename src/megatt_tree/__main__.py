import newick
from pandas import DataFrame


PATH_TREE = "assets/140k/140k-species-tree.nwk"
PATH_NAMES = "assets/140k/140k-species-map.txt"

BRANCHES = []

NAMES = {}


def convert_node(node: newick.Node):
    for child in node.descendants:
        id_parent = int(node.name.replace("'", "")) if node.name else 1
        id_child = int(child.name.replace("'", ""))
        BRANCHES.append([
            NAMES[id_parent] if id_parent in NAMES else id_parent,
            NAMES[id_child] if id_child in NAMES else id_child,
            child.length,
        ])
        convert_node(child)


if __name__ == "__main__":

    print(f"Loading {PATH_NAMES}")
    with open(PATH_NAMES, encoding="utf8") as f:
        for line in f.readlines():
            k, v = line.split("=", maxsplit=1)
            k, v = int(k), v.replace("\n", "")
            NAMES[k] = v

    print(f"Loading {PATH_TREE} (this takes a while, be patient and watch your RAM usage)")
    with open(PATH_TREE, encoding="utf8") as f:
        tree = newick.load(f)

    print("Converting tree")
    convert_node(tree[0])

    print("Saving tree")
    DataFrame(BRANCHES, columns=["Parent", "Child", "Length"]).to_csv("out.csv")

    print("Done")
