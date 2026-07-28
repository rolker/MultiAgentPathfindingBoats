import numpy as np
# point: (x, y, ...)
# position: (x, y, theta)
# circle: (x, y, radius)

def toDegrees(theta):
    return (theta * 180 / np.pi) % 360

#calculating distance between point1 and point2
def findEuclideanDistance(point1, point2):
    # print(f"{point1}, point2 {point2}")
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#calculating the angle from point1 to point2 
def findAngleBetweenPoints(point1, point2):
    opposite = point2[1] - point1[1]
    adjacent = point2[0] - point1[0]
    if round(adjacent, 10) == 0 and round(opposite, 10) == 0:
        return 0
    
    if round(adjacent, 10) == 0:
        if opposite > 0:
            return .5 * np.pi
        else:
            return 1.5 * np.pi
        
    if adjacent < 0:
        additionalTheta = np.pi
    else:
        additionalTheta = 0

    theta = (np.arctan((point2[1] - point1[1]) / (point2[0] - point1[0]))) + additionalTheta
    if theta < 0:
        theta += 2*np.pi

    return theta 

#calculating circles with boat's minimum radius tangent to the boat's current position at +90 and -90 degrees
def findTangentCircles(position, radius):
    x, y, theta = position

    thetaToLeftCircle = theta + np.pi / 2
    thetaToRightCircle = theta - np.pi / 2

    leftCircle = (x + radius * float(np.cos(thetaToLeftCircle)), y + radius * float(np.sin(thetaToLeftCircle)), radius)
    rightCircle = (x + radius * float(np.cos(thetaToRightCircle)), y + radius * float(np.sin(thetaToRightCircle)), radius)

    return (leftCircle, rightCircle)

def findAllPaths(startPosition, goalPosition, minimumRadius):
    startX, startY, startTheta = startPosition
    goalX, goalY, goalTheta = goalPosition

    startLeftCircle, startRightCircle = findTangentCircles(startPosition, minimumRadius)
    goalLeftCircle, goalRightCircle = findTangentCircles(goalPosition, minimumRadius)

    startLeftX, startLeftY, startLeftRadius = startLeftCircle
    startRightX, startRightY, startRightRadius = startRightCircle

    goalLeftX, goalLeftY, goalLeftRadius = goalLeftCircle
    goalRightX, goalRightY, goalRightRadius = goalRightCircle

    pathEntries = {}
    shortestPathLength = np.inf
    shortestPathName = ""

    #LSL--------------------------------------------------------------------------------------------------------------------------------------------------------------

    D = findEuclideanDistance(startLeftCircle, goalLeftCircle)
    
    tanTheta = findAngleBetweenPoints(startLeftCircle, goalLeftCircle)

    startArcLength = (tanTheta - startTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

    goalArcLength = (goalTheta - tanTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

    LSLPathLength = startArcLength + D + goalArcLength

    thetaToTan = tanTheta - np.pi/2

    tanStartPoint = [startLeftX + minimumRadius * np.cos(thetaToTan), startLeftY + minimumRadius * np.sin(thetaToTan)]

    tanGoalPoint =  [goalLeftX + minimumRadius * np.cos(thetaToTan), goalLeftY + minimumRadius * np.sin(thetaToTan)]
    
    pathEntries["LSL"] = [LSLPathLength, ["LSL", (startLeftCircle, toDegrees(startTheta - np.pi/2), toDegrees(thetaToTan)), (tanStartPoint, tanGoalPoint), (goalLeftCircle, toDegrees(thetaToTan), toDegrees(goalTheta - np.pi/2))]]

    if (LSLPathLength < shortestPathLength):
        shortestPathLength = LSLPathLength
        shortestPathName = "LSL"

    #RSR--------------------------------------------------------------------------------------------------------------------------------------------------------------

    D = findEuclideanDistance(startRightCircle, goalRightCircle)

    tanTheta = findAngleBetweenPoints(startRightCircle, goalRightCircle)

    startArcLength = (startTheta - tanTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

    goalArcLength = (tanTheta - goalTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

    RSRPathLength = startArcLength + D + goalArcLength

    thetaToTan = tanTheta + np.pi/2
    
    tanStartPoint = [startRightX + minimumRadius * np.cos(thetaToTan), startRightY + minimumRadius * np.sin(thetaToTan)]

    tanGoalPoint =  [goalRightX + minimumRadius * np.cos(thetaToTan), goalRightY + minimumRadius * np.sin(thetaToTan)]
    
    pathEntries["RSR"] = [RSRPathLength, ["RSR", (startRightCircle, toDegrees(thetaToTan), toDegrees(startTheta + np.pi/2)), (tanStartPoint, tanGoalPoint), (goalRightCircle, toDegrees(goalTheta + np.pi/2), toDegrees(thetaToTan))]]

    if (RSRPathLength < shortestPathLength):
        shortestPathLength = RSRPathLength
        shortestPathName = "RSR"


    #LSR--------------------------------------------------------------------------------------------------------------------------------------------------------------

    D = findEuclideanDistance(startLeftCircle, goalRightCircle)

    if (D >= 2*minimumRadius):
        startToGoalTheta = findAngleBetweenPoints(startLeftCircle, goalRightCircle)

        thetaBewteenGoalAndTan = np.arccos(minimumRadius/(D/2))

        tanTheta = startToGoalTheta - thetaBewteenGoalAndTan + np.pi/2

        tanLength = np.sin(thetaBewteenGoalAndTan) * D

        startArcLength = (tanTheta - startTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

        goalArcLength = (tanTheta - goalTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

        LSRPathLength = startArcLength + tanLength + goalArcLength
        
        startToTanTheta = tanTheta - np.pi/2

        goalToTanTheta = tanTheta + np.pi/2
        
        tanStartPoint = [startLeftX + minimumRadius * np.cos(startToTanTheta), startLeftY + minimumRadius * np.sin(startToTanTheta)]

        tanGoalPoint =  [goalRightX + minimumRadius * np.cos(goalToTanTheta), goalRightY + minimumRadius * np.sin(goalToTanTheta)]
        
        pathEntries["LSR"] = [LSRPathLength, ["LSR", (startLeftCircle, toDegrees(startTheta - np.pi/2), toDegrees(startToTanTheta)), (tanStartPoint, tanGoalPoint), (goalRightCircle, toDegrees(goalTheta + np.pi/2), toDegrees(goalToTanTheta))]]

        if (LSRPathLength < shortestPathLength):
            shortestPathLength = LSRPathLength
            shortestPathName = "LSR"


    #RSL--------------------------------------------------------------------------------------------------------------------------------------------------------------

    D = findEuclideanDistance(startRightCircle, goalLeftCircle)

    if (D >= 2*minimumRadius):
        startToGoalTheta = findAngleBetweenPoints(startRightCircle, goalLeftCircle)

        thetaBewteenGoalAndTan = np.arccos(minimumRadius/(D/2))

        tanTheta = startToGoalTheta + thetaBewteenGoalAndTan - np.pi/2

        tanLength = np.sin(thetaBewteenGoalAndTan) * D

        startArcLength = (startTheta - tanTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

        goalArcLength = (goalTheta - tanTheta) * minimumRadius % (minimumRadius * 2 * np.pi)

        RSLPathLength = startArcLength + tanLength + goalArcLength

        startToTanTheta = tanTheta + np.pi/2

        goalToTanTheta = tanTheta - np.pi/2
        
        tanStartPoint = [startRightX + minimumRadius * np.cos(startToTanTheta), startRightY + minimumRadius * np.sin(startToTanTheta)]

        tanGoalPoint =  [goalLeftX + minimumRadius * np.cos(goalToTanTheta), goalLeftY + minimumRadius * np.sin(goalToTanTheta)]
        
        pathEntries["RSL"] = [RSLPathLength, ["RSL", (startRightCircle, toDegrees(startToTanTheta), toDegrees(startTheta + np.pi/2)), (tanStartPoint, tanGoalPoint), (goalLeftCircle, toDegrees(goalToTanTheta), toDegrees(goalTheta - np.pi/2))]]

        if (RSLPathLength < shortestPathLength):
            shortestPathLength = RSLPathLength
            shortestPathName = "RSL"

    #LRL--------------------------------------------------------------------------------------------------------------------------------------------------------------

    D = findEuclideanDistance(startLeftCircle, goalLeftCircle)
    startToGoalTheta = findAngleBetweenPoints(startLeftCircle, goalLeftCircle)

    if (2*minimumRadius == D/2):

        startTanTheta = startToGoalTheta + np.pi/2

        startArcLength = minimumRadius * (startTanTheta - startTheta) % (minimumRadius * 2 * np.pi)

        midArcLength = minimumRadius * np.pi % (minimumRadius * 2 * np.pi)

        goalTanTheta = startTanTheta + np.pi

        goalArcLength = minimumRadius * (goalTheta - goalTanTheta) % (minimumRadius * 2 * np.pi)
 
        LRLPathLength = startArcLength + midArcLength + goalArcLength 

        midCircle = (startLeftX + np.cos(startToGoalTheta) * minimumRadius*2, startLeftY + np.sin(startToGoalTheta) * minimumRadius*2, minimumRadius)

        pathEntries["LRL"] = [LRLPathLength, ["LRL", (startLeftCircle, toDegrees(startTheta - np.pi/2), toDegrees(startToGoalTheta)), (midCircle, toDegrees(startToGoalTheta + np.pi), toDegrees(startToGoalTheta)), (goalLeftCircle, toDegrees(startToGoalTheta + np.pi), toDegrees(goalTheta - np.pi/2))]]
        if (LRLPathLength < shortestPathLength):
            shortestPathLength = LRLPathLength
            shortestPathName = "LRL"


    elif (2*minimumRadius > D/2):

        thetaBetweenMidAndGoal = np.arccos((D/2) / (2*minimumRadius))  

        startToMidTheta = startToGoalTheta + thetaBetweenMidAndGoal

        startTanTheta = startToMidTheta + np.pi/2

        startArcLength = minimumRadius * (startTanTheta - startTheta) % (minimumRadius * 2 * np.pi)

        thetaBetweenStartAndGoal = (np.pi + 2 * thetaBetweenMidAndGoal)

        midArcLength = thetaBetweenStartAndGoal * minimumRadius % (minimumRadius * 2 * np.pi)

        goalTanTheta = startTanTheta - thetaBetweenStartAndGoal

        goalArcLength = minimumRadius * (goalTheta - goalTanTheta) % (minimumRadius * 2 * np.pi)

        LRLPathLength = startArcLength + midArcLength + goalArcLength 

        midCircle = (startLeftX + np.cos(startToMidTheta) * minimumRadius*2, startLeftY + np.sin(startToMidTheta) * minimumRadius*2, minimumRadius)

        midToStartTheta = startToMidTheta + np.pi
        
        midToGoalTheta = midToStartTheta - thetaBetweenStartAndGoal

        pathEntries["LRL"] = [LRLPathLength, ["LRL", (startLeftCircle, toDegrees(startTheta - np.pi/2), toDegrees(startToMidTheta)), (midCircle, toDegrees(midToGoalTheta), toDegrees(midToStartTheta)), (goalLeftCircle, toDegrees(goalTanTheta - np.pi/2), toDegrees(goalTheta - np.pi/2))]]
        if (LRLPathLength < shortestPathLength):
            shortestPathLength = LRLPathLength
            shortestPathName = "LRL"


    #RLR--------------------------------------------------------------------------------------------------------------------------------------------------------------

    D = findEuclideanDistance(startRightCircle, goalRightCircle)
    startToGoalTheta = findAngleBetweenPoints(startRightCircle, goalRightCircle)

    if (2*minimumRadius == D/2):

        startTanTheta = startToGoalTheta - np.pi/2

        startArcLength = minimumRadius * (startTheta - startTanTheta) % (minimumRadius * 2 * np.pi)

        midArcLength = minimumRadius * np.pi % (minimumRadius * 2 * np.pi)

        goalTanTheta = startTanTheta + np.pi

        goalArcLength = minimumRadius * (goalTanTheta - goalTheta) % (minimumRadius * 2 * np.pi)
 
        RLRPathLength = startArcLength + midArcLength + goalArcLength 

        midCircle = (startRightX + np.cos(startToGoalTheta) * minimumRadius*2, startRightY + np.sin(startToGoalTheta) * minimumRadius*2, minimumRadius)

        pathEntries["RLR"] = [RLRPathLength, ["RLR", (startRightCircle, toDegrees(startTheta + np.pi/2), toDegrees(startToGoalTheta)), (midCircle, toDegrees(startToGoalTheta), toDegrees(startToGoalTheta + np.pi)), (goalRightCircle, toDegrees(goalTheta + np.pi/2), toDegrees(startToGoalTheta + np.pi))]]
        
        if (RLRPathLength < shortestPathLength):
            shortestPathLength = RLRPathLength
            shortestPathName = "RLR"


    elif (2*minimumRadius > D/2):

        thetaBetweenMidAndGoal = np.arccos((D/2) / (2*minimumRadius))  

        startToMidTheta = startToGoalTheta - thetaBetweenMidAndGoal

        startTanTheta = startToMidTheta - np.pi/2

        startArcLength = minimumRadius * (startTheta - startTanTheta) % (minimumRadius * 2 * np.pi)

        thetaBetweenStartAndGoal = (np.pi + 2 * thetaBetweenMidAndGoal)

        midArcLength = thetaBetweenStartAndGoal * minimumRadius % (minimumRadius * 2 * np.pi)

        goalTanTheta = startTanTheta + thetaBetweenStartAndGoal

        goalArcLength = minimumRadius * (goalTanTheta - goalTheta) % (minimumRadius * 2 * np.pi)

        RLRPathLength = startArcLength + midArcLength + goalArcLength 

        midCircle = (startRightX + np.cos(startToMidTheta) * minimumRadius*2, startRightY + np.sin(startToMidTheta) * minimumRadius*2, minimumRadius)

        midToStartTheta = startToMidTheta + np.pi
        
        midToGoalTheta = midToStartTheta + thetaBetweenStartAndGoal

        pathEntries["RLR"] = [RLRPathLength, ["RLR", (startRightCircle, toDegrees(startToMidTheta), toDegrees(startTheta + np.pi/2)), (midCircle, toDegrees(midToStartTheta), toDegrees(midToGoalTheta)), (goalRightCircle, toDegrees(goalTheta + np.pi/2), toDegrees(goalTanTheta + np.pi/2))]]
        if (RLRPathLength < shortestPathLength):
            shortestPathLength = RLRPathLength
            shortestPathName = "RLR"

    pathEntries["shortest"] = shortestPathName

    

    return pathEntries

def findShortestPath(startOppositePoint, startPoint, goalPoint, goalOppositePoint, minimumRadius):
    if (startOppositePoint == None):
        startPosition = (startPoint[0], startPoint[1], findAngleBetweenPoints(startPoint, goalPoint))
    else:
        startPosition = (startPoint[0], startPoint[1], findAngleBetweenPoints(startOppositePoint, startPoint))

    if (goalOppositePoint == None):
        goalPosition = (goalPoint[0], goalPoint[1], findAngleBetweenPoints(startPoint, goalPoint))
    else:
        goalPosition = (goalPoint[0], goalPoint[1], findAngleBetweenPoints(goalPoint, goalOppositePoint))

    
    pathEntries = findAllPaths(startPosition, goalPosition, minimumRadius)

    return pathEntries[pathEntries["shortest"]]