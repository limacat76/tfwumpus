from enum import Enum

class RoomItem:
	def __init__(self, description, lethal, death):
		self.description = description
		self.lethal = lethal
		self.death = death

class RoomContent(Enum):
	Empty=RoomItem('', False, False)
	Wumpus=RoomItem('You smell stench', True, 'You get eaten by the wumpus')
	Pit=RoomItem('You feel a draft', True, 'You fall into the pit')

#todo random maze
def generate_maze():
	e = RoomContent.Empty
	w = RoomContent.Wumpus
	p = RoomContent.Pit
	return [[e, e, e, e],
			[e, e, e, p],
			[e, p, w, e],
			[e, e, e, e]]

def sense(x, y):
	d = maze[y % 4][x % 4].value.description
	if d != '':
		print(d)

def sense_all():
	sense(x-1, y)
	sense(x, y+1)
	sense(x+1, y)
	sense(x, y-1)

def check_room():
	global quitcond
	r = maze[y % 4][x % 4]
	if r.value.lethal:
		print(r.value.death)
		quitcond=True

def check_attack(x, y):
	global victory
	r = maze[y % 4][x % 4]
	if r == RoomContent.Wumpus:
		print('You hear an animal scream. The Wumpus is no more')
		victory = True
	
def parse_sentence():
	a = input().lower().split()
	command = a[0]
	if len(a) > 1:
		obj = a[1]
	else:
		obj=''
	return command, obj

def scan_direction(command, x, y):
	tx = x
	ty = y
	if command == 'north':
		ty = y - 1
	if command == 'south':
		ty = y + 1
	if command == 'west':
		tx = x - 1
	if command == 'east':
		tx = x + 1
	return tx, ty

#simple rules
#unlimited arrows
#wumpus does not move but eats player
#no bats

maze=generate_maze()
x=0
y=0
alive=True
victory=False
quitcond=False

while alive and not quitcond and not victory:
	sense_all()
	check_room()
	if quitcond or victory:
		break
	
	print('$> ', end='', flush=True)
	command,obj = parse_sentence()
	print('verb {} object {}'.format(command, obj))
	if command == 'quit':
		quitcond = True
	elif command == 'fire' and obj != '':
		fx, fy = scan_direction(obj, x, y)
		check_attack(fx, fy)
	else:
		x, y = scan_direction(command, x, y)
    	
if victory:
	print('You won')
else:
	print('You lost')

