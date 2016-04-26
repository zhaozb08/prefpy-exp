import sys
import numpy as np
import matplotlib.pyplot as plt


def print_usage(argv0):
    print("USAGE: python3", argv0, "<error description> <error csv filename> <time csv filename> [output png filename]")
    sys.exit()

def plot_error_time_data(str_error_type,          # string, title of the error measure in use
                         error_results,           # error results
                         time_results,            # time results
                         orig_error_results,      # original GMM vs EMM error results
                         orig_time_results,       # original GMM vs EMM time results
                         emm1_error_results=None, # if not None, take the place of emm_new1 line
                         emm1_time_results=None,  # if not None, take the place of emm_new1 line
                         output_img_filename=None # output png filename
                        ):
    # Plot data
    fig = plt.figure(num=1, figsize=(1400/96, 500/96), dpi=96)
    plt.subplot(121)
    plt.title(str_error_type)
    plt.xlabel("n (votes)")
    gmm_line, = plt.plot(orig_error_results.T[0], orig_error_results.T[1], "bs", label="GMM")
    emm_line, = plt.plot(orig_error_results.T[0], orig_error_results.T[2], "g^", label="EMM")
    emm_new1 = None # declare in enclosing scope before using
    emm_new2 = None # declare in enclosing scope before using
    if emm1_error_results is None or emm1_time_results is None:
        emm_new1, = plt.plot(error_results.T[0], error_results.T[1], "co", label="EMM-10-10")
        emm_new2, = plt.plot(error_results.T[0], error_results.T[2], "mH", label="EMM-5-10")
    else:
        emm_new1, = plt.plot(emm1_error_results.T[0], emm1_error_results.T[1], "co", label="EMM-10-10")
        emm_new2, = plt.plot(error_results.T[0], error_results.T[1], "mH", label="EMM-5-10")

    plt.subplot(122)
    plt.title("Time (seconds)")
    plt.xlabel("n (votes)")
    plt.plot(orig_time_results.T[0], orig_time_results.T[3], "bs", label="GMM")
    plt.plot(orig_time_results.T[0], orig_time_results.T[4], "g^", label="EMM")
    if emm1_time_results is None or emm1_time_results is None:
        plt.plot(time_results.T[0], time_results.T[1], "co", label="EMM-10-10")
        plt.plot(time_results.T[0], time_results.T[2], "mH", label="EMM-5-10")
    else:
        plt.plot(emm1_time_results.T[0], emm1_time_results.T[1], "co", label="EMM-10-10")
        plt.plot(time_results.T[0], time_results.T[1], "mH", label="EMM-5-10")

    fig.legend([gmm_line, emm_line, emm_new1, emm_new2], ["GMM", "EMM", "EMM-10-10", "EMM-5-10"], loc="center right")
    if output_img_filename is not None:
        plt.savefig(output_img_filename, dpi=96)
    else:
        plt.show()

def main(argv):
    if len(argv) < 4:
        print("Inavlid number of arguments provided")
        print_usage(argv[0])

    error_type = argv[1] # i.e. "MSE" or "WMSE"

    # Load data from file
    error_results = np.loadtxt(argv[2], delimiter=',')
    time_results = np.loadtxt(argv[3], delimiter=',')

    out_img = None
    if len(argv) >= 5:
        out_img = argv[4]

    plot_error_time_data(str_error_type=error_type,
                         error_results=error_results,
                         time_results=time_results,
                         output_img_filename=out_img
                        )


if __name__ == "__main__":
    main(sys.argv)
