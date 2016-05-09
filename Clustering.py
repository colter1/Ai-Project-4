import sys
import matplotlib.pyplot as plt
from math import sqrt
from random import seed, randint, random

COLORS = ['b','r','c','y','k','m','g']
def distance(p1, p2):
    return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def getColors(k):
    # use fun rainbows
    if k <= len(COLORS):
        return COLORS[0:k]
    # use grayscale for large values of k
    r = []
    for i in range(1, k+1):
        r.append(str(i/k))
    return r

def epoch(centroids, data):
    sd = sortData(centroids, data)
    r = []
    for c in range(0, len(centroids)):
        xsum = 0
        ysum = 0
        for point in sd[c]:
            xsum += point[0]
            ysum += point[1]
        if len(sd[c]) != 0:
            r.append((xsum/len(sd[c]), ysum/len(sd[c])))
        else:
            r.append(centroids[c])
    return r
    
def converge(centroids, data):
    dist = float("inf")
    while dist > 0:
        old = centroids
        centroids = epoch(old, data)
        dist = 0
        for c in range(0, len(old)):
            dist += distance(centroids[c], old[c])
    return centroids
    
def sortData(centroids, data):
    r = []
    for c in centroids:
        r.append([])
    
    for point in data:
        closest = float("inf")
        index = 0
        for c in centroids:
            d = distance(point, c)
            if d < closest:
                closest = d
                index = centroids.index(c)
        r[index].append(point)
    return r

def displayGraph(centroids, data):
    sd = sortData(centroids, data)
    colors = getColors(len(centroids))
    circles = []
    for x in range(0, len(centroids)):
        furthest = 0
        for point in sd[x]:
            plt.plot(point[0], point[1], marker='o', color=colors[x])
            d = distance(centroids[x], point)
            if d > furthest:
                furthest = d # store the furthest distance in the cluster for radius
        circles.append(plt.Circle(centroids[x], furthest, color=colors[x], alpha = 0.6))
        plt.plot(centroids[x][0], centroids[x][1], color=colors[x], marker='^')
    fig = plt.gcf()
    for c in circles:
        fig.gca().add_artist(c)
    plt.show()
    

def initCentroids(data, k):
    # Forgy method for standard k-means
    ''' 
    r = []
    for i in range(0, k):
        r.append(data[randint(0, len(data)-1)])
    return r'''
    
    seed()
    
    # k-means++ method (spreads out starting centroid locations)
    r = [data[randint(0, len(data)-1)]]
    while len(r) < k:
        distances = []
        greatestDistance = 0
        
        # calculate distances to closest centroid and square values
        for point in data:
            closest = float("inf")
            for centroid in r:
                d = distance(point, centroid)
                if d < closest:
                    closest = d
            distances.append(closest**2)
            if closest**2 > greatestDistance:
                greatestDistance = closest**2
        
        # normalize data by dividing by the greatest valuse
        for d in range(0, len(distances)):
            distances[d] = distances[d]/greatestDistance
        
        # select another starting point based on probability
        chosen = False
        while not chosen:
            newIndex = randint(0, len(distances)-1)
            if random() < distances[newIndex]:
                chosen = True
                r.append(data[newIndex])
    return r

def readFile(inputfile="data.txt"):
    infile = open(inputfile, 'r')
    data = []
    for line in infile:
        point = line.split(',')
        data.append((int(point[0]), int(point[1])))
    return data

if __name__ == '__main__':
    k = int(sys.argv[1])
    inputfile = sys.argv[2]
    data = readFile(inputfile)
    centroids = initCentroids(data, k)
    centroids = converge(centroids, data)
    displayGraph(centroids, data)
