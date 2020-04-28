# categorization-tree-builder
Categorization tree builder (Fast and frugal trees (FFT))

# Overview

This Python-based software developed is a Categorization Tree Builder inspired in Fast-and-Frugal trees  (FFT). The builder lets the user import any dataset and build a categorization tree for it. The idea of having a manual builder for FFTs is to see how the performance of a tree as it is being built and try different combinations of configurations to try to find the optimal one.

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
