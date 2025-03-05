"""
Нерекурсивный варик
"""
def gen_bin_tree(root, height):
    tree = {}

    if height == 0:
        return {root: []}
    stack = [(root, height)]

    while stack:
        current, current_height = stack.pop()

        if current_height > 0:
            tree[current] = []
            left_leaf = current * 2
            right_leaf = current + 3

            stack.append((left_leaf, current_height - 1))
            stack.append((right_leaf, current_height - 1))
            tree[current].append(left_leaf)
            tree[current].append(right_leaf)

    return tree

def main():
    root = 1
    height = 5
    print(gen_bin_tree(root, height))

if __name__ == "__main__":
    main()
