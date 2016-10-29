# SNO-Reconstruction

Modules in the Package:
 
Main Programs
* Macro_Generator.py
*plotResidual.py
* plotError.py
* smear_all.py

Utility Programs
* PDFconverter.cc
* multifits.cc
* rat-cluster-good.sh
* do-all-plotError.sh

Overall Execution :
1.Input file with detector parameters (i.e. axis to be simulated over, range to be simulated over, simulation energy) used to create rat macros (Macro_Generator.py).
2. Rat macros used to create root files. 
3. Root files used to create residual histograms, data stored in json files (plotResidual.py)
4. Json data used to create Bias/Resolution plots for variable being simulated over (plotError.py)
5. Bias/Resolution plots used to create plots of how Mean/RMS/Normalised Chi Square vary with polynomial degree 
   (smear_all.py)
 
Utility Files:
* PDFconverter.cc: Used to extract all Bias/Resolution plots from a particular file and save them in PDF format
* multifits.cc: Used to apply all polynomial fits (pol2-9) on plots produced by plotError.py
* rat-cluster-good.sh: Shell script to run rat macros on LBL cluster.
* do-all-plotError.sh: Shell script to execute plotError.py 8 times to get all 8 graphs for a given input variable.  
