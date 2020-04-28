from tree import *

# It builds the nodes of a tree using a certain algorithm

# The reason behind making the functions static is that there is no need for an object of type TreeBuilder.
# The best approach to this would be to have a TreeBuilder class from which the GreedyTreeBuilder inherits.
# However, I thought that was too much for this moment.
class TreeBuilder:

    # Creates a tree using a greedy algorithm
    # Returns a tree
    @staticmethod
    def greedy(currentTree, dataset, maximumNodes=7, minimumPerformance=0.5):
        # Clone the current Tree (except for the nodes)
        tree = currentTree.clone()

        # Create the first node with the highest performing cue, operation and cutting point value,
        # regardless of its performance
        TreeBuilder._greedySearchFunction(tree, dataset, -1)

        # Create as many nodes as possible, as long as the performance is higher than 0.5
        # Also, the tree must have LESS than the amount of levels it has been said
        # Moreover, the tree has to have less nodes than the amount of columns
        while tree.getNodesCount() < maximumNodes and tree.getNodesCount() < len(dataset.getCueNames()):
            newNodeAdded = TreeBuilder._greedySearchFunction(tree, dataset, minimumPerformance)

            # If the newTree has as many nodes as the current tree, then it means that there was
            # no new node with the performance threshold was exceeded. Hence, the loop is broke.
            if not newNodeAdded:
                break

        # Return the greedy algorithm's tree
        return tree

    # Adds the best performing node to a tree
    # Returns True if a new node was added
    @staticmethod
    def _greedySearchFunction(tree, dataset, minimumPerformance):
        # All the available cues
        cueNames = list(dataset.getCueNames())

        # Remove the category cue because it should not be used as a predictor
        cueNames.remove(tree.getCategory())

        # Remove all the already used cues
        for name in tree.getNodesCuesNames():
            cueNames.remove(name)

        # Indexes for the search
        bestPerformance = minimumPerformance
        bestOverallPerformance = -1
        bestCue = None
        bestValue = None
        bestOperation = None

        # For each possible cue
        for name in cueNames:
            # Available values for the current cue
            levels = dataset.getCue(name).getLevels()

            # For each possible value of the cue
            for value in levels:

                # For each possible operation
                for operation in range(0, 4):

                    # Add the node to the tree
                    tree.newNode(name, value, operation)

                    # Calculate the performance of the first node
                    performance = tree.getTruePositivesAccuracyOfNode(dataset, tree.getNodesCount()-1)
                    overallPerformance = tree.getAccuracyNode(dataset, tree.getNodesCount()-1)

                    # If this performance is better than the best current performance, save the data
                    # OR If the performances are equal, but the overall performance is higher
                    if performance > bestPerformance or (performance == bestPerformance and overallPerformance > bestOverallPerformance):
                        bestPerformance = performance
                        bestOverallPerformance = overallPerformance
                        bestCue = name
                        bestValue = value
                        bestOperation = operation

                    # Remove the newly created node
                    tree.removeLastNode()

        # If there was a cue found that had a higher performance than the minimum received
        if bestCue is not None:
            tree.newNode(bestCue, bestValue, bestOperation)
            return True

        return False


