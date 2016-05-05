import sys
import numpy as np
import matplotlib.pyplot as plt


def print_usage(argv0):
    print("USAGE: python3", argv0, "<error description> <error csv filename> <time csv filename> <previous error csv filename> <previous time csv filename> [output png filename]")
    sys.exit()

def plot_error_time_data(str_error_type,          # string, title of the error measure in use
                         error_results,           # error results
                         time_results,            # time results
                         orig_error_results,      # original GMM vs EMM error results
                         orig_time_results,       # original GMM vs EMM time results
                         output_img_filename=None # output png filename
                        ):
    # Plot data
    fig = plt.figure(num=1, figsize=(1400/96, 500/96), dpi=96)
    plt.subplot(121)
    plt.title(str_error_type)
    plt.xlabel("n (votes)")
    gmm_line, = plt.plot(orig_error_results.T[0], orig_error_results.T[2], "bs", label="GMM")
    #emm_line, = plt.plot(orig_error_results.T[0], orig_error_results.T[2], "g^", label="EMM-500")
    emm_new1, = plt.plot(error_results.T[0], error_results.T[1], "mH", label="EMM-100-2")
    plt.subplot(122)
    plt.title("Time (seconds)")
    plt.xlabel("n (votes)")
    plt.plot(orig_time_results.T[0], orig_time_results.T[6], "bs", label="GMM")
    #plt.plot(orig_time_results.T[0], orig_time_results.T[4], "g^", label="EMM-500")
    plt.plot(time_results.T[0], time_results.T[1], "mH", label="EMM-100-2")
    #fig.legend([gmm_line, emm_line, emm_new1], ["GMM", "EMM-500", "EMM-10-5"], loc="center right")
    fig.legend([gmm_line, emm_new1], ["GMM", "EMM-100-2"], loc="center right")
    if output_img_filename is not None:
        plt.savefig(output_img_filename, dpi=96)
    else:
        plt.show()

def main(argv):
    if len(argv) < 6:
        print("Inavlid number of arguments provided")
        print_usage(argv[0])

    error_type = argv[1] # i.e. "MSE" or "WMSE"

    # Load data from file
    error_results = np.loadtxt(argv[2], delimiter=',')
    time_results = np.loadtxt(argv[3], delimiter=',')
    orig_error_results = np.loadtxt(argv[4], delimiter=',')
    orig_time_results = np.loadtxt(argv[5], delimiter=',')

    out_img = None
    if len(argv) >= 7:
        out_img = argv[6]

    plot_error_time_data(str_error_type=error_type,
                         error_results=error_results,
                         time_results=time_results,
                         orig_error_results=orig_error_results,
                         orig_time_results=orig_time_results,
                         output_img_filename=out_img
                        )


if __name__ == "__main__":
    main(sys.argv)
