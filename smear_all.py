#!usr/bin/env python
import ROOT, rat, sys, os
from array import array as array

ind_variable = sys.argv[1] # input variable
dep_variable = sys.argv[2] # variable on y axis , e.g x ke means graphs for x pos vs ke resolution / bias.
uniform_file = sys.argv[3]
input_file = ROOT.TFile(uniform_file, "READ") #  
bias_res_file = ROOT.TFile("output_graphs_" + ind_variable + ".root", "READ")
output_file = ROOT.TFile("smeared_" + ind_variable + ".root", "update")
written_output = open("coefficients_" + ind_variable + ".txt", "a")

variable_num = {"x": 0, "y": 1, "z": 2, "ke": 3}

bias_matrix, res_matrix = [], []
vals_xmc, vals_ymc, vals_zmc, vals_kemc = [], [], [], []
vals_xev, vals_yev, vals_zev, vals_keev = [], [], [], []
def extract_variables():
    """
    Extracts MC and EV values for variable var from the input file and adds
    them to the lists vals_mc and vals_ev.
    """
    def get_all():

        vals_xmc.append(mc.GetMCParticle(0).GetPosition().X())
        vals_ymc.append(mc.GetMCParticle(0).GetPosition().Y())
        vals_zmc.append(mc.GetMCParticle(0).GetPosition().Z())
        vals_kemc.append(mc.GetMCParticle(0).GetKineticEnergy())

        vals_xev.append(ev.GetDefaultFitVertex().GetPosition().X())
        vals_yev.append(ev.GetDefaultFitVertex().GetPosition().Y())
        vals_zev.append(ev.GetDefaultFitVertex().GetPosition().Z())
        vals_keev.append(ev.GetDefaultFitVertex().GetEnergy())

    for ds, run in rat.dsreader(uniform_file):
        mc = ds.GetMC()
        for iev in range(ds.GetEVCount()):
            ev = ds.GetEV(iev)
            get_all()

print("Extracting variables")
extract_variables() 
print("Done.")
index = len(vals_xmc); print(index)

info_MC = {
(vals_xmc[i], vals_ymc[i], vals_zmc[i], vals_kemc[i]) : [[vals_xev[i]], [vals_yev[i]], [vals_zev[i]], [vals_keev[i]]] for i in range(index)
}

def extract_fit(bias_name, res_name, fit):
    """Creates smeared plots using random values from gaussians with parameters
       dictated by the fits in the graphs bias_name and res_name.
       Creates one for MC and one for EV.
    """
    print("Creating smeared plots with fit type " + fit + '\n')

    pol_degree = int(fit[-1:])
    indep_var_num = variable_num[ind_variable] # Variable on x axis
    dep_var_num = variable_num[dep_variable] # Variable on y axis
    bias_graph = bias_res_file.Get(bias_name)
    res_graph = bias_res_file.Get(res_name)

    bias_graph.Fit(fit)
    res_graph.Fit(fit)
    num_points_bias = bias_graph.GetN()
    num_points_res = res_graph.GetN()     

    num_deg_free_bias = num_points_bias - (pol_degree + 1)
    num_deg_free_res = num_points_res - (pol_degree + 1)
	
    bias_func = bias_graph.GetFunction(fit)
    bias_chi_square_array.append(bias_func.GetChisquare()/(num_deg_free_bias))
    res_func = res_graph.GetFunction(fit)
    res_chi_square_array.append(res_func.GetChisquare()/(num_deg_free_res))

    bias_coefficients = [bias_func.GetParameter(i) for i in range(pol_degree+1)] # b0, b1, b2, ... , bn
    res_coefficients = [res_func.GetParameter(i) for i in range(pol_degree+1)] # r0, r1, r2, ... , rn
    bias_matrix.append(bias_coefficients)
    res_matrix.append(res_coefficients)


    def add_to_info(info):
        """Add appropriate bias/resolution values to each key in the dictionary
           called info using the fit function extracted from the input files.
        """
        for MC_tuple in info:
            bias_value, res_value = 0, 0
            for i in range(pol_degree):
                bias_value += bias_coefficients[i] * pow(MC_tuple[indep_var_num], i) # bias = b0 + b1*val + b2*val^2 + ...
                res_value += res_coefficients[i] * pow(MC_tuple[indep_var_num], i) # res = r0 + r1*val + r2*val^2 + ...
            info[MC_tuple][dep_var_num] += [bias_value, res_value]

    add_to_info(info_MC)

    if dep_variable == "ke":
        Histogram_MC = ROOT.TH1F("Smearing MC " + ind_variable + ' vs ' + dep_variable + ' ' + fit,
                                 "Smearing MC " + ind_variable + ' vs ' + dep_variable + ' ' + fit,
                                 100,
                                -20,
                                 20)
    else:
        Histogram_MC = ROOT.TH1F("Smearing MC " + ind_variable + ' vs ' + dep_variable + ' ' + fit,
                                 "Smearing MC " + ind_variable + ' vs ' + dep_variable + ' ' + fit,
                                500,
                                -1000,
                                1000)
    
    Histogram_MC.GetXaxis().SetTitle("EV - smeared")
    def get_plots(info, histo):
        """ Fills histogram histo with random values generated from gaussian functions
        for each key-value pair in info.
        """
        for MC_tuple in info:

            EV = info[MC_tuple][dep_var_num][0] # indep_var_num = 0 means entries for x will be accessed etc.
            bias = info[MC_tuple][dep_var_num][1]
            resolution = info[MC_tuple][dep_var_num][2]

            centre = MC_tuple[dep_var_num] + bias
            func = ROOT.TF1("X", "TMath::Gaus(x, %s, %s)" % (centre, resolution),
                            centre - 500, centre + 500)
            random_val = func.GetRandom() # Smeared value
            histo.Fill(EV - random_val)


    print("Filling histograms...\n")
    get_plots(info_MC, Histogram_MC)


    if dep_variable == "ke":
        Histogram_MC.Fit("gaus", "", "", -10, 10)
    else:
        Histogram_MC.Fit("gaus", "", "", -300, 300)

    fit_function = Histogram_MC.GetFunction("gaus")

    RMS_MC.append(fit_function.GetParameter(2))
    Mean_MC.append(fit_function.GetParameter(1))
    error_mean.append(fit_function.GetParError(1))
    error_rms.append(fit_function.GetParError(2))
    output_file.WriteTObject(Histogram_MC)

fits = ["pol2", "pol3", "pol4", "pol5", "pol6", "pol7", "pol8", "pol9"]
pol_degrees = array('f', [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
RMS_EV, RMS_MC, Mean_EV, Mean_MC = array('f'), array('f'), array('f'), array('f')
bias_chi_square_array, res_chi_square_array = array('f'), array('f')
error_mean, error_rms, zero = array('f'), array('f'), array('f', [0 for i in range(8)])



if dep_variable != "ke":
    written_output.write(dep_variable + " Position\n")
else:
    written_output.write(dep_variable + "\n")

def writeToFile(matrix):
    """write the numbers in a matrix line by line to a file"""
    for j in range(len(matrix)):
        line = matrix[j]
        for i in range(len(line)):
            if i == 0:
		written_output.write("pol" + str(j+2) + " " + str(line[i]) + " ")
            elif i == len(line) - 1:
                written_output.write(str(line[i]) + "\n")
            else:
                written_output.write(str(line[i]) + " ")

for fit in fits:
    extract_fit(ind_variable + " Pos vs " + dep_variable + " Bias",
                ind_variable + " Pos vs " + dep_variable + " Resolution",
                fit)

written_output.write("Bias\n")
writeToFile(bias_matrix)
written_output.write("Resolution\n")
writeToFile(res_matrix)

rms_mc_graph = ROOT.TGraphErrors(8, pol_degrees, RMS_MC, zero, error_rms) 
mean_mc_graph = ROOT.TGraphErrors(8, pol_degrees, Mean_MC, zero, error_mean)
chi_square_res = ROOT.TGraph(8, pol_degrees, res_chi_square_array)
chi_square_bias = ROOT.TGraph(8, pol_degrees, bias_chi_square_array)

rms_mc_graph.SetName("MC " + ind_variable + " vs " + dep_variable + " RMS vs Pol Degree")
mean_mc_graph.SetName("MC " + ind_variable + " vs " + dep_variable + " Mean vs Pol Degree")
chi_square_bias.SetName("MC " + ind_variable + " vs " + dep_variable + " bias Chi Square vs Pol Degree" )
chi_square_res.SetName("MC " + ind_variable + " vs " + dep_variable + " resolution Chi Square vs Pol Degree")

rms_mc_graph.SetTitle("MC " + ind_variable + " vs " + dep_variable + " RMS")
mean_mc_graph.SetTitle("MC " + ind_variable + " vs " + dep_variable + " Mean")
chi_square_bias.SetTitle("MC " + ind_variable + " vs " + dep_variable + " Bias Chi Square")
chi_square_res.SetTitle("MC " + ind_variable + " vs " + dep_variable + " Resolution Chi Square")

rms_mc_graph.Draw("AC*")
mean_mc_graph.Draw("AC*")
chi_square_res.Draw("AC*")
chi_square_bias.Draw("AC*")

def setLabels(Graph, xAxisName, yAxisName):
    """Utility function to set labels on graphs"""
    Graph.GetXaxis().SetTitle(xAxisName)
    Graph.GetYaxis().SetTitle(yAxisName)

setLabels(rms_mc_graph, "Polynomial Degree", dep_variable + " RMS")
setLabels(mean_mc_graph, "Polynomial Degree", dep_variable + " Mean")
setLabels(chi_square_bias, "Polynomial Degree", dep_variable + " Bias Nomalised ChiSquare")
setLabels(chi_square_res, "Polynomial Degree", dep_variable + " Resolution Normalised ChiSquare")

output_file.WriteTObject(rms_mc_graph)
output_file.WriteTObject(mean_mc_graph)
output_file.WriteTObject(chi_square_res)
output_file.WriteTObject(chi_square_bias)

