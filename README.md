# Bachelor Semester Project : The stabbing problem
This repository contains the code for my semester project at EPFL with the DISOPT chair under the supervision of Martina Gallato. The report is included. More information on the problem and the main functions can be found inside.

## Introduction
The horizontal stabbing problem consists in finding a set of horizontal segments of minimal length that stabs a given set of n axis-aligned rectangles such that each segment starts and ends at the extremity of one or multiple rectangles. The algorithm implemented here give an 8-approximation algorithm for this problem in O(n<sup>4</sup>). This algorithm was first described in Eisenbrand et al. (2021).

## Usage

### Librairies
The libraries math, copy, igraph, numpy, matplotlib, random, time and gurobipy are needed to run all the files.  
A gurobi licence might be necessary to have the optimal solution for big instances.

### Files and folders
*ClassRectangle.py* : The main class defining the rectangle that are stabbed.   

*Dpfonction.py* :  The main parts of the algorithm.  

*approxi_particular exemple* : This file return a figure with 3 subfigures corresponding to the optimal solution, the final solution given by our algorithm and the solution on the laminar instance given by the dynamic program on a given example.  

*laminar_graph.py* : Create a laminar instance of the problem : A set of axis-aligned rectangles is laminar if, for any pair of rectangles in it, their projection on the x-axis are either disjoint or one is contained in the other.  

*main.py* : Create a given or random example of an instance of the problem, run the algorithm and plot the result.  

*test_approximation.py* : Apply the algorithm on a multitude of random cases and save the interesting results. This was done with the goal of empirically testing the approximation.  

*test_complexity.py* : Apply the algorithm and register the time to run it for different axis size and number of rectangle. This was done in order to empirically test the complexity.

*figures and ratio* : Folder containing figures and results created by the algorithm. The folder is then further divided by the advancement in the project.

*test debug and presentation* : Folder containing scripts used to debug and analyze results. To use the script, the path name to the result files need to be updated. 

## References
Eisenbrand et al. (2021) : Eisenbrand, Gallato, Svensson and Venzin (2021) A qptas for stabbing rectangles.
