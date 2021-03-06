import os

# Prepare the enviorment for tiemeloop
os.system("scons -j4")
os.system("source env/setup-env.bash")

# Prepare the layout of folders
isDirR = os.path.isdir("./result")
isDirA = os.path.isdir("./analysis")
if isDirR is False:
    os.mkdir("./result")
if isDirA is False:
    os.mkdir("./analysis")
if os.path.isfile("./analysis/cycles.txt"):
    os.remove("./analysis/cycles.txt")
if os.path.isfile("./analysis/ag.txt"):
    os.remove("./analysis/ag.txt")
if os.path.isfile("./analysis/ac.txt"):
    os.remove("./analysis/ac.txt")
if os.path.isfile("./analysis/ac.txt"):
    os.remove("./analysis/energy.txt")
if os.path.isfile("./analysis/invalid.txt"):
    os.remove("./analysis/invalid.txt")
cycles_name = "./analysis/cycles.txt"
ag_name = "./analysis/ag.txt"
ac_name = "./analysis/ac.txt"
energy_name = "./analysis/energy.txt"
invalid_name = "./analysis/invalid.txt"

# Go through the file following the topological order
f_topo_order = open("topo_order.txt", "r")
char = f_topo_order.read(1)
fname = ""
while char:
    if char != " ":
        fname += char
    if char == " ":
        # Run timeloop on each problem
        in_name = "layer-info/%s.yaml" % fname
        out_name = "./result/%s.out" % fname
        command_source = "build/timeloop-mapper ./"
        command_source += in_name
        command_source += " > "
        command_source += out_name
        os.system(command_source)

        # Rename and move the outcome to destination folder
        isFile = os.path.isfile("./timeloop-mapper.stats.txt")
        if isFile is True:
            result_name = "./analysis/%s.txt" % fname
            os.rename("./timeloop-mapper.stats.txt", result_name)
            # Analyze the outcome
            cycles_f = open(cycles_name, "a")
            ag_f = open(ag_name, "a")
            ac_f = open(ac_name, "a")
            energy_f = open(energy_name, "a")
            analysis_file = open(result_name, "r")
            line = analysis_file.readline()
            num_line = 1
            while num_line <= 15:
                line = analysis_file.readline()
                num_line = num_line + 1
            
            # Write algorithm_computes
            cycles_f.write(line)
            cycles_f.close()
            line = analysis_file.readline()
            # Write cycles
            ag_f.write(line)
            ag_f.close()
            line = analysis_file.readline()
            # Write actual_computs
            ac_f.write(line)
            ac_f.close()
            # Write Energy
            line = analysis_file.readline()
            line = analysis_file.readline()
            line = analysis_file.readline()
            energy_f.write(line)
            energy_f.close()
            analysis_file.close()
            
        # Record the invalid files
        else:
            f_invalid = open(invalid_name, "a")
            invalid = "%s.txt" % fname
            f_invalid.write(invalid)
            f_invalid.close()            
        fname = ""
    char = f_topo_order.read(1)
f_topo_order.close()
