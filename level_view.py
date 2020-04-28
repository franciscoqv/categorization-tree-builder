import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import *

# The Level of a Tree
class LevelView:

    # Creates a new Level in the Tree View
    # position: integer from 0 onwards. It defines the position of the Level.
    def __init__(self, view, ui, position):
        self.view = view
        self.ui = ui
        self.position = position

        # Create all the different elements of the Level View
        self._createElements()

        # Show all of them
        self.levelWidget.show()

    # Updates the values in the labels
    def refreshLabels(self):
        values = self.view.getCategorizationValues(self.position)

        # Left label
        leftLabel = self.leftNodeText

        # Calculate the total amount of items categorized towards that leaf
        leftTotal = values['truePositives'] + values['falsePositives']

        # And calculate the percentage of correctly categorized to the left
        if leftTotal != 0:
            leftPercentage = values['truePositives'] / leftTotal * 100
            leftPercentage = round(leftPercentage, 1)
        else:
            leftPercentage = 'N/A '

        # Refresh the label
        self._refreshLeafLabel(leftLabel, leftTotal, leftPercentage)

        # The same for the right label:
        rightLabel = self.rightNodeText
        rightTotal = values['trueNegatives'] + values['falseNegatives']
        if rightTotal != 0:
            rightPercentage = values['trueNegatives'] / rightTotal * 100
            rightPercentage = round(rightPercentage, 1)
        else:
            rightPercentage = 'N/A '

        # Refresh the value on the label
        self._refreshLeafLabel(rightLabel, rightTotal, rightPercentage)

    # Refreshes a specific label with new data
    def _refreshLeafLabel(self, label, total, percentage):
        text = str(total) + '\n' + str(percentage) + '% acc.'
        label.setText(text)


    # Destroys the current level widget on the UI (this destroys its elements too)
    def destroy(self):
        self.levelWidget.hide()
        self.levelWidget.destroy()

    # Creates all the different elements that compose the Level View
    def _createElements(self):
        self._createLevelWidget()
        self._createRightNodeText()
        self._createLeftNodeText()
        self._createCueCombo()
        self._createOperationCombo()
        self._createValueCombo()
        self._createImage()

        # The "Add level button" appears until the 5th level
        if self.position < 5:
            self._createAddLevelButton()
        else:
            self.addLevelButton = None

        # The "Remove level button" always appears, except for the 1st level
        if self.position > 0:
            self._createRemoveLevelButton()
        else:
            self.removeLevelButton = None

    def _createLevelWidget(self):
        self.levelWidget = QtGui.QWidget(self.ui.treeWidget)
        self.levelWidget.setGeometry(QtCore.QRect(self.position*76, self.position*140+60, 360, 260))
        self.levelWidget.setObjectName("levelWidget")

    def _createRightNodeText(self):
        self.rightNodeText = QtGui.QLabel(self.levelWidget)
        self.rightNodeText.setGeometry(QtCore.QRect(170, 120, 61, 51))
        self.rightNodeText.setAlignment(QtCore.Qt.AlignCenter)
        self.rightNodeText.setObjectName("rightNodeText")
        self.rightNodeText.setText("Right Node Text")

    def _createLeftNodeText(self):
        self.leftNodeText = QtGui.QLabel(self.levelWidget)
        self.leftNodeText.setGeometry(QtCore.QRect(22, 120, 61, 51))
        self.leftNodeText.setAlignment(QtCore.Qt.AlignCenter)
        self.leftNodeText.setObjectName("leftNodeText")
        self.leftNodeText.setText("Right Node Text")

    def _createCueCombo(self):
        self.cueCombo = QtGui.QComboBox(self.levelWidget)
        self.cueCombo.setGeometry(QtCore.QRect(260, 10, 91, 22))
        self.cueCombo.setObjectName("cueCombo")

        # Get all the names of the cues of the current dataset
        cuesNames = self.view.getCuesNames()

        # Add the possible values of cues to the ComboBox
        self.cueCombo.addItems(cuesNames)

        # Select the first item of the ComboBox
        self.cueCombo.setCurrentIndex(0)

        # Connect the change event of the Cue Combo to the View
        self.cueCombo.currentIndexChanged.connect(self.updateValueCombo)
        self.cueCombo.currentIndexChanged.connect(self._levelChanged)

    def _createOperationCombo(self):
        self.operationCombo = QtGui.QComboBox(self.levelWidget)
        self.operationCombo.setGeometry(QtCore.QRect(260, 40, 91, 22))
        self.operationCombo.setObjectName("operationCombo")
        self.operationCombo.addItem("<")
        self.operationCombo.addItem("≤")
        self.operationCombo.addItem(">")
        self.operationCombo.addItem("≥")

        # Connect the change event of the Combobox
        self.operationCombo.currentIndexChanged.connect(self._levelChanged)

    def _createValueCombo(self):
        self.valueCombo = QtGui.QComboBox(self.levelWidget)
        self.valueCombo.setGeometry(QtCore.QRect(260, 70, 91, 22))
        self.valueCombo.setObjectName("valueCombo")

        self.updateValueCombo()

        # Connect the change event of the Combobox
        self.valueCombo.currentIndexChanged.connect(self._levelChanged)


    def _createImage(self):
        self.image = QtGui.QLabel(self.levelWidget)
        self.image.setPixmap(QtGui.QPixmap("img/level.png"))
        self.image.setGeometry(QtCore.QRect(8, 40, 235, 151))

    # Updates the possible values of the "Value Combo Box"
    def updateValueCombo(self):
        # Remove all the current options
        self.valueCombo.clear()

        # Get all the possible values of the currently selected cue
        cueValues = self.view.getCueLevels(self.getCueName())

        # Add the possible values of the current cue to the ComboBox
        self.valueCombo.addItems(cueValues)

        # Select the first item of the ComboBox
        self.valueCombo.setCurrentIndex(0)

    def _createAddLevelButton(self):
        self.addLevelButton = QtGui.QPushButton(self.levelWidget)
        self.addLevelButton.setGeometry(QtCore.QRect(260, 100, 40, 22))
        self.addLevelButton.setObjectName("loadDatasetButton")
        self.addLevelButton.setText("+")

        self.addLevelButton.clicked.connect(self.view.addTreeLevel)

    def _createRemoveLevelButton(self):
        self.removeLevelButton = QtGui.QPushButton(self.levelWidget)
        self.removeLevelButton.setGeometry(QtCore.QRect(310, 100, 40, 22))
        self.removeLevelButton.setObjectName("loadDatasetButton")
        self.removeLevelButton.setText("–")

        self.removeLevelButton.clicked.connect(self.view.removeTreeLevel)

    ############## CONNECTION FUNCTIONS ##############

    # When any setting in the level changes, this function is called
    def _levelChanged(self):
        # The view is informed that something in the level has changed
        self.view.treeLevelChanged(self.position)

    ############## GETTERS AND SETTERS ##############

    def getCueName(self):
        return self.cueCombo.currentText()

    def getCuttingPoint(self):
        return self.valueCombo.currentText()

    def getOperation(self):
        return self.operationCombo.currentIndex()

    def setEnabledAddRemoveLevelButtons(self, boolean):
        if self.addLevelButton is not None:
            self.addLevelButton.setEnabled(boolean)

        if self.removeLevelButton is not None:
            self.removeLevelButton.setEnabled(boolean)

    # Sets the values of the comboboxes
    # array = [text, index, text]
    def setCombosValues(self, array):
        self.setCueComboValue(array[0])
        self.setOperationComboValue(array[1])
        self.setValueComboValue(array[2])

    # Sets the value in the Cue Combobox
    def setCueComboValue(self, text):
        index = self.cueCombo.findText(text)

        self.cueCombo.setCurrentIndex(index)

    # Sets the value in the Operation Combobox
    def setOperationComboValue(self, index):
        # Check if the index received is within the correct margins:
        if index > 3 or index < 0:
            # If it is not, it is set to zero.
            index = 0

        self.operationCombo.setCurrentIndex(index)

    # Sets the value in the Value Combobox
    def setValueComboValue(self, text):
        index = self.valueCombo.findText(str(text))

        # If the value doesnt exist in the combobox, it is created
        if index == -1:
            self.valueCombo.addItem(str(text))

            # The index now points to the last item of the combobox list
            index = self.valueCombo.count() - 1

        self.valueCombo.setCurrentIndex(index)
