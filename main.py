from Grafo import Grafo

if __name__ == "__main__":
    grafo_emails = Grafo(direcionado=True, ponderado=True)
    path = 'enron_menor'

    grafo_emails.processar_emails(path)
    grafo_emails.salvar_lista_adjacencias('grafo_adjacencias_teste.txt')
    grafo_emails.informacoes_grafo()

    print(f"Grafo euleriano? {grafo_emails.e_euleriano()}")

    mike = "mike.carson@enron.com"
    mcarson = "mcarson@gtemail.net"
    print(f"É possivel ir de {mike} a {mcarson}? {grafo_emails.bfs(mike, mcarson)}")
    thenninger = "thenninger@mail.law.utexas.edu"
    print(f"É possivel ir de {mike} a {thenninger}? {grafo_emails.bfs(mike, thenninger)}")

    resultado = grafo_emails.vertices_ate_distancia_D('james.derrick@enron.com', 1)
    print("Vértices até a distância D de N: (james.derrick@enron.com)", resultado)

    diametro, caminho = grafo_emails.encontrar_diametro()
    print("Diâmetro do grafo:", diametro)
    print("Caminho do diâmetro:", caminho)

