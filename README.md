# categorization-tree-builder
Categorization tree builder ([Fast and frugal trees (FFT)] [1]).

# Overview

This Python-based software developed is a Categorization Tree Builder inspired in Fast-and-Frugal trees [2] (FFTs). The builder lets the user import any dataset and build a categorization tree for it. The idea of having a manual builder for FFTs is to see how the performance of a tree as it is being built and try different combinations of configurations to try to find the optimal one.

# Procedure

The first step is to import a dataset into the software. After this is done, the software analyses the dataset and builds an internal representation of it, where every column of the dataset is separated into cues. Each column of a dataset is a cue.

Then, the user has to specify which of the columns (cues) will be the target category. This is an essential part of the procedure. The category indicates which column is the one to be **predicted**, while all the others should be considered as **predictors**. The category also comes along with a “true value”, which signifies the value at which this category is considered True. To exemplify, consider the following dataset:

| Age | Gender | Risk   | Within-category |
|-----|--------|--------|:---------------:|
| 17  | Female | Low    |                 |
| 18  | Male   | High   |        *        |
| 20  | Male   | Low    |                 |
| 18  | Female | Medium |                 |
| 18  | Male   | Medium |                 |
| 16  | Female | High   |        *        |
| 17  | Female | High   |        *        |

Given this dataset, a goal could be to predict the value of **High Risk** using the cues of Age and Gender. The background to this, hypothetically, could be that age and gender are relatively public characteristics of a person and we want to identify which individuals are in High Risk in order to further investigate their individual situations. Hence, specifically in this scenario, the **Category Cue** would be **Risk** and its **True Value** would be **High**. Using the example dataset, one can see that tree data-points are within-category and the rest are out-of-category.

After the Category values have been set, the user can start building the tree by manually adding binary nodes, by loading a tree from a file or by running an automatic optimization algorithm. 

## Step 1: load a dataset
image

There are two default datasets in the software’s folder. One is called results.csv and the other one is results2.csv. Any of them can be used to test the software. Also, any other dataset can be loaded to the software as long as these restrictions apply:

- It must be a comma-separated-value file.
- The first line is for the column’s titles.
- It must have two columns or more.
- No cell should be empty.

## Step 2: set category settings
image

Once the dataset is loaded, a tree will appear. At these moment, there are three options to follow:

1. Start building the tree.
2. Load a tree.
3. Optimise a tree.

If the second option is chosen, there is a tree file in the software’s folder called tree.csv that can be loaded and will work with any of the two provided datasets
If the first option is chosen, the first thing to do is to set the category settings. First, the category cue has to be chosen and then its true value. Remember that these two settings define the target value against which the data-points will be defined as within-category or out-of-category (as explained in the Procedure section).

## Step 3: build tree
image

To build a tree, there are three settings for each node (see the green rectangle on the right). These settings are: Cue, Operation, Value. The way in which this works is that every data-point that reaches the node will be divided to the left or to the right of the node, depending on whether the node categorized the data-point as having a True or False value against the node settings, respectively.
For example, let us say that a data-point has this data: [Age=23, Gender=Female]. The way how this data-point will flow in the previously shown tree is the following:

image

The first node specifies that every data-point that has an **Age < 22** will be categorized as True and hence go to the Left. Given that our example has Age=23, then it was categorized as False and hence goes to the Right of the Node. Then, the next Node has a configuration of **Gender ≤ Female**[3] and our example has a value of Gender=Female, the data-point is categorized as True (hence it foes to the Left of the Node).

The accuracy values inside of each circle depict the percentage of data-points that are correctly categorized in that leaf. The left nodes expect to have data-points that are within-category, while the ones to the right expect data-points that are out-of-category. Hence, in the previously shown tree, the first node categorized 150 elements, 18 to the left and 132 to the right. Of the 18 elements categorized to the left (i.e. categorized as within-category), 61.1% really belong to the category. On the other hand, of the 132 elements categorized to the right (i.e. categorized as out-of-category), only 49.2% of them are actually out-of-category.

As the user builds the tree manually, checking the Statistics box (left green rectangle) would be very useful.

# Highlights

The software enables a user to explore and create a categorization tree from scratch. Moreover, once the tree is created it can be saved to be used later. The best use-case for this would be as follows:
1. Load a training dataset.
2. Create a tree using the training dataset.
3. ave the tree.
4. Close and reopen the program.
5. Load a testing dataset.
6. Load the previously saved tree and see how it performs.

From a software engineering perspective, the software separated the Controller, the Model and the View so in the future, the backend (controller and model) can be connected to a completely different View, such as HTML.

## Other highlights
1. The software checks that the loaded tree cues exist in the current dataset before loading the tree.
2. Greedy tree optimization: it creates tree that optimizes (greedily) the categorization of a tree. A nice way to try it is by:
  1. Loading results.csv dataset
  2. Setting the Category to Gender and the True Value to Female
  3. Pressing the Greedy tree optimization option in the Optimize menu
  4. This should bring calculate a greedy tree that will automatically show the following:


# References
[1]: The following is an assignment made by me for a UCL Programming course.

[2]: Martignon, L., Vitouch, O., Takezawa, M., & Forster, M. R. (2003). Naive and yet enlightened: From natural frequencies to fast and frugal decision trees. Thinking: Psychological perspective on reasoning, judgment, and decision making, 189-211.

[3]: Comparisons in numerical cues are done as expected. Comparisons in cues that are not numerical (i.e. that are text) are done alphabetically. For example, “Female” < “Male” is a True statement because the word “Female” alphabetically precedes the word “Male”. 
