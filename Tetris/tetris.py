import random
import pygame


colores = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


#region clase Figura
#clase figura
class figura:
    #tipos de figura y su respectiva rotacion
    figuras = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    #inicializador
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.randint(0, len(self.figuras) - 1)
        self.color = random.randint(1, len(colores) - 1)
        self.rotacion = 0

    def imagen(self):
        return self.figuras[self.tipo][self.rotacion]

    def rotar(self):
        self.rotacion = (self.rotacion + 1) % len(self.figuras[self.tipo])
#endregion

#region clase Tetris
class tetris:
    nivel = 2
    puntaje = 0
    estado = "start"
    campo = []
    alto = 0
    ancho = 0
    x = 100
    y = 60
    acercamiento = 20
    figura = None

    #inicializador
    def __init__(self, alto, ancho):
        self.nivel = 2
        self.puntaje = 0
        self.estado = "start"
        self.campo = []
        self.x = 100
        self.y = 60
        self.acercamiento = 20
        self.figura = None
        self.alto = 0
        self.ancho = 0


        self.alto = alto
        self.ancho = ancho
        for i in range(alto):
            nuevaLinea = []
            for j in range(ancho):
                nuevaLinea.append(0)
            self.campo.append(nuevaLinea)

    def nuevaFigura(self):
        self.figura = figura(3, 0)

    def intersecta(self):
        interseccion = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figura.imagen():
                    if i + self.figura.y > self.alto - 1 or \
                            j + self.figura.x > self.ancho - 1 or \
                            j + self.figura.x < 0 or \
                            self.campo[i + self.figura.y][j + self.figura.x] > 0:
                        interseccion = True
        return interseccion


    def congela(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figura.imagen():
                    self.campo[i + self.figura.y][j + self.figura.x] = self.figura.color
        self.rompeLinea()
        self.nuevaFigura()
        if self.intersecta():
            tetris.estado = "gameover"


    def rompeLinea(self):
        lineas = 0
        for i in range(1, self.alto):
            ceros = 0
            for j in range(self.ancho):
                if self.campo[i][j] == 0:
                    ceros += 1
            if ceros == 0:
                lineas += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.ancho):
                        self.campo[i1][j] = self.campo[i1 - 1][j]
        self.puntaje += lineas ** 2

    def vaDespacio(self):
        while not self.intersecta():
            self.figura.y += 1
        self.figura.y -= 1
        self.congela()

    def bajando(self):
        self.figura.y += 1
        if self.intersecta():
            self.figura.y -= 1
            self.congela()

    def vaAlLado(self, dx):
        old_x = self.figura.x
        self.figura.x += dx
        if self.intersecta():
            self.figura.x = old_x

    def rotando(self):
        viejaRotacion = self.figura.rotacion
        self.figura.rotar()
        if self.intersecta():
            self.figura.rotacion = viejaRotacion


#endregion

#region funcionalidad
pygame.init()
negro = (0, 0, 0)
blanco = (255, 255, 255)
gris = (128, 128, 128)

tamano = (400, 500)
pantalla = pygame.display.set_mode(tamano)

pygame.display.set_caption("Jugando Tetris")

terminado = False
reloj = pygame.time.Clock()
fps = 25
juego = tetris(20, 10)
contador = 0

presionaAbajo = False

while not terminado:
    if juego.figura is None:
        juego.nuevaFigura()
    contador += 1
    if contador > 100000:
        contador = 0

    if contador % (fps // juego.nivel // 2) == 0 or presionaAbajo:
        if juego.estado == "start":
            juego.bajando()


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            terminado = True
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                juego.rotando()
            if evento.key == pygame.K_DOWN:
                pressing_down = True
            if evento.key == pygame.K_LEFT:
                juego.vaAlLado(-1)
            if evento.key == pygame.K_RIGHT:
                juego.vaAlLado(1)
            if evento.key == pygame.K_SPACE:
                juego.vaDespacio()
            if evento.key == pygame.K_ESCAPE:
                juego.__init__(20, 10)

    if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_DOWN:
                presionaAbajo = False

    pantalla.fill(blanco)

    for i in range(juego.alto):
        for j in range(juego.ancho):
            pygame.draw.rect(pantalla, gris, [juego.x + juego.acercamiento * j, juego.y + juego.acercamiento * i,
                                              juego.acercamiento, juego.acercamiento], 1)
            if juego.campo[i][j] > 0:
                pygame.draw.rect(pantalla, colores[juego.campo[i][j]],
                                 [juego.x + juego.acercamiento * j + 1, juego.y + juego.acercamiento * i + 1,
                                  juego.acercamiento - 2, juego.acercamiento - 1])

    if juego.figura is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in juego.figura.imagen():
                    pygame.draw.rect(pantalla, colores[juego.figura.color],
                                     [juego.x + juego.acercamiento * (j + juego.figura.x) + 1,
                                      juego.y + juego.acercamiento * (i + juego.figura.y) + 1,
                                      juego.acercamiento - 2, juego.acercamiento - 2])

    fuente = pygame.font.SysFont('Calibri', 25, True, False)
    fuente1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = fuente.render("Score: " + str(juego.puntaje), True, negro)
    text_game_over = fuente1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = fuente1.render("Press ESC", True, (255, 215, 0))

    pantalla.blit(text, [0, 0])
    if juego.estado == "gameover":
        pantalla.blit(text_game_over, [20, 200])
        pantalla.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    reloj.tick(fps)

pygame.quit()


#endregion