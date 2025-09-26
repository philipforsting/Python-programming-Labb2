# Labb 2
# Specification : Syftet med den här laborationen är att använda verktygen du lärt dig i Python för att implementera en förenklad 
# maskininlärningsalgoritm. I den här laborationen finns (simulerad) data på Pichus och Pikachus längder och bredder. Du ska skapa 
# en algoritm som baserat på den givna datan kunna avgöra om en ny data punkt ska klassificeras som Pichu eller Pikachu.

import matplotlib.pyplot as plt
import numpy as np


def ReadPointsFromFile(path, splitter): 
    """Opens text file content specified from input path, cleans content and add cleaned content to array which is returned"""
    pointsFromFile = []
    with open(path, "r") as f_read:      
        next(f_read)                                
        for line in f_read:
            row = line.strip().split(splitter)                   
            for i in range(len(row)):
                row[i] = row[i].strip(".,()") 
            pointsFromFile.append([float(row[0]), float(row[1]), float(row[2])]) 
    f_read.close()
    return np.array(pointsFromFile)               


def ReadPointFromUser():              
    """Allows user to enter a manual test point. Only positive numbers are accepted"""
    print("Enter a width and height of pokémon and program will classify it as Pikachu or Pichu")
    pointFromUser = []
    while True:
        try:
            width = float(input("Enter width of pokémon: "))
            if not 0 < width:
                print("Pokémon width must be between lanrger than 0")
                continue
        except ValueError:
            print("This is not a number")
            continue

        try:
            height = float(input("Enter height of pokémon: "))
            if not 0 < height:
                print("Pokémon height must be larger than 0")
                continue
            pointFromUser.append([width, height])
            return np.array(pointFromUser)
        except ValueError:
            print("This is not a number")
            continue
    

def PredictClassification(testRow, dataPoints, nrOfVoters):
    """The data points nearest the test point (specified by nrOfVoters) will be sumarized. Predicted classification of test point will be determended by the winner of the poll"""
    vote_sum = 0
    for voter in range(nrOfVoters):
        vote_sum += dataPoints[voter][2]            # 0 = Pichu, 1 = Pikachu
    if vote_sum == nrOfVoters/2.0:                                     
        vote_sum = np.random.randint(nrOfVoters)    # if voting result is a tie, radomize a class
    if vote_sum >= nrOfVoters/2.0:
        return 1
    else:
        return 0


def CalcDistAndClassify(testPoints, dataPoints, nrOfVoters):
    """Distance to testpoints will be calculated for every test point. Prediction will be added into a new column in array testPoints"""               
    testPointsZeroColumn = np.zeros((testPoints.shape[0], 1))           # Prepairing to store classification result in testPionts array
    testPoints = np.column_stack((testPoints, testPointsZeroColumn))              
    for testRow in testPoints:
        dataPointZeroColumn = np.zeros((dataPoints.shape[0], 1))        # Prepairing to store distance to testpoint for each datapoint in dataPoint array
        dataPoints = np.column_stack((dataPoints, dataPointZeroColumn))              
        for dataRow in dataPoints:
            dataRow[-1] = np.sqrt((testRow[0] - dataRow[0])**2 + (testRow[1] - dataRow[1])**2)   # Storing distanse from test point to every datapoint in the new column  
        dataPoints = dataPoints[np.argsort(dataPoints[:,-1])]           # Sorting the dataPoints array based on the distance value in new column. Datapoint closest to testpoint will be at row 0
        testRow[-1] = PredictClassification(testRow, dataPoints, nrOfVoters)
    return testPoints

def SplitPointsFromFile(allPoints):
    """Splitting and shuffling points based on their classification"""
    allPoints = allPoints[np.argsort(allPoints[:,2])]
    allPichuPoints = allPoints[0:75, :]
    allPikachuPoints = allPoints[75:150, :]
    np.random.shuffle(allPichuPoints)               
    np.random.shuffle(allPikachuPoints)
    shuffledDataPoints = np.concatenate((allPichuPoints[0:50,:], allPikachuPoints[0:50,:]), axis=0)   # 100 data points(50 Pichu, 50 Pikachu)
    shuffledTestPoints = np.concatenate((allPichuPoints[50:75,:], allPikachuPoints[50:75,:]), axis=0)  # 50 data points(25 Pichu, 25 Pikachu)
    return shuffledDataPoints, shuffledTestPoints

def Accuracy(testPoints):
    """Calculate the accuracy of this simple Machine Learning algorithm"""
    TP = np.sum(testPoints[0:25,-1] == 0)  # Found Pichus
    TN = np.sum(testPoints[25:50,-1] == 1) # Found Pikachus
    FP = np.sum(testPoints[0:25,-1] == 1)  # Classified Pichu was actually Pikachu
    FN = np.sum(testPoints[25:50,-1] == 0) # Classified Pikachu was actually Pichu
    return (TP+TN) / (TP+TN+FP+FN)

# MAIN
def main():
    """Simple Machine Learning algorithm that uses data of simulated size measures of Pichus and Pikachus to predict how new test points shall be classified. 
    Some funcion calls can be enabled/disabled or repeted by changing value of flags readTestPointsFromUser and executeBonusAssignments"""
    dataPoints = []     
    testPoints = []
    nrOfVoters = 10
    n = 0
    acc = np.empty(0)  
    readTestPointsFromUser = False
    executeBonusAssignments = True
    path_dataPoints = "../Python-programming-Labb2/datapoints.txt"
    path_testpoints = "../Python-programming-Labb2/testpoints.txt"

    dataPoints_org = ReadPointsFromFile(path_dataPoints, ",")               # After call, array dataPoints contains 3 columns ["width", "height", "isPikachu"]
    while (executeBonusAssignments and n<10) or n<1:                       # Repeat Bonus assignments 10 times if they are enabled
        dataPoints = dataPoints_org
        if executeBonusAssignments:
            dataPoints, testPoints = SplitPointsFromFile(dataPoints_org)
        elif readTestPointsFromUser:
            testPoints = ReadPointFromUser()                                # Se om denna kan optimeras
        else:
            testPoints = ReadPointsFromFile(path_testpoints, " ")           # After call, array testPoints contains 3 columns ["index" , "width", "height"]
            testPoints = np.delete(testPoints, 0, 1)                         # Deleting index column from testPoint after reading from file. 
    
        testPoints = CalcDistAndClassify(testPoints, dataPoints, nrOfVoters)    
        if executeBonusAssignments:
            acc = np.append(acc, [Accuracy(testPoints)])
        n += 1
    if executeBonusAssignments:
        plt.figure(figsize=(16,16), dpi=100)
        plt.subplot(1,2,2)
        plt.scatter(range(n), acc)
        plt.plot(range(n), [np.mean(acc) for n in range(n)], c='r')
        plt.title("Accuracy per iteration")
        plt.legend(("Accuracy per iteration", "Mean accuracy"))
        plt.subplot(1,2,1)

    plt.scatter(dataPoints[:,0], dataPoints[:,1], c=dataPoints[:,2] )     
    plt.scatter(testPoints[:,0], testPoints[:,1], marker="x", label="Testpunkter")
    plt.legend(("Pichu", "Pikachu"))                                    # only "Pichu" is visible in legend. Are two scatters (separated for each class) needed?
    plt.show()
        
if __name__ == "__main__":   # The following rows have been copied from https://realpython.com/python-main-function/
    main()
