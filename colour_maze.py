from collections import defaultdict 

class Step(object):
	
	def __init__(self, path, seq_len):
		self.path = path
		self.xy = path[-1]
		self.seq_len = seq_len
		self.seq_state = (len(path) - 1) % seq_len
		self.next_seq_state = len(path) % seq_len
		valid_xy[self.seq_state].remove(self.xy)
		
	def neighbours(self):
		x, y = self.xy
		return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
		
	def next_steps(self):
		for xy in self.neighbours():
			if xy in valid_xy[self.next_seq_state]:
				path = self.path + [xy] 
				yield Step(path=path, seq_len=self.seq_len) 
		
		
def walk(step):
	for next_step in step.next_steps():
		if next_step.xy[0] == 0:
			return next_step.path
		else:
			path = walk(next_step)
			return path
	return 'No valid path' 
	

if __name__ == '__main__':

    s = '''B O R O Y
    O R B G R
    B O G O Y
    Y G B Y G
    R O R B R'''
    
    colour_seq = ['O', 'G']
    colour_map = defaultdict(set) 

    for x, row in enumerate(s.split('\n')):
	     for y, colour in enumerate(row.split()):
		     colour_map[colour].add((x, y))

    valid_xy = [colour_map[colour] for colour in colour_seq] 

    step = Step(path=[(4,1)], seq_len=len(colour_seq))

    path = walk(step) 
    print(path) 

   
  
