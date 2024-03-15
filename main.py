import datetime
import random
import copy
import sys
sys.setrecursionlimit(10000000)

class item():
    def __init__(self, weight, value, order):
        self.weight = weight
        self.value = value
        self.ratio = value/weight
        self.order = order

def createList(n, maxWeight, maxVal):
    l = [item(random.randint(1,maxWeight),random.randint(0,maxVal), x+1) for x in range(n)]
    return l

def fromfile(filename):
    arr = []
    with open(filename) as f:
        n, b = [int(x) for x in next(f).split()]
        for i in range(n):
            w, v = [int(x) for x in next(f).split()]
            arr.append(item(w, v, i+1))
    return b, arr

def Brute(capacity, arr):
    max_value = 0
    max_weight = 0
    out_items = []
    for i in range(2**len(arr)):
        items = []
        value, weight = 0, 0
        y = bin(i)[2::]
        x = (len(arr) - len(y)) * '0'
        x = x + y
        for j in range(len(x)):
            if x[j] == '1':
                items.append(arr[j].order)
                value += arr[j].value
                weight += arr[j].weight
        if weight <= capacity and value >= max_value:
            max_weight = weight
            max_value = value
            out_items = items.copy()
    return max_value, max_weight, out_items


def wypisz(i, w, mat, arr, items):
    if i == 0:
        return w
    if mat[i][w] > mat[i - 1][w]:
        items.append(i)
        return wypisz(i - 1, w - arr[i-1].weight, mat, arr, items)
    else:
        return wypisz(i - 1, w, mat, arr, items)
def Dynamic(capacity, arr):
    items = []
    mat = [[0 for x in range(capacity + 1)] for x in range(len(arr) + 1)]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if i == 0 or j == 0:
                mat[i][j] = 0
            elif arr[i-1].weight <= j:
                mat[i][j] = max(arr[i-1].value + mat[i-1][j-arr[i-1].weight], mat[i-1][j])
            else:
                mat[i][j] = mat[i-1][j]
    weight = capacity - wypisz(i, j, mat, arr, items)
    items.sort()
    return mat[-1][-1], weight, items

def Greedy(capacity, lista):
    value = 0
    weight = capacity
    items = []
    arr = copy.deepcopy(lista)
    arr.sort(key = lambda x:x.ratio)
    while len(arr)>0 and capacity > 0:
        if (capacity - arr[-1].weight) >= 0:
            value += arr[-1].value
            capacity -= arr[-1].weight
            items.append(arr[-1].order)
            arr.pop()
        else:
            arr.pop()
    weight = weight - capacity
    items.sort()
    return value, weight, items

def printElems(arr):
    file = open('przedmioty.txt', 'w')
    file.write("ID\twgh\tval\tratio\n")
    print("ID\twgh\tval\tratio")
    for i in arr:
        print(f"{i.order}\t{i.weight}\t{i.value}\t{i.ratio}")
        file.write(f"{i.order}\t{i.weight}\t{i.value}\t{i.ratio}\n")
    file.close()