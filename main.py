from Grafo import Grafo

if __name__ == "__main__":
    grafo_emails = Grafo(direcionado=True, ponderado=True)
    path = 'enron'
    grafo_emails.processar_emails(path)
    grafo_emails.salvar_lista_adjacencias('grafo_adjacencias_teste.txt')
    grafo_emails.informacoes_grafo()

    # diametro, caminho = grafo_emails.encontrar_diametro()
    # print("Diâmetro do grafo:", diametro)
    # print("Caminho do diâmetro:", caminho)

    # resultado = grafo_emails.vertices_ate_distancia_D('anitha.mathis@enron.com', 2)
    # print("Vértices até a distância 10 de N:", resultado)