"""
Вариант 1 -- Поиск в ширину. 
Поочерёдная обработка вершин текущего фронта, перебор вершин в алфавитном порядке.
"""

class SemiEdge:
    """
    Структура для хранения полуребра, т.е. вершину, в которую ведет ребро, её
    пропускную способность, текущий поток, и флаг, были ли это ребро в изначальной сети 
    """

    to: str
    cost: int
    flow: int
    orig: bool
    def __init__(self, to_, cost_, flow_=0, orig_=False):
        self.to = to_
        self.cost = cost_
        self.flow = flow_
        self.orig = orig_

    def __str__(self):
        return f"-> {self.to}, capacity: {self.cost}, current_flow: {self.flow}"
    
    def __repr__(self):
        return self.__str__()

    """
    Переопределение сравнений для сортировки, чтобы получить корректный формат вывода
    """
    def __lt__(self, rhs):
        return self.to < rhs.to

    def __gt__(self, rhs):
        return self.to > rhs.to

    def __le__(self, rhs):
        return not self > rhs
    
    def __eq__(self, rhs):
        return self.to == rhs

#Считывание данных
edge_count = int(input())
source = input().strip()
drain = input().strip()
graph = dict()

"""
Будем хранить отображения из вершины в массив полуребер, т.е. u -> [SemiEdge(v, ...), SemiEdge(w, ...), ...]
для представления графа
"""

for _ in range(edge_count):
    from_, to_, cost_ = input().split()
    graph[from_] = graph.get(from_, []) + [SemiEdge(to_, int(cost_), 0, True)]

print("Считанный граф: ", graph)

def get_path(graph):
    """
    Функция нахождения пути от истока к стоку, согласно варианту, использует поиск в ширину
    """

    path_from = dict() # мапа, для восстановления пути
    visited = set()
    queue = [source] # очередь для поиска в ширину
    delta = {source: 1e9} # для каждой вершины в пути необходимо знать изменение потока

    while len(queue):
        """
        Поиск в ширину
        """

        cur = queue.pop()
        print(f"Рассматриваем вершину {cur}")
        visited.add(cur)
        if cur == drain: # дошли до стока
            break
        if not graph.get(cur): # у вершины нет исходящих рёбер
            continue
        for semi_edge in sorted(graph[cur]): # перебираем соседние вершины, отсортированные в лекс. граф. порядке
            to_, cost_, flow_ = semi_edge.to, semi_edge.cost, semi_edge.flow
            if to_ not in visited and flow_ < cost_: # еще не были в вершине и можно увеличить поток
                queue.append(to_)
                print(f"Добавляем {to_} в очередь")
                path_from[to_] = cur
                delta[to_] = min(delta[cur], cost_ - flow_)

    """
    Восстановление пути
    """

    result_path = [drain]; cur = drain
    while path_from.get(cur):
        result_path.append(path_from[cur])
        cur = path_from[cur]

    return list(reversed(result_path)), delta.get(drain, 0) # возвращаем дельту, чтобы знать, когда закончить алгоритм

flow = 0
flow_delta = 1
while flow_delta:
    path, flow_delta = get_path(graph)
    print("-" * 10)
    print("Получен путь: ", path)
    print(f"Изменение потока на {flow_delta}")
    for cur in range(len(path)-1): # пройдем по пути и обновим потоки, добавим обратные ребра, если необходимо
        for semi_edge_idx, semi_edge in enumerate(graph[path[cur]]):
            if semi_edge.to == path[cur+1]:
                graph[path[cur]][semi_edge_idx].flow += flow_delta # увеличим поток
                if not graph.get(semi_edge.to):
                    graph[semi_edge.to] = [SemiEdge(path[cur], graph[path[cur]][semi_edge_idx].cost, -flow_delta)] # добавим обратное ребро
                    print(f"Добавлено обратное ребро ({semi_edge.to},{path[cur]})")
                else:
                    """ Ищем обратное ребро, если оно есть, либо опять же добавляем новое """

                    try:
                        to = graph[semi_edge.to].index(path[cur])
                        graph[semi_edge.to][to].flow -= flow_delta
                    except:
                        graph[semi_edge.to].append(SemiEdge(path[cur], graph[path[cur]][semi_edge_idx].cost, -flow_delta))
                        print(f"Добавлено обратное ребро ({semi_edge.to},{path[cur]})")
    flow += flow_delta # обновляем макс. поток
    print("Граф после итерации:", graph)
    print("-" * 10)

print(f"Максимальный поток {flow}")
edges = []

"""
Решаем проблему двойных ребер, формируем ответ    
"""
for node in graph:
    for semi_edge_idx, semi_edge in enumerate(graph[node]):
        if semi_edge.orig:
            try:
                idx = graph[semi_edge.to].index(node)
                if graph[semi_edge.to][idx].orig: # есть (u,v) и (v,u) принадлежащие исходной сети.
                    if semi_edge.flow > 0 and graph[semi_edge.to][idx].flow > 0: # если оба положительные, то в одно разность, в другое 0
                        if semi_edge.flow > graph[semi_edge.to][idx].flow:
                            semi_edge.flow -= graph[semi_edge.to][idx].flow
                            graph[semi_edge.to][idx].flow = 0
                        else:
                            graph[semi_edge.to][idx].flow -= semi_edge.flow
                            semi_edge.flow = 0
                    else: # иначе зануляем отрицательное
                        if semi_edge.flow > graph[semi_edge.to][idx].flow:
                            graph[semi_edge.to][idx].flow = 0
                        else:
                            semi_edge.flow = 0
            except:
                pass
            edges.append((node, semi_edge.to, semi_edge.flow)) # добавляем ребро в ответ
print("Список ребер с потоками:")
import operator # для сортировки по обеим ребрам
edges.sort(key=operator.itemgetter(0, 1))
for edge in edges:
    print(" ".join(map(str, edge))) # вывод списка ребер