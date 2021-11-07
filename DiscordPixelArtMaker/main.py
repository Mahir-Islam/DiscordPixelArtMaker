import pygame
import pyperclip
import PROCESS as prc

pygame.init()

W = 400
H = 500
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Discord Pixel Art Maker")

ROWS = 7

#Colours
RED = (221,46,68)
GREEN = (120,177,89)
BLUE = (85,172,238)
YELLOW = (253,203,88)
WHITE = (255,255,255)
BLACK = (49,55,61)
PURPLE = (170,142,214)
ORANGE = (244,144,12)
GREY = (124,124,124)
LIGHT_GREY = (230,231,232)
BROWN = (193,106,79)
YELLOW = (253,203,88)

Colours = {
	"black":BLACK,
	"white":WHITE,
	"red":RED,
	"green":GREEN,
	"blue":BLUE,
	"orange":ORANGE,	
	"purple":PURPLE,
	"brown":BROWN,
	"yellow":YELLOW,
	"grey":GREY,
	"light_grey":LIGHT_GREY,
}

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.colour = WHITE
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def setColour(self, name):
		try:
			self.colour = Colours[name]
		except KeyError:
			self.colour = BLACK

	def draw(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

	def __lt__(self, other):
		return False

class Button:

	def __init__(self, window, colour, x, y, width, height):
		self.window = WIN
		self.colour = colour
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def create(self):
		return pygame.draw.rect(self.window,self.colour,(self.x,self.y,self.width,self.height));

spots = []

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			spots.append(spot)
			spot.setColour("black")
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width, colour=LIGHT_GREY):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, colour, (0,i*gap), (width, i*gap))
		for j in range(rows):
			pygame.draw.line(win, colour, (j*gap,0), (j*gap,width))

def draw(win, grid, rows, width):
	#win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y,x = pos

	row = y // gap
	col = x // gap

	return row, col

def SAVE(Matrix):
	TEXT = prc.process(Matrix)
	clip = ''.join(prc.process(Matrix))
	print(TEXT)
	pyperclip.copy(clip)

def main(win, width):
	grid = make_grid(ROWS, width)
	BOARD = [0] * ROWS**2
	brushIndex = 1
	"""
	0 = black
	1 = white
	2 = red
	3 = green
	4 = blue
	5 = orange
	6 = purple
	7 = brown
	8 = yellow
	"""

	run = True
	win.fill(WHITE)
	currentColour = "white"

	FONT = pygame.font.Font("bluether.ttf",27)
	TXTcopy  = FONT.render("COPY",True,(255,255,255),GREY)
	TXTclear = FONT.render("CLEAR",True,(255,255,255),RED)
	TXTsave = FONT.render("SAVE",True,(255,255,255),(32,64,128))
	xSkew = 7

	BLACKb = Button(WIN,BLACK,xSkew,410,30,30).create()
	WHITEb = Button(WIN,LIGHT_GREY,xSkew+44,410,30,30).create()
	REDb = Button(WIN,RED,xSkew+44*(2),410,30,30).create()
	GREENb = Button(WIN,GREEN,xSkew+44*(3),410,30,30).create()
	BLUb = Button(WIN,BLUE,xSkew+44*(4),410,30,30).create()
	ORANGEb = Button(WIN,ORANGE,xSkew+44*(5),410,30,30).create()		
	PURPLEb = Button(WIN,PURPLE,xSkew+44*(6),410,30,30).create()
	BROWNb = Button(WIN,BROWN,xSkew+44*(7),410,30,30).create()
	YELLOWb = Button(WIN,YELLOW,xSkew+44*(8),410,30,30).create()

	Palette = [BLACKb, WHITEb, REDb, GREENb, BLUb, ORANGEb, PURPLEb, BROWNb, YELLOWb]

	while run:
		draw(win, grid, ROWS, W)
		
		COPYb = Button(WIN,GREY,xSkew,455,xSkew+112,30).create()
		WIN.blit(TXTcopy,(38, 455)) #56

		CLEARb = Button(WIN,RED,xSkew+132,455,xSkew+112,30).create()
		WIN.blit(TXTclear,(160, 455))

		SAVEb = Button(WIN,(32,64,128),xSkew+264,455,xSkew+112,30).create()
		WIN.blit(TXTsave,(300, 455))

		pygame.display.flip();

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:

				pos = pygame.mouse.get_pos()

				for x in range(0,9): #checks for colour
					if Palette[x].collidepoint(pos):
						brushIndex = x
						currentColour = list(Colours)[x]

				if COPYb.collidepoint(pos):
					SAVE(BOARD)

				if CLEARb.collidepoint(pos):
					BOARD = [0] * ROWS**2
					for s in spots:
						s.setColour("black")

				if SAVEb.collidepoint(pos):
					screenRect = pygame.Rect(0,0,ROWS*(W // ROWS), ROWS*(W // ROWS) )
					pygame.image.save( WIN.subsurface(screenRect), "screenshot.jpg" )

				row, col = get_clicked_pos(pos, ROWS, width)
				try:
					spot = grid[row][col]
					spot.setColour(currentColour)
					BOARD[ROWS*col+row] = brushIndex
				except:
					continue

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)

				try:
					spot = grid[row][col]
					spot.setColour("black")
					BOARD[ROWS*col+row] = 0
				except:
					continue


	pygame.quit()


main(WIN, W)

