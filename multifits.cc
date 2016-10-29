/**
   Program to produce bias/resolution plots with all fits together.
   @author: Jyotirmai Singh 30/10/2016
*/
#include <string>
#include <sstream>

std::string intToString(int num) {
  std::stringstream ss;
  ss << num;
  std::string str = ss.str();
  return str;
}

TGraphErrors* fitGraph(std::string graphname, int degree, TFile* source_file) {
  TGraphErrors* extracted_graph = source_file->Get(graphname.c_str());
  std::string pol = "pol" + intToString(degree);
  extracted_graph->Fit(pol.c_str());
  extracted_graph->GetFunction(pol.c_str())->SetLineColor(degree);
  extracted_graph->SetTitle(pol.c_str());
  extracted_graph->SetFillStyle(0);

  switch (degree) {
    case 0:
      extracted_graph->GetFunction(pol.c_str())->SetLineColor(28);
      extracted_graph->SetLineColor(28);
      break;
    default:
      extracted_graph->GetFunction(pol.c_str())->SetLineColor(degree);
      extracted_graph->SetLineColor(degree);
      break;
  }

  return extracted_graph;
}

void GetMultiPlot(std::string graphname, TFile* source_file, TFile* out_file, std::string var) {
  TCanvas*  c1 = new TCanvas(graphname.c_str(), graphname.c_str(), 800, 800);
  TMultiGraph* output = new TMultiGraph(graphname.c_str(), graphname.c_str());
  TLegend* legend = new TLegend(.1, .7, .48, .9);
//  legend->SetHeader("Legend", "C");
  for (int degree = 0; degree < 10; degree++) {
    TGraphErrors* fitted_graph = fitGraph(graphname, degree, source_file);
    output->Add(fitted_graph);
    legend->AddEntry(fitted_graph, fitted_graph->GetTitle(), "l");
  }
  output->Draw("AP");
  //c1->BuildLegend();
  legend->Draw();
  output->GetXaxis()->SetTitle((var + " Position/mm").c_str());
  out_file->WriteTObject(c1);
}

void multifits(std::string var) {
  
  TFile* source_file = new TFile(("output_graphs_"+var+".root").c_str(), "READ");
  TFile* out_file = new TFile(("MultipleFits_"+var+".root").c_str(), "recreate");

  GetMultiPlot(var + " Pos vs ke Bias", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs ke Resolution", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs x Bias", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs x Resolution", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs y Bias", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs y Resolution", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs z Bias", source_file, out_file, var);
  GetMultiPlot(var + " Pos vs z Resolution", source_file, out_file, var);

  source_file->Close();
  out_file->Close();
}
