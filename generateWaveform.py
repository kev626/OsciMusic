import math
from chinesepostman import eularian, network
import wave
import struct
import numpy

def run():
    pointsFile = open("C:\\Users\\Kevin\\Documents\\osciMusic\\points.txt")

    edges = []
    points = []

    reachedPoints = False
    for line in pointsFile:
        splitresult = line.split(",")
        if len(splitresult) == 1:
            reachedPoints = True
            continue

        if not reachedPoints:
            edges.append((int(splitresult[0]), int(splitresult[1])))
        else:
            points.append((2 * float(splitresult[0]) - 1, 2 * float(splitresult[1]) - 1))
    
    pointsFile.close()
    
    distances = []
    for edge in edges:
        x1 =points[edge[0]][0]
        y1 =points[edge[0]][1]
        x2 =points[edge[1]][0]
        y2 =points[edge[1]][1]

        distances.append(math.sqrt((x1-x2)**2 + (y1-y2)**2))
    
    graphArr = []
    for i in range(len(edges)):
        graphArr.append((edges[i][0], edges[i][1], distances[i]))

    original_graph = network.Graph(graphArr)
    if not original_graph.is_eularian:
        print("Making eularian path")
        graph = eularian.make_eularian(original_graph)
    else:
        graph = original_graph
    
    route, attempts = eularian.eularian_path(graph)
    if not route:
        print("Can't solve path!")
        return
    else:
        route.append(route[0])
        print("Solved for best path")
        print(route)
    
    samples = 192000.0 # Sample rate in Hz
    freq = 256 # Audio frequency
    duration = 2 # Audio duration (seconds)
    totalSamples = int(samples * duration)

    wavFile = wave.open("out.wav", "wb")
    wavFile.setnchannels(2)
    wavFile.setsampwidth(2)
    wavFile.setframerate(samples)
    wavFile.setnframes(totalSamples)

    samplesPerPeriod = int(samples / freq)

    distances = []
    for i in range(1, len(route)):
        distances.append(dist(route[i-1], route[i], points))
    totalDistance = sum(distances)

    distancePerSample = totalDistance / samplesPerPeriod
    
    for sample in range(totalSamples):
        i = sample % samplesPerPeriod
        distanceTravelledSoFar = i * distancePerSample
        currentSegment = 0

        walkedDistance = 0
        for seg in range(1, len(route)):
            walkedDistance += dist(route[seg-1], route[seg], points)
            if walkedDistance >= distanceTravelledSoFar or currentSegment == len(route) - 1:
                break
            currentSegment += 1
        
        segmentLength = dist(route[currentSegment], route[currentSegment + 1], points)

        distanceIntoCurrent = distanceTravelledSoFar - (walkedDistance - segmentLength)
        percentOfCurrentSegment = distanceIntoCurrent / segmentLength

        h = int(32767.0 * lerp(points[route[currentSegment]][0], points[route[currentSegment + 1]][0], percentOfCurrentSegment))
        v = int(32767.0 * lerp(points[route[currentSegment]][1], points[route[currentSegment + 1]][1], percentOfCurrentSegment))

        wavFile.writeframesraw(struct.pack('<hh', h, v))
    
    wavFile.close()



def lerp(a, b, x):
    return a + x * (b - a)

def dist(indA, indB, points):
    return math.sqrt((points[indA][0]-points[indB][0])**2 + (points[indA][1]-points[indB][1])**2)
    pass

if __name__ == "__main__":
    run()