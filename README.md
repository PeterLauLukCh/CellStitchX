# E-CellStitch: 3D Cellular Image Reconstruct Approach via Earthmover's Distance to Correct 2D Cell Mis-segmentation

Keywords: Geometry Processing, Optimal Transport, Earthmover's Distance, Biomedical Image Analysis

*Disclaim*: This research is based on [CellStitch](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-023-05608-2) (Y. Liu and Y. Jin et al., 2023). We aim to improve CellStitch by considering how to reconstruct 3D cells based on the cellular images with 2D segmentation errors. The 2D segmentation errors will cause a 3D cell to be wrongly segmentated into two 3D cells in CellStitch.  

We invent a new model based on Earthmover's Distance (EMD) to tackle this problem, and it is composed of three algorithms:
1) Candidate Searching algorithm
2) Shape Detection algorithm
3) Connecting Layer Validation algorithm

We also produces MaskRemover, which can simulate the 2D segmentation error, producing a set of errored images to train and validate our model.

## CandidateSearching
In this algorithm, we try to search for the potential candidates (pair of cells) that may have a missing cell mask (2D segmentation error) between them. 
We will then do a one-to-one correspondence check using the original optimal transport model in CellStitch 

## ShapeDetection (IN PROGRESS)
In this algorithm, we consider the following question: if stitch a candidate pair, then whether they can from a cell with **regular** shape 
We will also use clustering method to determine what is a **regular-shaped** cell

### Experiment 1: Harsh Criterion (only accept strict monotonous increasing/decreasing/quadratic)
Source: all the leaf cells

Number of cells: 2208

Number of total cells that passed all the strict criterion: 2048

Passing rate: 92.75%

Even though they have a linear or quadratic trend, there exists some oscillations which is not strictly monotonous. Therefore, we are considering doing a regression and setting an arbitrary $R^2$ threshold seperately for linear and quadratic cells. 

This is the statistics we get after using the regression method:

Linear Type: mean of $R^2=0.9377$, standard deviation of $R^2=0.0715$

Quadratic Type: mean of $R^2=0.9149$, standard deviation of $R^2=0.1109$

<img width="481" alt="Screen Shot 2024-03-22 at 9 38 54 PM" src="https://github.com/PeterLauLukCh/CellStitchX/assets/147995851/3d89caf5-3137-4d89-89f8-5dc42f538941">

### Experiment 2: Lenient Criterion
We start by calculating the mean ($µ$) and standard deviation ($σ$) of $R^2$ values from cells that pass a strict criterion. Then, for each cell ($Cell_{i}$) that doesn't meet this criterion, we compute its $R^2$ using both linear and quadratic regression. If either the linear or quadratic $R^2$ value falls within 1 standard deviation from the mean, we consider the cell as a potential candidate.

## EMDValidation (IN PROGRESS)
In this algorithm, we study the following question: whehter the shape of mask changes drastically near the missing the layer.
We propose a method to use EMD to quantify the change between layers and layers in each cell.
