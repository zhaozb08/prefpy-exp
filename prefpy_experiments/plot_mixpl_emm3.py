import sys
import numpy as np
import matplotlib.pyplot as plt


def print_usage(argv0):
    print("USAGE: python3", argv0, "<error description> <# outer iterations 1> <# inner iterations 1> <# outer iterations 2> <# inner iterations 2> <error csv filename> <time csv filename> <previous error csv filename> <previous time csv filename> [output png filename]")
    sys.exit()

def plot_error_time_data(str_error_type,          # string, title of the error measure in use
                         emm1_outer,              # int, outer iterations
                         emm1_inner,              # int, outer iterations
                         emm2_outer,              # int, outer iterations
                         emm2_inner,              # int, outer iterations
                         error_results,           # error results
                         time_results,            # time results
                         orig_error_results,      # original GMM vs EMM error results
                         orig_time_results,       # original GMM vs EMM time results
                         emm1_error_results=None, # if not None, take the place of emm_new1 line
                         emm1_time_results=None,  # if not None, take the place of emm_new1 line
                         output_img_filename=None # output png filename
                        ):
    emm1_str = "EMM-"+str(emm1_outer)+"-"+str(emm1_inner)
    emm2_str = "EMM-"+str(emm2_outer)+"-"+str(emm2_inner)
    # Plot data
    fig = plt.figure(num=1, figsize=(1400/96, 500/96), dpi=96)
    plt.subplot(121)
    plt.title(str_error_type)
    plt.xlabel("n (votes)")
    gmm_line, = plt.plot(orig_error_results.T[0], orig_error_results.T[2], "bs", label="GMM")
    #emm_line, = plt.plot(orig_error_results.T[0], orig_error_results.T[2], "g^", label="EMM")
    emm_new1 = None # declare in enclosing scope before using
    emm_new2 = None # declare in enclosing scope before using
    if emm1_error_results is None or emm1_time_results is None:
        emm_new1, = plt.plot(error_results.T[0], error_results.T[1], "co", label=emm1_str)
        emm_new2, = plt.plot(error_results.T[0], error_results.T[2], "mH", label=emm2_str)
    else:
        emm_new1, = plt.plot(emm1_error_results.T[0], emm1_error_results.T[1], "co", label=emm1_str)
        emm_new2, = plt.plot(error_results.T[0], error_results.T[1], "mH", label=emm2_str)

    plt.subplot(122)
    plt.title("Time (seconds)")
    plt.xlabel("n (votes)")
    plt.plot(orig_time_results.T[0], orig_time_results.T[6], "bs", label="GMM")
    #plt.plot(orig_time_results.T[0], orig_time_results.T[4], "g^", label="EMM")
    if emm1_time_results is None or emm1_time_results is None:
        plt.plot(time_results.T[0], time_results.T[1], "co", label=emm1_str)
        plt.plot(time_results.T[0], time_results.T[2], "mH", label=emm2_str)
    else:
        plt.plot(emm1_time_results.T[0], emm1_time_results.T[1], "co", label=emm1_str)
        plt.plot(time_results.T[0], time_results.T[1], "mH", label=emm2_str)

    #fig.legend([gmm_line, emm_line, emm_new1, emm_new2], ["GMM", "EMM", "EMM-10-10", "EMM-5-10"], loc="center right")
    fig.legend([gmm_line, emm_new1, emm_new2], ["GMM", emm1_str, emm2_str], loc="center right")
    if output_img_filename is not None:
        plt.savefig(output_img_filename, dpi=96)
    else:
        plt.show()

def main(argv):
    if len(argv) < 10:
        print("Inavlid number of arguments provided")
        print_usage(argv[0])

    error_type = argv[1] # i.e. "MSE" or "WMSE"

    emm1_outer = int(argv[2])
    emm1_inner = int(argv[3])
    emm2_outer = int(argv[4])
    emm2_inner = int(argv[5])

    # Load data from file
    error_results = np.loadtxt(argv[6], delimiter=',')
    time_results = np.loadtxt(argv[7], delimiter=',')
    orig_error_results = np.loadtxt(argv[8], delimiter=',')
    orig_time_results = np.loadtxt(argv[9], delimiter=',')

    out_img = None
    if len(argv) >= 11:
        out_img = argv[10]

    plot_error_time_data(str_error_type=error_type,
                         emm1_outer=emm1_outer,
                         emm1_inner=emm1_inner,
                         emm2_outer=emm2_outer,
                         emm2_inner=emm2_inner,
                         error_results=error_results,
                         time_results=time_results,
                         orig_error_results=orig_error_results,
                         orig_time_results=orig_time_results,
                         output_img_filename=out_img
                        )


if __name__ == "__main__":
    main(sys.argv)
