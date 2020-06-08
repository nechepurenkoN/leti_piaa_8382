#Вариант 2. Подсчитать количество вершин в автомате; 
#вывести список найденных образцов, имеющих пересечения с другими найденными образцами в строке поиска.

import operator

class TrieNode:
    ''' Вспомогательный класс для построения дерева
    '''
    def __init__(self):
        self.goto = {}
        self.out = []
        self.fail = None
        self.pNumber = 0

    def __str__(self):
        return f"[Node: goto={self.goto.keys()}, suff={self.fail}, pNumber={self.pNumber}]"


def aho_create_forest(patterns):
    '''Создать бор - дерево паттернов
    '''
    root = TrieNode()

    for idx, path in enumerate(patterns):
        node = root
        for symbol in path:
            node = node.goto.setdefault(symbol, TrieNode())
            node.pNumber = idx + 1
        node.out.append(path)
    return root


def aho_create_statemachine(patterns):
    '''Создать автомат Ахо-Корасика.
    Фактически создает бор и инициализирует fail-функции
    всех узлов, обходя дерево в ширину.
    '''
    # Создаем бор, инициализируем
    # непосредственных потомков корневого узла
    root = aho_create_forest(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        node.fail = root

    # Инициализируем остальные узлы:
    # 1. Берем очередной узел (важно, что проход в ширину)
    # 2. Находим самую длинную суффиксную ссылку для этой вершины - это и будет fail-функция
    # 3. Если таковой не нашлось - устанавливаем fail-функцию в корневой узел
    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            queue.append(unode)
            fnode = rnode.fail
            while fnode is not None and key not in fnode.goto:
                fnode = fnode.fail
            unode.fail = fnode.goto[key] if fnode else root
            unode.out += unode.fail.out

    return root


def aho_find_all(text, root, number):
    '''Находит все возможные подстроки из набора паттернов в строке.
    '''
    node = root
    answer = []
    overlapping = set()
    for i in range(len(text)):
        while node is not None and text[i] not in node.goto:
            if node is not root and node.fail is not root:
                overlapping.add((node.pNumber, node.fail.pNumber))
            node = node.fail
        if node is None:
            node = root
            continue
        node = node.goto[text[i]]
        for pattern in node.out:
            answer.append((i - len(pattern) + 1 + 1, number[pattern] + 1))
    return sorted(answer, key=operator.itemgetter(0, 1)), overlapping

def get_nodes_count(root):
    """
    Подсчёт числа узлов поиском в ширину
    """
    queue = [root]
    count = 0
    while len(queue):
        current = queue.pop(0)
        count += 1
        queue.extend(current.goto.values())
    return count

def print_trie(root):
    """
    Вывод узлов поиском в ширину
    """
    queue = [root]
    while len(queue):
        current = queue.pop(0)
        print(current)
        queue.extend(current.goto.values())
    
#Читаем данные
s = input()
n = int(input())
patterns = []
for _ in range(n):
    patterns.append(input())

root = aho_create_statemachine(patterns)
print_trie(root)
print(f"Nodes in trie: {get_nodes_count(root)}")
answer, preoverlapping = aho_find_all(s, root, {pattern: idx for idx, pattern in enumerate(patterns)})
overlapping = {(patterns[a-1], patterns[b-1]) for a, b in preoverlapping if a != b} # переведем индексы в образцы
print("Answer:")
for row in answer:
    print(*row)
print(f"Overlapping strings: {overlapping}")
