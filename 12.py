#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:17:55 2018

@author: michael
"""

# 12 | Knapsack and Graph Optimization Problems

# In general Optimization problems have two parts: 
#    1. An objective function that is to be maximized or minimized
#    2. A set of constraints that must be honored 

#%% 12.1 Knapsack Problems

class Item(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.weight = w
    def getName(self):
        return self.name
    def getValue(self):
        return self.value
    def getWeight(self):
        return self.weight
    def __str__(self):
        result = '<' + self.name + ', ' + str(self.value) + ', ' + str(self.weight) + '>'
        return result 

def value(item):
    return item.getValue()
def weightInverse(item):
    return 1.0 / item.getWeight()
def density(item):
    return item.getValue() / item.getWeight()

def greedy(items, maxWeight, keyFunction):
    '''
    Assumes items is a list, maxweight >= 0
    keyFunction maps elements of items to numbers
    '''
    itemsCopy = sorted(items, key = keyFunction, reverse = True)
    result = []
    totalValue, totalWeight = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalWeight + itemsCopy[i].getWeight()) <= maxWeight:
            result.append(itemsCopy[i])
            totalWeight += itemsCopy[i].getWeight()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

#%% 
def buildItems():
    names = ['clock', 'painting', 'radio', 'vase', 'book', 'computer']
    values = [175, 90, 20, 50, 10, 200]
    weights = [10, 9, 4, 2, 1, 20]
    Items = []
    for i in range(len(values)):
        Items.append(Item(names[i], values[i], weights[i]))
    return Items

def testGreedy(items, maxWeight, keyFunction):
    taken, val = greedy(items, maxWeight, keyFunction)
    print('Total value of items taken is', val)
    for item in taken:
        print('  ', item)

def testGreedys(maxWeight = 20):
    items = buildItems()
    print('Use greedy by value to fill knapsack of size', maxWeight)
    testGreedy(items, maxWeight, value)
    print('\nUse greedy by weight to fill knapsack of size', maxWeight)
    testGreedy(items, maxWeight, weightInverse)
    print('\nUse greedy by density to fill knapsack of size', maxWeight)
    testGreedy(items, maxWeight, density)
    
testGreedys()

#%% 12.1.2 | An Optimal Solution for the 0/1 Knapsack Problem

#1. Enumerate all possible combinations of items
#2. Remove those that exceed the weight
#3. From the remaining, choose highest value 

def getBinaryRep(n, numDigits):
    '''
    Assumes n and numDigits are non negative ints
    Returns a str of length numDigits that is a binary representation of n
    '''
    result = ''
    while n > 0:
        result = str(n%2) + result
        n = n//2
    if len(result) > numDigits:
        raise ValueError('not enough digits')
    for i in range(numDigits - len(result)):
        result = '0' + result
    return result

def getPowerset(L):
    '''
    Assumes L is a list. Returns a list of lists that contains all possible combinations of the elements of L
    '''
    powerset = []
    for i in range(0, 2**len(L)):
        binStr = getBinaryRep(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
    return powerset 

getPowerset([1,2,3])

def chooseBest(pset, maxWeight, getVal, getWeight):
    bestVal = 0.0
    bestSet = None
    for items in pset:
        itemsVal = 0.0
        itemsWeight = 0.0
        for item in items:
            itemsVal += getVal(item)
            itemsWeight += getWeight(item)
        if itemsWeight <= maxWeight and itemsVal > bestVal:
            bestVal = itemsVal
            bestSet = items
    return (bestSet, bestVal)

def testBest(maxWeight = 20):
    items = buildItems()
    pset = getPowerset(items)
    taken, val = chooseBest(pset, maxWeight, Item.getValue, Item.getWeight)
    print('Total value of items taken is', val)
    for item in taken:
        print(item)
        
testBest()

#%% 12.2 Graph Optimization Problems

class Node(object):
    def __init__(self, name):
        '''
        Assumes name is a string
        '''
        self.name = name
        
    def getName(self):
        return self.name
    
    def __str__(self):
        return self.name 
    
class Edge(object):
    
    def __init__(self, src, dest):
        '''
        Assumes src and dest are nodes
        '''
        self.src = src
        self.dest = dest
    
    def getSource(self):
        return self.src
    
    def getDestination(self):
        return self.dest
    
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()
    
class WeightedEdge(Edge):
    
    def __init__(self, src, dest, weight = 1.0):
        '''
        Assumes src and dest are nodes, weight a number
        '''
        self.src = src
        self.dest = dest
        self.weight = weight
    
    def getWeight(self):
        return self.weight
    
    def __str__(self):
        return self.src.getName() + '->(' + str(self.weight) + ')' + self.dest.getName()
    
class Digraph(object):
    # nodes is a list of the nodes in the graph
    # edges is a dict mapping each node to a list of its children
    
    def __init__(self):
        self.nodes = []
        self.edges = {}
    
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate Node')
        else: 
            self.nodes.append(node)
            self.edges[node] = []
    
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    
    def childrenOf(self, node):
        return self.edges[node]
    
    def hasNode(self, node):
        return node in self.nodes
    
    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.getName() + '->' + dest.getName() + '\n'
        return result[:-1] # omit final newline
    
class Graph(Digraph):
    
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination, edge.getSource())
        Digraph.addEdge(self, rev)

#%% Shortest Path: Depth-First Search and Breadth-First Search

def printPath(path):
    '''
    Assumes path is a list of nodes
    '''
    result = ''
    for i in range(len(path)):
        result += str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result 

def DFS(graph, start, end, path, shortest, toPrint = False):
    '''
    Assumes graph is a Digraph; start and end are nodes; path and shortest are a list of nodes
    Returns a shortest path from start to end in graph
    '''
    path = path + [start]
    if toPrint:
        print('Current DFS path: ', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: # avoid cycles
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path, shortest, toPrint)
                if newPath != None:
                    shortest = newPath
    return shortest

def shortestPath(graph, start, end, toPrint = False):
    '''
    Assumes graph is a digraph; start and end are nodes
    Returns a shortest path from start to end in a graph
    '''
    return DFS(graph, start, end, [], None, toPrint)

def testSP():
    nodes = []
    for name in range(6): # create 6 nodes
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes: 
        g.addNode(n)
    g.addEdge(Edge(nodes[0], nodes[1]))
    g.addEdge(Edge(nodes[1], nodes[2]))
    g.addEdge(Edge(nodes[2], nodes[3]))
    g.addEdge(Edge(nodes[2], nodes[4]))
    g.addEdge(Edge(nodes[3], nodes[4]))
    g.addEdge(Edge(nodes[3], nodes[5]))
    g.addEdge(Edge(nodes[0], nodes[2]))
    g.addEdge(Edge(nodes[1], nodes[0]))
    g.addEdge(Edge(nodes[3], nodes[1]))
    g.addEdge(Edge(nodes[4], nodes[0]))
    sp = shortestPath(g, nodes[0], nodes[5], toPrint = True)
    print('Shortest path is', printPath(sp))
    sp = BFS(g, nodes[0], nodes[5])
    print('Shortest path found by BFS: ', printPath(sp))
    
#%%

testSP()
    
#%% 

def BFS(graph, start, end, toPrint =  False):
    '''
    Assumes graph is a digraph; start and end are nodes
    returns a shortest path from start to end in graph
    '''
    initPath = [start]
    pathQueue = [initPath]
    if toPrint: 
        print('Current BFS path: ', printPath(pathQueue))
    while len(pathQueue) != 0:
        # Get and remove oldest element in the queue
        tmpPath = pathQueue.pop(0)
        print('Current BFS path: ', printPath(tmpPath))
        lastNode = tmpPath[-1]
        if lastNode == end: 
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None

#%% finger exercise

# No. Imagine a digraph in which there are 2 parent nodes with the same child node which happens to be our target.
# Then BFS will select the leftmost edge directing itself to our target node, which is not guaranteed to be the minimum
# of the two edges which connect to our target. Thus, we would have two different paths to our target node, and the leftmost
# is not guaranteed to have the minimum sum. 

