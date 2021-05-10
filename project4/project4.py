########################################################################################################
##       Project 4                                                                                 #####
##       CSCE 5320      : Computer Networks (Spring 2021 1)                                        #####
##       Author         : Mahima Sunmoriya                                                         ##### 
##       Date           : 04/22/2021                                                               #####
##       Description    : This is a OSPF link-state(LS) alogrithm. The nodes are identified by     #####
##                      : case charcter . The distance of graph are taken as input from cost matrix#####
##                      : text file. After that source node is taken as input from console and     #####
##                      : after that Dijkstra Algorithm is applied to that input filr to identify  #####
##                      : the shortest path for the graph                                          ##### 
########################################################################################################


#Importing all the required libraries


import csv
import sys
import os

#Global Variable declaration
global input_matrix


# Defining function to store distance

def set_distances(input_matrix):
    global distances
    global number_nodes

    distances = {}
    number_nodes = []

    num_number_nodes = len(input_matrix)

    for i in range(num_number_nodes):
        tempdict = {}
        for j in range(num_number_nodes):
            if i != j and input_matrix[i][j] != -1:
                tempdict[j + 1] = input_matrix[i][j]
        distances[i + 1] = tempdict
        number_nodes.append(i + 1)

# Defining function to implement Dijkstra's algorith
def dijkstra(initial):
    global distances
    global number_nodes
    global remaining
    global previous
    global completed
    global interface

#Initializing values
    remaining = {node: None for node in number_nodes}
    previous = {node: None for node in number_nodes}
    interface = {node: None for node in number_nodes}
    completed = {node: None for node in number_nodes}

    current = int(initial)
    currentDist = 0
    remaining[current] = currentDist

    while True:
        for next, distance in distances[current].items():

            if next not in remaining: continue

            newDist = currentDist + distance

            if not remaining[next] or remaining[next] > newDist:
                remaining[next] = newDist
                previous[next] = current

                if not interface[current]:
                    interface[next] = next
                else:
                    interface[next] = interface[current]

        completed[current] = currentDist
        del remaining[current]

        done = 1
        for x in remaining:
            if remaining[x]:
                done = 0
                break
        if not remaining or done:
            break

        elements = [node for node in remaining.items() if node[1]]

        current, currentDist = sorted(elements, key=lambda x: x[1])[0]


#Defining function to calculate the shortest path for the parent table from Dijkstra's function
def shortest_path(initial, end):
    global path

    path = []
    dest = int(end)
    src = int(initial)
    path.append(dest)

    while dest != src:
        path.append(previous[dest])
        dest = previous[dest]

    path.reverse()


#Starting point of the program

# Declaring all the variables 
input_matrix = []     #Variable to store Matrix from the input data file
mset = 0              #Variable to set starting of matrix
number_nodes = []     #Variable to store nodes
distances = {}        #Variable to store distance
remaining = {}        #Variable to store the remaining node
previous = {}         #Variable to hold the previous node
completed = {}        #Variable to store the visited nodes
interface = {}
path = []             #Variable to store the path
initial = 0
end = 0 


#Getting Input values from user

print("OSPF Link-State (LS) Routing:")
print('-----------------------------')
print('Enter the number of routers:')
num_router = input()
print('Enter filename with cost matrix values:')
filename = raw_input()


try:
    filedismat = open(filename,"r")
    input_matrix = [list(map(int, x.split(" "))) for x in filedismat]
    mset = 1
    set_distances(input_matrix)
    if num_router == len(input_matrix):

        if mset == 1:
       
            try:
                initial = raw_input("Enter the source router in Numeric value : ")
                if int(initial) > 0 and int(initial) <= len(input_matrix):
                    dijkstra(initial)
                else:
                    initial = 0
                    print("Source router is greater then Number of routers , Please try again with valid value")
                    sys.exit()
            except ValueError:
                print('please enter numeric value')
                sys.exit()
            

        #Calculation for the shortest path and cost 
        if mset == 1:
            end = 1
            while int(end) <= len(input_matrix):
                if 0 < int(end) <= len(input_matrix):
                        if int(initial) == int(end):
                                print("%s ==> %s :" %(initial,end))
                                print("path cost: 0")
                                print("path taken: %s" %(initial))
                        elif not previous[int(end)]:
                                print("There is no route from source : %s to give destination : %s. \nProvide some other destination " % (initial, end))
                        else:
                                shortest_path(initial, end)
                                print("%s ==> %s : " %(initial, end))
                                print ("path taken:") ,
                                for item in path:
                                        if item == path[len(path)-1] :
                                                print (str(item))
                                        else :
                                                print (str(item)+ "-->"),
                                        cost = 0
                                        if completed[int(end)]:
                                                cost = completed[int(end)]
                                print ("path cost : " + str(cost))
                end = end + 1
                pass
        else:
            print("error: unable to open file: notexist")
    else:
        print("error: upload correct matrix file of size :", num_router) 

except IOError as e:
    print(e)

