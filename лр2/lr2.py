import random
import timeit
import matplotlib.pyplot as plt


def setup_data(n: int) -> list:
    min_root = 1  # Минимальное значение корня
    max_root = 200  # Максимальное значение корня
    min_height = 1  # Минимальная высота дерева
    max_height = 15  # Максимальная высота дерева

    data = []
    for _ in range(n):
        root = random.randint(min_root, max_root)
        height = random.randint(min_height, max_height)
        data.append((root, height))  # Добавляем пару (root, height) в список

    return data


def calculate_time(n: int, func) -> float:
    data = setup_data(n)
    delta = 0
    for root, height in data:
        start_time = timeit.default_timer()
        func(root, height)
        delta += timeit.default_timer() - start_time
    return delta


def gen_bin_tree1(root=0, height=0):
    """
    Рекурсивная функция для генерации бинарного дерева.
    """
    tree = {}

    def tree_build(root2, height2):
        if height2 > 0:
            left_leaf = root2 * 2
            right_leaf = root2 + 3

            tree[root2] = [
                {left_leaf: tree_build(left_leaf, height2 - 1)},  # Левый потомок
                {right_leaf: tree_build(right_leaf, height2 - 1)}  # Правый потомок
            ]

        else:
            return {}  # Если глубина равна нулю, возвращаем пустой словарь

        return tree[root2]

    if height == 0:
        return {root: []}

    return {root: tree_build(root, height)}


def gen_bin_tree2(root, height):
    """
    Нерекурсивная функция для генерации бинарного дерева.
    """
    tree = {}

    if height == 0:
        return {root: []}

    stack = [(root, height)]  # Стартуем с корнем и полной высотой

    while stack:
        current, current_height = stack.pop()

        if current_height > 1:  # Если глубина больше 1, добавляем дочерние узлы
            left_leaf = current * 2
            right_leaf = current + 3
            stack.append((left_leaf, current_height - 1))
            stack.append((right_leaf, current_height - 1))

        # Создаем текущий узел с дочерними элементами или пустым списком
        tree[current] = []
        if current_height == 1:  # Если следующая глубина должна быть нулевой, добавляем пустые списки
            tree[current].extend([])  # Добавляем пустой список как дочерний элемент
        elif current_height > 1:  # Иначе добавляем реальные узлы
            tree[current].extend([left_leaf, right_leaf])

    return tree
def main():
    # Графики времени выполнения для рекурсивной и нерекурсивной версий
    recursive_times = []
    iterative_times = []

    for n in range(10, 101, 10):  # Измеряем для n от 10 до 100 с шагом 10
        recursive_times.append(calculate_time(n, gen_bin_tree1))
        iterative_times.append(calculate_time(n, gen_bin_tree2))

    plt.figure(figsize=(12, 6))
    plt.title("Сравнение времени выполнения рекурсивной и нерекурсивной версий")
    plt.xlabel("Размер списка (n)")
    plt.ylabel("Общее время выполнения (секунды)")

    # Строим графики для рекурсивной и нерекурсивной версий
    plt.plot(range(10, 101, 10), recursive_times, label="Рекурсия")
    plt.plot(range(10, 101, 10), iterative_times, label="Нерекурсия")

    plt.legend()  # Легенда для обозначения графиков
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()