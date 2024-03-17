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

## ShapeDetection (Not finished yet)
In this algorithm, we consider the following question: if stitch a candidate pair, then whether they can from a cell with **regular** shape 
We will also use clustering method to determine what is a **regular-shaped** cell

## EMDValidation (Not finished yet)
In this algorithm, we study the following question: whehter the shape of mask changes drastically near the missing the layer.
We propose a method to use EMD to quantify the change between layers and layers in each cell.
