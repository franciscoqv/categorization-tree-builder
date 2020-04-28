import os
from cue import *

# Holds the information and builds a dataset from a file
class Dataset:

    def __init__(self, filePath):
        self.path = filePath
        self.lines = self._importData()
        self.cues = self._buildCues()

    # Returns a list of cues, building them from the current dataset
    def _buildCues(self):
        # The amount of column is the count of commas, plus one
        columnCount = self.lines[0].count(',') + 1

        # Cues' dictionary
        cues = {}

        # For every column, create a cue
        for i in range(0, columnCount):
            cueData = []

            # For each line, get the corresponding element for the cue
            for line in self.lines:
                # Separate line by comma
                commaSeparatedLine = line.split(",")

                # Append the column "i" element into the cueData
                cueData.append(commaSeparatedLine[i])

            # Now that the cueData is complete, create the cue and add it to the array
            newCue = Cue(cueData)
            cues[newCue.getName()] = newCue

        return cues

    # Imports data from the path and checks its correctness.
    # Returns the dataset (or None if there was an error)
    def _importData(self):
        dataByLines = self._importDataByLines()

        # If the file was correctly read and its internal data is correct
        if dataByLines != None and self._checkDataCorrectness(dataByLines):
            # Return the dataByLines variables (to be saved as the dataset)
            return dataByLines
        else:
            return None

    # Checks that the internal data of the file is correct
    def _checkDataCorrectness(self, dataByLines):
        # The amount of comas in the first line should be equal to all the others
        # Assumption of the CSV file: there are no commas within a datapoint
        commasCount = dataByLines[0].count(',')

        # If there are no commas (i.e. only one or none columns), return False
        if commasCount == 0:
            return False

        for datapoint in dataByLines:
            # Check that all the lines have the same amount of columns
            if commasCount != datapoint.count(','):
                # If any single commas' count is different to the initial commas' count
                return False

            # Also check that no element is empty (i.e. "")
            splitData = datapoint.split(',')

            for element in splitData:
                if len(element) == 0:
                    return False


        return True

    # Read the file where the dataset is saved
    def _importDataByLines(self):
        # If the file exists
        if os.path.isfile(self.path):
            # Open the file, read it, and split it into different lines
            file = open(self.path, 'r')
            fileData = file.read().split('\n')

            return self._removeEmptyElements(fileData)

        else:
            return None

    # Removes all the blank elements in a list of strings
    def _removeEmptyElements(self, list):
        newList = []

        # Check every element of the list of strings
        for element in list:
            if len(element) > 0:
                newList.append(element)

        return newList


    ### GETTERS AND SETTERS

    # Returns a list of cues' values
    # cueName: the name of the targeted cue
    # position: list of indexes
    def getCueValues(self, cueName, positions):
        return self.cues[cueName].getValuesInPositions(positions)

    def getCue(self, cueName):
        return self.cues[cueName]

    def getCueNames(self):
        return self.cues.keys()

    def getFilepath(self):
        return self.path

    # Amount of lines
    def getLength(self):
        return len(self.lines) - 1  # It is -1 because the first line is the column's titles