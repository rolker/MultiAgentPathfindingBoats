import gurobipy as gp
from matplotlib.patches import Arc
import numpy as np
import pylab as plt
from matplotlib import collections  as mc
from matplotlib.collections import LineCollection
from datetime import datetime


def getMid(end):
    return end+1 if end % 2 == 0 else end-1

def printTranscriptAndPlot(ax, boat, start, end, Boats, EndPoints, points, pathMatrix):
    
    if end >= EndPoints+Boats:
        print(f"Boat {boat} moves from endpoint {start} and ends at rendezvous {end}")
        if pathMatrix != None:
            plotTransit(ax, boat, start, end, pathMatrix)
        else:
            plotLine(boat, start, end, points, False)

    elif start >= EndPoints and start < EndPoints+Boats:
        mid = getMid(end)
        print(f"Boat {boat} moves from start point {start} and then traverses line ({mid},{end})")
        if pathMatrix != None:
            plotTransit(ax, boat, start, end, pathMatrix)
        else:
            plotLine(boat, start, mid, points, False)

        plotLine(boat, mid, end, points, True)

    elif start < EndPoints:
        mid = getMid(end)
        print(f"Boat {boat} moves from endpoint {start} and then traverses line ({mid},{end})")
        if pathMatrix != None:
            plotTransit(ax, boat, start, end, pathMatrix)
        else:
            plotLine(boat, start, mid, points, False)

        plotLine(boat, mid, end, points, True)

def plotLine(boat, start, end, points, isPair):
    boatColors = {
        0 : "red",
        1 : "blue",
        2 : "green",
        3 : "yellow",
        4 : "orange",
    }
    
    if boat < 0:
        plt.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color="black", alpha=0.01)
    else: 
        if isPair:
            plt.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color=boatColors.get(boat % 5, "black"), alpha=0.5)
        else:
            plt.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color=boatColors.get(boat % 5, "black"), alpha=0.5, linestyle='dashed')

        
def plotTransit(ax, boat, start, end, pathMatrix):
    boatColors = {
        0 : "red",
        1 : "blue",
        2 : "green",
        3 : "yellow",
        4 : "orange",
    }

    if pathMatrix[start][end][0] != "LRL" and pathMatrix[start][end][0] != "RLR":
        startCircle, startTheta1, startTheta2  = pathMatrix[start][end][1]
        startCircleX, startCircleY, startCircleRadius = startCircle
        
        tanStart, tanEnd = pathMatrix[start][end][2]

        goalCircle, goalTheta1, goalTheta2 = pathMatrix[start][end][3]
        goalCircleX, goalCircleY, goalCircleRadius = goalCircle
       

        startArc = Arc((startCircleX, startCircleY), width=startCircleRadius*2, height=startCircleRadius*2, angle=0, theta1=startTheta1, theta2=startTheta2, color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5, lw=1.5)
        ax.add_patch(startArc)

        plt.plot([tanStart[0], tanEnd[0]], [tanStart[1], tanEnd[1]], color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5, lw=1.5)

        goalArc = Arc((goalCircleX, goalCircleY), width=goalCircleRadius*2, height=goalCircleRadius*2, angle=0, theta1=goalTheta1, theta2=goalTheta2, color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5, lw=1.5)
        ax.add_patch(goalArc)

    else:
        startCircle, startTheta1, startTheta2  = pathMatrix[start][end][1]
        startCircleX, startCircleY, startCircleRadius = startCircle
        
        midCircle, midTheta1, midTheta2  = pathMatrix[start][end][2]
        midCircleX, midCircleY, midCircleRadius = midCircle

        goalCircle, goalTheta1, goalTheta2 = pathMatrix[start][end][3]
        goalCircleX, goalCircleY, goalCircleRadius = goalCircle

        startArc = Arc((startCircleX, startCircleY), width=startCircleRadius*2, height=startCircleRadius*2, angle=0, theta1=startTheta1, theta2=startTheta2, color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5, lw=1.5)
        ax.add_patch(startArc)

        midArc = Arc((midCircleX, midCircleY), width=midCircleRadius*2, height=midCircleRadius*2, angle=0, theta1=midTheta1, theta2=midTheta2, color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5, lw=1.5)
        ax.add_patch(midArc)

        goalArc = Arc((goalCircleX, goalCircleY), width=goalCircleRadius*2, height=goalCircleRadius*2, angle=0, theta1=goalTheta1, theta2=goalTheta2, color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5, lw=1.5)
        ax.add_patch(goalArc)

# prints problem solution to output and uses matplotlib to plot the solution
def printProblem(model, x, numBoats, numLines, numEndPoints, points, Weight, transitSpeeds, surveySpeeds, toPDF, limitHit, maxes, pdfTitle, pathMatrices):
    show = True
    if show:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # plotting lines going between survey lines
        for boat in range(numBoats):
            for l in range(numLines):
                j, k = [2*l, 2*l+1]
                for i in range(numEndPoints):
                    if i != j and i != k:
                        if(x[boat, j, i] > .5):
                            printTranscriptAndPlot(ax, boat, j, i, numBoats, numEndPoints, points, pathMatrices[boat])
                        if(x[boat, k, i] > .5):
                            printTranscriptAndPlot(ax, boat, k, i, numBoats, numEndPoints, points, pathMatrices[boat])
        
        # plotting lines going from start point/to rendezvous
        for boat in range(numBoats):
            for i in range(numEndPoints):
                if x[boat, numEndPoints+boat, i] > .5:
                    printTranscriptAndPlot(ax, boat, numEndPoints+boat, i, numBoats, numEndPoints, points, pathMatrices[boat])
                if x[boat, i, numEndPoints+numBoats+boat] > .5:
                    printTranscriptAndPlot(ax, boat, i, numEndPoints+numBoats+boat, numBoats, numEndPoints, points, pathMatrices[boat])
        
        objectiveValue = model.ObjVal
        makespan = model.getVarByName('t').X
        weightedSumOfCosts = objectiveValue - makespan
        if Weight == 0:
            sumOfCosts = weightedSumOfCosts
        else:
            sumOfCosts = weightedSumOfCosts / Weight

        # Create a scatter plot for the points and label them
        x1, y = zip(*points)
        scatter = plt.scatter(x1, y, label="Points")

        # Annotate each point with its index
        for i, point in enumerate(points):
            ax.annotate(f'{i}', (point[0], point[1]), textcoords="offset points", xytext=(0, 5), ha='center')

        #for step-through, center graph with max and min points
        if maxes != None:
            plotLine(-1, 0, 1, maxes)
            plotLine(-1, 2, 3, maxes)

        ax.autoscale()

        ax.set_aspect('auto')

        if limitHit:
            outcome = "Suboptimal"
        else:
            outcome = "Optimal"
            
        SLCP_tradeoff_solution_title = (outcome + " SLCP Solution - " + "Lines: " + str(numLines) + ", Boats: " + str(numBoats) + ", T. Speed: " + str(transitSpeeds) + ", S. Speed: " + str(surveySpeeds) + 
                                        "\nTrue Obj.: " + str(round(sumOfCosts + makespan, 2)) + ", SoC: " + str(round(sumOfCosts, 2)) + ", MS: "+ str(round(makespan, 2)) + " ("+ str(round(makespan*100/sumOfCosts, 2)) + "%)" +
                                        "\nWObj.: " + str(round(objectiveValue, 2)) + ", WSoC: " + str(round(weightedSumOfCosts, 2))) + ", W: " + str(Weight)
        
        plt.title(SLCP_tradeoff_solution_title)
        plt.grid()
        if (toPDF):
            plt.savefig(f"{pdfTitle}", format="pdf")    
        else:
            plt.show()  

        plt.close()
