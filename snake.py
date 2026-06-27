# Importando bibliotecas
import turtle
import time
import random
import os

# Ajuste o FPS aqui. 
# Nota: Como a cobra anda 20 pixels por quadro, 60 FPS vai ser rápido demais.
# Recomendo testar valores entre 10 e 15 para começar, e ir aumentando para dificultar!

# -------------------------------------------------------------
#!-----------------------IMPORTANT-----------------------------
fps_alvo = 30
intervalo_por_quadro = 1 / fps_alvo
eixoX = 690 # variavel que guarda
eixoY = 400
pontuacao = 0 # Variável para armazenar a quantidade de maçãs comidas
# -------------------------------------------------------------

# 1. Configuração da Tela
tela = turtle.Screen()
tela.title("Snake game")
tela.bgcolor("#344055")
tela.setup(width = 1366, height = 768) # resolução da tela do game.
tela.tracer(0) # Desliga atualizações automáticas para deixar o jogo mais suave
ultimo_tempo = time.time()

# 3.5. Medidor de FPS
caneta_fps = turtle.Turtle()
caneta_fps.speed(0)
caneta_fps.color("white") # Cor do texto
caneta_fps.penup()
caneta_fps.hideturtle() # Esconde a seta para aparecer só o texto
caneta_fps.goto(-640, 340)

# 3.6. Contador de Pontuação (Maçãs Comidas)
caneta_pontos = turtle.Turtle()
caneta_pontos.speed(0)
caneta_pontos.color("white")
caneta_pontos.penup()
caneta_pontos.hideturtle()
caneta_pontos.goto(500, 340) # Posiciona no canto superior direito

# Escreve o placar inicial
caneta_pontos.write(f"🍎: {pontuacao}", font=("Arial", 14, "bold"))

# --------------------------------------------------------------
# 2. Cabeça da Cobra
cabeca = turtle.Turtle()
cabeca.speed(0)
cabeca.shape("circle")
cabeca.color("pink")
cabeca.penup() # Não desenha o rastro
cabeca.goto(0, 0)
cabeca.direcao = "stop"

# -------------------------------------------------------------
# 3. Comida da Cobra
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
cabeca.shapesize(stretch_wid = 1, stretch_len = 1.5)
comida.color("red")
comida.penup()
comida.goto(0, 100)
# -------------------------------------------------------------
corpo = []
# -------------------------------------------------------------
# 4. Funções de Direção
def ir_cima():
    if cabeca.direcao != "baixo":
        cabeca.direcao = "cima"

def ir_baixo():
    if cabeca.direcao != "cima":
        cabeca.direcao = "baixo"

def ir_esquerda():
    if cabeca.direcao != "direita":
        cabeca.direcao = "esquerda"

def ir_direita():
    if cabeca.direcao != "esquerda":
        cabeca.direcao = "direita"
# ------------------------------------------------------------
# 5. Função de Movimento
def mover():
    if cabeca.direcao == "cima":
        y = cabeca.ycor()
        cabeca.sety(y + 20)
    if cabeca.direcao == "baixo":
        y = cabeca.ycor()
        cabeca.sety(y - 20)
    if cabeca.direcao == "esquerda":
        x = cabeca.xcor()
        cabeca.setx(x - 20)
    if cabeca.direcao == "direita":
        x = cabeca.xcor()
        cabeca.setx(x + 20)
# --------------------------------------------------------------
# 6. Mapeamento do Teclado
tela.listen()
tela.onkeypress(ir_cima, "w")
tela.onkeypress(ir_baixo, "s")
tela.onkeypress(ir_esquerda, "a")
tela.onkeypress(ir_direita, "d")
tela.onkeypress(ir_cima, "Up")
tela.onkeypress(ir_baixo, "Down")
tela.onkeypress(ir_esquerda, "Left")
tela.onkeypress(ir_direita, "Right")
# ---------------------------------------------------------------
# 7. Loop Principal do Jogo
while True:
    tempo_atual = time.time()
    tempo_passado = tempo_atual - ultimo_tempo

    # SÓ executa se o tempo passado for maior que o intervalo do FPS
    if tempo_passado >= intervalo_por_quadro:
        
        # === ENTRADA DO MEDIDOR DE FPS ===
        caneta_fps.clear() 
        fps_real = 1 / tempo_passado 
        caneta_fps.write(f"FPS: {fps_real:.0f}", font=("Arial", 14, "bold"))
        # =================================
        
        # Reseta o cronômetro para o próximo quadro
        ultimo_tempo = tempo_atual

        # Move os segmentos do corpo do fim para o começo
        for i in range(len(corpo) - 1, 0, -1):
            x = corpo[i - 1].xcor()
            y = corpo[i - 1].ycor()
            corpo[i].goto(x, y)

        # Move o segmento 0 (logo atrás da cabeça) para onde a cabeça está
        if len(corpo) > 0:
            x = cabeca.xcor()
            y = cabeca.ycor()
            corpo[0].goto(x, y)

        # Agora sim, move a cabeça da cobra
        mover()

        # Verifica colisão com as bordas da tela
        if cabeca.xcor() > eixoX or cabeca.xcor() < -eixoX or cabeca.ycor() > eixoY or cabeca.ycor() < -eixoY:
            os.system("aplay morreu.wav &") # Toca o som de morte
            time.sleep(0.5)
            cabeca.goto(0, 0)
            cabeca.direcao = "stop"

            # Esconde os segmentos do corpo cortados
            for segmento in corpo:
                segmento.goto(1000, 1000)
            corpo.clear()

            # Reseta a pontuação ao morrer
            pontuacao = 0
            caneta_pontos.clear()
            caneta_pontos.write(f"🍎: {pontuacao}", font=("Arial", 14, "bold"))

        # Verifica colisão com a comida
        if cabeca.distance(comida) < 20:
            os.system("aplay comida.wav &") # Toca o som de comer de forma assíncrona
            
            x = random.randint(-int(eixoX - 40), int(eixoX - 40))
            y = random.randint(-int(eixoY - 40), int(eixoY - 40))
            comida.goto(x, y)

            # Adiciona um novo segmento ao corpo
            novo_segmento = turtle.Turtle()
            novo_segmento.speed(0)
            novo_segmento.shape("circle")
            novo_segmento.color("#BA55D3")
            novo_segmento.penup()
            corpo.append(novo_segmento)

            # === ATUALIZAÇÃO DA PONTUAÇÃO ===
            pontuacao += 1
            caneta_pontos.clear() # Apaga o texto antigo
            caneta_pontos.write(f"🍎: {pontuacao}", font=("Arial", 14, "bold"))
            # ================================

        # Verifica colisão com o próprio corpo
        for segmento in corpo:
            if segmento.distance(cabeca) < 20:
                os.system("aplay morreu.wav &") # Toca o som de morte
                time.sleep(0.5)
                cabeca.goto(0, 0)
                cabeca.direcao = "stop"
                for seg in corpo:
                    seg.goto(1000, 1000)
                corpo.clear()

                # Reseta a pontuação ao colidir com o próprio corpo
                pontuacao = 0
                caneta_pontos.clear()
                caneta_pontos.write(f"🍎: {pontuacao}", font=("Arial", 14, "bold"))
        
        # Atualiza a tela com todas as modificações do quadro atual de uma vez só
        tela.update()