def novo_tabuleiro():
    return [[0] * 10 for _ in range(10)]


def celula_do_mouse(mouse_x, mouse_y):
    coluna = (mouse_x - 40) // 52
    linha = (mouse_y - 40) // 52
    if 0 <= coluna < 10 and 0 <= linha < 10:
        return coluna, linha


def pode_colocar(tabuleiro, coluna, linha):
    if coluna + 3 > 10:
        return False
    for deslocamento in range(3):
        if tabuleiro[linha][coluna + deslocamento] != 0:
            return False
    return True


def coloca_navio(tabuleiro, coluna, linha, id_navio):
    for deslocamento in range(3):
        tabuleiro[linha][coluna + deslocamento] = id_navio


def aplicar_tiro(tabuleiro, tiros_jogador, coluna, linha):
    id_navio = tabuleiro[linha][coluna]

    if id_navio == 0:
        tiros_jogador.append((coluna, linha))
        return False

    for indice_linha in range(10):
        for indice_coluna in range(10):
            if tabuleiro[indice_linha][indice_coluna] == id_navio and (indice_coluna, indice_linha) not in tiros_jogador:
                tiros_jogador.append((indice_coluna, indice_linha))
    return True


def todos_destruidos(tabuleiro, tiros_jogador):
    for linha in range(10):
        for coluna in range(10):
            if tabuleiro[linha][coluna] != 0 and (coluna, linha) not in tiros_jogador:
                return False
    return True


def contar_destruidos(tabuleiro, tiros_jogador):
    ids_destruidos = set()
    for linha in range(10):
        for coluna in range(10):
            id_navio = tabuleiro[linha][coluna]
            if id_navio != 0 and (coluna, linha) in tiros_jogador:
                ids_destruidos.add(id_navio)
    return len(ids_destruidos)
