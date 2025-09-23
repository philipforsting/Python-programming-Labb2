# Labb 2
# Specification : Syftet med den här laborationen är att använda verktygen du lärt dig i Python för att implementera en förenklad 
# maskininlärningsalgoritm. I den här laborationen finns (simulerad) data på Pichus och Pikachus längder och bredder. Du ska skapa 
# en algoritm som baserat på den givna datan kunna avgöra om en ny data punkt ska klassificeras som Pichu eller Pikachu.

# Grunduppgift: Läs in datan och spara i lämplig datastruktur
import matplotlib.pyplot as plt
import numpy as np

dataPoints = []
path_dataPoints = "../Python-programming-Labb2/datapoints.txt"

with open(path_dataPoints, "r") as f_read:      # gör detta till en funktion istället
    next(f_read)                                # Skip first row. Inspiration: https://stackoverflow.com/questions/4796764/read-file-from-line-2-or-skip-header-row
    for line in f_read:
        row = line.split(",")                   # row contains ["width", "height", "isPikachu"]
        dataPoints.append([float(row[0]), float(row[1]), float(row[2])]) # converting elements in row to floats and adding them to list dataPoints Inspiration: https://stackoverflow.com/questions/21238242/python-read-file-into-2d-list
f_read.close()
dataPoints = np.array(dataPoints)               


# Grunduppgift: Plotta alla punkterna (varje klass får en färg) i samma fönster
DataPoints_x = [line[0] for line in dataPoints] 
DataPoints_y = [line[1] for line in dataPoints] 
DataPoints_P = [line[2] for line in dataPoints] # for coloring each class separately 
# Konvertera till Numpy så behövs inte koden ovan

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
        testPoints.append((float(row[0]), float(row[1]), float(row[2])))
f_read.close()

testPoints_x = [line[1] for line in testPoints] 
testPoints_y = [line[2] for line in testPoints] 
plt.scatter(testPoints_x,testPoints_y) 
plt.show()

# Grunduppgift: Beräkna avstånd mellamn testpunkt och träningspunkter

# Preparing to store distance between testpoint and datapoints in additinoal column
zeroColumn = np.zeros((dataPoints.shape[0], 1)) # Creating a new row of zeroes, same size of rows as data point array. 
dataPoints = np.column_stack((dataPoints, zeroColumn)) # Adding the new zero column. Inspiration: https://medium.com/@heyamit10/numpy-add-column-guide-0427e394b333

# MAIN
# dataPoints = ReadDataPointsFromFile()
# PlotPoints(testPoints)
# testPoints = ReadDataPointsFromFile()
# testPoints = ReadDataPointsFromUser()
# FindClosestPoint(dataPoints, testPoints, nrOfVoters)


for i in testPoints:
    testWidth = i[1]
    testHeight = i[2]
    for j in dataPoints:
        dataWidth = j[0]
        dataHeight = j[1]
        j[3] = np.sqrt((testWidth - dataWidth)**2 + (testHeight - dataHeight)**2) # Storing distanse from test point to every datapoint in the new column  
    dataPoints = dataPoints[np.argsort(dataPoints[:,3])] # Sorting the dataPoints array based on the distance value in new column. Inspiration: https://stackoverflow.com/questions/22698687/how-to-sort-2d-array-numpy-ndarray-based-to-the-second-column-in-python
    print(f"Sample with (width, height): ({testWidth}, {testHeight}) classified as Pikachu") if dataPoints[0][2] == 1 else print(f"Sample with (width, height): ({testWidth}, {testHeight}) classified as Pichu")

