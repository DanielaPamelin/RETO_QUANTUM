import turtle
import random
import math

# Global variables
XR, YR, ΘR = 0, 0, 0
MAX_X = 300
MAX_Y = 270
STEP_SIZE = 5
NUM_OBSTACLES = 200  

# Distance between two points
def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# Random coordinates for ArUco
X_min, X_max = -MAX_X, MAX_X
Y_min, Y_max = -MAX_Y, MAX_Y
aruco_coords = (random.uniform(X_min, X_max), random.uniform(Y_min, Y_max))

# Generate random obstacle coordinates
obstacles = [(random.uniform(X_min, X_max), random.uniform(Y_min, Y_max)) for _ in range(NUM_OBSTACLES)]

# Turtle setup
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Autonomous Navigation")
screen.bgpic('superficie.png')
rover = turtle.Turtle()
rover.speed(50)

# Move the Rover
def move_rover(x, y, theta):
    rover.penup()
    rover.goto(x, y)
    rover.setheading(theta)
    rover.pendown()

# Print the current coordinates and orientation
def print_rover_state(x, y, theta):
    print(f"Current Rover coordinates: ({x}, {y})")
    print(f"Current Rover orientation: {theta} degrees")

# Draw obstacles as orange squares
rover.penup()
rover.color("purple")
for obstacle in obstacles:
    x, y = obstacle
    rover.goto(x, y)
    rover.dot(5)

# Starting point for the Rover (blue)
move_rover(XR, YR, ΘR)
rover.dot(10, "blue")
print_rover_state(XR, YR, ΘR)

# ArUco code location (pink)
rover.penup()
rover.goto(aruco_coords)
rover.color("yellow")
rover.begin_fill()
for _ in range(5):
    rover.forward(10)
    rover.right(144)
rover.end_fill()

# Final position of the Rover
move_rover(XR, YR, ΘR)
print_rover_state(XR, YR, ΘR)

# Algorithm to search for the ArUco
route = []
while distance((XR, YR), aruco_coords) > STEP_SIZE:
    delta_X = aruco_coords[0] - XR
    delta_Y = aruco_coords[1] - YR
    new_angle = math.degrees(math.atan2(delta_Y, delta_X))
    distance_to_target = min(STEP_SIZE, distance((XR, YR), aruco_coords))
    XR += distance_to_target * math.cos(math.radians(new_angle))
    YR += distance_to_target * math.sin(math.radians(new_angle))

    # Check for collisions with obstacles and avoid them
    for obstacle in obstacles:
        if distance((XR, YR), obstacle) < 10:
            # If too close to an obstacle, move away
            new_angle += 90  # Turn 90 degrees to avoid the obstacle
            XR += 10 * math.cos(math.radians(new_angle))
            YR += 10 * math.sin(math.radians(new_angle))

    route.append((XR, YR))
    move_rover(XR, YR, ΘR)
    print_rover_state(XR, YR, ΘR)

# Final position of the Rover
print_rover_state(XR, YR, ΘR)

# Route on the screen
rover.penup()
for x, y in route:
    rover.goto(x, y)
    rover.pendown()
    rover.dot(5, "green")
    rover.penup()


# Close the window on click
screen.exitonclick()


