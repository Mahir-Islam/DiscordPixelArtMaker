names = {
	0:':black_large_square:',
	1:':white_large_square:',
	2:':red_square:',
	3:':green_square:',
	4:':blue_square:',
	5:':orange_square:',
	6:':purple_square:',
	7:':brown_square:',
	8:':yellow_square:',
}

NewLine = "\n"
def process(flatPack):
	s = []
	root = int(len(flatPack)**0.5)
	i = -1
	for x in flatPack:
		i+=1
		if i % root == 0 and i != 0:
			s.append(NewLine)
		s.append(names[x])


	return s