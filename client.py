#multiple client scripts can be run on the same script on the same machine that the server script is on
import pygame
from network import Network
from player import player

width = 500
height = 500
win = pygame.display.set_mode((width,height))

pygame.display.set_caption("Client")

clientNumber = 0


def read_pos(str):
    str = str.split(",")
    #print(str[0],str[1])
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0])+","+str(tup[1])



        


def redrawWindow(win, player, player2):
    win.fill((0,0,0))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos()) #return the starting position of the cubes - tuple
    p = player(startPos[0], startPos[1], 100, 100, (0,255,0))
    p2 = player(0,0, 100, 100, (0,255,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        p2Pos = read_pos(n.send(make_pos((p.x,p.y)))) #convert tuple to string after sending it to make_pos
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        p.move()
        redrawWindow(win,p, p2)

main()