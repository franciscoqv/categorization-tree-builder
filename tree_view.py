from level_view import *

# Shows the tree in the GUI
class TreeView:

    # view: Receives the View object so it can connect events to functions
    # ui: Receives the UI object so it can paint the tree on it
    # level: {0, 1, 2, ...} It defines the level of this
    def __init__(self, view, ui):
        self.view = view
        self.ui = ui
        self.levels = []

        # Create the root level
        self.createRoot()

    # Creates a new level on the tree
    # Returns the newly created level
    def addLevel(self):
        # The position of the new level will be the last one
        position = len(self.levels)

        # Create a new level
        newLevel = LevelView(self.view, self.ui, position)

        # Add it to the levels' list
        self.levels.append(newLevel)

        # Returns the new level
        return newLevel

    # Removes the last level of the Tree View
    def removeLevel(self):
        # Pop out the last level from the list of levels
        lastLevel = self.levels.pop(-1)

        # Destroy it in the UI
        lastLevel.destroy()

    # Destroy the tree view and its parts
    def destroy(self):
        for level in self.levels:
            level.destroy()


    # Refreshes the values of the leaves
    def refreshTreeValues(self):
        for level in self.levels:
            level.refreshLabels()


    # Shows the root node
    def createRoot(self):
        self.root = QtGui.QLabel(self.ui.treeWidget)
        self.root.setPixmap(QtGui.QPixmap("img/circle.png"))
        self.root.setGeometry(QtCore.QRect(86, 28, 80, 80))
        self.root.show()
        self._createRootLabel()

    # Shows the label of the root node
    def _createRootLabel(self):
        self.rootNodeText = QtGui.QLabel(self.ui.treeWidget)
        self.rootNodeText.setGeometry(QtCore.QRect(96, 40, 61, 51))
        self.rootNodeText.setAlignment(QtCore.Qt.AlignCenter)

        # Gets the length of the current dataset (i.e. the amount of objects)
        datasetLength = self.view.getDatasetLength()

        # Shows this information
        self.rootNodeText.setText(str(datasetLength))
        self.rootNodeText.show()

    ############## GETTERS AND SETTERS ###################

    # Returns the CueName of the targeted level
    def getCueName(self, position):
        return self.levels[position].getCueName()

    # Returns the CueName of the last level
    def getLastCueName(self):
        return self.getCueName(len(self.levels) - 1)

    # Returns the CuttingPoint of the targeted level
    def getCuttingPoint(self, position):
        return self.levels[position].getCuttingPoint()

    # Returns the CuttingPoint of the last level
    def getLastCuttingPoint(self):
        return self.getCuttingPoint(len(self.levels) - 1)

    # Returns the Operation of the targeted level
    def getOperation(self, position):
        return self.levels[position].getOperation()

    # Returns the Operation of the last level
    def getLastOperation(self):
        return self.getOperation(len(self.levels) - 1)

    # Updates the values of the ValueCombo
    def updateValueCombo(self, position):
        self.levels[position].updateValueCombo()

    # Returns how many levels are currently on the tree
    def getLevelsCount(self):
        return len(self.levels)

    # Sets the add/remove level buttons enabled/disabled.
    # Only the last level should have them enabled.
    def setEnabledButtons(self):
        for i in range(0, len(self.levels)):
            # Disable all the add/remove level buttons, except for the last level
            self.levels[i].setEnabledAddRemoveLevelButtons(i == len(self.levels)-1)
