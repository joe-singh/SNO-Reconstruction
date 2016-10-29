#!/usr/bin/env python
"""A program which uses json files to make a plot of how input quantities vary
given different initial conditions (specified in user generated macros). Inputs
should be correct parameters from json files made by plotError.py and stored in
a folder called json_files."""

from array import array as array
from os import listdir as listdir
import sys
from ROOT import TCanvas, TGraphErrors, TFile, TGraph, TMultiGraph, TLegend
import json

# Get all json files produced by plotResidual.py
files_list = listdir("json_files")
json_files = ["json_files" + "/" + json_file for json_file in files_list]

arg1, arg2, error = str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
var = arg1[0]
# Initialise list to store json data and file to store ouput histograms.
datapoints = []
new_file = TFile("output_graphs_" + var + ".root", "update")

fit = "pol3"

for json_file in json_files:

    # Get value tuples from json file and add to initialised list.
    json_decode = json.load(open(json_file, 'r'))
    data_val_1, data_val_2, error_val = json_decode.get(arg1), json_decode.get(arg2), json_decode.get(error)
    datapoints.append((data_val_1, data_val_2, error_val))

# Initialise arrays to store individual datapoints.
x_axis_pars, y_axis_pars, error_vals = array('f'), array('f'), array('f')

for datapoint in datapoints:
    x_axis_pars.append(datapoint[0])
    y_axis_pars.append(datapoint[1])
    error_vals.append(datapoint[2])


Title = arg1 + " vs " + arg2
c1 = TCanvas("c1", Title)
#c1.SetGrid()

gr = TGraphErrors(len(x_axis_pars), x_axis_pars, y_axis_pars, array('f', [0 for i in range(len(x_axis_pars))]), error_vals)

if "ke" in arg1:
    gr.GetXaxis().SetTitle(arg1 + "/MeV")
else:
    gr.GetXaxis().SetTitle(arg1 + "/mm")
if "ke" in arg2:
    gr.GetYaxis().SetTitle(arg2 + "/MeV")
else:
    gr.GetYaxis().SetTitle(arg2 + "/mm")

gr.SetTitle(Title)
gr.Fit(fit)
gr.SetMarkerStyle(5); gr.SetMarkerColor(4); gr.SetLineColor(1); gr.SetLineWidth(1); gr.SetLineStyle(1)

gr.Draw("AP")
gr.SetName(Title)
new_file.WriteTObject(gr)
