#include <string>
#include <iostream>
std::string correctedName(std::string name) {
 for(std::string::iterator it = name.begin(); it != name.end(); ++it) {
  if (*it == ' ') {*it = '_';}
 } 
std::cout << name << std::endl;
 return name;
}

void convert(std::string graphname, TFile* source) {
 TCanvas* canvas = (TCanvas*) source->Get(graphname.c_str());
 canvas->SaveAs((correctedName(graphname)+".pdf").c_str());
}

void PDFConverter(std::string var) {
 TFile* source = new TFile(("MultipleFits_"+ var + ".root").c_str(), "READ");
 convert(var + " Pos vs x Bias",source);
 convert(var + " Pos vs x Resolution",source);
 convert(var + " Pos vs y Bias",source);
 convert(var + " Pos vs y Resolution",source);
 convert(var + " Pos vs y Bias",source);
 convert(var + " Pos vs z Bias",source);
 convert(var + " Pos vs z Resolution",source);
 convert(var + " Pos vs ke Bias",source);
 convert(var + " Pos vs ke Resolution",source);

}
