# PathFinder2D

## Contribuidores
- [André Augusto](https://github.com/AndreAugusto0908)
- [Gabriel Matos](https://github.com/gabrielmatosmartins)
- [Italo Lelis](https://github.com/italohdc)
- [Kayler Moura](https://github.com/KaylerMm)
- [Pedro Couto](https://github.com/PedroPCouto)

## Visão Geral

PathFinder2D é uma implementação didática do algoritmo A* (A-estrela) para encontrar o caminho mais curto em um labirinto 2D. O projeto foi desenvolvido para a disciplina de FPAA, com foco em:
- Compreender os conceitos de busca informada.
- Aplicar a heurística de Manhattan.
- Visualizar o caminho encontrado diretamente na matriz do labirinto.

O algoritmo utiliza uma fila de prioridade (heap) para expandir sempre o nó mais promissor, combinando o custo acumulado do caminho com uma estimativa da distância restante até o objetivo.

## Problema

Dado um labirinto representado por uma matriz 2D:
- `S` = início
- `E` = objetivo
- `0` = célula livre
- `1` = parede/obstáculo

Objetivo: encontrar o menor caminho entre `S` e `E` evitando obstáculos.  
Movimentação permitida: ortogonal (cima, baixo, esquerda, direita).

## Algoritmo A*

O A* combina:
- Custo do caminho g(n): custo acumulado desde `S` até o nó `n`.
- Heurística h(n): estimativa do custo de `n` até `E`. Aqui usamos a distância de Manhattan:
  
  h(n) = |x1 − x2| + |y1 − y2|

- Função de avaliação f(n): f(n) = g(n) + h(n)

Estruturas:
- Lista Aberta: candidatos a explorar (implementada com `heapq`).
- Melhores custos conhecidos (`g_score`) e predecessores (`caminho`) para reconstrução da rota.

Fluxo resumido:
1. Coloca `S` na lista aberta.
2. Remove o nó com menor `f`.
3. Expande vizinhos válidos (não são paredes).
4. Atualiza `g`, `h` e `f`; registra predecessores quando encontra um caminho melhor.
5. Repete até alcançar `E` ou esgotar a lista aberta.
6. Reconstrói o caminho usando o mapa de predecessores.

## Destaques da Implementação

- Heurística Manhattan (`heuristica(a, b)`).
- Vizinhança ortogonal com checagem de limites e obstáculos (`vizinhos`).
- Reconstrução do caminho via predecessores (`reconstruir_caminho`).
- Impressão do labirinto com o caminho marcado por `*` sem alterar `S` e `E` (`imprimir_labirinto`).
- Três cenários de exemplo no `main()`:
  - Labirinto simples com solução.
  - Labirinto sem solução.
  - Labirinto com múltiplos caminhos.

## Código Principal (trecho)

```python
import heapq

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def encontrar_ponto(labirinto, valor):
    for i, linha in enumerate(labirinto):
        for j, celula in enumerate(linha):
            if celula == valor:
                return (i, j)
    return None

def vizinhos(pos, labirinto):
    direcoes = [(-1,0),(1,0),(0,-1),(0,1)]
    resultado = []
    for dx, dy in direcoes:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]):
            if labirinto[nx][ny] != '1':
                resultado.append((nx, ny))
    return resultado

def reconstruir_caminho(caminho, atual):
    total = [atual]
    while atual in caminho:
        atual = caminho[atual]
        total.append(atual)
    total.reverse()
    return total

def a_estrela(labirinto):
    inicio = encontrar_ponto(labirinto, 'S')
    fim = encontrar_ponto(labirinto, 'E')

    if not inicio or not fim:
        print("Labirinto inválido: ponto S ou E não encontrado.")
        return

    fila = []
    heapq.heappush(fila, (0, inicio))
    caminho = {}
    g_score = {inicio: 0}
    f_score = {inicio: heuristica(inicio, fim)}

    while fila:
        _, atual = heapq.heappop(fila)

        if atual == fim:
            return reconstruir_caminho(caminho, atual)

        for viz in vizinhos(atual, labirinto):
            tentativo_g = g_score[atual] + 1
            if tentativo_g < g_score.get(viz, float('inf')):
                caminho[viz] = atual
                g_score[viz] = tentativo_g
                f_score[viz] = tentativo_g + heuristica(viz, fim)
                heapq.heappush(fila, (f_score[viz], viz))

    return None

def imprimir_labirinto(labirinto, caminho):
    labirinto_copia = [linha.copy() for linha in labirinto]
    for x, y in caminho:
        if labirinto_copia[x][y] == '0':
            labirinto_copia[x][y] = '*'
    for linha in labirinto_copia:
        print(" ".join(linha))

def main():
    print("\n=== Exemplo 1: Labirinto Simples ===")
    labirinto1 = [
        ['S','0','1','0','0'],
        ['0','0','1','0','1'],
        ['1','0','1','0','0'],
        ['1','0','0','E','1']
    ]
    print("\nLabirinto Original:")
    for linha in labirinto1:
        print(" ".join(linha))
    caminho1 = a_estrela(labirinto1)
    if caminho1:
        print("\nMenor caminho encontrado:")
        imprimir_labirinto(labirinto1, caminho1)
    else:
        print("Sem solução.")

    print("\n=== Exemplo 2: Labirinto Sem Solução ===")
    labirinto2 = [
        ['S','1','0','0','0'],
        ['1','1','1','0','1'],
        ['0','0','1','0','0'],
        ['1','1','1','E','1']
    ]
    print("\nLabirinto Original:")
    for linha in labirinto2:
        print(" ".join(linha))
    caminho2 = a_estrela(labirinto2)
    if caminho2:
        print("\nMenor caminho encontrado:")
        imprimir_labirinto(labirinto2, caminho2)
    else:
        print("Sem solução.")

    print("\n=== Exemplo 3: Labirinto com Múltiplos Caminhos ===")
    labirinto3 = [
        ['S','0','0','0','0'],
        ['1','1','0','1','0'],
        ['0','0','0','0','0'],
        ['0','1','1','1','E']
    ]
    print("\nLabirinto Original:")
    for linha in labirinto3:
        print(" ".join(linha))
    caminho3 = a_estrela(labirinto3)
    if caminho3:
        print("\nMenor caminho encontrado:")
        imprimir_labirinto(labirinto3, caminho3)
    else:
        print("Sem solução.")

if __name__ == "__main__":
    main()