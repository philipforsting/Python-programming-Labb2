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
    

def ClassifyTestPoints(testRow, dataPoints, nrOfVoters):
    vote_sum = 0
    for voter in range(nrOfVoters):
        vote_sum += dataPoints[voter][2] 
    if vote_sum == nrOfVoters/2.0:                                      # if voting result is a tie, radomize a class
        vote_sum = np.random.randint(nrOfVoters)
        print(f"Vote for sample with (width, height): ({testRow[0]}, {testRow[1]}) resulted in tie. Class has been randomized.")
    if vote_sum >= nrOfVoters/2.0:
        print(f"Sample with (width, height): ({testRow[0]}, {testRow[1]}) classified as Pikachu")
        return 1
    else:
        print(f"Sample with (width, height): ({testRow[0]}, {testRow[1]}) classified as Pichu")
        return 0


def CalcDistAndClassify(testPoints, dataPoints, nrOfVoters):                # slå isär denna till CalcDist() och Classify()
    testPointsZeroColumn = np.zeros((testPoints.shape[0], 1))                   # Prepairing to store classification result: Creating a new column of zeroes, same size of rows as data point array. 
    testPoints = np.column_stack((testPoints, testPointsZeroColumn))              # Adding the new zero column to array d_Points
    for testRow in testPoints:
        d_zeroColumn = np.zeros((dataPoints.shape[0], 1))                   # Prepairing to store classification result: Creating a new column of zeroes, same size of rows as data point array. 
        dataPoints = np.column_stack((dataPoints, d_zeroColumn))              # Adding the new zero column to array d_Points Inspiration: https://medium.com/@heyamit10/numpy-add-column-guide-0427e394b333
        for dataRow in dataPoints:
            dataRow[-1] = np.sqrt((testRow[0] - dataRow[0])**2 + (testRow[1] - dataRow[1])**2)   # Storing distanse from test point to every datapoint in the new column  
        dataPoints = dataPoints[np.argsort(dataPoints[:,-1])]                          # Sorting the d_Points array based on the distance value in new column. Inspiration: https://stackoverflow.com/questions/22698687/how-to-sort-2d-array-numpy-ndarray-based-to-the-second-column-in-python
        testRow[2] = ClassifyTestPoints(testRow, dataPoints, nrOfVoters)
    print(dataPoints[:, 2:7])
    print(testPoints)           # FELSÖK

def SplitPointsFromFile(allPoints):
    # Shuffling Pichu and Pikachu separately to ensure that the returning arrays have the same amount of each class
    allPoints = allPoints[np.argsort(allPoints[:,2])]
    allPichuPoints = allPoints[0:75, :]
    allPikachuPoints = allPoints[75:150, :]
    np.random.shuffle(allPichuPoints)               
    np.random.shuffle(allPikachuPoints)
    shuffledDataPoints = np.concatenate((allPichuPoints[0:50,:], allPikachuPoints[0:50,:]), axis=0)   # 100 data points(50 Pichu, 50 Pikachu)
    shuffledTestPoints = np.concatenate((allPichuPoints[50:75,:], allPikachuPoints[50:75,:]), axis=0)  # 50 data points(25 Pichu, 25 Pikachu)
    return shuffledDataPoints, shuffledTestPoints

def Accuracy(testPoints, dataPoints):
    print(testPoints)
    TP = np.sum(testPoints[0:25,2] == 0)  # Found Pichus
    TN = np.sum(testPoints[25:50,2] == 1) # Found Pikachus
    FP = np.sum(testPoints[0:25,2] == 1)  # Classified Pichu was actually Pikachu
    FN = np.sum(testPoints[25:50,2] == 0) # Classified Pikachu was actually Pichu
    print(f"TP: {TP}")
    print(f"TN: {TN}")
    print(f"FP: {FP}")
    print(f"FN: {FN}")
    acc = (TP+TN) / (TP+TN+FP+FN)
    print(f"acc: {acc}")

# Grunduppgift: Beräkna avstånd mellamn testpunkt och träningspunkter

# Preparing to store distance between testpoint and datapoints in additinoal column

# MAIN

dataPoints = []     
testPoints = []
nrOfVoters = 10
readTestPointsFromUser = False
executeBonusAssignments = False
path_dataPoints = "../Python-programming-Labb2/datapoints.txt"
path_testpoints = "../Python-programming-Labb2/testpoints.txt"

dataPoints = ReadPointsFromFile(path_dataPoints, dataPoints, ",")   # After call, array dataPoints contains 3 columns ["width", "height", "isPikachu"]
if executeBonusAssignments:
    dataPoints, testPoints = SplitPointsFromFile(dataPoints)
elif readTestPointsFromUser:
    testPoints = ReadPointFromUser(testPoints)                      # Se om denna kan optimeras
else:
    testPoints = ReadPointsFromFile(path_testpoints, testPoints, " ")   # After call, array testPoints contains 3 columns ["index" , "width", "height"]
    testPoints = np.delete(testPoints, 0, 1)                            # Deleting index column from testPoint after reading from file. Arrays dataPoints and testPoints now both contain width and height in the first two columns. Inspiration:  https://stackoverflow.com/questions/64180609/delete-both-row-and-column-in-numpy-array
plt.scatter(dataPoints[:,0],dataPoints[:,1], c=dataPoints[:,2])     
plt.legend(("Pichu", "Pikachu"))                                    # only "Pichu" is visible in legend. Are two scatters (one for each class) needed?
plt.show()

CalcDistAndClassify(testPoints, dataPoints, nrOfVoters)             # After call, 
if executeBonusAssignments:
    Accuracy(testPoints, dataPoints)
       

