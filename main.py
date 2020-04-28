# This is an assessed project for the Programming class at UCL. March 2017.
from cue import *
from dataset import *
from tree import *
from view import *
from tree_builder import *

# Controller class in the MVC model.
class Controller:

    def __init__(self):
        import os
        self.mainDirectory = os.path.dirname(os.path.realpath(__file__))
        self.dataset = None
        self.tree = Tree()

    # Load a new dataset and cleans the current's tree categorizations
    def loadDataset(self, filepath):
        # True is this is the first dataset of the running program
        firstDataset = self.dataset is None

        # Load the dataset and save it
        self.dataset = Dataset(filepath)

        # Recalculate the previously done categorizations
        self.recalculateCategorizations()

        return firstDataset

    # Creates a new and empty tree
    def newTree(self):
        self.tree = Tree()

    # Loads a tree from a file
    def loadTree(self, filepath):
        # Load a tree and save it
        newTree = Tree(filepath)

        # Check if the new tree is consistent with the dataset's cue names
        if newTree.checkConsistency(list(self.dataset.getCueNames())):
            self.tree = newTree
            return self.tree
        else:
            # If the tree is not consistent with the dataset, return None
            return None

    # Optimizes the tree, greedily
    # maximumNodes: the maximum number of nodes of the tree
    # minimumPerformance: the least acceptable performance for any exist node
    def loadGreedyTree(self, maximumNodes, minimumPerformance):
        self.tree = TreeBuilder.greedy(self.tree, self.dataset, maximumNodes, minimumPerformance)
        return self.tree

    # Saves the current three to a file
    def saveTree(self, filepath):
        self.tree.saveTree(filepath)

    # Sets the current category and true-value
    def setCategory(self, cueName, trueValue):
        self.tree.setCategory(cueName, trueValue)

    # Clear all the categorizations from the tree
    def clearTree(self):
        if self.tree is not None:
            self.tree.clearCategorizations()

    # Clears the current categorizations and calculates them again
    def recalculateCategorizations(self):
        if self.tree is not None:
            self.clearTree()
            self.tree.calculateCategorizations(self.dataset)

    # Modifies a specific node
    def modifyNode(self, position, cueName, cuttingPoint, operation):
        # Remove all previous categorizations
        self.clearTree()

        # Modify the target node
        self.tree.modifyNode(position, cueName, cuttingPoint, operation)

    # Add new node to the tree
    def newNode(self, cueName, cuttingPoint, operation):
        self.tree.newNode(cueName, cuttingPoint, operation)

    # Remove the last node of the tree
    def removeLastNode(self):
        self.tree.removeLastNode()

    # Returns the category cue of the current tree
    def getCategoryCue(self):
        return self.tree.getCategory()

    # Returns the true value of the category of the current tree
    def getCategoryTrueValue(self):
        return self.tree.getTrueValue()

    # Returns the categorizations values of a specific node
    def getCategorizationValues(self, position):
        return self.tree.getCategorizationValues(self.dataset, position)

    # Returns all the cue names in a list, sorted alphabetically
    # Type: list of strings
    def getCuesNames(self):
        return sorted(self.dataset.getCueNames())

    # Returns all the levels (i.e. possible values) of a certain cue
    def getCueLevels(self, cueName):
        return sorted(self.tree.getCueLevels(self.dataset, cueName))

    # Returns all different values that the current category (specific cue) can have
    # Type: list of strings
    def getCategoryLevels(self):
        return sorted(self.tree.getCategoryLevels(self.dataset))

    # Returns a string of the dataset filepath (as used to load it)
    def getDatasetFilepath(self):
        return self.dataset.getFilepath()

    # Returns the tree's filepath
    def getTreeFilepath(self):
        return self.tree.getTreeFilepath()

    # Returns the length of the current dataset
    def getDatasetLength(self):
        return self.dataset.getLength()

    # Returns the amount of datapoints that belong to the category's true value
    def getCategoryLength(self):
        return self.tree.getCategoryCount(self.dataset)

    # Returns the length of the current tree (i.e. the amount of nodes)
    def getTreeLength(self):
        return self.tree.getNodesCount()

    # Returns the amount of correctly categorized datapoints
    def getAccuracyCount(self):
        return self.tree.getTotalTruths(self.dataset)

    # Returns the overall accuracy of the current tree, with the current dataset
    def getTotalAccuracy(self):
        return self.tree.getAccuracy(self.dataset)

    # Returns the accuracy of a certain, specified node
    # nodePosition: index
    def getNodeAccuracy(self, nodePosition):
        return self.tree.getAccuracyNode(self.dataset, nodePosition)

    # Returns the index of the best performing node
    def getBestNodeIndex(self):
        return self.tree.getBestPerformingNodeIndex(self.dataset)

    # Returns the index of the worst performing node
    def getWorstNodeIndex(self):
        return self.tree.getWorstPerformingNodeIndex(self.dataset)

    # Returns the amount of datapoints that have reached any node
    def getCountOfCategorizedDatapoints(self):
        return self.tree.getCountOfCategorizedDatapoints()

    # Prints tree into console
    def printTree(self):
        self.tree.printTree(self.dataset)

def main():
    # Create a controller that will hold the information of the dataset
    controller = Controller()

    # Create a view. This view holds a controller to use functions and access data
    view = View(controller)

    # Start the view
    view.start()

# Run the main function
main()
