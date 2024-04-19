from collections import defaultdict
from email.parser import Parser
import os
import heapq

class Grafo:
    def __init__(self, direcionado=False, ponderado=False):
        self.lista_adjacencias = defaultdict(list)
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.num_vertices = 0
        self.num_arestas = 0
        print(self.ponderado)

    def adiciona_vertice(self, u):
        if u not in self.lista_adjacencias:
            self.lista_adjacencias[u] = []
            self.num_vertices += 1

    def adiciona_aresta(self, u, v, peso=1):
        if not self.ponderado:
            peso = 1

        if v not in self.lista_adjacencias:
            self.adiciona_vertice(v)

        if u not in self.lista_adjacencias:
            self.adiciona_vertice(u)

        if not any(aresta for aresta in self.lista_adjacencias[u] if aresta[0] == v):
            self.lista_adjacencias[u].append((v, peso))
            if not self.direcionado:
                self.lista_adjacencias[v].append((u, peso))
            self.num_arestas += 1
            if not self.direcionado and u != v:
                self.num_arestas += 1
        else:
            for to in self.lista_adjacencias[u]:
                if to[0] == v:
                    segundo_valor = to[1]
                    novo_segundo_valor = segundo_valor + 1  
                    nova_tupla = (to[0], novo_segundo_valor)
                    indice = self.lista_adjacencias[u].index(to)
                    self.lista_adjacencias[u][indice] = nova_tupla
                    print(nova_tupla)

    def remove_aresta(self, u, v):
        antes = len(self.lista_adjacencias[u])
        self.lista_adjacencias[u] = [aresta for aresta in self.lista_adjacencias[u] if aresta[0] != v]
        depois = len(self.lista_adjacencias[u])
        self.num_arestas -= antes - depois
        if not self.direcionado:
            antes = len(self.lista_adjacencias[v])
            self.lista_adjacencias[v] = [aresta for aresta in self.lista_adjacencias[v] if aresta[0] != u]
            depois = len(self.lista_adjacencias[v])
            self.num_arestas -= antes - depois

    def remove_vertice(self, u):
        if u in self.lista_adjacencias:
            self.num_arestas -= len(self.lista_adjacencias[u])
            del self.lista_adjacencias[u]
            self.num_vertices -= 1
            for vertice in self.lista_adjacencias:
                antes = len(self.lista_adjacencias[vertice])
                self.lista_adjacencias[vertice] = [aresta for aresta in self.lista_adjacencias[vertice] if aresta[0] != u]
                depois = len(self.lista_adjacencias[vertice])
                self.num_arestas -= antes - depois

    def tem_aresta(self, u, v):
        return any(aresta for aresta in self.lista_adjacencias[u] if aresta[0] == v)

    def grau_entrada(self, u):
        return sum(1 for vertice in self.lista_adjacencias for aresta in self.lista_adjacencias[vertice] if aresta[0] == u)

    def grau_saida(self, u):
        return len(self.lista_adjacencias[u])

    def grau(self, u):
        return self.grau_entrada(u) + self.grau_saida(u)

    def get_peso(self, u, v):
        for aresta in self.lista_adjacencias[u]:
            if aresta[0] == v:
                return aresta[1]
        return None
    
    def retorna_adjacentes(self, u):
        return [aresta[0] for aresta in self.lista_adjacencias[u]]

    def get_max_arestas(self):
        if self.direcionado:
            return self.num_vertices * (self.num_vertices - 1)
        else:
            return self.num_vertices * (self.num_vertices - 1) / 2

    def imprime_lista_adjacencias(self):
        for vertice, arestas in self.lista_adjacencias.items():
            print(f'{vertice}:', ' -> '.join(f"('{aresta[0]}', {aresta[1]})" for aresta in arestas), '->')
        print(f"Ordem do grafo: {self.num_vertices}")
        print(f"Tamanho do grafo: {self.num_arestas}")

    
    def Dijkstra(self, u):
        distancias = {vertice: float('infinity') for vertice in self.lista_adjacencias}
        distancias[u] = 0
        pq = [(0, u)]
        anterior = {u: None}

        while pq:
            distancia_atual, vertice_atual = heapq.heappop(pq)

            for vizinho, peso in self.lista_adjacencias[vertice_atual]:
                distancia = distancia_atual + peso
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    anterior[vizinho] = vertice_atual
                    heapq.heappush(pq, (distancia, vizinho))

        return distancias, anterior
    
    # Requisito 1
    def processar_emails(self, pasta_emails):

        parser = Parser()
        #caminhando nos diretorios
        for root, dirs, files in os.walk(pasta_emails):
            for filename in files:

                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    email = parser.parsestr(content)
                    from_email = email['from'].strip() if email['from'] else None
                    to_emails = email['to']

                    if from_email and to_emails:
                        recipients = to_emails.split(',')
                        for recipient in recipients:
                            recipient = recipient.strip()
                            if recipient:
                                self.adiciona_aresta(from_email, recipient)
    
    def salvar_lista_adjacencias(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for vertice, arestas in self.lista_adjacencias.items():
                arestas_str = ' -> '.join(f"('{vizinho}', {peso})" for vizinho, peso in arestas)
                file.write(f'{vertice}: {arestas_str}\n')

    # Requisito 2
    def imprime_top_graus(self, tipo='saida'):
        lista_graus = []
        for vertice in self.lista_adjacencias:
            if tipo == 'saida':
                grau = self.grau_saida(vertice)
            else:
                grau = self.grau_entrada(vertice)
            lista_graus.append((vertice, grau))
        
        lista_graus.sort(key=lambda x: x[1], reverse=True)
        print(f"Top 20 graus de {tipo}:")
        for vertice, grau in lista_graus[:20]:
            print(f"{vertice}: {grau}")

    def informacoes_grafo(self):
        print(f"Ordem do grafo: {self.num_vertices}")
        print(f"Tamanho do grafo: {self.num_arestas}")
        self.imprime_top_graus(tipo='saida')
        self.imprime_top_graus(tipo='entrada')

    # Requisito 3
    def e_euleriano(self):
        if not self.direcionado:
            for vertice in self.lista_adjacencias:
                if self.grau(vertice) % 2 != 0:
                    print(f"Vértice com grau ímpar: {vertice}")
                    return False
            return True
        else:
            for vertice in self.lista_adjacencias:
                if self.grau_entrada(vertice) != self.grau_saida(vertice):
                    print(f"Vértice com grau de entrada diferente do grau de saída: {vertice}")
                    return False
            return True
   
    # Requisito 4
    def bfs(self, u, v):
        visitados = set()
        fila = [u]
        caminho = []
        
        while fila:
            vertice = fila.pop(0)
            if vertice not in visitados:
                visitados.add(vertice)
                caminho.append(vertice)
                if vertice == v:
                    print("Caminho encontrado:")
                    print(caminho)
                    return True
                for vizinho, _ in self.lista_adjacencias[vertice]:
                    if vizinho not in visitados:
                        fila.append(vizinho)
        print("Não há caminho entre os vértices fornecidos")
        return False
    
    # Requisito 5
    def vertices_ate_distancia_D(self, N, D):
        if N not in self.lista_adjacencias:
            return "O vértice não existe no grafo", []

        distancias, _ = self.Dijkstra(N)
        vertices_ate_D = [vertice for vertice, distancia in distancias.items() if distancia <= D]
        return vertices_ate_D

    # Requisito 6
    def encontrar_diametro(self):
        maior_caminho = 0
        caminho_diametro = []

        for u in self.lista_adjacencias:
            distancias, anteriores = self.Dijkstra(u)
            for v, distancia in distancias.items():
                if distancia > maior_caminho and distancia != float('infinity'):
                    maior_caminho = distancia
                    caminho_diametro = []
                    passo = v

                    while passo is not None:
                        caminho_diametro.append(passo)
                        passo = anteriores[passo]

                    caminho_diametro.reverse()

        return maior_caminho, caminho_diametro