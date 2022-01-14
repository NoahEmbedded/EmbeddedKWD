import pygame
import numpy as np 

h,w = 5, 3
border = 50
pygame.init()
screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
done = False
clock = pygame.time.Clock()

bild1 = np.array(np.mat("10000 10000 10000 10000 10000 ; 5000 5000 5000 5000 5000 ; 100 100 100 100 100"))
bild2 = np.array(np.mat("100 100 100 100 100;1000 1000 1000 1000 1000;10000 10000 10000 10000 10000"))
rgb = np.ones((w,h,3))
print(rgb)
w,h = bild1.shape
for i in range(w):
    for j in range(h):
        rgb[i,j,:]=bild1[i,j]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255, 255, 255))
    surface = pygame.surfarray.make_surface(rgb)
    screen.blit(surface, (border, border))        
    pygame.display.flip()
    clock.tick(60)
   

                  