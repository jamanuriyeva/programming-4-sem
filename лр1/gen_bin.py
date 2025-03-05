"""
Рекурсивный варик
"""
def gen_bin_tree(root=0, height=0):

    tree = {}


    def tree_build(root2, height2):
        if height2 > 0:
            tree[root2] = []
            left_leaf = root2 * 2
            right_leaf = root2 + 3

            tree[root2].append(tree_build(left_leaf, height2 - 1))
            tree[root2].append(tree_build(right_leaf, height2 - 1))

        return root2
    if height == 0:
        return {root: []}
    tree_build(root, height)
    return tree

def main():
    root = 1
    height = 5
    print(gen_bin_tree(root, height))

if __name__ == "__main__":
    main()