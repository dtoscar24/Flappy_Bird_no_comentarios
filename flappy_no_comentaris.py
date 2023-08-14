import pygame 
import neat
import os 
import random 

pygame.font.init() 
FONT = pygame.font.SysFont('comicsans', 25) 
blanc = (255, 255, 255)
                              
FINESTRA_AMPLADA = 450
FINESTRA_ALTURA = 600 

FINESTRA = pygame.display.set_mode((FINESTRA_AMPLADA, FINESTRA_ALTURA)) 
pygame.display.set_caption("Flappy Bird") 

imatges_ocells = [pygame.transform.scale2x(pygame.image.load(os.path.join("imatges", "ocell1.png"))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join("imatges", "ocell2.png"))), 
                  pygame.transform.scale2x(pygame.image.load(os.path.join("imatges", "ocell3.png")))]

imatge_columna = pygame.transform.scale(pygame.image.load(os.path.join("imatges", "columna.png")), (78, 480))
imatge_base = pygame.transform.scale(pygame.image.load(os.path.join("imatges", "base.png")), (504, 168)) 
imatge_fons = pygame.transform.scale(pygame.image.load(os.path.join("imatges", "fons.png")), (450, 600))

GEN = 0

class Ocell:  
    OCELL = imatges_ocells  
    MAX_ROTATION = 25 
    ROTATION_VELOCITAT = 20 
    ANIMATION_TEMPS = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.inclinació = 0
        self.velocitat = 0 
        self.altura = self.y 
        self.comptador_física = 0 
        self.comptador_imatge = 0 
        self.imatge = self.OCELL[0] 

    def saltar(self):
        self.velocitat = -10.5
        self.comptador_física = 0 
        self.altura = self.y 

    def moviment(self):
        self.comptador_física += 1

        desplaçament = (self.velocitat * self.comptador_física) + (1.5 * (self.comptador_física ** 2))

        if desplaçament >= 16:
            desplaçament = 16 

        if desplaçament < 0: 
            desplaçament -= 2 

        self.y = self.y + desplaçament

        if desplaçament < 0 or self.y < self.altura:

            if self.inclinació < self.MAX_ROTATION:
                self.inclinació = self.MAX_ROTATION

        else:

            if self.inclinació > -90:           
                self.inclinació -= self.ROTATION_VELOCITAT 

    def dibuixar(self, finestra):
        self.comptador_imatge += 1

        if self.comptador_imatge <= self.ANIMATION_TEMPS:
            self.imatge = self.OCELL[0] 

        elif self.comptador_imatge <= self.ANIMATION_TEMPS*2:
            self.imatge = self.OCELL[1] 

        elif self.comptador_imatge <= self.ANIMATION_TEMPS*3:
            self.imatge = self.OCELL[2] 

        elif self.comptador_imatge <= self.ANIMATION_TEMPS*4:
            self.imatge = self.OCELL[1] 
 
        else:
            self.imatge = self.OCELL[0] 
            self.comptador_imatge = 0 

        if self.inclinació <= -80:
            self.imatge = self.OCELL[1] 
            self.comptador_imatge = self.ANIMATION_TEMPS*2 

        imatge_girada = pygame.transform.rotate(self.imatge, self.inclinació)
        nou_rectangle = imatge_girada.get_rect(center=self.imatge.get_rect(topleft = (self.x, self.y)).center)
        finestra.blit(imatge_girada, nou_rectangle.topleft)

    def obtenir_mask(self):
        return pygame.mask.from_surface(self.imatge) 

class Columna:
    ESPAI = 200 
    VELOCITAT = 20

    def __init__(self, x): 
        self.x = x
        self.adalt = 0 
        self.avall = 0 
        self.altura = 0

        self.COLUMNA_ADALT = pygame.transform.flip(imatge_columna, False, True) 
        self.COLUMNA_AVALL = imatge_columna

        self.passat = False 
        self.establir_altura()

    def establir_altura(self):

        self.altura = random.randrange(50, 200)

        self.adalt = self.altura - self.COLUMNA_ADALT.get_height() 
        self.avall = self.altura + self.ESPAI 

    def moviment(self):
        self.x -= self.VELOCITAT 

    def dibuixar(self, finestra):
        finestra.blit(self.COLUMNA_ADALT, (self.x, self.adalt)) 
        finestra.blit(self.COLUMNA_AVALL, (self.x, self.avall)) 

    def col·lisió(self, ocell):
        ocell_mask = ocell.obtenir_mask()
        columna_adalt_mask = pygame.mask.from_surface(self.COLUMNA_ADALT)
        columna_avall_mask = pygame.mask.from_surface(self.COLUMNA_AVALL)

        ocell_columna_adalt_offset = (self.x - ocell.x, self.adalt - round(ocell.y)) 
        ocell_columna_avall_offset = (self.x - ocell.x, self.avall - round(ocell.y))

        col·lisió_ocell_adalt = ocell_mask.overlap(columna_adalt_mask, ocell_columna_adalt_offset) 
        col·lisió_ocell_avall = ocell_mask.overlap(columna_avall_mask, ocell_columna_avall_offset) 

        if col·lisió_ocell_adalt or col·lisió_ocell_avall:
            return True 
        return False

class Base:
    VELOCITAT = 5
    AMPLADA = imatge_base.get_width() 

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.AMPLADA 

    def moviment(self):
        self.x1 -= self.VELOCITAT
        self.x2 -= self.VELOCITAT

        if self.x1 + self.AMPLADA < 0:
            self.x1 = self.x2 + self.AMPLADA

        if self.x2 + self.AMPLADA < 0:
            self.x2 = self.x1 + self.AMPLADA

    def dibuixar(self, finestra):
        finestra.blit(imatge_base, (self.x1, self.y))
        finestra.blit(imatge_base, (self.x2, self.y))

def dibuixar_elements(finestra, ocells, columnes, bases, puntuació, GEN):

    finestra.blit(imatge_fons, (0,0))

    for columna in columnes:
        columna.dibuixar(finestra) 

    for ocell in ocells:
        ocell.dibuixar(finestra) 

    bases.dibuixar(finestra) 

    puntuació_text = FONT.render('Puntuació: '+ str(puntuació), True, blanc)
    generació_text = FONT.render('Generació: '+ str(GEN), True, blanc)
    supervivents_text = FONT.render('Supervivents: '+ str(len(ocells)), True, blanc)

    finestra.blit(puntuació_text, (FINESTRA_AMPLADA - puntuació_text.get_width() - 10, 10)) 
    finestra.blit(generació_text, (10, 10))
    finestra.blit(supervivents_text, (10, 50))

    pygame.display.update() 

def main(genomes, configuració):

    global GEN 
    GEN += 1 
    finestra = FINESTRA

    bases = Base(500) 
    columnes = [Columna(600)] 

    partida = True 
    clock = pygame.time.Clock()
    puntuació = 0

    xarxes = [] 
    ge = [] 
    ocells = [] 

    for _, genoma in genomes:

        xarxa = neat.nn.FeedForwardNetwork.create(genoma, configuració)

        xarxes.append(xarxa)
        ocells.append(Ocell(200, 250)) 

        genoma.fitness = 0
        ge.append(genoma) 

    while partida:

        clock.tick(30) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                quit()

        columna_índex = 0 

        if len(ocells) > 0:

            if ocells[0].x > (columnes[0].x + columnes[0].COLUMNA_ADALT.get_width()):
                columna_índex = 1

        else: 
            partida = False 

        for índex, ocell in enumerate(ocells):

            ge[índex].fitness += 0.1 

            ocell.moviment() 

            output = xarxes[índex].activate((ocell.y, 
                                        abs(ocell.y - columnes[columna_índex].altura),
                                        abs(ocell.y - columnes[columna_índex].avall)))   
            
            if output[0] > 0.5:
                ocell.saltar()

        eliminar_columnes = [] 

        for columna in columnes:

            for índex, ocell in enumerate(ocells):

                if columna.col·lisió(ocell):

                    ge[índex].fitness -= 1 

                    ocells.pop(índex) 
                    xarxes.pop(índex)
                    ge.pop(índex) 

                if not columna.passat and (ocell.x > columna.x): 
                    columna.passat = True

            if columna.x + columna.COLUMNA_ADALT.get_width() < 0:
                eliminar_columnes.append(columna)
 
            columna.moviment() 

        if columna.passat: 

            puntuació += 1 

            for genoma in ge:
                genoma.fitness += 5 

            columnes.append(Columna(600))

        for eliminar in eliminar_columnes:

            columnes.remove(eliminar) 

        for índex, ocell in enumerate(ocells):

            if ocell.y + ocell.imatge.get_height() >= 500 or ocell.y < 0: 

                ge[índex].fitness -= 1 

                ocells.pop(índex) 
                xarxes.pop(índex) 
                ge.pop(índex) 

        bases.moviment() 

        dibuixar_elements(finestra, ocells, columnes, bases, puntuació, GEN) 

def importar(configuració_ruta):
   
    configuració = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                      configuració_ruta)

    població = neat.Population(configuració)

    població.add_reporter(neat.StdOutReporter(True)) 

    població.run(main, 100) 

if __name__ == '__main__':

    local_ruta = os.path.dirname(__file__) 

    configuració_ruta = os.path.join(local_ruta, "config.txt") 

    importar(configuració_ruta) 