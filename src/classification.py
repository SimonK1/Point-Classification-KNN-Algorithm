import random
import math
from csv import reader
import sys
import time
import os, psutil
from matplotlib import pyplot as plt
import numpy as np

# Global variables
xs = []
ys = []
cls = []
k = 1
success = 0
points = 5000

# Regions for colors
red = [(-5000, 500), (-5000, 500)]
green = [(-500, 5000), (-5000, 500)]
blue = [(-5000, 500), (-500, 5000)]
purple = [(-500, 5000), (-500, 5000)]

# Visualisation of data
def visual(xs, ys, cls):
    plt.figure()
    plt.scatter(xs, ys,s=0.1, c=cls)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('tight')
    plt.show()
    plt.close('all')


# Classification of one point
def classify(x, y, supposedColor):
    global success, k
    best = [[],[]]
    counter = 0

    # Iterating through every classified point
    for i in xs:
        best[0].append(math.sqrt(((i - x) ** 2) + ((ys[counter] - y) ** 2)))
        best[1].append((i,ys[counter],cls[counter]))
        counter += 1

    # Sorting to find closest neighbour
    indexes = list(range(len(best[0])))
    indexes.sort(key=best[0].__getitem__)
    sorted_list2 = list(map(best[1].__getitem__, indexes))
    reds = 0

    # Counting color occurances
    for i in range(0, k):
        if sorted_list2[i][2] == 'red':
            reds += 1
    blues = 0
    for i in range(0, k):
        if sorted_list2[i][2] == 'blue':
           blues += 1
    greens = 0
    for i in range(0, k):
        if sorted_list2[i][2] == 'green':
            greens += 1
    purples = 0
    for i in range(0, k):
        if sorted_list2[i][2] == 'purple':
            purples += 1
    var = {reds: "red", blues: "blue", greens: "green", purples: "purple"}
    col = var.get(max(var))

    # Choosing color according to occurences
    if col == 'red':
        if 'red' == supposedColor:
            success += 1
        return 'red'
    if col == 'blue':
        if 'blue' == supposedColor:
            success += 1
        return 'blue'
    if col == 'green':
        if 'green' == supposedColor:
            success += 1
        return 'green'
    if col == 'purple':
        if 'purple' == supposedColor:
            success += 1
        return 'purple'

# Iterations across all points
def classifyPoints():
    global points

    # Opening file with generated points
    with open("generatedData.csv", 'r') as file:
        csv_reader = reader(file)
        counter = 0

        # Iterating through every point
        for row in csv_reader:
            helper = row[0].split()

            # Classification of one point
            color = classify(int(helper[0]), int(helper[1]), helper[2])

            # Savinf points to arrays
            xs.append(int(helper[0]))
            ys.append(int(helper[1]))
            cls.append(color)
            counter = counter + 1
            if counter == points:
                break

# Generating N points
def generatePoints():
    global points
    color = 0

    # Filling matrix with zeroes
    arr = np.zeros((10001, 10001))
    supposedColor = ''

    # Opening file
    file = open("generatedData.csv", "w")

    # Choosing range for that exact color
    for i in range (points):
        if color == 0:
            x_range = red[0]
            y_range = red[1]
        elif color == 1:
            x_range = green[0]
            y_range = green[1]
        elif color == 2:
            x_range = blue[0]
            y_range = blue[1]
        elif color == 3:
            x_range = purple[0]
            y_range = purple[1]
        randInt = random.randint(1, 100)

        # Applying 99% chance
        if randInt < 100:
            while 1:
                # Choosing number in desired interval
                x = random.randint(x_range[0], x_range[1])
                y = random.randint(y_range[0], y_range[1])
                hx = x + 5000
                hy = y + 5000

                # Checking if this point is unique
                if arr[hx][hy] == 0:
                    break
                else:
                    continue
        else:
            while 1:
                # Choosing region out of desired intervals
                rx = list(range(-5000, x_range[0])) + list(range(x_range[1], 5000))
                ry = list(range(-5000, y_range[0])) + list(range(y_range[1], 5000))
                x = random.choice(rx)
                y = random.choice(ry)
                hx = x + 5000
                hy = y + 5000
                # Checking if this point is unique
                if arr[hx][hy] == 0:
                    break
                else:
                    continue
        hx = x+5000
        hy = y+5000
        arr[hx][hy] = 1

        # Transforming int to str for better orientation
        if color == 0:
            supposedColor = 'red'
        if color == 1:
            supposedColor = 'green'
        if color == 2:
            supposedColor = 'blue'
        if color == 3:
            supposedColor = 'purple'

        # Writing into the file
        line = str(x) + " " + str(y) + " " + str(supposedColor) + "\n"
        file.write(line)
        color = (color + 1) % 4
    file.close()
    return

# Counting % of success
def countPercentage():
    global success, points
    return success/points*100

def printing():
    print("_______________________________________")
    print("Elapsed Time:")
    print("%i Minutes" % ((time.time() - start_time) // 60), "%s Seconds" % ((time.time() - start_time) % 60))
    process = psutil.Process(os.getpid())
    print("Memory used:", process.memory_info().rss / 1000000, "MB")
    print("Success Rate: ",countPercentage(),"%")
    print("_______________________________________")


# Loading points that are default
def load_csv():
    with open("dataset.csv", 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            # Adding points to arrays
            helper = row[0].split()
            xs.append(int(helper[0]))
            ys.append(int(helper[1]))
            cls.append(helper[2])
    return xs, ys, cls

def main():
    global k, points, success
    print("_______________________________________")
    print("       Welcome to classificator        ")
    print("_______________________________________")
    print("Press: Exit, Points(Generate Points), Start")
    while 1:
        answer = input()
        if answer == "Exit" or answer == "exit":
            print("_______________________________________")
            print("        Thank you and good bye         ")
            sys.exit()
        elif answer == "Start" or answer == "start":
            print("_______________________________________")
            print("Choose K: 1, 3, 7, 15")
            k = int(input())
            print("      Preparing classification...      ")
            global start_time
            success = 0
            start_time = time.time()
            xs, ys, cls = load_csv()
            classifyPoints()
            printing()
            visual(xs, ys, cls)
            print("       Classification completed        ")
            print("_______________________________________")
        elif answer == "Points" or answer == "points":
            print("_______________________________________")
            print("How many points ?")
            points = int(input())
            print("          Preparing points...          ")
            generatePoints()
            print("           Points prepared             ")
            print("_______________________________________")
        else:
            print("_______________________________________")
            print("    Wrong command. Please try again    ")
            print("_______________________________________")


if __name__ == "__main__":
    main()