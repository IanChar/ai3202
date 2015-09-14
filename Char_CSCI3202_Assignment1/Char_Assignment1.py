# Ian Char
# Intro to AI

# 1. Queue
from Queue import Queue as BuiltInQueue
class Queue(object):
    def __init__(self):
        self.builtInQueue = BuiltInQueue()

    def enqueue(self, someInteger):
        if isinstance(someInteger, int):
            self.builtInQueue.put(someInteger)
        else:
            raise TypeError("This queue only accepts integers.")

    def dequeue(self):
        if self.builtInQueue.qsize() == 0:
            raise IndexError("Pop from empty queue.")
        return self.builtInQueue.get()

    def isEmpty(self):
        return self.builtInQueue.empty()

    def size(self):
        return self.builtInQueue.qsize()

# 2. Stack
class Stack(object):
    def __init__(self):
        self.list = []

    def push(self, someInteger):
        if isinstance(someInteger, int):
            self.list.append(someInteger)
        else:
            raise TypeError("This stack only accepts integers.")

    def pop(self):
        if len(self.list) == 0:
            raise IndexError("Pop from empty stack.")
        return self.list.pop()

    def checkSize(self):
        return len(self.list)

# 3. Binary Tree
class Node(object):
    def __init__(self, key, parent = None, leftChild = None, rightChild = None):
        if not isinstance(key, int):
            raise TypeError("Nodes can only have integers for keys.")
        self.key = key
        self.parent = parent
        self.leftChild = leftChild
        self.rightChild = rightChild

    def getKey(self):
        return self.key

    def getParent(self):
        return self.parent

    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    def setKey(self, someInteger):
        if isinstance(someInteger, int):
            self.key = someInteger
        else:
            raise TypeError("Nodes can only have integers for keys.")

    def setParent(self, parentNode):
        if isinstance(parentNode, Node) or parentNode is None:
            self.parent = parentNode
        else:
            raise TypeError("Parent must be of type Node or None.")

    def setLeftChild(self, leftChild):
        if isinstance(leftChild, Node) or leftChild is None:
            self.leftChild = leftChild
        else:
            raise TypeError("Children must be of type Node or None.")

    def setRightChild(self, rightChild):
        if isinstance(rightChild, Node) or rightChild is None:
            self.rightChild = rightChild
        else:
            raise TypeError("Children must be of type Node or None.")

    def __str__(self):
        return str(self.key)

class BinaryTree(object):
    def __init__(self, rootValue):
        self.root = Node(rootValue)
        # Map where the key is some integer and the value is a list of nodes.
        self.keyNodeMap = {rootValue: self.root}

    def getRoot(self):
        return self.root

    def add(self, value, parentValue):
        if not parentValue in self.keyNodeMap:
            print "Parent not found."
            return
        if value in self.keyNodeMap:
            print "This value has already been added."
            return
        parentNode = self.keyNodeMap[parentValue]
        if parentNode.getLeftChild() is None:
            newNode = Node(value, parentNode)
            parentNode.setLeftChild(newNode)
            self.keyNodeMap[value] = newNode
        elif parentNode.getRightChild() is None:
            newNode = Node(value, parentNode)
            parentNode.setRightChild(newNode)
            self.keyNodeMap[value] = newNode

    def delete(self, value):
        if not value in self.keyNodeMap:
            print "Node not found."
            return
        node = self.keyNodeMap[value]
        if node.getLeftChild() is None and node.getRightChild() is None:
            if node is self.root:
                print "Cannot delete root node."
            else:
                parent = node.getParent()
                if parent.getLeftChild() is node:
                    parent.setLeftChild(None)
                else:
                    parent.setRightChild(None)
                del self.keyNodeMap[value]
        else:
            print "Node not deleted, has children."

    # Returns a string. Will be called in the context: print <someTreeHere>
    def __str__(self):
        def printCurrNode(currNode):
            if currNode is None:
                return ""
            return (" " + str(currNode) + " "
                    + printCurrNode(currNode.getLeftChild())
                    + printCurrNode(currNode.getRightChild()))
        return printCurrNode(self.root)

# 4. Graph
class Vertex(object):
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError("Vertices must have value with type int.")
        self.value = value
        # Dictionary where key is some value and value is corresponding vertex.
        self.edges = {}

    def getValue(self):
        return self.value

    def setValue(self, value):
        if not isinstance(value, int):
            raise TypeError("Vertices must have value with type int.")
        self.value = value

    def getEdges(self):
        return self.edges

    def addEdge(self, vertex):
        if not isinstance(vertex, Vertex):
            raise TypeError("Edge must be to a Vertex.")
        self.edges[vertex.getValue()] = vertex

    def __str__(self):
        return str(value)

class Graph(object):
    def __init__(self):
        # Dictionary where key is some int and value is corresponding vertex.
        self.vertices = {}

    def addVertex(self, value):
        if value in self.vertices:
            print "Vertex already exists."
        else:
            self.vertices[value] = Vertex(value)

    def addEdge(self, value1, value2):
        if not value1 in self.vertices or not value2 in self.vertices:
            print "One or more vertices not found."
            return
        vertex1 = self.vertices[value1]
        vertex2 = self.vertices[value2]
        vertex1.addEdge(vertex2)
        vertex2.addEdge(vertex1)

    def findVertex(self, value):
        if not value in self.vertices:
            print "Vertex not in graph."
            return
        vertex = self.vertices[value]
        print "Vertex with value", value, "is in the graph adjacent to..."
        edges = vertex.getEdges()
        if len(edges) == 0:
            print "Nothing"
        else:
            for adj in vertex.getEdges():
                print adj
        print ""

# 5. Testing
import random

def testQueue():
    print "-----------------1 Queue-----------------"
    queue = Queue()

    print "\nTry to dequeue an empty queue..."
    try:
        queue.dequeue()
        print "Something went wrong!"
    except IndexError:
        print "Dequeue index error successfully raised."

    print "\nQueue 10 random integers..."
    for _ in range(10):
        randInt = random.randrange(100)
        print "Queueing", randInt
        queue.enqueue(randInt)

    print "\nTry to enqueue something that isn't an integer..."
    try:
        queue.enqueue("This should fail.")
        print "Something went wrong!"
    except TypeError:
        print "Enqueue type error successfully raised."

    print "\nDequeue the 10 random integers and print them..."
    for _ in range(10):
        print "Dequeueing", queue.dequeue()

def testStack():
    print "\n-----------------2 Stack-----------------"
    stack = Stack()
    print "\nTry popping from empty stack..."
    try:
        stack.pop()
        print "Something went wrong!"
    except IndexError:
        print "Pop index error successfully raised."

    print "\nPush 10 random integers onto the stack..."
    for _ in range(10):
        randInt = random.randrange(100)
        stack.push(randInt)
        print "Pushing", randInt, " Current size:", stack.checkSize()

    print "\nTry pushing non-integer onto the stack..."
    try:
        stack.push("This should fail.")
        print "Something went wrong!"
    except TypeError:
        print "Push type error successfully raised."

    print "\nPop the 10 integers off of the stack..."
    for _ in range(10):
        print "Popped", stack.pop(), " Current size:", stack.checkSize()

def testTree():
    print "\n-----------------3 Tree-----------------"

    print "\nTry to make a tree with a non-integer node..."
    try:
        BinaryTree("This should fail.")
        print "Something went wrong!"
    except TypeError:
        print "Node constructor raised type error successfully."

    tree = BinaryTree(0)

    print "\nTry to delete root node..."
    tree.delete(0)

    print "\nAdd 10 integers to the tree... "
    tree.add(1, 0)
    tree.add(2, 0)
    tree.add(3, 1)
    tree.add(4, 1)
    tree.add(5, 2)
    tree.add(6, 2)
    tree.add(7, 3)
    tree.add(8, 3)
    tree.add(9, 4)

    print "\nTry to add node with invalid parent..."
    tree.add(10, -1)

    print "\nTry to add non-unique node..."
    tree.add(1, 9)

    print "\nPre-order printing of tree..."
    print tree

    print "\nTry to delete a node that doesn't exist..."
    tree.delete(-1)

    print "\nTry to delete nodes with children..."
    tree.delete(3)
    tree.delete(2)
    tree.delete(1)

    print "\nDelete nodes 6 and 7..."
    tree.delete(6)
    tree.delete(7)

    print "\nAnother tree printing to reflect deletions."
    print tree

def testGraph():
    print "\n-----------------4 Graph-----------------"
    graph = Graph()

    print "\nAdding vertices..."
    for i in range(10):
        graph.addVertex(i)
    graph.addVertex(10)

    print "\nTry to add non-unique vertex..."
    graph.addVertex(1)

    print "\nTry to add a non-integer vertex..."
    try:
        graph.addVertex("This should fail.")
        print "Something went wrong!"
    except TypeError:
        print "Type error raised successfully from vertex constructor."
    print "\nAdding edges..."
    for i in range(8):
        graph.addEdge(i, i + 1)
        graph.addEdge(i, i + 2)
    graph.addEdge(5, 3)
    graph.addEdge(7, 1)
    graph.addEdge(0, 9)
    graph.addEdge(9, 8)

    print "\nTry to add invalid edges..."
    graph.addEdge(1, -1)
    graph.addEdge(-1, 1)
    graph.addEdge(-1, -1)

    print "\nFinding vertices..."
    graph.findVertex(0)
    graph.findVertex(1)
    graph.findVertex(3)
    graph.findVertex(7)
    graph.findVertex(8)
    graph.findVertex(9)
    graph.findVertex(10)

    print "\nLook for a vertex not in the graph..."
    graph.findVertex(-1)

def testStrucs():
    testQueue()
    testStack()
    testTree()
    testGraph()

if __name__ == "__main__":
    testStrucs()
