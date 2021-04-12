# Them cac thu vien neu can
import numpy as np
from copy import deepcopy
from math import sqrt, exp

#MSSV: 1813897
#Pham Nguyen Anh Tai

def calFunc(result, listOrder, listWage, numShipper, wareCoord):
    minimize = 0.0
    listProfit = []
    for x in result:
        currentCoord = deepcopy(wareCoord)
        sumWage = 0
        sumExpenses = 10.0
        for y in x:
            sumWage += listWage[y]
            sumExpenses += sqrt((listOrder[y][0]-currentCoord[0])**2 + (listOrder[y][1]-currentCoord[1])**2) / 2
            currentCoord = deepcopy([listOrder[y][0], listOrder[y][1]])
        listProfit.append(sumWage - sumExpenses)
    for i in range(numShipper):
        k = 0.0
        for j in range(numShipper):
            k += abs(listProfit[i] - listProfit[j])
        minimize += k
    return minimize

    
def changeState(currentState):
    current = deepcopy(currentState)
    while True:
        i = np.random.randint(0,len(current))
        k = np.random.randint(0,len(current[i]))
        m = np.random.randint(0,len(current))
        n = np.random.randint(0,len(current[m]))
        if i!=m or k!=n:
            current[i][k], current[m][n] = current[m][n], current[i][k]
            return current


def assign(file_input, file_output):

    listOrder = []
    f = open(file_input, 'r')
    buffer = f.readline()
    temp = buffer.split(' ')
    wareCoord = [int(temp[0]),int(temp[1])]
    buffer = f.readline()
    temp = buffer.split(' ')
    numOrder = int(temp[0])
    numShipper = int(temp[1])
    for i in range(numOrder):
        buffer = f.readline()

        temp = buffer.split(' ')
        listOrder.append([int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3])])
    f.close()


    listWage = []
    for x in listOrder:
        listWage.append(5 + x[2] + x[3]*2)
    # run algorithm
    #init state
    result = []
    result1 = []
    result2 = []
    result3 = []
    temp = list(x for x in range(numOrder))
    np.random.shuffle(temp)
    tempo = np.array_split(temp, numShipper)
    for x in tempo:
        result1.append(deepcopy(list(x)))
    currentState = deepcopy(result1)

    temp = list(x for x in range(numOrder))
    np.random.shuffle(temp)
    tempo = np.array_split(temp, numShipper)
    for x in tempo:
        result2.append(deepcopy(list(x)))
    currentState2 = deepcopy(result2)

    temp = list(x for x in range(numOrder))
    np.random.shuffle(temp)
    tempo = np.array_split(temp, numShipper)
    for x in tempo:
        result3.append(deepcopy(list(x)))
    currentState3 = deepcopy(result3)


    if calFunc(result1, listOrder, listWage, numShipper, wareCoord) < calFunc(result2, listOrder, listWage, numShipper, wareCoord) and\
    calFunc(result1, listOrder, listWage, numShipper, wareCoord) < calFunc(result3, listOrder, listWage, numShipper, wareCoord):
        result = deepcopy(result1)
    elif calFunc(result2, listOrder, listWage, numShipper, wareCoord) < calFunc(result3, listOrder, listWage, numShipper, wareCoord):
        result = deepcopy(result2)
    else:
        result = deepcopy(result3)
    goal = calFunc(result, listOrder, listWage, numShipper, wareCoord)

    loop = 0
    t = 5000.0
    while loop < 100*numOrder:
        t *= 0.99
        loop += 1
        newState = changeState(currentState)
        newState2 = changeState(currentState2)
        newState3 = changeState(currentState3)
        

        cal1 = calFunc(newState, listOrder, listWage, numShipper, wareCoord)
        deltaE = cal1 - calFunc(currentState, listOrder, listWage, numShipper, wareCoord)
        if cal1 < goal:
            goal = cal1
            result = deepcopy(newState)
            currentState = deepcopy(newState)
        elif deltaE<0 or np.random.rand()<exp(-deltaE/t):
            currentState = deepcopy(newState)
       
        cal2 = calFunc(newState2, listOrder, listWage, numShipper, wareCoord)
        deltaE2 = cal2 - calFunc(currentState2, listOrder, listWage, numShipper, wareCoord)
        if cal2 < goal:
            goal = cal2
            result = deepcopy(newState2)
            currentState2 = deepcopy(newState2)
        elif deltaE2<0 or np.random.rand()<exp(-deltaE2/t):
            currentState2 = deepcopy(newState2)

        cal3 = calFunc(newState3, listOrder, listWage, numShipper, wareCoord)
        deltaE3 = cal3 - calFunc(currentState3, listOrder, listWage, numShipper, wareCoord)
        if cal3 < goal:
            goal = cal3
            result = deepcopy(newState3)
            currentState3 = deepcopy(newState3)
        elif deltaE3<0 or np.random.rand()<exp(-deltaE3/t):
            currentState3 = deepcopy(newState3)
        
        

    # write output
    fw = open(file_output, 'w')
    for i in range(len(result)):
        for j in range(len(result[i])):
            fw.write(str(result[i][j]))
            if j != len(result[i]) - 1 :
                fw.write(' ')
        if i != len(result) - 1:
            fw.write('\n')
    

    fw.close()

    return


assign('input.txt', 'output.txt')
