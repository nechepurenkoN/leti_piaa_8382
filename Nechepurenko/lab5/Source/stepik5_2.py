
class TrieNode:
    ''' Вспомогательный класс для построения дерева
    '''
    def __init__(self):
        self.goto = {}
        self.out = []
        self.fail = None
        self.idx = None


def aho_create_forest(patterns):
    '''Создать бор - дерево паттернов
    '''
    root = TrieNode()

    for idx, pattern in enumerate(patterns):
        node = root
        for symbol in pattern:
            node = node.goto.setdefault(symbol, TrieNode())
        node.out.append(pattern)
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


def aho_find_all(s, root, bias):
    '''Находит все возможные подстроки из набора паттернов в строке.
    '''
    node = root
    answer = []
    visited = [set() for x in s]
    dp = [0 for _ in range(len(s))]
    for i in range(len(s)):
        while node is not None and s[i] not in node.goto:
            node = node.fail
        if node is None:
            node = root
            continue
        node = node.goto[s[i]]
        for pattern in set(node.out):
            for bias_ in bias[pattern]:
                if i >= bias_:
                    dp[i - len(pattern) + 1 - bias_] += 1
    return dp


text = input()
pattern = input()
joker = input()
patterns = [x for x in pattern.split(joker) if x != '']
assert len(patterns) > 0
bias = {}
used = set()
for pattern_ in reversed(sorted(patterns, key=len)):
    for i in range(len(pattern)):
        idx = pattern.find(pattern_, i)
        if idx != -1 and idx not in used:
            bias[pattern_] = bias.get(pattern_, []) + [idx]
            for j in range(len(pattern_)):
                used.add(idx+j)
bias = {key: set(value) for key, value in bias.items()}
print(f"String biases are: {bias}")
root = aho_create_statemachine(patterns)
answer = aho_find_all(text, root, bias)
print(f"Got dp array: {answer}")
for idx, number in enumerate(answer):
    if number == len(patterns) and idx + len(pattern) <= len(text):
        print(idx+1)