import time

class Item:
    def __init__(self,weight,value):
        self.value=value
        self.weight=weight

def knapsack_bruteforce(MyItems, index, capacity, cap, selected_items=None):
    if selected_items is None:
        selected_items = []
    
    if index == -1 or capacity == 0:
        # Zwracamy wartość i listę wybranych przedmiotów
        return (0, selected_items)
    
    if MyItems[index].weight > capacity:
        return knapsack_bruteforce(MyItems, index-1, capacity, cap, selected_items)
    else:
        # Tworzymy kopię listy wybranych przedmiotów dla gałęzi 'includes'
        new_selected = selected_items.copy()
        new_selected.append(MyItems[index])
        
        # Obliczamy wartość i listę przedmiotów, jeśli bierzemy aktualny przedmiot
        includes_value, includes_items = knapsack_bruteforce(
            MyItems, index-1, capacity - MyItems[index].weight, cap, new_selected
        )
        includes_value += MyItems[index].value
        
        # Obliczamy wartość i listę przedmiotów, jeśli pomijamy aktualny przedmiot
        excludes_value, excludes_items = knapsack_bruteforce(
            MyItems, index-1, capacity, cap, selected_items
        )
        
        # Wybieramy lepszą opcję (większą wartość)
        if includes_value > excludes_value:
            return (includes_value, includes_items)
        else:
            return (excludes_value, excludes_items)


##zachłanny
def sort_items_by_value_per_weight(MyItems):
    MyItems.sort(key=lambda item: item.value / item.weight, reverse=True)

def knapsack_greedy(MyItems,capacity,elements):
    sort_items_by_value_per_weight(MyItems)
    i=0
    actual=capacity
    endvalue=0
    while actual>0 and i<elements:
     ##   print(i , actual, capacity, elements)
        if MyItems[i].weight<=actual:
            print(f"Masa przedmiotu: {MyItems[i].weight}, wartosc przedmiotu {MyItems[i].value}")
            endvalue+=MyItems[i].value
            actual-=MyItems[i].weight
        i+=1
    print(f"Masa plecaka: {capacity-actual}")
    print(f"Maksymalna wartość: {endvalue}")


##dynamiczny
def sort_items_per_weight(MyItems):
    MyItems.sort(key=lambda item: item.weight, reverse=False)

def knapsack_dynamic2(MyItems, capacity, elements, printingFlag):
    sort_items_by_value_per_weight(MyItems) 
    allTablesTogether = []
    previousTable = [0 for _ in range(capacity + 1)]
    
    for i in range(elements):
        actualTable = [0 for _ in range(capacity + 1)] 
        
        for j in range(capacity + 1):
            back = j - MyItems[i].weight
            if back >= 0:
                newvalue = MyItems[i].value + previousTable[back]
                actualTable[j] = max(previousTable[j], newvalue)
            else:
                actualTable[j] = previousTable[j]

     ##   print(f"Previous: {previousTable}")
     ##   print(f"Actual:   {actualTable}")
        
        allTablesTogether.append(previousTable.copy()) 
        previousTable = actualTable.copy() 

    allTablesTogether.append(previousTable.copy())
    
    def findIncludedElements(TogetherTable):
        x=capacity
        y=elements
        weight=0
        while(TogetherTable[y][x]!=0):
            ##print(f"{x}, {y}, {weight}")   
            if(TogetherTable[y][x]!=TogetherTable[y-1][x]):
                print(f"Przedmiot o masie {MyItems[y-1].weight} i wartosci {MyItems[y-1].value}" )
                weight+=MyItems[y-1].weight
                x-=MyItems[y-1].weight 
            y-=1
            
        print(f"Masa plecaka to: {weight}")
        return previousTable[capacity]
    def printTable(Tab):
        for i in Tab:
            print(i)
    if printingFlag:
        print(f"Final table: \n")
        printTable(allTablesTogether)
        findIncludedElements(allTablesTogether)
    return previousTable[capacity]


 ##tworzenie tablicy elementów
def from_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines
def check(val1, val2):
    return val1>0 and val2>0

def createTable(lines):
    MyItems=[]
    elements,capacity=map(int,lines[0].split())
    if not check(elements,capacity):
        return -1
    for i in range(1,elements+1):
        a,b=map(int,lines[i].split())
        if not check(a,b):
            return -1
        c=Item(int(a),int(b))
        MyItems.append(c)
    return [elements,capacity,MyItems]





print("1) wpisz z pliku\n")
print("2) z klawiatury\n")
format = int(input())

MyItems=[]
if format == 1:
    file = input("wczytaj graf z pliku: ")
    dataFromFile = from_file(file)
    [elements,capacity,MyItems]= createTable(dataFromFile)
  
elif format == 2:
    [elements,capacity]= input().split()
    elements=int(elements)
    capacity=int(capacity)
    if not check(elements,capacity):
        print("Niepoprawna wartosc")
        exit
    for i in range(elements):
        [weight,value]=input().split()
        if not check(weight,value):
            print("Niepoprawna wartosc")
            exit
        a=Item(int(weight),int(value))
        MyItems.append(a)

print("wybór algorytmu:\n")
print("1) bruteforce\n")
print("2) greedy\n")
print("3) dynamic\n")
alg = int(input())
if alg == 1:
    start = time.time()
    value, selected_elements = knapsack_bruteforce(MyItems,elements-1,capacity,capacity)
    end = time.time()
    sumWeight=0
    for i in selected_elements:
        sumWeight+=i.weight
        print(f"Masa przedmiotu {i.weight}, wartosc {i.value}")
    print("Masa plecaka: ", sumWeight)
    print("Wartosc plecaka: ", value)
if alg == 2:
    start = time.time()
    value=knapsack_greedy(MyItems,capacity,elements)
    end = time.time()
    optimalresult=knapsack_dynamic2(MyItems,capacity,elements,0)
    if optimalresult==value:
        print("Wynik zgodny z optymalnym")
    else:
        print("Wynik niezgodny z optymalnym")
if alg == 3:
    start = time.time()
    value=knapsack_dynamic2(MyItems,capacity,elements,1)
    print("Wartosc plecaka: ",value)
    end = time.time()

print(f"Czas wykonania algorytmu: {start-end}")
