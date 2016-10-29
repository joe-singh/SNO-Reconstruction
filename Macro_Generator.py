#!/usr/bin/env python
"""Call in command line by using python3 Macro_Generator.py "file-name".txt.
Outputs .mac files for use with rat, stored in folders called 'x_Macros',
'y_Macros', 'z_Macros' in the directory. If these already exist, the created
macros are added to them."""

import os
from sys import argv
b = str(argv[1])
args_list = []
for line in open(b):
    args_list += [line.split()]
params = {}
for arg_pair in args_list:
    if arg_pair[0] == 'filepath':
        params[arg_pair[0]] = arg_pair[1]
    else:
        params[arg_pair[0]] = eval(arg_pair[1])

try:
    path = params["filepath"]
    x_min = params["xmin"]
    x_max = params["xmax"]
    dx = params["xstep"]
    x_steps = 0 if dx == 0 else (x_max - x_min)/dx

    y_min = params["ymin"]
    y_max = params["ymax"]
    dy = params["ystep"]
    y_steps = 0 if dy == 0 else (y_max - y_min)/dy

    z_min = params["zmin"]
    z_max = params["zmax"]
    dz = params["zstep"]
    z_steps = 0 if dz == 0 else (z_max - z_min)/dz

    e_min = params["kemin"]
    e_max = params["kemax"]
    de = params["kestep"]
    e_steps = 0 if de == 0 else (e_max - e_min)/de

    n = params["runs"]
except KeyError as e:
    print("Missing value for " + str(e) + ". Program terminated.")
    os._exit(-1)

def write_to_file_x(path):
    """A function to write macros for changing x values to an output directory
    called x_Macros."""
    path1 = path + "/x_Macros"
    if not os.path.exists(path1):
        os.mkdir(path1)
    for e in range(int(e_steps)+1):
        filename = "x%sy0z0ke%s.mac" %(dx*x + x_min, e*de + e_min)
        path = path1
        fullpath = os.path.join(path, filename)
        f = open(fullpath, "w")
        f.write('/rat/physics_list/OmitMuonicProcesses true\n')
        f.write("/rat/physics_list/OmitHadronicProcesses true \n")
        f.write("\n")
        f.write("\n")
        f.write('/rat/db/set DETECTOR geo_file "geo/snoplus.geo"\n')
        f.write('/rat/db/set GEO[scint] material "labppo_scintillator"\n')
        f.write('/rat/db/set DAQ dqxx_info 0\n')
        f.write("/run/initialize \n")
        f.write("\n")
        f.write("\n")
        f.write("/rat/proc frontend\n")
        f.write("/rat/proc trigger\n")
        f.write("/rat/proc eventbuilder\n")
        f.write("/rat/proc count\n")
        f.write("/rat/procset update 100\n")
        f.write("/rat/proc calibratePMT\n")
        f.write("/rat/proc scintFitter\n")
        f.write("/rat/proclast outroot\n")
        f.write('/rat/procset file "x%sy0z0ke%s.root"\n' %(dx*x + x_min, e*de + e_min))
        f.write("\n")
        f.write("\n")
        f.write("/generator/add combo gun:point:poisson\n")
        f.write("# want random, isotropic momentum distribution; energy given in MeV\n")
        f.write("/generator/vtx/set e- 0 0 0 %s\n" %(e*de + e_min))
        f.write("# position given in Cartesians, relative to detector center, in mm\n")
        f.write("/generator/pos/set %s 0 0\n" % (dx*x + x_min))
        f.write("/generator/rate/set 1\n")
        f.write("\n")
        f.write("\n")
        f.write("/rat/run/start %s\n" %(n))
        f.write("exit")

def write_to_file_y(path):
    """A function to write macros for changing x values to an output directory
    called y_Macros."""
    path1 = path + "/y_Macros"
    if not os.path.exists(path1):
        os.mkdir(path1)
    for e in range(int(e_steps)+1):
        filename = "x0y%sz0ke%s.mac" %(dy*y + y_min, e*de + e_min)
        path = path1
        fullpath = os.path.join(path, filename)
        f = open(fullpath, "w")
        f.write('/rat/physics_list/OmitMuonicProcesses true\n')
        f.write("/rat/physics_list/OmitHadronicProcesses true \n")
        f.write("\n")
        f.write("\n")
        f.write('/rat/db/set DETECTOR geo_file "geo/snoplus.geo"\n')
        f.write('/rat/db/set GEO[scint] material "labppo_scintillator"\n')
        f.write('/rat/db/set DAQ dqxx_info 0 \n')
        f.write("/run/initialize \n")
        f.write("\n")
        f.write("\n")
        f.write("/rat/proc frontend\n")
        f.write("/rat/proc trigger\n")
        f.write("/rat/proc eventbuilder\n")
        f.write("/rat/proc count\n")
        f.write("/rat/procset update 100\n")
        f.write("/rat/proc calibratePMT\n")
        f.write("/rat/proc scintFitter\n")
        f.write("/rat/proclast outroot\n")
        f.write('/rat/procset file "x0y%sz0ke%s.root"\n' %(dy*y + y_min, e*de + e_min))
        f.write("\n")
        f.write("\n")
        f.write("/generator/add combo gun:point:poisson\n")
        f.write("# want random, isotropic momentum distribution; energy given in MeV\n")
        f.write("/generator/vtx/set e- 0 0 0 %s\n" %(e*de + e_min))
        f.write("# position given in Cartesians, relative to detector center, in mm\n")
        f.write("/generator/pos/set 0 %s 0\n" % (dy*y + y_min))
        f.write("/generator/rate/set 1\n")
        f.write("\n")
        f.write("\n")
        f.write("/rat/run/start %s\n" %(n))
        f.write("exit")

def write_to_file_z(path):
    """A function to write macros for changing x values to an output directory
    called z_Macros."""
    path1 = path + "/z_Macros"
    if not os.path.exists(path1):
        os.mkdir(path1)
    for e in range(int(e_steps)+1):
        filename = "x0y0z%ske%s.mac" %(dz*z + z_min, e*de + e_min)
        path = path1
        fullpath = os.path.join(path, filename)
        f = open(fullpath, "w")
        f.write('/rat/physics_list/OmitMuonicProcesses true\n')
        f.write("/rat/physics_list/OmitHadronicProcesses true \n")
        f.write("\n")
        f.write("\n")
        f.write('/rat/db/set DETECTOR geo_file "geo/snoplus.geo"\n')
        f.write('/rat/db/set GEO[scint] material "labppo_scintillator"\n')
        f.write('/rat/db/set DAQ dqxx_info 0 \n')
        f.write("/run/initialize \n")
        f.write("\n")
        f.write("\n")
        f.write("/rat/proc frontend\n")
        f.write("/rat/proc trigger\n")
        f.write("/rat/proc eventbuilder\n")
        f.write("/rat/proc count\n")
        f.write("/rat/procset update 100\n")
        f.write("/rat/proc calibratePMT\n")
        f.write("/rat/proc scintFitter\n")
        f.write("/rat/proclast outroot\n")
        f.write('/rat/procset file "x0y0z%ske%s.root"\n' %(dz*z + z_min, e*de + e_min))
        f.write("\n")
        f.write("\n")
        f.write("/generator/add combo gun:point:poisson\n")
        f.write("# want random, isotropic momentum distribution; energy given in MeV\n")
        f.write("/generator/vtx/set e- 0 0 0 %s\n" %(e*de + e_min))
        f.write("# position given in Cartesians, relative to detector center, in mm\n")
        f.write("/generator/pos/set 0 0 %s\n" % (dz*z + z_min))
        f.write("/generator/rate/set 1\n")
        f.write("\n")
        f.write("\n")
        f.write("/rat/run/start %s\n" %(n))
        f.write("exit")

for x in range(int(x_steps)+1):
    write_to_file_x(path)
for y in range(int(y_steps)+1):
    write_to_file_y(path)
for z in range(int(z_steps)+1):
    write_to_file_z(path)
