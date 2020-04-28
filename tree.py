import os
from node import *

# A tree is a set of cues, in a certain nodes.
class Tree:

    def __init__(self, filepath=None):
        self.nodes = []  # List of nodes
        self.category = None
        self.trueValue = None
        self.filepath = "tree.csv"

        if filepath is not None:
            self.filepath = filepath
            self._buildTreeFromFile(filepath)

    # Returns the dataset split by the Node in position X
    # dataset: complete dataset
    # x: position of the Node
    def getCategorization(self, dataset, x):
        # Check if the X value is correct
        if x >= len(self.nodes):
            return False
        else:
            categorization = self.nodes[x].splitDataset(dataset)

            # If this is the first categorization
            if x == 0:
                return categorization
            else:
                # Get the categorization of the level over the current one
                upperLevelCategorization = self.getCategorization(dataset, x-1)

                # Intersect the upper level with the categorization of the focused Node.
                return self._intersectCategorizations(upperLevelCategorization, categorization)

    # Intersect categorizations
    def _intersectCategorizations(self, topLevel, bottomLevel):
        # The indexes not categorized (i.e. categorized as FALSE) by the top level
        uncategorized = topLevel[1]

        # Intersect the uncategorized indexes with the bottom level categorizations
        intersected_0 = self._intersectArrays(uncategorized, bottomLevel[0])
        intersected_1 = self._intersectArrays(uncategorized, bottomLevel[1])

        return [intersected_0, intersected_1]

    # Returns the intersection of two lists
    def _intersectArrays(self, list1, list2):
        intersection = []

        for element in list1:
            # Try to find the datapoint inside the data
            try:
                # If it is found, add it to the intersection
                list2.index(element)
                intersection.append(element)
            except ValueError:
                pass

        return intersection

    # Creates a new node at the end of the tree
    def newNode(self, cueName, cuttingPoint, operation):
        newNode = Node(cueName, cuttingPoint, operation)
        self.nodes.append(newNode)

    # Clear all the categorizations done (e.g. because there is a new dataset)
    def clearCategorizations(self):
        for node in self.nodes:
            node.clearCategorization()

    # Removes the last node of the tree
    def removeLastNode(self):
        # Pop out the last element of the nodes' list
        self.nodes.pop(-1)

    # Builds a tree from a file
    def _buildTreeFromFile(self, filepath):
        # If the file exists
        if os.path.isfile(filepath):
            # Open the file, read it, and split it into different lines
            file = open(filepath, 'r')

            # Split the file into lines
            fileData = file.read().split('\n')

            # Process the data from the file (by saving the tree and node values into the objects)
            self._processFile(fileData)
        else:
            return None

    # Saves the data from the file into the corresponding Tree and Node objects
    def _processFile(self, fileData):
        # The first line includes the category. The second line includes the "true value"
        self.setCategory(fileData[0], fileData[1])

        # Then, the nodes come.
        for i in range(2, len(fileData)):
            # Each line is one node, in this structure: cueName,operation,cuttingPoint
            nodeData = fileData[i].split(',')

            # This is helpful for trailing lines
            if len(nodeData) == 3:
                # Extract the data from the file
                cueName = nodeData[0]
                operation = int(nodeData[1])
                cuttingPoint = nodeData[2]

                # Create a new node in the tree
                self.newNode(cueName, cuttingPoint, operation)

    # Saves the Tree in a file
    def saveTree(self, filepath):
        self.filepath = filepath

        # Create new file (if it exists, it will rewrite it)
        file = open(filepath, 'w')

        # Write the category and the true value
        file.write(self.category + '\n' + self.trueValue + '\n')

        # Write the nodes, in order
        for node in self.nodes:
            file.write(node.getNodeAsFileLine())

        # Close the file
        file.close()

    # Checks that the cues of the tree exist in the current dataset
    # Returns True if everything is alright.
    # cuesNames: a list of strings with the names of all the cues in the dataset
    def checkConsistency(self, cuesNames):
        # Check that every element of the tree exists in the dataset's cue names
        treeCuesNames = self.getNodesCuesNames()
        treeCuesNames.append(self.getCategory())

        for name in treeCuesNames:
            # Try to find the name in the cueNames of the dataset
            try:
                cuesNames.index(name)
            except ValueError:
                return False

        return True


    # Prints the tree into the console:
    def printTree(self, dataset):
        for i in range(0, len(self.nodes)):
            print(self.nodes[i].getCueName() + " " +
                  str(self.nodes[i].getOperationSymbol()) + " " +
                  str(self.nodes[i].getCuttingPoint())
                 )
            print(self.getCategorization(dataset, i))

    # Calculates the categorizations for every node
    def calculateCategorizations(self, dataset):
        for node in self.nodes:
            node.splitDataset(dataset)

    # Returns a dictionary summarizing the categorization of a specific node
    def getCategorizationValues(self, dataset, nodePosition):
        # Get the categorization done by the targeted node
        categorization = self.getCategorization(dataset, nodePosition)

        # Get the category cue
        cue = dataset.getCue(self.category)

        # Get the values of the category cue, for the positive (left) and the
        # negative (right) categorizations
        categorizedPositive = cue.getValuesInPositions(categorization[0])
        categorizedNegative = cue.getValuesInPositions(categorization[1])

        # Count how many were correctly categorized as true
        truePositives = self._countAppearances(categorizedPositive, self.trueValue)

        # Count how many were incorrectly categorized as false
        falseNegatives = self._countAppearances(categorizedNegative, self.trueValue)

        return{'truePositives': truePositives,
               'falsePositives': len(categorizedPositive) - truePositives,
               'trueNegatives': len(categorizedNegative) - falseNegatives,
               'falseNegatives': falseNegatives}

        # Counts how many times the target appears on a list
    def _countAppearances(self, list, target):
        count = 0

        for element in list:
            if str(target) == str(element):
                count += 1

        return count

    ########## GETTERS AND SETTERS ##########

    # Modify a specific node
    def modifyNode(self, position, cueName, cuttingPoint, operation):
        # Retrieve the target node
        node = self.nodes[position]

        # Modify it accordingly
        node.setCueName(cueName)
        node.setCuttingPoint(cuttingPoint)
        node.setOperation(operation)

    # Returns all the levels (i.e. possible values) of the current category
    def getCategoryLevels(self, dataset):
        return self.getCueLevels(dataset, self.category)

    # Returns the category cue
    def getCategoryCue(self, dataset):
        return dataset.cues[self.category]

    # Returns the amount of times the category occurs in the dataset
    def getCategoryCount(self, dataset):
        # Get the category cue
        categoryCue = self.getCategoryCue(dataset)

        # Count the occurrences of the True Value in the Category's Cue
        return categoryCue.getValueCount(self.trueValue)

    # Returns the accuracy (i.e. amount of correctly categorized data-points divided by the
    # total amount of datapoints) of the entire tree, for the current dataset
    def getAccuracy(self, dataset):
        return self.getTotalTruths(dataset) / dataset.getLength()

    # Returns the amount of items that have been categorized
    def getCountOfCategorizedDatapoints(self, dataset):
        # The first node definitely categorized as many datapoints as the dataset has:
        count = dataset.getLength()

        # If the tree has more than 1 node, then see how many datapoints reached each one:
        if self.getNodesCount() > 1:

            # From the first to the second-last node, check how many datapoints were categorized as Negative
            for nodePosition in range(0, self.getNodesCount() - 1):

                # Only the negatives are counted because these are the datapoints that are categorized
                # by the node.
                count += self._getNegativesNode(dataset, nodePosition)

        return count

    # Returns the accuracy of a certain node
    def getAccuracyNode(self, dataset, nodePosition):
        # Calculate the accuracy on a numerator of total truths
        # i.e. True Negatives + True Positives divided by the amount of positives to categorize
        successes = self.getTotalTruthsNode(dataset, nodePosition)

        return self._calculateAccuracy(dataset, nodePosition, successes)

    # Returns the TRUE POSITIVES accuracy of a certain node
    def getTruePositivesAccuracyOfNode(self, dataset, nodePosition):
        values = self.getCategorizationValues(dataset, nodePosition)

        successes = values['truePositives']
        total = (values['truePositives'] + values['falsePositives'])

        if total == 0:
            return -1
        else:
            return successes/total

    def _calculateAccuracy(self, dataset, nodePosition, successes):
        # How many datapoints reached the target node
        toCategorizeCount = self._getToCategorizeCount(dataset, nodePosition)

        # If the amount to categorize is zero, return 0
        if toCategorizeCount == 0:
            return 0
        # In other case, return the proportion
        else:
            return successes / toCategorizeCount

    # Returns the amount of datapoints reached a certain node to be categorized
    def _getToCategorizeCount(self, dataset, nodePosition):
        # Number of datapoints that get to that node.
        if nodePosition == 0:
            # If the target node is the first one, then the amount of datapoints to categorize
            # is the total amount of datapoints
            toCategorizeCount = dataset.getLength()
        else:
            # In any other case, it is the amount of Negatives of the previous node:
            toCategorizeCount = self._getNegativesNode(dataset, nodePosition - 1)

        return toCategorizeCount

    # Returns the amount of negatives of a specific node
    def _getNegativesNode(self, dataset, nodePosition):
        categorization = self.getCategorizationValues(dataset, nodePosition)

        return categorization['trueNegatives'] + categorization['falseNegatives']

    # Returns the index of the best performing node, in terms of accuracy
    def getBestPerformingNodeIndex(self, dataset):
        performances = self.getNodesPerformances(dataset)
        index = 0

        for p in range(0, len(performances)):
            # If the performance of the current node is better than the performance of the current target node
            # replace the index. If equal, the current (smaller) index stays (it gets prioritized for being
            # closer to the root).
            if performances[index] < performances[p]:
                index = p

        return index

    # Returns the index of the worst performing node, in terms of accuracy
    def getWorstPerformingNodeIndex(self, dataset):
        performances = self.getNodesPerformances(dataset)
        index = 0

        for p in range(0, len(performances)):
            # If the performance of the current node is worse than the performance of the current target node
            # replace the index. If equal, the new (larger) index stays (it gets prioritized for being
            # further to the root).
            if performances[index] >= performances[p]:
                index = p

        return index

    # Returns the performance of all the nodes, in order.
    def getNodesPerformances(self, dataset):
        performances = []

        # For each node, calculate its performance.
        for nodePosition in range(0, self.getNodesCount()):
            performances.append(self.getAccuracyNode(dataset, nodePosition))

        return performances

    # Returns the amount of truePositives+trueNegatives of the last node, plus the truePositives of each node
    def getTotalTruths(self, dataset):
        truePositives = 0
        trueNegativesLastNode = 0

        if self.getNodesCount() > 0:
            # For each node, calculate the amount of datapoints correctly categorized as true
            for nodePosition in range(0, self.getNodesCount()):
                truePositives += self.getCategorizationValues(dataset, nodePosition)['truePositives']

            # Only for the last node (because these datapoints are not consequently categorized,
            # calculate and consider its True Negatives
            trueNegativesLastNode = self.getCategorizationValues(dataset, self.getNodesCount()-1)['trueNegatives']

        return truePositives + trueNegativesLastNode

    # Returns the amount of truePositives+trueNegatives in a certain node
    def getTotalTruthsNode(self, dataset, nodePosition):
        values = self.getCategorizationValues(dataset, nodePosition)

        return values['truePositives'] + values['trueNegatives']

    # Returns all the levels (i.e. possible values) of a specific cue
    def getCueLevels(self, dataset, cueName):
        return dataset.cues[cueName].getLevels()

    # Sets which of the cues (columns) is the category
    def setCategory(self, cueName, trueValue):
        self.category = cueName
        self.trueValue = trueValue

    # Returns the amount of nodes that the tree has
    def getNodesCount(self):
        return len(self.nodes)

    # Returns the filepath
    def getTreeFilepath(self):
        return self.filepath

    # Returns the relevant values of a specific node
    def getNodeValues(self, index):
        node = self.nodes[index]
        return [node.getCueName(), node.getOperation(), node.getCuttingPoint()]

    # Returns the category (cue name) of the tree object
    def getCategory(self):
        return self.category

    # Returns the true value associated to the category
    def getTrueValue(self):
        return self.trueValue

    # Returns the names of all the nodes' cues
    def getNodesCuesNames(self):
        names = []

        for node in self.nodes:
            names.append(node.getCueName())

        return names

    # Sets the filepath
    def setFilepath(self, filepath):
        self.filepath = filepath

    # Returns a copy of the tree, except for the nodes
    def clone(self):
        clone = Tree()
        clone.setCategory(self.getCategory(), self.getTrueValue())
        clone.setFilepath(self.getTreeFilepath())

        return clone

