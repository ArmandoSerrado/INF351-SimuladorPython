# INF351-SimuladorPython

## Trabalho de Embarcados - INF 351
Proposta de um jogo de exploração de salas, e desviar de inimigos e projeteis.

Azul - Jogador
Vermelho - Inimigo
Amarelo - Chave
Marrom - Porta
Verde - Objetivo

Controles:
  Setas direcionais para se movimentar
  Tecla R reinicia o mapa
  Tecla P volta ao menu

Demonstração
  https://youtu.be/wI5nxdq754s

O menu possui dois níveis de seleção:
  Início - podendo escolher entre duas dificuldades (fácil e normal)
  Tempos - ao finalizar a fase, o tempo é salvo em segundos. 

Observações:
  O arquivo mqtt-client.py é o controle do jogo, onde usu;ario enviará inputs do teclado (note que uma janela preta abrirá, o pygame precisa de um display para ler eventos do teclado.)
