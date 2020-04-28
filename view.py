import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import *
from tree_view import *

# Holds the information and processes to show the Dialog
class View:

    def __init__(self, controller):
        # The view has a controller, so it can use the dataset and tree through it
        self.controller = controller

        # Create an app and a window
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()

        # Build the GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        # Tree Widget
        self.ui.treeWidget = QWidget()
        self.ui.treeWidget.setMinimumSize(400, 400)
        self.ui.scrollArea.setWidget(self.ui.treeWidget)

        # Tree View
        self.treeView = None

    # Initialize the View by connecting the events and showing the main window
    def start(self):
        # Connect default button events
        self.connectEvents()

        # Show the window. Exit it when the X is pressed.
        self.window.show()
        sys.exit(self.app.exec_())

    ################ REFRESH ################

    # Creates a new tree
    def createTree(self, tree=None):
        # Create a new tree
        self.treeView = TreeView(self, self.ui)

        if tree is None:
            # Add its first level
            self.addTreeLevel()
        else:
            # Adds levels from the tree that was received
            self._addLevelsFromTree(tree)

        # Set the values of the general comboboxes
        self._setCombosValues()

        # Update the values the tree shows
        self.refreshTreeValues()

        # Enable the save tree and load button
        self.ui.saveTreeButton.setEnabled(True)
        self.ui.actionSave_current_tree.setEnabled(True)
        self.ui.loadTreeButton.setEnabled(True)
        self.ui.actionLoad_tree.setEnabled(True)

        # "New tree" button enabled
        self.ui.actionNew_tree.setEnabled(True)

        # Disable the load dataset button
        self.ui.loadDatasetButton.setEnabled(False)
        self.ui.actionLoad_new_dataset.setEnabled(False)

    # Set comboboxes values
    def _setCombosValues(self):
        # Get the category name and true value from the current tree (via the controller)
        categoryName = self.controller.getCategoryCue()
        trueValue = self.controller.getCategoryTrueValue()

        # Set these two values into the view
        self._setCategoryCombo(categoryName)
        self._setTrueValueCombo(trueValue)

    # Sets the category combobox into the position where the text specifies
    # The text must be part of the options available in the combobox
    def _setCategoryCombo(self, text):
        self._setTextInCombobox(self.ui.categoryCombo, text)

    # Sets the "true value" combobox into the position where the text specifies
    # The text must be part of the options available in the combobox
    def _setTrueValueCombo(self, text):
        self._setTextInCombobox(self.ui.trueValueCombo, text, True)

    # Searches for a text within the combobox options. Once it finds its, it sets the
    # combobox to select the index where that text was found
    def _setTextInCombobox(self, combobox, text, addIfInexistent = False):
        index = combobox.findText(text)

        # If the value doesnt exist in the combobox
        if index == -1 and addIfInexistent:
            # The value is added to the combobox
            combobox.addItem(str(text))

            # The index now points to the last item of the combobox list
            index = combobox.count() - 1

        combobox.setCurrentIndex(index)

    # Adds levels from an incoming tree object
    def _addLevelsFromTree(self, tree):
        levelsCount = tree.getNodesCount()

        # Add levels to the TreeView
        for i in range(0, levelsCount):
            # Add a new level directly into the tree
            newLevel = self.treeView.addLevel()

            # Set the values in the comboboxes
            newLevel.setCombosValues(tree.getNodeValues(i))

        # Refresh the buttons
        self.treeView.setEnabledButtons()

        # Update the window's size given the new tree
        self._resizeWindow()

    # Refreshes the labels and the tree
    def refresh(self):
        self.refreshComboBoxes()
        self.refreshLabels()

    # Refreshes the information in the labels
    def refreshLabels(self):
        # Set the Dataset Filepath into the text space
        self.ui.datasetText.setText(self.controller.getDatasetFilepath())

        # Update the statistics label/table
        self.updateStatistics()

    def refreshComboBoxes(self):
        # The Category ComboBox has to be on enabled...
        self.ui.categoryCombo.setEnabled(True)
        # ...and show the cues of the current dataset
        self.replaceComboBoxItemList(self.ui.categoryCombo, self.controller.getCuesNames())

        # The "True Value" ComboBox also has to be enabled and configured
        self.refreshTrueValueComboBox()

    # Refreshes the visualization of the tree (maybe because a new tree was loaded)
    def refreshTreeValues(self):
        if self.treeView is not None:
            self.treeView.refreshTreeValues()

        self.updateStatistics()

    # Adds a tree level in the end of the tree
    # (both in the view and on the model, through the controller)
    def addTreeLevel(self):
        # Create a new level in the tree's view
        self.treeView.addLevel()

        # Get the values marked in the view to pass them through to the controller
        cueName = self.treeView.getLastCueName()
        cuttingPoint = self.treeView.getLastCuttingPoint()
        operation = self.treeView.getLastOperation()

        # Create a new level in the tree
        self.controller.newNode(cueName, cuttingPoint, operation)

        self._numberOfLevelsChange()

    # Resizes the window depending on how many levels are currently on the tree
    def _resizeWindow(self):
        levelsCount = self.treeView.getLevelsCount() - 1

        #self.window.resize(600+100*levelsCount, 450+90*levelsCount)
        self.ui.treeWidget.setMinimumSize(400 + 100*levelsCount, 400 + 120*levelsCount)


    # Removes the last tree level
    def removeTreeLevel(self):
        # Remove the last level from the Tree View
        self.treeView.removeLevel()

        # Tell the controller to remove the last node
        self.controller.removeLastNode()

        self._numberOfLevelsChange()

    # To be called when a level is added or removed.
    # If updates the values of all the leafs, resizes the window and enables/disables buttons
    def _numberOfLevelsChange(self):
        # Update the values of all the leafs
        self.refreshTreeValues()

        # Resize the window:
        self._resizeWindow()

        # Enables/disables add/remove level buttons
        self.treeView.setEnabledButtons()

    # When the category combo box changes of selected value
    def categoryComboChanged(self):
        # Updates the options available in the "True value" ComboBox
        self.refreshTrueValueComboBox()

    # When the "true value" combobox changes of selected value
    def trueValueComboChanged(self):
        # Sets the new category (and true value) into the tree
        self.setCategory()

        # Update the values of all the leafs
        self.refreshTreeValues()


    def refreshTrueValueComboBox(self):
        # Update the values for the "True value combo":
        combo = self.ui.trueValueCombo

        # Enable the combobox...
        combo.setEnabled(True)

        # ... and change its item's list with the current category's possible values
        categoryName = self.ui.categoryCombo.currentText()
        items = self.stringifyListItems(self.controller.getCueLevels(categoryName))
        self.replaceComboBoxItemList(combo, items)

    # Function to be called when a configuration of any level has changed
    def treeLevelChanged(self, position):
        # Get the relevant data of the level that changed
        cueName = self.treeView.getCueName(position)
        cuttingPoint = self.treeView.getCuttingPoint(position)
        operation = self.treeView.getOperation(position)

        # Set this data in the Tree
        self.controller.modifyNode(position, cueName, cuttingPoint, operation)

        # Recalculate the categorizations of the tree
        self.controller.recalculateCategorizations()

        # Update the values of all the leafs
        self.refreshTreeValues()

    # Sets the current category (and true value) into the tree, through the controller
    def setCategory(self):
        categoryName = self.ui.categoryCombo.currentText()
        trueValue = self.ui.trueValueCombo.currentText()

        self.controller.setCategory(categoryName, trueValue)


    # Replaces the comboBox Item list entirely
    # comboBox: a ComboBox object
    # itemList: list of strings
    def replaceComboBoxItemList(self, comboBox, itemList):
        # Clears all the current items
        comboBox.clear()

        # Add all the items
        comboBox.addItems(itemList)

        # Points to the first item
        comboBox.setCurrentIndex(0)


    ################ OTHERS ################

    # Connect the onClick events of the default buttons
    def connectEvents(self):
        # Load dataset buttons
        self.ui.loadDatasetButton.clicked.connect(self.loadDataset)
        self.ui.actionLoad_new_dataset.triggered.connect(self.loadDataset)

        # Load and save tree buttons
        self.ui.loadTreeButton.clicked.connect(self.loadTree)
        self.ui.actionLoad_tree.triggered.connect(self.loadTree)

        self.ui.saveTreeButton.clicked.connect(self.saveTree)
        self.ui.actionSave_current_tree.triggered.connect(self.saveTree)

        # Tree configuration buttons
        self.ui.categoryCombo.currentIndexChanged.connect(self.categoryComboChanged)
        self.ui.trueValueCombo.currentIndexChanged.connect(self.trueValueComboChanged)

        # "New tree" button
        self.ui.actionNew_tree.triggered.connect(self.newTree)

        # Greedy optimization
        self.ui.actionGreedy_tree_optimization.triggered.connect(self.loadGreedyTree)

    def saveTree(self):
        # Get the current tree's filepath
        treeFilepath = self.controller.getTreeFilepath()

        filepath = self.showSaveFileDialog('Save Tree', treeFilepath)

        # If any filepath was chosen:
        if len(filepath) > 0:
            # Controller saves the tree
            try:
                self.controller.saveTree(filepath)
            except TypeError:
                pass

    # Function called when any of the "load tree" buttons is pressed
    # Destroys the current tree view and creates a new one
    def newTree(self):
        if self.treeView is not None:
            self.treeView.destroy()
        self.createTree()

    # Function called when any of the "load tree" buttons is pressed
    # It opens a load file dialog, loads the tree (using the controller) and shows it
    def loadTree(self):
        # Get the filepath from a dialog
        filepath = self.showLoadFileDialog('Load Tree file', 'tree.csv')

        # If any filepath was chosen:
        if len(filepath) > 0:
            # Controller loads the tree
            tree = self.controller.loadTree(filepath)

            if tree is not None:
                # And the view shows it
                self.treeView.destroy()
                self.createTree(tree)
            else:
                self.showMessage("Tree file error", "The tree could not be created. Please check that the selected tree file has the correct format.")

    def loadGreedyTree(self):
        # Load a greedy tree with a maximum amount of 7 nodes, and a minimum performance of 0.5
        # (these values could be defined in the View in a future version)
        tree = self.controller.loadGreedyTree(7, 0.5)

        self.treeView.destroy()
        self.createTree(tree)

    # Displays a popup
    def showMessage(self, title, text):
        messageBox = QMessageBox()
        messageBox.setWindowTitle(title)
        messageBox.setText(text)
        messageBox.exec_()

    # To be called to open a load file dialog and make the controller load a new dataset
    def loadDataset(self):
        # Get the filepath from a dialog
        filepath = self.showLoadFileDialog("Load Dataset file", "results.csv")

        # If any filepath was chosen:
        if len(filepath) > 0:
            # Make the controller load the dataset
            try:
                correctlyLoaded = self.controller.loadDataset(filepath)

                # If this was the first dataset loaded in the running program:
                if correctlyLoaded:
                    self.refresh()
                    self.createTree()
                else:
                    self.refresh()
            except TypeError:
                title = "File error"
                text = "The file has fewer than two columns, or an inconsistent amount of columns, or at least one cell is empty."
                self.ui.datasetText.setText(text)
                self.showMessage(title, text)



    # Opens a "LOAD file" dialog
    def showLoadFileDialog(self, title, filepath="./"):
        return QtGui.QFileDialog.getOpenFileName(self.window, title, filepath, "CSV file (*.csv)")

    # Opens a "SAVE file" dialog
    def showSaveFileDialog(self, title, filepath="./"):
        return QtGui.QFileDialog.getSaveFileName(self.window, title, filepath, "CSV file (*.csv)")

    # Applies str() to every item in a list
    def stringifyListItems(self, list):
        newList = []

        for element in list:
            newList.append(str(element))

        return newList

    # Updates the information shown in the statistics label
    def updateStatistics(self):
        text = "<b>Statistics:</b>"

        text = self._addToText(text, ["Total data-points: ", self.controller.getDatasetLength()])

        text = self._addToText(text, ["Data-points belonging to category: ", self.controller.getCategoryLength()])

        text = self._addToText(text, ["Tree levels: ", self.controller.getTreeLength()])

        accuracy = str(self.controller.getAccuracyCount()) + \
                   "/" + str(self.controller.getDatasetLength()) + \
                   "=" + str(round(self.controller.getTotalAccuracy() * 100, 1)) + "%"

        text = self._addToText(text, ["Accuracy: ", accuracy])

        text = self._addToText(text, ["Best performing level: ", self.controller.getBestNodeIndex() + 1])

        text = self._addToText(text, ["Worst performing level: ", self.controller.getWorstNodeIndex() + 1])

        self.ui.statisticsLabel.setText(text)

    # Adds all the elements of the array to the initial text
    # Also adds initial and ending <p> tags
    def _addToText(self, initialText, array):
        initialText += "<p>"

        for element in array:
            initialText += str(element)

        initialText += "<p>"

        return initialText


    ####### GETTERS AND SETTERS #######

    # Returns all the possible names of cues
    def getCuesNames(self):
        return self.stringifyListItems(self.controller.getCuesNames())

    # Returns all the possible values (i.e. levels) of a specific cue
    def getCueLevels(self, cueName):
        return self.stringifyListItems(self.controller.getCueLevels(cueName))

    # Returns the categorization values of the specified level/node
    def getCategorizationValues(self, position):
        return self.controller.getCategorizationValues(position)

    # Returns the length of the current dataset
    def getDatasetLength(self):
        return self.controller.getDatasetLength()
