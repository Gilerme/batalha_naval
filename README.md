# Batalha Naval

Jogo local para 2 jogadores, feito em Python com Pygame-ce

## Resumo do jogo

- Cada jogador posiciona 7 navios
- Cada navio ocupa 3 células
- O tabuleiro é 10x10
- Durante a batalha, o tabuleiro inimigo fica oculto (apenas acertos e erros aparecem)
- Vence quem destruir os 7 navios adversários primeiro

## Regras implementadas

- Navios são colocados apenas na horizontal
- Uma posição só é válida se houver espaço para 3 células livres
- Não é permitido atirar duas vezes na mesma célula
- Ao acertar qualquer parte do navio, o navio inteiro é marcado como destruído
- Ao acertar, o jogador continua atacando
- O turno troca apenas quando o jogador erra (acerta água)

## Como executar

### Requisitos

- Python 3.x
- Biblioteca `pygame-ce`

### Instalação

```bash
pip install pygame-ce
```

### Rodar o jogo

```bash
python batalha_naval.py
```

## Controles

- Mouse (botao esquerdo) para avancar telas, posicionar navios e atacar

## Estrutura do projeto

```text
batalha_naval/
├── batalha_naval.py
├── interface_jogo.py
├── logica_jogo.py
├── README.md
├── imagens/
│   ├── barco_1.png
│   ├── barco_2.png
│   ├── barco_3.png
│   ├── barco_destruido_1.png
│   ├── barco_destruido_2.png
│   ├── barco_destruido_3.png
│   └── inteiro/
│       ├── barco.png
│       ├── barco_destruido.png
│       ├── tela_inicial.png
│       ├── trans_1.jpeg
│       ├── trans_2.jpeg
│       ├── trans_batalha.jpeg
│       ├── trans_p2.jpeg
│       ├── vitoria_1.jpeg
│       └── vitoria_2.jpeg
└── sons/
    ├── acertou.mp3
    ├── agua.mp3
    ├── mar.mp3
    ├── radar.mp3
    ├── trilha.mp3
    ├── vitoria.mp3
    └── war.mp3
```

## Arquitetura por módulo

### batalha_naval.py

Responsável por:

- inicializar o jogo
- processar eventos de mouse
- alternar entre telas e turnos
- reiniciar a partida

Estado da partida controlado por `estado_jogo` com os valores:

- `tela_inicial`
- `setup1`
- `trans_p2`
- `setup2`
- `trans_batalha`
- `batalha1`
- `trans_2`
- `batalha2`
- `trans_1`
- `vitoria`

Fluxo de turno em batalha:

```text
batalha1
  acerto -> continua em batalha1
  erro   -> trans_2 -> batalha2

batalha2
  acerto -> continua em batalha2
  erro   -> trans_1 -> batalha1
```

Quando há vitória, a tela final é exibida e, ao continuar, o jogo volta para `tela_inicial` com variáveis iniciais resetadas

### logica_jogo.py

Funções principais:

- `novo_tabuleiro()`: cria matriz 10x10 preenchida com `0`
- `celula_do_mouse(mouse_x, mouse_y)`: converte coordenadas da tela para `(coluna, linha)`
- `pode_colocar(tabuleiro, coluna, linha)`: valida navio horizontal de 3 casas
- `coloca_navio(tabuleiro, coluna, linha, id_navio)`: grava o ID do navio em 3 casas
- `aplicar_tiro(tabuleiro, tiros_jogador, coluna, linha)`: retorna `True` em acerto e `False` em agua; no acerto, registra as 3 partes do navio
- `todos_destruidos(tabuleiro, tiros_jogador)`: verifica condição de vitoria
- `contar_destruidos(tabuleiro, tiros_jogador)`: conta navios destruidos por IDs

### interface_jogo.py

Responsavel por janela, desenhos e audio.

- `criar_janela()` Inicializa o pygame e retorna:

```python
(tela_jogo, relogio_jogo, fonte_pequena, fonte_grande, sons_jogo)
```

- Carrega os sons: `acerto`, `erro`, `trilha`, `guerra`, `mar`, `colocou`, `vitoria`
- Desenha grade, navios, impactos e informacoes de status
- Exibe telas de transicao e vitoria usando imagens em `imagens/inteiro/`

## Modelo de dados

### Tabuleiro

- Lista 10x10 de inteiros
- `0` representa água
- `1` a `7` representam IDs de navios

Exemplo:

```python
tabuleiro = [
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
]
```

### Tiros

- Lista de tuplas `(coluna, linha)`
- Exemplo: `[(0, 0), (5, 3), (9, 1)]`

## Interface e áudio

- Janela: `600x680`
- Área do tabuleiro: `600x600`
- Barra de informação inferior: `600x80`
- Célula: `52x52`, com margem de `40px`

Sons carregados por chave:

- `acerto`, `erro`, `trilha`, `mar`, `colocou`, `vitoria`, `guerra`
