# Snake game
import turtle, time, random, os

# ---------- Configurações ----------
FPS = 90                  # Quadros por segundo
PASSO = 5                 # Pixels que a cobra anda por quadro
LIM_X, LIM_Y = 690, 400   # Limites da tela (bateu = morreu)
FONTE = ("Arial", 14, "bold")

# ---------- TELA ----------
tela = turtle.Screen()
tela.title("Snake game")
tela.bgcolor("#344055")
tela.setup(1366, 768)
tela.tracer(0)  # Desliga a atualização automática (jogo mais suave)

# ---------- Função que cria objetos ----------
def criar(cor, x = 0, y = 0, visivel = True):
    objeto = turtle.Turtle("circle", visible = visivel)
    objeto.speed(0)
    objeto.color(cor)
    objeto.penup()
    objeto.goto(x, y)
    return objeto

cabeca = criar("pink")
cabeca.shapesize(1, 1.5)
comida = criar("red", 0, 100)
texto_fps = criar("white", -640, 340, False)
texto_pts = criar("white", 500, 340, False)
corpo = []        # Gomos da cobra
pontos = 0
direcao = "stop"

# ---------- Direções e teclado ----------
MOVIMENTO = {"cima": (0, PASSO), "baixo": (0, -PASSO),
             "esquerda": (-PASSO, 0), "direita": (PASSO, 0), "stop": (0, 0)}
OPOSTO = {"cima": "baixo", "baixo": "cima", "esquerda": "direita", "direita": "esquerda"}
TECLAS = {"w": "cima", "s": "baixo", "a": "esquerda", "d": "direita",
          "Up": "cima", "Down": "baixo", "Left": "esquerda", "Right": "direita"}

def mudar_direcao(nova):
    global direcao
    if direcao != OPOSTO[nova]:  # Impede de voltar para trás
        direcao = nova

tela.listen()
for tecla, d in TECLAS.items():
    tela.onkeypress(lambda d = d: mudar_direcao(d), tecla)

# ---------- PLACAR E REINÍCIO ----------
def placar():
    texto_pts.clear()
    texto_pts.write(f"🍎: {pontos}", font=FONTE)

def reiniciar():
    global pontos, direcao
    os.system("aplay morreu.wav &")
    time.sleep(0.5)
    cabeca.goto(0, 0)
    direcao = "stop"
    for gomo in corpo:
        gomo.hideturtle()
    corpo.clear()
    pontos = 0
    placar()

# ---------- LOOP PRINCIPAL ----------
placar()
ultimo = time.time()
while True:
    agora = time.time()
    if agora - ultimo < 1 / FPS:
        continue  # ainda não é hora do próximo quadro

    texto_fps.clear()
    texto_fps.write(f"FPS: {1 / (agora - ultimo):.0f}", font=FONTE)
    ultimo = agora

    # Cada gomo vai para onde estava o da frente
    posicoes = [cabeca.pos()] + [gomo.pos() for gomo in corpo]
    for gomo, pos in zip(corpo, posicoes):
        gomo.goto(pos)

    # Move a cabeça
    dx, dy = MOVIMENTO[direcao]
    cabeca.goto(cabeca.xcor() + dx, cabeca.ycor() + dy)

    # Bateu na borda
    if abs(cabeca.xcor()) > LIM_X or abs(cabeca.ycor()) > LIM_Y:
        reiniciar()

    # Comeu a maçã
    if cabeca.distance(comida) < 20:
        os.system("aplay comida.wav &")
        comida.goto(random.randint(-LIM_X + 40, LIM_X - 40),
                    random.randint(-LIM_Y + 40, LIM_Y - 40))
        corpo.append(criar("#BA55D3", 1000, 1000))
        pontos += 1
        placar()

    # Bateu no próprio corpo
    if any(gomo.distance(cabeca) < PASSO for gomo in corpo):
        reiniciar()

    tela.update()