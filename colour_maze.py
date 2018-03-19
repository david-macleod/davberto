'''https://www.reddit.com/r/dailyprogrammer/comments/6qutez/20170801_challenge_325_easy_color_maze/

Program tries to be efficient by never visiting the same step multiple times (even from different input paths)
Can also handle no valid solution i.e. all possible paths are dead ends or get stuck in endless loops
'''

from collections import defaultdict 
from copy import copy


class Step(object):
	
    def __init__(self, path, seq_state):
        '''
        Step object is defined as a combination of an xy position AND a specific state in colour sequence
        :param path: list of (x,y) tuples recording path leading to step (inclusive)
        :param seq_state: integer position in colour sequence corresponding to step
        '''
        self.path = path
        self.seq_state = seq_state
        self.xy = path[-1]
        self.x, self.y = self.xy
        
    def neighbour_xy(self):
        ''' get xy coordinates of positions adjacent to step '''
        x, y = self.xy
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]



class Maze(object):
    
    def __init__(self, maze_string, seq_string):
        '''
        Maze object generates Step objects from parsed input, and executes walks to find solutions to maze
        Maze also maintains list of possible inputs for creating Step objects
        :param maze_string: grid of maze colours, columns delimited by space, rows delimited by newline
        :param seq_string: sequence of maze colours, space delimited
        '''
        self.seq = seq_string.split()
        self.seq_len = len(self.seq)
        self.max_y = 0
        self.valid_xy = self.parse_maze(maze_string)
        
        
    def parse_maze(self, maze_string):
        '''
        Convert maze into a list of sets containing valid (x,y) coordinates which we can create steps from 
        Each element in list corresponds to a state (position) in colour sequence
        :param maze_string: grid of maze colours
        :returns: list of sets 
        '''
        colour_map = defaultdict(set) 
        for y, row in enumerate(maze_string.split('\n')):
    	     for x, colour in enumerate(row.split()):
                colour_map[colour].add((x, y))
                self.max_y = max(y, self.max_y)
        return [copy(colour_map[colour]) for colour in self.seq]

    
    def get_first_steps(self):
        ''' generate valid steps in bottom row of maze '''
        initial_xy = [(x, y) for x, y in self.valid_xy[0] if y == self.max_y]
        first_steps = self.generate_steps(
            xy_list=initial_xy,
            seq_state=0)
        return first_steps
    
    
    def get_next_steps(self, step):
        ''' generate valid steps which neighbour current step '''
        next_steps = self.generate_steps(
            xy_list=step.neighbour_xy(),
            seq_state=self.next_state(step.seq_state),
            input_path=step.path)
        return next_steps
        
    
    def generate_steps(self, xy_list, seq_state, input_path=[]):
        '''
        Generate steps dynamically from a static list of input coordinates, so that we do not visit the same step twice
        :param xy_list: list of (x,y) coordinate tuples
        :param seq_state: state in colour sequence for steps to be generated
        :param input_path: current path to prepend to xy coordinates
        :returns: Step object
        '''
        for xy in xy_list:
            if xy in self.valid_xy[seq_state]:
                path = input_path + [xy]
                self.valid_xy[seq_state].remove(xy)
                yield Step(path=path, seq_state=seq_state)
             
                
    def next_state(self, seq_state):
        ''' Incremenent state of colour sequence '''
        return (seq_state + 1) % self.seq_len
                
                
    def walk(self, steps):
        '''
        Recursive walk which follows steps until it reaches a step which exists in the top row of the maze
        If all possible paths reach a dead-end, or get stuck in a loop, an empty path is returned
        :param steps: list of Step objects to attempt, which share the same state in colour sequence
        :returns: list of (x,y) coordinates recording solution path (or an empty list if no valid solution)
        '''
        for step in steps:
            if step.y == 0:
                return step.path
            else:
                next_steps = self.get_next_steps(step)
                path = self.walk(next_steps)
                if path:
                    return path
        return []
               
    
    def solve_maze(self):
        first_steps = self.get_first_steps()
        final_path = self.walk(first_steps)
        return final_path
	

if __name__ == '__main__':
    
    small_maze_string = '''B O R O Y
    O R B G R
    B O G O Y 
    Y G B Y G 
    R O R B R'''
    
    small_seq_string = 'O G'
    
    small_maze = Maze(maze_string=small_maze_string, seq_string=small_seq_string)
    solution = small_maze.solve_maze() 
    print('SMALL maze path:', solution)


    big_maze_string = '''R R B R R R B P Y G P B B B G P B P P R
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
    
    big_seq_string = 'R O Y P O'
    
    big_maze = Maze(maze_string=big_maze_string, seq_string=big_seq_string)
    solution = big_maze.solve_maze() 
    print('BIG maze path:', solution)
    
  
    
    
