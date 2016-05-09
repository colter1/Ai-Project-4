import argparse
from random import seed, randint
from sys import exit
from os import path

def makeData(args):
    data = []
    seed()
    if(args.totalpoints == 0):
        # Check args
        if(args.clusters == 0):
            print("Program exiting: totalpoints = 0 and clusters = 0")
            exit(1)
        if(args.clusterpoints == 0):
            print("Program exiting: totalpoints = 0 and clusterpoints = 0")
            exit(1)
            
        # Generate data
        for cluster in range(args.clusters):
            centroid = (randint(args.xmin, args.xmax), randint(args.ymin, args.ymax))
            for point in range(args.clusterpoints):
                x = randint(max(centroid[0] - args.deviation, args.xmin), min(centroid[0] + args.deviation, args.xmax))
                y = randint(max(centroid[1] - args.deviation, args.ymin), min(centroid[1] + args.deviation, args.ymax))
                data.append((x,y))
    else:
        # Random data
        if(args.clusters == 0):
            for point in range(args.totalpoints):
                x = randint(args.xmin, args.xmax)
                y = randint(args.ymin, args.ymax)
                data.append((x,y))
        # totalpoints/clusters
        else:
            for cluster in range(args.clusters):
                centroid = (randint(args.xmin, args.xmax), randint(args.ymin, args.ymax))
                for point in range(int(args.totalpoints/args.clusters)):
                    x = randint(max(centroid[0] - args.deviation, args.xmin), min(centroid[0] + args.deviation, args.xmax))
                    y = randint(max(centroid[1] - args.deviation, args.ymin), min(centroid[1] + args.deviation, args.ymax))
                    data.append((x,y))
    return data                    
    
def filecheck(filename="data.txt"):
    if(path.isfile(filename)):
        print("{} already exists.  Overwrite {}?".format(filename, filename))
        if(query()):
            # write data to file 
            print("writing data to {}".format(filename))
            return
        else:
            print("exiting...")
            exit(0)
    else:
        # write data to file 
        print("writing data to {}".format(filename))
        return
    
def query():
    yes = set(["yes", "y"])
    no = set(["no", "n", ""])
    
    # do-while loop
    while True:    
        choice = input().lower()
        if choice in yes:
            return True
        if choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'")
    
def writeData(data, filename="data.txt"):
    outputfile = open(filename, 'w')
    outputfile.truncate()
    for point in data:
        outputfile.write(str(point[0]) + ' ' + str(point[1]) + '\n')
    outputfile.close()

def getParser():
    parser = argparse.ArgumentParser(description="Generate files of random 2D clusters")
    parser.add_argument("filename", help="the name of the file to be written")
    parser.add_argument("-xn", "--xmin", help="the minimum value for x (inclusive)", type=int, default=-25)
    parser.add_argument("-xx", "--xmax", help="the maximum value for x (inclusive)", type=int, default=25)
    parser.add_argument("-yn", "--ymin", help="the minimum value for y (inclusive)", type=int, default=-25)
    parser.add_argument("-yx", "--ymax", help="the maximum value for y (inclusive)", type=int, default=25)
    parser.add_argument("-d", "--deviation", help="the max deviation of a cluster point from the cluster's centroid", type=int, default=5)
    parser.add_argument("-c", "--clusters", help="the number of natural clusters", type=int, default=3, choices=range(0,100))
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-tp", "--totalpoints", help="the total number of points in the data set", type=int, default=0)
    group.add_argument("-cp", "--clusterpoints", help="the number of points per cluster", type=int, default=5)
    return parser

if __name__ == '__main__':
    p = getParser()
    args = p.parse_args()
    data = makeData(args)
    filecheck(args.filename)
    writeData(data, args.filename)
    
