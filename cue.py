# Holds al the data of a certain column
class Cue:

    # column: an array with this structure: [title, datapoint_1, ..., datapoint_n]
    def __init__(self, column):
        # The name of the Cue is the first element of the column.
        # At the same time, the element is popped out of the column.
        self.name = column.pop(0)

        # Calculate the data-type of the column
        self.numerical = self._getDataType(column)

        # Transform the data from string to number (if necessary)
        self.data = self._getTransformedData(column)

        # Calculate the levels available in the data and save them
        self.levels = self._getLevels()

    # Returns the minimum value available in the data of the cue
    def getMinimum(self):
        return self.levels[0]

    # Returns the maximum value available in the data of the cue
    def getMaximum(self):
        return self.levels[len(self.levels)-1]

    # Returns the data, sorted
    def _sortedData(self):
        return sorted(self.data)

    # Calculates the levels (i.e. all the different categories) of a dataset
    # The levels are returned sorted from low to high (or alphabetically)
    def _getLevels(self):
        levels = []

        # Loop all the data
        for datapoint in self.data:
            # Is the datapoint present in the levels array?
            if not self.isDatapointPresent(datapoint, levels):
                # If the datapoint is not present, add it to the levels array:
                levels.append(datapoint)

        return sorted(levels)

    # Returns true if a certain datapoint is present in the data of the cue
    # datapoint: Element to be searched
    # data: array on where to look. Defaults to the data of the current cue
    def isDatapointPresent(self, datapoint, data=None):
        if data is None:
            data = self.data

        # Try to find the datapoint inside the data
        try:
            # If it is found, return True
            data.index(datapoint)
            return True
        except ValueError:
            # If it is not found, return False
            return False

    # Transforms the data to numbers (if possible)
    # data: an array of datapoints
    def _getTransformedData(self, data):
        # Only if the cue is a number type cue, the transformation is performed
        if self.numerical:
            for i in range(0, len(data)):
                data[i] = float(data[i])

        return data

    # Returns True if all the values in the column are numbers
    # data: an array of datapoints
    def _getDataType(self, data):
        # For every datapoint, check if it is a digit
        for datapoint in data:
            if not datapoint.replace('.','',1).isdigit():
                # If any single one is not a digit, return False
                return False

        return True

    # Returns the amount of times a target value appears in the cue
    def getValueCount(self, value):
        count = 0

        # Search across all the data
        for datapoint in self.data:
            if str(datapoint) == str(value):
                count += 1

        return count

    # Returns the datapoint in position 'index'
    def getDataInIndex(self, index):
        return self.data[index]

    # Returns the amount of datapoints in the cue
    def getCueLength(self):
        return len(self.data)

    # Returns the name of the cue
    def getName(self):
        return self.name

    # Returns all the possible values of the cue
    def getLevels(self):
        return self.levels

    # Returns a list of the values in the specific positions
    # positions: targeted indexes
    def getValuesInPositions(self, positions):
        values = []

        # Add all the positions into a new list of lines
        for p in positions:
            # Get the value in that position
            value = self.data[p]

            # Append the value into the values' list
            values.append(value)

        return values