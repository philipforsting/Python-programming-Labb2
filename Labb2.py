# Labb 2
# Specification : Syftet med den här laborationen är att använda verktygen du lärt dig i Python för att implementera en förenklad 
# maskininlärningsalgoritm. I den här laborationen finns (simulerad) data på Pichus och Pikachus längder och bredder. Du ska skapa 
# en algoritm som baserat på den givna datan kunna avgöra om en ny data punkt ska klassificeras som Pichu eller Pikachu.

# Grunduppgift: Läs in datan och spara i lämplig datastruktur
import matplotlib.pyplot as plt
import numpy as np


def ReadPointsFromFile(path, points, splitter):
    with open(path, "r") as f_read:      
        next(f_read)                                # Skip first row. Inspiration: https://stackoverflow.com/questions/4796764/read-file-from-line-2-or-skip-header-row
        for line in f_read:
            row = line.strip().split(splitter)                   
            for i in range(len(row)):
                row[i] = row[i].strip(".,()") 
            points.append([float(row[0]), float(row[1]), float(row[2])]) # converting elements in row to floats and adding them to list Inspiration: https://stackoverflow.com/questions/21238242/python-read-file-into-2d-list
    f_read.close()
    return np.array(points)               


def ReadPointFromUser(testPoints):              # OPTIMERA DETTA
    print("Enter a width and height of pokémon and program will classify it as Pikachu or Pichu")
    while True:
        try:
            width = float(input("Enter width of pokémon: "))
            if not 0 < width <= 1000:
                print("Pokémon width must be between 0 and 1000 cm")
                continue
        except ValueError:
            print("This is not a number")
            continue

        try:
            height = float(input("Enter height of pokémon: "))
            if not 0 < height <= 1000:
                print("Pokémon height must be between 0 and 1000 cm")
                continue
            testPoints.append([width, height])
            return np.array(testPoints)
        except ValueError:
            print("This is not a number")
            continue
    


def CalcDistAndClassify(testPoints, dataPoints, nrOfVoters):                # slå isär denna till CalcDist() och Classify()
    testPointsZeroColumn = np.zeros((testPoints.shape[0], 1))                   # Prepairing to store classification result: Creating a new column of zeroes, same size of rows as data point array. 
    testPoints = np.column_stack((testPoints, testPointsZeroColumn))              # Adding the new zero column to array d_Points
    for testRow in testPoints:
        vote_sum = 0
        d_zeroColumn = np.zeros((dataPoints.shape[0], 1))                   # Prepairing to store classification result: Creating a new column of zeroes, same size of rows as data point array. 
        dataPoints = np.column_stack((dataPoints, d_zeroColumn))              # Adding the new zero column to array d_Points Inspiration: https://medium.com/@heyamit10/numpy-add-column-guide-0427e394b333
        testWidth = testRow[0]
        testHeight = testRow[1]
        for dataRow in dataPoints:
            dataWidth = dataRow[0]
            dataHeight = dataRow[1]
            dataRow[-1] = np.sqrt((testWidth - dataWidth)**2 + (testHeight - dataHeight)**2)   # Storing distanse from test point to every datapoint in the new column  
        dataPoints = dataPoints[np.argsort(dataPoints[:,-1])]                          # Sorting the d_Points array based on the distance value in new column. Inspiration: https://stackoverflow.com/questions/22698687/how-to-sort-2d-array-numpy-ndarray-based-to-the-second-column-in-python
        for voter in range(nrOfVoters):
            vote_sum += dataPoints[voter][2] 
        if vote_sum == nrOfVoters/2.0:                                      # if voting result is a tie, radomize a class
            vote_sum = np.random.randint(nrOfVoters)
            print(f"Vote for sample with (width, height): ({testWidth}, {testHeight}) resulted in tie. Class has been randomized.")
        if vote_sum >= nrOfVoters/2.0:
            print(f"Sample with (width, height): ({testWidth}, {testHeight}) classified as Pikachu")
            testRow[2] = 1
        else:
            print(f"Sample with (width, height): ({testWidth}, {testHeight}) classified as Pichu")
            testRow[2] = 0
 

#testPoints_x = [line[1] for line in testPoints] 
#testPoints_y = [line[2] for line in testPoints] 
#plt.scatter(testPoints_x,testPoints_y) 
#plt.show()

# Grunduppgift: Beräkna avstånd mellamn testpunkt och träningspunkter

# Preparing to store distance between testpoint and datapoints in additinoal column

# MAIN

dataPoints = []     
testPoints = []
nrOfVoters = 10
readTestPointsFromUser = True
path_dataPoints = "../Python-programming-Labb2/datapoints.txt"
path_testpoints = "../Python-programming-Labb2/testpoints.txt"

dataPoints = ReadPointsFromFile(path_dataPoints, dataPoints, ",")   # After call, array dataPoints contains 3 columns ["width", "height", "isPikachu"]
plt.scatter(dataPoints[:,0],dataPoints[:,1], c=dataPoints[:,2])     # colouring condition inspiration taken from: https://www.tutorialspoint.com/scatter-a-2d-numpy-array-in-matplotlib
plt.legend(("Pichu", "Pikachu"))                                    # only "Pichu" is visible in legend. Are two scatters (for each class) needed?
#plt.show()

if readTestPointsFromUser:
    testPoints = ReadPointFromUser(testPoints)                      # Se om denna kan optimeras
else:
    testPoints = ReadPointsFromFile(path_testpoints, testPoints, " ")   # After call, array testPoints contains 3 columns ["index" , "width", "height"]
    testPoints = np.delete(testPoints, 0, 1)                            # Deleting index column from testPoint after reading from file. Arrays dataPoints and testPoints now both contain width and height in the first two columns. Inspiration:  https://stackoverflow.com/questions/64180609/delete-both-row-and-column-in-numpy-array
CalcDistAndClassify(testPoints, dataPoints, nrOfVoters)             # After call, 

       

