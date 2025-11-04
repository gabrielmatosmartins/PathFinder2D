from __future__ import annotations
import heapq
from typing import Dict, Iterable, List, Optional, Tuple

Pos = Tuple[int, int]
Labirinto = List[List[str]]

# ------------------------------------------------------------
# Heurística e utilitários
# ------------------------------------------------------------

def manhattan(a: Pos, b: Pos) -> int:
    """Distância de Manhattan entre as posições a e b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def encontrar(lab: Labirinto, alvo: str) -> Optional[Pos]:
    """Encontra a primeira ocorrência do símbolo alvo no labirinto."""
    for i, linha in enumerate(lab):
        for j, celula in enumerate(linha):
            if celula == alvo:
                return (i, j)
    return None


def dentro_dos_limites(lab: Labirinto, x: int, y: int) -> bool:
    """Verifica se (x, y) é uma posição válida no labirinto."""
    return 0 <= x < len(lab) and 0 <= y < len(lab[0])


def eh_transponivel(lab: Labirinto, x: int, y: int) -> bool:
    """Verifica se a célula pode ser atravessada (não é parede)."""
    return lab[x][y] != '1'


def vizinhos_ortogonais(pos: Pos, lab: Labirinto) -> Iterable[Pos]:
    """Gera posições vizinhas ortogonais válidas e transponíveis."""
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if dentro_dos_limites(lab, nx, ny) and eh_transponivel(lab, nx, ny):
            yield (nx, ny)


def reconstruir_caminho(antecessor: Dict[Pos, Pos], destino: Pos) -> List[Pos]:
    """Reconstrói a lista de posições desde a origem até o destino."""
    caminho: List[Pos] = [destino]
    atual = destino
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
    Retorna a lista de posições do menor caminho de S até E usando A*.
    Se não houver solução, retorna None.
    """
    inicio = encontrar(lab, 'S')
    fim = encontrar(lab, 'E')

    if not inicio or not fim:
        print("Labirinto inválido: ponto 'S' ou 'E' não encontrado.")
        return None

    # Min-heap com tuplas (f, pos)
    aberta: List[Tuple[int, Pos]] = []
    heapq.heappush(aberta, (0, inicio))

    antecessor: Dict[Pos, Pos] = {}
    g: Dict[Pos, int] = {inicio: 0}
    f: Dict[Pos, int] = {inicio: manhattan(inicio, fim)}

    while aberta:
        _, atual = heapq.heappop(aberta)

        if atual == fim:
            return reconstruir_caminho(antecessor, atual)

        for viz in vizinhos_ortogonais(atual, lab):
            custo_tentativo = g[atual] + 1  # custo uniforme = 1
            if custo_tentativo < g.get(viz, float('inf')):
                antecessor[viz] = atual
                g[viz] = custo_tentativo
                f[viz] = custo_tentativo + manhattan(viz, fim)
                heapq.heappush(aberta, (f[viz], viz))

    return None


# ------------------------------------------------------------
# Visualização
# ------------------------------------------------------------

def imprimir_labirinto(lab: Labirinto, caminho: Optional[List[Pos]] = None) -> None:
    """
    Imprime o labirinto. Se um caminho for fornecido, marca-o com '*'
    sem sobrescrever 'S' e 'E'.
    """
    copia = [linha.copy() for linha in lab]

    if caminho:
        for x, y in caminho:
            if copia[x][y] == '0':
                copia[x][y] = '*'

    for linha in copia:
        print(" ".join(linha))


def executar_exemplo(titulo: str, lab: Labirinto) -> None:
    """Executa A* em um labirinto exemplo e imprime entrada e saída."""
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
    labirinto1: Labirinto = [
        ['S', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '1'],
        ['1', '0', '1', '0', '0'],
        ['1', '0', '0', 'E', '1'],
    ]

    labirinto2: Labirinto = [
        ['S', '1', '0', '0', '0'],
        ['1', '1', '1', '0', '1'],
        ['0', '0', '1', '0', '0'],
        ['1', '1', '1', 'E', '1'],
    ]

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