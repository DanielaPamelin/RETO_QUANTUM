import math
import random
from simpleai.search import SearchProblem, astar, greedy, breadth_first, depth_first, uniform_cost
from colorama import Fore, Style

class Exploreterrain(SearchProblem):
    def __init__(self, board):
        self.board = board 
        self.goal = (0, 0)
        self.initial = (0,0)
        #Starting and ending points
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "@": #Rover
                    self.board[y][x]=0
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "$":   #ArUco
                    self.board[y][x]=0
                    self.goal = (x, y)
                    
        super(Exploreterrain, self).__init__(initial_state=self.initial)

    # Take actions to reach the solution
    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] not in ("#","^"):
                if abs(int(self.board[newy][newx]) - int(self.board[self.initial[1]][self.initial[0]])) <= 1:
                    actions.append(action)
        return actions

    # Update state based on action
    def result(self, state, action):
        x, y = state
        
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)

        return new_state

    #Check target
    def is_goal(self, state):
        return state == self.goal

    #Cost
    def cost(self, state, action, state2):
        return COSTS[action]

    #Heuristics
    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal

        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

if __name__ == "__main__":
    MAP = """
################################
#4015^514^1414^3532050^11325202#
#2^3302103035333155124051314^24#
#3041^^0201545450502^3113514522#
#5^21352^45^^333^^24320^101^440#
#05504$0^2^02202014^22^52121^42#
#241313^0^^244131341^3^151^3130#
#1^55320434^2135^^5051354^0415^#
#5253505^12^5003^50254425502053#
#^42215341022115555024^32211212#
#^2^4102304^334502542^^25150102#
#^^0^230414^0550322035401330205#
#13330@03010142401100341^2^2^3^#
#5404034^0^540311130^404114550^#
#1^^1500^003505^3^102145120^0^^#
#443555^^2401424^0^24042^331204#
################################
    """
    
    #Split the map into lines and convert each line to a list of characters
    lines = MAP.strip().splitlines()
    board = [list(line) for line in lines]

    # Loop through each position, convert numbers to integers
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x].isdigit():
                board[y][x] = int(board[y][x])

    # Join the character for the the new map
    MAP = "\n".join("".join(str(cell) for cell in row) for row in board)
    print(MAP)
    MAP = [list(x) for x in MAP.split("\n") if x]
    
    #The cost of movement 
    cost_regular = 1.0

    # Dictionary
    COSTS = {
        "up": cost_regular,
        "down": cost_regular,
        "left": cost_regular,
        "right": cost_regular,
        "up left": cost_regular,
        "up right": cost_regular,
        "down left": cost_regular,
        "down right": cost_regular,
    }

    # Create maze solver object
    problem = Exploreterrain(MAP)

    # Run the solver
    # Here you CAN CHANGE THE ALGORITHM you want to use
    result = depth_first(problem, graph_search=True)

    # Path
    path = [x[1] for x in result.path()]
    print(f" \n The movements to reach ArUco: {path}")
    
    #Calculates the total cost 
    sum_values = 0
    for coor in path:
        x, y = coor
        value = int(MAP[y][x])
        sum_values += value +1
        

    # Print the result
    print()
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print(Fore.BLUE +'*'+Style.RESET_ALL, end='')
            elif (x, y) == problem.goal:
                print(Fore.GREEN +'x'+Style.RESET_ALL, end='')
            elif (x, y) in path:
                print(Fore.RED +'$'+Style.RESET_ALL, end='')
            else:
                print(MAP[y][x], end='')

        print()