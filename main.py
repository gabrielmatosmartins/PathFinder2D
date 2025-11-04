from __future__ import annotations
import heapq
from typing import Dict, Iterable, List, Optional, Tuple

Pos = Tuple[int, int]           # (linha, coluna)
Labirinto = List[List[str]]     # matriz 2D de strings: 'S', 'E', '0', '1'

# ------------------------------------------------------------
# Heurística e utilitários
# ------------------------------------------------------------

def manhattan(a: Pos, b: Pos) -> int:
    """
    Calcula a distância de Manhattan entre as posições a e b.
    Admissível e consistente para grids com movimentos ortogonais.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def encontrar(lab: Labirinto, alvo: str) -> Optional[Pos]:
    """
    Localiza a primeira ocorrência do símbolo 'alvo' no labirinto.
    Retorna a posição (linha, coluna) ou None se não existir.
    """
    for i, linha in enumerate(lab):
        for j, celula in enumerate(linha):
            if celula == alvo:
                return (i, j)
    return None


def dentro_dos_limites(lab: Labirinto, x: int, y: int) -> bool:
    """
    Verifica se a posição (x, y) pertence ao grid do labirinto.
    """
    return 0 <= x < len(lab) and 0 <= y < len(lab[0])


def eh_transponivel(lab: Labirinto, x: int, y: int) -> bool:
    """
    Retorna True se a célula pode ser atravessada (não é parede '1').
    """
    return lab[x][y] != '1'


def vizinhos_ortogonais(pos: Pos, lab: Labirinto) -> Iterable[Pos]:
    """
    Gera até 4 vizinhos ortogonais transponíveis a partir de 'pos'.
    Filtra por limites do grid e por obstáculos.
    """
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if dentro_dos_limites(lab, nx, ny) and eh_transponivel(lab, nx, ny):
            yield (nx, ny)


def reconstruir_caminho(antecessor: Dict[Pos, Pos], destino: Pos) -> List[Pos]:
    """
    Reconstrói o caminho completo da origem até 'destino' utilizando
    o dicionário de antecessores (predecessor de cada posição).
    """
    caminho: List[Pos] = [destino]
    atual = destino
    # Retorna caminhando pelos antecessores até chegar ao início,
    # que não aparece como chave em 'antecessor'.
    while atual in antecessor:
        atual = antecessor[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho


# ------------------------------------------------------------
# A* (A-estrela)
# ------------------------------------------------------------

def a_estrela(lab: Labirinto) -> Optional[List[Pos]]:
    """
    Executa o A* e retorna a lista de posições do menor caminho de 'S' até 'E'.
    Caso não exista caminho, retorna None.
    Pré-condições: deve haver exatamente um 'S' e um 'E' no labirinto.
    """
    inicio = encontrar(lab, 'S')
    fim = encontrar(lab, 'E')

    if not inicio or not fim:
        print("Labirinto inválido: ponto 'S' ou 'E' não encontrado.")
        return None

    # Lista aberta (min-heap) prioriza menor f(n)
    aberta: List[Tuple[int, Pos]] = []
    heapq.heappush(aberta, (0, inicio))

    # Dicionários de estado
    antecessor: Dict[Pos, Pos] = {}
    g: Dict[Pos, int] = {inicio: 0}
    f: Dict[Pos, int] = {inicio: manhattan(inicio, fim)}

    while aberta:
        # Seleciona nó com menor f
        _, atual = heapq.heappop(aberta)

        # Chegou ao objetivo
        if atual == fim:
            return reconstruir_caminho(antecessor, atual)

        # Expande vizinhos
        for viz in vizinhos_ortogonais(atual, lab):
            custo_tentativo = g[atual] + 1  # custo uniforme
            if custo_tentativo < g.get(viz, float('inf')):
                antecessor[viz] = atual
                g[viz] = custo_tentativo
                f[viz] = custo_tentativo + manhattan(viz, fim)
                heapq.heappush(aberta, (f[viz], viz))

    # Sem solução
    return None


# ------------------------------------------------------------
# Visualização
# ------------------------------------------------------------

def imprimir_labirinto(lab: Labirinto, caminho: Optional[List[Pos]] = None) -> None:
    """
    Imprime a matriz do labirinto. Caso 'caminho' seja fornecido, marca as
    posições com '*' sem sobrescrever 'S' e 'E'.
    """
    copia = [linha.copy() for linha in lab]

    if caminho:
        for x, y in caminho:
            if copia[x][y] == '0':
                copia[x][y] = '*'

    for linha in copia:
        print(" ".join(linha))


def executar_exemplo(titulo: str, lab: Labirinto) -> None:
    """
    Executa A* para um labirinto de exemplo, imprimindo entrada e saída.
    Facilita testes manuais e demonstração do algoritmo.
    """
    print(f"\n=== {titulo} ===")
    print("\nLabirinto Original:")
    imprimir_labirinto(lab)

    caminho = a_estrela(lab)
    if caminho:
        print("\nMenor caminho encontrado:")
        imprimir_labirinto(lab, caminho)
    else:
        print("\nSem solução.")


# ------------------------------------------------------------
# Exemplos
# ------------------------------------------------------------

def main() -> None:
    # Exemplo 1: solução simples
    labirinto1: Labirinto = [
        ['S', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '1'],
        ['1', '0', '1', '0', '0'],
        ['1', '0', '0', 'E', '1'],
    ]

    # Exemplo 2: sem solução
    labirinto2: Labirinto = [
        ['S', '1', '0', '0', '0'],
        ['1', '1', '1', '0', '1'],
        ['0', '0', '1', '0', '0'],
        ['1', '1', '1', 'E', '1'],
    ]

    # Exemplo 3: múltiplos caminhos
    labirinto3: Labirinto = [
        ['S', '0', '0', '0', '0'],
        ['1', '1', '0', '1', '0'],
        ['0', '0', '0', '0', '0'],
        ['0', '1', '1', '1', 'E'],
    ]

    executar_exemplo("Exemplo 1: Labirinto Simples", labirinto1)
    executar_exemplo("Exemplo 2: Labirinto Sem Solução", labirinto2)
    executar_exemplo("Exemplo 3: Labirinto com Múltiplos Caminhos", labirinto3)


if __name__ == "__main__":
    main()
