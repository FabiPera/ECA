import numpy as np, copy, pygame
from pygame.locals import *
from BitString import BitString
from ECA import ECA

width=157
height=218
black=(0, 0, 0)
white=(255, 255, 255)
gray=(160, 160, 160)
screen=pygame.Surface((width, height))

def drawLattice():
	screen.fill(white)
	y=10
	x=10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	x += 10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	y = 31
	x = 31
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	x = 104
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	y=11
	x=126
	screen.fill(black, (x, y, 20, 20))

	y=62
	x=10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	x += 10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	y = 83
	x = 31
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	x = 104
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	y=63
	x=32
	screen.fill(black, (x, y, 20, 20))
	x=105
	screen.fill(black, (x, y, 20, 20))
	x=126
	screen.fill(black, (x, y, 20, 20))

	y=114
	x=10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	x += 10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	y = 135
	x = 31
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	x = 104
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	y=115
	x=11
	screen.fill(black, (x, y, 20, 20))
	x=84
	screen.fill(black, (x, y, 20, 20))
	x=126
	screen.fill(black, (x, y, 20, 20))

	y=166
	x=10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	x += 10
	for xc in range(3):
		pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
		x += 21
	y = 187
	x = 31
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	x = 104
	pygame.draw.rect(screen, gray, (x, y, 22, 22), 1)
	y=167
	x=11
	screen.fill(black, (x, y, 20, 20))
	x=32
	screen.fill(black, (x, y, 20, 20))
	x=84
	screen.fill(black, (x, y, 20, 20))
	x=105
	screen.fill(black, (x, y, 20, 20))
	x=126
	screen.fill(black, (x, y, 20, 20))

for	i in range(1):
	drawLattice()
	eca=ECA(i, 3)
	print(eca.rule.bits)
	eca.setConf("000", 0)
	
	k=0
	if(eca.rule.bits[k]):
		screen.fill(black, (32, 32, 20, 20))
	k += 1

	if(eca.rule.bits[k]):
		screen.fill(black, (105, 32, 20, 20))
	k += 1

	if(eca.rule.bits[k]):
		screen.fill(black, (32, 84, 20, 20))
	k += 1

	if(eca.rule.bits[k]):
		screen.fill(black, (105, 84, 20, 20))
	k += 1

	if(eca.rule.bits[k]):
		screen.fill(black, (32, 136, 20, 20))
	k += 1

	if(eca.rule.bits[k]):
		screen.fill(black, (105, 136, 20, 20))
	k += 1

	if(eca.rule.bits[k]):
		screen.fill(black, (32, 188, 20, 20))
	k += 1
	
	if(eca.rule.bits[k]):
		screen.fill(black, (105, 188, 20, 20))
	k += 1

	ruleFile="rule"+str(i)+".png"
	pygame.image.save(screen, ruleFile)