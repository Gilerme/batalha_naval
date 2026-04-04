import pygame
import sys
from logica_jogo import (
    novo_tabuleiro,
    celula_do_mouse,
    pode_colocar,
    coloca_navio,
    aplicar_tiro,
    contar_destruidos,
    todos_destruidos
)
from interface_jogo import (
    criar_janela,
    desenhar_grade,
    desenhar_info,
    mensagem,
    tocar_som,
    tela_vitoria,
    tela_inicial
)

def main():
    tela_jogo, relogio_jogo, fonte_pequena, fonte_media, fonte_grande, sons_jogo = criar_janela()

    estado_jogo = "tela_inicial"
    tocar_som(sons_jogo, "trilha", -1)
    tocar_som(sons_jogo, "mar", -1)
    tocar_som(sons_jogo, "guerra", -1)
    tabuleiro_player1 = novo_tabuleiro()
    tabuleiro_player2 = novo_tabuleiro()
    tiros_player1 = []
    tiros_player2 = []
    navios_colocados_player1 = 0
    navios_colocados_player2 = 0
    jogador_vencedor = 0
    som_vitoria_tocado = False

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: 
                if estado_jogo == "tela_inicial":
                    estado_jogo = "setup1"
                
                elif estado_jogo == "setup1":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and navios_colocados_player1 < 7:
                        coluna, linha = celula
                        if pode_colocar(tabuleiro_player1, coluna, linha):
                            navios_colocados_player1 += 1
                            coloca_navio(tabuleiro_player1, coluna, linha, navios_colocados_player1)
                            tocar_som(sons_jogo, "colocou")
                            if navios_colocados_player1 == 7:
                                estado_jogo = "trans_p2"

                elif estado_jogo == "trans_p2":
                    estado_jogo = "setup2"

                elif estado_jogo == "setup2":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and navios_colocados_player2 < 7:
                        coluna, linha = celula
                        if pode_colocar(tabuleiro_player2, coluna, linha):
                            navios_colocados_player2 += 1
                            coloca_navio(tabuleiro_player2, coluna, linha, navios_colocados_player2)
                            tocar_som(sons_jogo, "colocou")
                            if navios_colocados_player2 == 7:
                                estado_jogo = "trans_batalha"

                elif estado_jogo == "trans_batalha":
                    estado_jogo = "batalha1"

                elif estado_jogo == "batalha1":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and celula not in tiros_player1:
                        coluna, linha = celula
                        acertou = aplicar_tiro(tabuleiro_player2, tiros_player1, coluna, linha)
                        if acertou: 
                            tocar_som(sons_jogo, "acerto")
                            if todos_destruidos(tabuleiro_player2, tiros_player1):
                                jogador_vencedor = 1
                                estado_jogo = "vitoria"
                        else:
                            tocar_som(sons_jogo, "erro")
                            estado_jogo = "trans_2"

                elif estado_jogo == "trans_2":
                    estado_jogo = "batalha2"

                elif estado_jogo == "batalha2":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and celula not in tiros_player2:
                        coluna, linha = celula
                        acertou = aplicar_tiro(tabuleiro_player1, tiros_player2, coluna, linha)
                        if acertou:
                            tocar_som(sons_jogo, "acerto")
                            if todos_destruidos(tabuleiro_player1, tiros_player2):
                                jogador_vencedor = 2
                                estado_jogo = "vitoria"
                        else:
                            tocar_som(sons_jogo, "erro")
                            estado_jogo = "trans_1"

                elif estado_jogo == "trans_1":
                    estado_jogo = "batalha1"

                elif estado_jogo == "vitoria":
                    estado_jogo = "tela_inicial"
                    sons_jogo["vitoria"].stop()
                    som_vitoria_tocado = False
                    tocar_som(sons_jogo, "trilha", -1)
                    tocar_som(sons_jogo, "mar", -1)
                    tocar_som(sons_jogo, "guerra", -1)
                    tabuleiro_player1 = novo_tabuleiro()
                    tabuleiro_player2 = novo_tabuleiro()
                    tiros_player1 = []
                    tiros_player2 = []
                    navios_colocados_player1 = 0
                    navios_colocados_player2 = 0
                    jogador_vencedor = 0
                    
        tela_jogo.fill('darkgray')

        if estado_jogo == "vitoria" and not som_vitoria_tocado:
            sons_jogo["trilha"].stop()
            sons_jogo["mar"].stop()
            sons_jogo["guerra"].stop()
            tocar_som(sons_jogo, "vitoria")
            som_vitoria_tocado = True

        if estado_jogo == "tela_inicial":
            tela_inicial(tela_jogo, fonte_media, fonte_grande)
        
        elif estado_jogo == "setup1":
            celula = celula_do_mouse(mouse_x, mouse_y)
            if celula:
                coluna, linha = celula
                posicao_valida = pode_colocar(tabuleiro_player1, coluna, linha)
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiro_player1, tiros_player1, False, celula)
            mensagem_info = f"Jogador 1: navio {navios_colocados_player1 + 1}/7"
            if celula:
                if posicao_valida:
                    mensagem_info += " (Posição válida)"
                else:
                    mensagem_info += " (Posição inválida)"
            desenhar_info(tela_jogo, fonte_media, mensagem_info)

        elif estado_jogo == "trans_p2":
            titulo = "Jogador 1 está pronto!"
            subtitulo = "Passe o computador para o Jogador 2"
            texto_botao = "Continuar"
            mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao)

        elif estado_jogo == "setup2":
            celula = celula_do_mouse(mouse_x, mouse_y)
            if celula:
                coluna, linha = celula
                posicao_valida = pode_colocar(tabuleiro_player2, coluna, linha)
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiro_player2, tiros_player2, False, celula)
            mensagem_info = f"Jogador 2: navio {navios_colocados_player2 + 1}/7"
            if celula:
                if posicao_valida:
                    mensagem_info += " (Posição válida)"
                else:
                    mensagem_info += " (Posição inválida)" 
            desenhar_info(tela_jogo, fonte_media, mensagem_info)

        elif estado_jogo == "trans_batalha":
            titulo = "Batalha vai começar!"
            subtitulo = "Jogador 1 ataca primeiro"
            texto_botao = "Iniciar"
            mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao)

        elif estado_jogo == "batalha1":
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiro_player2, tiros_player1, True)
            navios_destruidos = contar_destruidos(tabuleiro_player2, tiros_player1)
            mensagem_info = f"Jogador 1 ataca! Navios destruidos: {navios_destruidos}/7"
            desenhar_info(tela_jogo, fonte_media, mensagem_info)

        elif estado_jogo == "trans_2":
            titulo = "Água!"
            subtitulo = "Vez do Jogador 2"
            texto_botao = "Continuar"
            mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao)

        elif estado_jogo == "batalha2":
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiro_player1, tiros_player2, True)
            navios_destruidos = contar_destruidos(tabuleiro_player1, tiros_player2)
            mensagem_info = f"Jogador 2 ataca! Navios destruidos: {navios_destruidos}/7"
            desenhar_info(tela_jogo, fonte_media, mensagem_info)

        elif estado_jogo == "trans_1":
            titulo = "Água!"
            subtitulo = "Vez do Jogador 1"
            texto_botao = "Continuar"
            mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao)

        elif estado_jogo == "vitoria":
            tela_vitoria(tela_jogo, fonte_media, fonte_grande, jogador_vencedor)

        pygame.display.flip()
        relogio_jogo.tick(60)


if __name__ == "__main__":
    main()
