import itertools
import random
import math
import time


"""
Nome: Miguel Filipe Rodrigues Almeida de Matos Fazenda
Nº 110877
Curso: Mestrado em Engenharia Informática
"""


"""-----------------Funções que criam os dados-----------------"""


# verifica se os pontos estão muito perto uns dos outros
def check_closeness(pontos, x, y):
    if len(pontos) == 0:
        return False
    else:
        for ponto in pontos:
            dist = math.sqrt((x - ponto[0]) ** 2 + (y - ponto[1]) ** 2)  # distância euclidiana no espaço bidimensional
            if dist < 2:  # ponto está muito perto
                return True

        return False


# Função que cria os pontos do gráfica
def create_vertices(quant_vertices):
    vertices = []

    for ind in range(quant_vertices):
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        while check_closeness(vertices, x, y):
            x = random.randint(1, 10)
            y = random.randint(1, 10)
        vertices.append((x, y))

    return vertices


# Função que cria as arestas entre os pontos
def create_arestas(lista_vertices):
    return set(itertools.combinations(lista_vertices,
                                      2))  # cria arestas sem repetições(para mesmo par de vertices, só há 1 aresta)


# função que cria a grafo com base nas arestas
def create_grafo(set_arestas, quant_arestas):
    return set(itertools.combinations(set_arestas,
                                      quant_arestas))  # cria todas as combinações de arestas possíveis de acordo com quantArestas


"""-----------------Lógica para encontrar o Maximum Matching-----------------"""


# função que ajuda a ordenar a lista
# O(1)
def order(comb_arestas):
    return len(comb_arestas)  # retorna a quantidade de pontos


# função que calcula o maximum matching
# a diferença entre brute force e greedy heuristics está no input
# no brute force o input não sofre alterações
# no greedy heuristics o input é ordenado descendentemente pela quantidade de arestas
# O(n^2 + n)
def maximum_matching(comb_arestas):
    pontos = []

    for aresta in comb_arestas:
        for ponto in aresta:
            pontos.append(ponto)

    # O(n) -> transformar lista para set
    if len(pontos) - len(set(pontos)) == 0:  # não há ligações (BEST CASE!!!)
        return comb_arestas
    return None  # há ligações (ignora...)


if __name__ == '__main__':
    random.seed(110877)

    create_init = time.time()

    quant_vertices = 6
    quant_arestas = 4

    # 20C4 -> res
    # resC4 -> todas as combinações

    # verificar se está em [1, 9]
    # while quant_vertices > 10 or quant_vertices < 1:
    #     quant_vertices = input("Indique a quantidade de pontos pretendida(1 a 10): ")

    # verificar se está em [1, quantVertices-1]
    # while quant_arestas > len(
    #         lista_arestas) or quant_arestas < 1:  # len(listaArestas) -> quantidade máxima de combinações possíveis
    #     quant_arestas = input("Indique a quantidade de arestas pretendidas: ")

    lista_vertices = create_vertices(quant_vertices)  # tuplo (x, y)
    set_arestas = create_arestas(lista_vertices)  # set com tuplos ((x, y), (x, y))

    # cria matriz com a quantidade de arestas pretendidas
    # {(((), ()), ((), ())), (((), ()), ((), ())), (((), ()), ((), ()))}
    # descomentar comentário de cima para perceber a estrutura(com plugin "rainbow brackets")
    grafo = create_grafo(set_arestas, quant_arestas)
    # grafo é composto por lista de arestas
    # arestas são compostas por lista de tuplos de pontos(ponto1, ponto2)
    # pontos são compostos por tuplos de coordenadas(x, y)

    create_end = time.time()

    # escolhe maximum matching(combinação de arestas)
    # brute force
    # O(n^3) -> O(n) * O(n^2)
    brute_start = time.time()
    brute = []
    brute_count = 0
    for comb_arestas in grafo:
        if maximum_matching(comb_arestas) is not None:
            brute.append(comb_arestas)

    # print(time.time())
    brute_time = time.time() - brute_start

    # greedy heuristics
    # O(n^3) -> O(2n) + O(n) * O(n^2)  (WORST CASE)
    # O(m + n^2) -> O(2n) + O(m) * O(n^2) (NOT SURE... visto que a ideia é encontrar um "máximo local"/primeiro maximum match)
    # m ∈ [1, n]
    greedy_start = time.time()
    greed = None
    lista = list(grafo)  # transforma para lista para conseguir ordenar O(n)
    lista.sort(key=order)  # ordena por ordem descendente e quantidade de arestas O(n)

    for x in lista:
        greed = maximum_matching(x)
        if greed is not None:
            break

    greedy_time = time.time() - greedy_start

    print("Tempo para criar tudo: " + str(create_end - create_init) + " segundos")
    print("Tempo para brute force: " + str(brute_time) + " segundos")
    print("Tempo para greedy heuristics: " + str(greedy_time) + " segundos")
    print("Quantidade de soluções para brute-force: " + str(len(brute)))
    if greed:
        print("Quantidade de soluções para greedy heuristics: " + str(greed))
    else:
        print("Quantidade de soluções para greedy heuristics: " + str(0))
