# Labb 2
# Specification : Syftet med den här laborationen är att använda verktygen du lärt dig i Python för att implementera en förenklad 
# maskininlärningsalgoritm. I den här laborationen finns (simulerad) data på Pichus och Pikachus längder och bredder. Du ska skapa 
# en algoritm som baserat på den givna datan kunna avgöra om en ny data punkt ska klassificeras som Pichu eller Pikachu.

# Grunduppgift: Läs in datan och spara i lämplig datastruktur
import matplotlib.pyplot as plt
import numpy as np

dataPoints = []
path_dataPoints = "../Python-programming-Labb2/datapoints.txt"

with open(path_dataPoints, "r") as f_read:
    next(f_read)                                # Skip first row. Inspiration: https://stackoverflow.com/questions/4796764/read-file-from-line-2-or-skip-header-row
    for line in f_read:
        row = line.strip().split(",")           # Ta bort .strip()?
        width = float(row[0])                   #städa bort dessa 3 rader?
        height = float(row[1])
        isPikachu = int(row[2])
        dataPoints.append((width, height, isPikachu))
#        line_np = np.array([width, height, isPikachu])
 #       DataPoints = np.concatenate((DataPoints, line_np))
f_read.close()


# Grunduppgift: Plotta alla punkterna (varje klass får en färg) i samma fönster
#print(f"DataPoints: {DataPoints}")
DataPoints_x = [line[0] for line in dataPoints] 
DataPoints_y = [line[1] for line in dataPoints] 
DataPoints_P = [line[2] for line in dataPoints] # for coloring each class separately 


plt.scatter(DataPoints_x,DataPoints_y, c=DataPoints_P) # colouring condition inspiration taken from: https://www.tutorialspoint.com/scatter-a-2d-numpy-array-in-matplotlib
plt.legend(("Pichu", "Pikachu"))                # only first element is visible in legend. Are two scatters (for each class) needed?
#plt.show()

# Grunduppgift: Läs in testpunkter
path_testpoints = "../Python-programming-Labb2/testpoints.txt"
testPoints = []
with open(path_testpoints, "r") as f_read:
    next(f_read)                                # Skip first row. Inspiration: https://stackoverflow.com/questions/4796764/read-file-from-line-2-or-skip-header-row
    for line in f_read:
        row = line.strip().split(" ")
        for i in range(len(row)):
            row[i] = row[i].strip(".,()")       
        index = int(row[0])
        width = float(row[1])
        height = float(row[2])
        testPoints.append((index, width, height))
    print(testPoints)
f_read.close()

# Grunduppgift: Beräkna avstånd mellamn testpunkt och träningspunkter
# Gör dessa till en numpy array

for i in testPoints:
    
    testWidth = testPoints[i][1]
    testHeight = testPoints[i][2]

    for j in dataPoints:
        dataWidth = dataPoints[j][0]
        dataHeight = dataPoints[j][1]
        shortDistTemp = np.sqrt((testWidth - dataWidth)**2 + (testHeight - dataHeight)**2)
        if shortDistTemp < shortDist or j==0:
            shortDist = shortDistTemp




