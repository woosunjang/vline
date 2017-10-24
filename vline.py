#!/usr/local/bin/python
import argparse
import numpy as np


def get_keyword_outcar(keyword):
    with open('OUTCAR', 'r') as out:
        for line in out:
            if keyword in line:
                return line.split()[2]


def vline_plotter(args):
    system_name = input("Please input the system name : ")

    if args.output is None:
        outname = "locpot.itx"
    else:
        outname = args.output + ".itx"

    efermi = float(get_keyword_outcar('E-fermi'))
    
    with open(args.input, "r") as data:
        vline_lines = data.readlines()
        vline_header = vline_lines.pop(0).split()

        if vline_header[1] == "1":
            direction = "x"
        elif vline_header[1] == "2":
            direction = "y"
        elif vline_header[1] == "3":
            direction = "z"
        else:
            raise ImportError("header line is damaged!")

        data_array = []

        for line in vline_lines:
            data_array.append(line.split())

        data_array = np.array(data_array)

        with open(outname, "w") as out:
            out.write("IGOR\n")
            out.write("WAVES/D " + system_name + "_" + direction + " " + system_name + "_locpot\n")
            out.write("BEGIN\n")
            
            # for line in vline_lines:
            #     out.write(line)

            for x in data_array:
                out.write(x[0])
                out.write(" ")

                if args.shift is True:
                    out.write(str(float(x[1]) - efermi))
                else:
                    out.write(x[1])
                out.write("\n")

            out.write("END\n")

            preset = """X ModifyGraph width=340.157,height=340.157
X ModifyGraph marker=19
X ModifyGraph lSize=1.5
X ModifyGraph tick=2
X ModifyGraph mirror=1
X ModifyGraph zero(bottom)=8
X ModifyGraph fSize=28
X ModifyGraph lblMargin(left)=15,lblMargin(bottom)=10
X ModifyGraph standoff=0
X ModifyGraph axThick=1.5
X ModifyGraph axisOnTop=1
X Label left "\\Z28 Local Potential (eV)"
X Label bottom "\\Z28 z (a.u)"
"""
    
            out.write("X Display " + system_name + "_locpot" + " vs " + system_name + "_" + direction + " as " + '"' +
                      system_name + "_locpot_" + direction + '"' + "\n")
            out.write(preset)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-i", dest="input", type=str, default="VLINE")
    parser.add_argument("-o", dest="output", type=str, default=None)
    parser.add_argument("-s", dest="shift", action="store_true")
    parser.set_defaults(func=vline_plotter)

    args = parser.parse_args()

    try:
        getattr(args, "func")
    except AttributeError:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
