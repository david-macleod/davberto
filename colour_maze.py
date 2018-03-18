from collections import defaultdict 
from copy import copy

class Step(object):
	
    def __init__(self, path, seq_state):
        self.path = path
        self.seq_state = seq_state
        self.xy = path[-1]
        self.x, self.y = self.xy
        valid_xy[self.seq_state].remove(self.xy)
        
    def get_neighbour_xy(self):
        x, y = self.xy
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    def next_steps(self):
        steps = generate_steps(
            xy_list=self.get_neighbour_xy(),
            seq_state=next_state(self.seq_state, seq_len),
            input_path=self.path
        )
        return steps
           

def get_initial_xy():
    max_y = max(y for x, y in valid_xy[0])
    return [(x, y) for x, y in valid_xy[0] if y == max_y]
    
		
def generate_steps(xy_list, seq_state, input_path=[]):
    for xy in xy_list:
        if xy in valid_xy[seq_state]:
            path = input_path + [xy]
            yield Step(path=path, seq_state=seq_state)
            
            
def next_state(seq_state, seq_len):
    return (seq_state + 1) % seq_len
	
	
def walk(steps):
    for step in steps:
        if step.y == 0:
            return step.path
        else:
            next_steps = step.next_steps()
            path = walk(next_steps)
            if path:
                return path
    return []


	

if __name__ == '__main__':

    maze_string = '''R R B R R R B P Y G P B B B G P B P P R
    B G Y P R P Y Y O R Y P P Y Y R R R P P
    B P G R O P Y G R Y Y G P O R Y P B O O
    R B B O R P Y O O Y R P B R G R B G P G
    R P Y G G G P Y P Y O G B O R Y P B Y O
    O R B G B Y B P G R P Y R O G Y G Y R P
    B G O O O G B B R O Y Y Y Y P B Y Y G G
    P P G B O P Y G B R O G B G R O Y R B R
    Y Y P P R B Y B P O O G P Y R P P Y R Y
    P O O B B B G O Y G O P B G Y R R Y R B
    P P Y R B O O R O R Y B G B G O O P B Y
    B B R G Y G P Y G P R R P Y G O O Y R R
    O G R Y B P Y O P B R Y B G P G O O B P
    R Y G P G G O R Y O O G R G P P Y P B G
    P Y P R O O R O Y R P O R Y P Y B B Y R
    O Y P G R P R G P O B B R B O B Y Y B P
    B Y Y P O Y O Y O R B R G G Y G R G Y G
    Y B Y Y G B R R O B O P P O B O R R R P
    P O O O P Y G G Y P O G P O B G P R P B
    R B B R R R R B B B Y O B G P G G O O Y'''
    
    seq_string = 'R O Y P O'
    
    colour_seq = seq_string.split()
    seq_len = len(colour_seq)
    colour_map = defaultdict(set) 
    

    for y, row in enumerate(maze_string.split('\n')):
	     for x, colour in enumerate(row.split()):
		     colour_map[colour].add((x, y))

    valid_xy = [copy(colour_map[colour]) for colour in colour_seq]
    
    initial_steps = generate_steps(
        xy_list=get_initial_xy(),
        seq_state=0,
    )


    path = walk(initial_steps) 
    print(path) 

   
  
