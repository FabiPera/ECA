import numpy as np, copy
from pygame.locals import *
from BitString import BitString
from ECA import ECA

class Simulator:
	
	steps = 0
	eca = ECA()