import random as rand
import keyboard
import time
import sys
sys.path.append('..') # Path to the directory
from style import set_cursor, set_cursor_str

maze_off = 18
num_rows = 9
num_cols = 19

class MazeNode:
    def __init__(self, row, col):
        self.col: int = row
        self.row: int = col

        self.visited: bool = False
        '''
        Creates array of tuple. Neighboring MazeNodes and a boolean to idicate if the
        neighboring MazeNodes are connected.
        '''
        '''
        (i+1,j) -> Maze node below
        (i, j+1) -> Maze node to right
        (i-1, j) -> Maze node above
        (i, j-1) -> Maze node left
        '''
        self.neighbors = []
        self.connected_neighbors = []

def findNeighbor(self: MazeNode, row, col) -> MazeNode:
    for i in range(0, len(self.connected_neighbors)):
        if row == self.connected_neighbors[i].row and col == self.connected_neighbors[i].col:
            return self.connected_neighbors[i]
    return None

#Create data structure
def maze_array_init() -> list[list[MazeNode]]:
    #maze_node_list = [MazeNode]
    maze_node_list = [[MazeNode(i, j) for i in range(num_cols)] for j in range(num_rows)]

    #Link neighbors. Need to ensure maze nodes don't have neighbors out of bounds.
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            neighbors_check = [(i+1,j), (i, j+1), (i-1, j), (i, j-1)]

            for k in range(0, len(neighbors_check)):
                if(neighbors_check[k][0] < num_rows and neighbors_check[k][0] >= 0):
                    if(neighbors_check[k][1] < num_cols and neighbors_check[k][1] >= 0):
                        maze_node_list[i][j].neighbors.append(maze_node_list[neighbors_check[k][0]][neighbors_check[k][1]])

                    else:
                        continue
                else:
                    continue
                    
    return maze_node_list
            
#Maze generation algo
def maze_generator() -> list[list[MazeNode]]:
        def visit_node(visited_node : MazeNode) -> None:
            visited_node.visited = True
            #print("Visited node at (", visited_node.row,", ", visited_node.col, ")")
            rand.shuffle(visited_node.neighbors)
            for i in range(0, len(visited_node.neighbors)):
                mazeNode : MazeNode = visited_node.neighbors[i]
                if(mazeNode.visited):
                    continue
                else:
                    #Connect nodes
                    visited_node.neighbors[i].connected_neighbors.append(visited_node)
                    visited_node.connected_neighbors.append(visited_node.neighbors[i])
                    visit_node(visited_node.neighbors[i])
            return None
        
        mazeNodes : list[list[MazeNode]] = maze_array_init()
        visit_node(mazeNodes[0][0])        

        return mazeNodes
'''
Use data structure to create string form of maze to print to terminal
Terminal space: 75*20 chars
Maze space: 39*19 chars with row 20 being fully spaces
num rows: 9
num cols: 19
Maze offset: 18

Will print all of terminal space
MazeNode[0][0] is bottom left
maze_nodes: list[list[MazeNode]]
'''
def maze_data_to_string() -> list[list[str]]:
    #maze_str = [[' '] * 75]*20
    maze_str = [[' ' for i in range(75)] for j in range(20)]
    corner = '+'
    verticalBar = '|'
    horizontalBar = '-'
    space = ' '
    maze_nodes : list[list[MazeNode]] = maze_generator()

    #Generate corners - i is rows, j is cols
    for i in range(0, 19, 2):
        for j in range(0, 39, 2):
            maze_str[i][j+maze_off] = corner
    
    for i in range(0, 19, 2):
        for j in range(1, 39, 2):
            maze_str[i][j+maze_off] = horizontalBar
    
    for i in range(1, 19, 2):
        for j in range(0, 39, 2):
            maze_str[i][j+maze_off] = verticalBar
    
    #Maze entrance
    maze_str[17][-3+maze_off] = '-'
    maze_str[17][-2+maze_off] = '-'
    maze_str[17][-1+maze_off] = '>'
    maze_str[17][0+maze_off] = space
    # maze_str[17][1+maze_off] = '@'

    #Maze exit
    maze_str[1][38+maze_off] = space
    maze_str[1][38+maze_off+2] = '-'
    maze_str[1][38+maze_off+3] = '-'
    maze_str[1][38+maze_off+4] = '>'
    
    connections_made : int = 0
    
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            neighbors_check = [(i-1, j), (i, j+1)]
            for k in range(0, len(neighbors_check)):
                neighbor_node = findNeighbor(maze_nodes[i][j], neighbors_check[k][0], neighbors_check[k][1])
                if neighbor_node == None:
                    continue
                else:
                    connections_made += 1
                    if k == 0:
                        maze_str[18 + (-2*i)][1 + (2*j) + maze_off] = " "
                    else:
                        maze_str[17 + (-2*i)][2 + (2*j) + maze_off] = " "
                
    #print("Connections made: ", connections_made)
    return maze_str
    

#The main problem seems to be the translation from screenspace to mazespace. 
def maze_input():
    print("You've been trapped in a maze! Use the arrow keys to move and escape!")
    maze_str = maze_data_to_string()
    print_maze(maze_str)
    xPos = [17, maze_off+1]
    in_maze = True
    while in_maze == True:
        if maze_str[1][39+maze_off] == "@":
            print("You escaped!")
            break
        set_cursor(xPos[1]+1, xPos[0]+3)
        print("@")
        key = keyboard.read_key()
        if key == 'up' and maze_str[xPos[0]-1][xPos[1]] != "-":
            set_cursor(xPos[1]+1, xPos[0]+3)
            print(" ")
            maze_str[xPos[0] - 2][xPos[1]] = "@"
            maze_str[xPos[0]][xPos[1]] = " "
            xPos[0] -= 2
            set_cursor(xPos[1]+1, xPos[0]+3)
        elif key == 'down' and maze_str[xPos[0]+1][xPos[1]] != "-":
            set_cursor(xPos[1]+1, xPos[0]+3)
            print(" ")
            maze_str[xPos[0] + 2][xPos[1]] = "@"
            maze_str[xPos[0]][xPos[1]] = " "
            xPos[0] += 2
            set_cursor(xPos[1]+1, xPos[0]+3)
        elif key == 'left' and maze_str[xPos[0]][xPos[1]-1] != "|":
            set_cursor(xPos[1]+1, xPos[0]+3)
            print(" ")
            maze_str[xPos[0]][xPos[1] - 2] = "@"
            maze_str[xPos[0]][xPos[1]] = " "
            xPos[1] -= 2
            set_cursor(xPos[1]+1, xPos[0]+3)
        elif key == 'right' and maze_str[xPos[0]][xPos[1]+1] != "|":
            set_cursor(xPos[1]+1, xPos[0]+3)
            print(" ")
            maze_str[xPos[0]][xPos[1] + 2] = "@"
            maze_str[xPos[0]][xPos[1]] = " "
            xPos[1] += 2
            set_cursor(xPos[1]+1, xPos[0]+3)
        elif key == 'esc':
            print(xPos)
            break
        time.sleep(0.2)

def print_maze(maze):
    for i in range(0, 20):
        for j in range(0, 75):
            print(maze[i][j], end = "")
            # if(j == 74):
            #     print("Line ", i)
        print()

'''
+ +
|X
+-+
input as string, resolves in "for" loop to be able to type many directions at once (use wait or sleep command to force it to stop between)
'''
#maze_off = 18
#num_rows = 9
#num_cols = 19
#maze_input()