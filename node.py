
# A node of the tree is connected to one specific cue of the dataset.
# The way the cue is identified is by its name, because the Tree (several nodes)
# can be used in different datasets, as long as the Cue's names coincide.
class Node:

    # cueName: string. It is the name (i.e. unique identifier) of the cue
    # cuttingPoint: Point where the Node is split. Can be a number or a string.
    # operation: a number from 0 to 3, which corresponds to the operation to be done in the node
    #            (see getOperationSymbol function)
    def __init__(self, cueName, cuttingPoint, operation):
        self.cueName = cueName
        self.setCuttingPoint(cuttingPoint)
        self.operation = operation
        self.categorization = None

    # Splits the dataset according to the Node's values
    def splitDataset(self, dataset):
        # If no categorization has been done before
        if self.categorization is None:
            # Get the corresponding cue
            cue = dataset.getCue(self.cueName)

            # A specific cue value can be categorized as True or False by the Node
            trueResults = []
            falseResults = []

            # For each datapoint inside the cue
            for i in range(0, cue.getCueLength()):
                # Get the datapoint in the current index
                datapoint = cue.getDataInIndex(i)

                # Perform the operation and categorize the datapoint's index
                if self._performOperation(datapoint):
                    trueResults.append(i)
                else:
                    falseResults.append(i)

            # Save a list where the first element is the list of indexes categorized
            # as true, and the second element is the list of indexes categorized as false.
            self.categorization = [trueResults, falseResults]

        return self.categorization

    # Performs the node operation on a single value
    def _performOperation(self, value):
        if len(str(self.cuttingPoint)) > 0:
            if self.operation == 0:
                return value < self.cuttingPoint
            elif self.operation == 1:
                return value <= self.cuttingPoint
            elif self.operation == 2:
                return value > self.cuttingPoint
            elif self.operation == 3:
                return value >= self.cuttingPoint
        return False

    ### GETTERS AND SETTERS
    def getCueName(self):
        return self.cueName

    def getCuttingPoint(self):
        return self.cuttingPoint

    def getOperation(self):
        return self.operation

    def getOperationSymbol(self):
        if self.operation == 0:
            return "<"
        elif self.operation == 1:
            return "<="
        elif self.operation == 2:
            return ">"
        elif self.operation == 3:
            return ">="
        return False

    # Deletes the current saved categorization
    def clearCategorization(self):
        self.categorization = None

    def setCueName(self, cueName):
        self.cueName = cueName

    # Sets the value of the cutting point
    # cutting point: string
    def setCuttingPoint(self, cuttingPoint):
        # If the received cutting point is not a float and is not an integer
        if (not isinstance(cuttingPoint, float)) and (not isinstance(cuttingPoint, int)):

            # If the received cutting point is a number in a string, transform it to a float
            if cuttingPoint.replace('.','',1).isdigit():
                cuttingPoint = float(cuttingPoint)

        # Save the value
        self.cuttingPoint = cuttingPoint

    def setOperation(self, operation):
        self.operation = operation

    # Gets the node in a format to write it in a file
    def getNodeAsFileLine(self):
        return str(self.cueName) + ',' + str(self.operation) + ',' + str(self.cuttingPoint) + '\n'

