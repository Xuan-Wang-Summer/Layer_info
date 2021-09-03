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
if os.path.isdir("./analysis/cycles") is False:
    os.mkdir("./analysis/cycles")
if os.path.isdir("./analysis/algorithm_computes") is False:
    os.mkdir("./analysis/algorithm_computes")
if os.path.isdir("./analysis/actual_computes") is False:
    os.mkdir("./analysis/actual_computes")
if os.path.isfile("./analysis/cycles/cycles.txt"):
    os.remove("./analysis/cycles/cycles.txt")
if os.path.isfile("./analysis/algorithm_computes/ag.txt"):
    os.remove("./analysis/algorithm_computes/ag.txt")
if os.path.isfile("./analysis/actual_computes/ac.txt"):
    os.remove("./analysis/actual_computes/ac.txt")
cycles_name = "./analysis/cycles/cycles.txt"
ag_name = "./analysis/algorithm_computes/ag.txt"
ac_name = "./analysis/actual_computes/ac.txt"

# Go through the file following the topological order
f_topo_order = open("topo_order.txt", "r")
char = f_topo_order.read(1)
fname = ""
run = 0
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
        print(command_source)
        os.system(command_source)
        run = run + 1
        # Rename and move the outcome to destination folder
        isFile = os.path.isfile("./timeloop-mapper.stats.txt")
        if isFile is True:
            result_name = "./analysis/%s.txt" % fname
            os.rename("./timeloop-mapper.stats.txt", result_name)
            # Analyze the outcome
            cycles_f = open(cycles_name, "a")
            ag_f = open(ag_name, "a")
            ac_f = open(ac_name, "a")
            analysis_file = open(result_name, "r")
            line = analysis_file.readline()
            num_line = 1
            while num_line <= 14:
                line = analysis_file.readline()
                num_line = num_line + 1
            # Write algorithm_computes
            ag_f.write(line)
            ag_f.close()
            line = analysis_file.readline()
            # Write cycles
            cycles_f.write(line)
            cycles_f.close()
            line = analysis_file.readline()
            # Write actual_computs
            ac_f.write(line)
            ac_f.close()
            analysis_file.close()
        fname = ""
    char = f_topo_order.read(1)
f_topo_order.close()
