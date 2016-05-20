import sys
import time
import pickle
import numpy as np
from prefpy import plackettluce as pl
from prefpy import stats as stats
from prefpy import gmm_mixpl
from prefpy_experiments import plot_mixpl_gmm1 as plot
np.seterr(all='raise')


def print_usage(argv0):
    print("USAGE: python3", argv0, "<# of alternatives> <# of trials> <# of votes start> <# of votes end> <# votes step> <dataset input filename base> <wsse output filename.csv> <sse output filename.csv> <time output filename.csv> <plot output filename.png> <gmm results output filename.p>\n" +
          "    Notes:\n    All data files read from disk must be CSV format and have the explicit file extension '.csv'" +
          "    The dataset base file name given must be suffixed with an underscore, followed by padding zeros, and without the '.csv' extension (e.g. 'mixpl-dataset_000' where there are at most 999 'mixpl-dataset_<number>.csv' files in the same directory)")
    sys.exit()

def main(argv):
    if len(argv) != 12:
        print_usage(argv[0])
    m = int(argv[1]) # number of alternatives
    t = int(argv[2]) # (index + 1) of final dataset (number of datasets if base filename is 0...00)
    n_init = int(argv[3]) # initial experiment number of votes
    if not n_init > 0:
        print("Error: Starting number of votes must be greater than 0")
        print_usage(argv[0])
    n_stop = int(argv[4]) # final experiment number of votes
    if not n_stop > n_init:
        print("Error: Final number of votes must be greater than starting number of votes")
        print_usage(argv[0])
    n_step = int(argv[5]) # number of votes to increment by each time
    if not n_step > 0:
        print("Error: Step number of votes must be greater than 0")
        print_usage(argv[0])
    elif (n_stop - n_init) < n_step or (n_stop - n_init) % n_step != 0:
        print("Warning: Step number of votes doesn't fit range")
    p = ((n_stop - n_init) // n_step) + 1 # always positive and >= 1 by above

    # read in all data required for experiments
    print("Reading Datasets from Disk...")
    datasets = []
    data_filename_base = argv[6]
    d = int(data_filename_base.split("_")[-1])
    if d < 0:
        print("Error: dataset base file name must not contain a negative number")
        print_usage(argv[0])
    len_d = str(len(data_filename_base.split("_")[-1]))
    data_filename_base = "_".join(data_filename_base.split("_")[:-1])
    for i in range(t):
        infilename = data_filename_base + '_' + ("{0:0" + len_d + "d}").format(i + d) + ".csv"
        infile = open(infilename)
        datasets.append(pl.read_mix2pl_dataset(infile, numVotes=n_stop))

    # Check files can be written to later:
    wsse_filename = argv[7]
    wsse_file = open(wsse_filename, 'w')
    sse_filename = argv[8]
    sse_file = open(sse_filename, 'w')
    time_filename = argv[9]
    time_file = open(time_filename, 'w')
    plot_filename = argv[10]
    plot_file = open(plot_filename, 'w')
    gmm_solns_filename = argv[11]
    gmm_solns_file = open(gmm_solns_filename, 'wb') # writable binary mode

    wsse_res = np.empty((p, 2))
    sse_res = np.empty((p, 2))
    time_res = np.empty((p, 4))

    gmm_solns = []

    alts = np.arange(m)

    # initialize the aggregators for each class of algorithm
    print("Initializing Aggregator Classes...")
    gmmagg = gmm_mixpl.GMMMixPLAggregator(alts, use_matlab=True)

    print("Starting Experiments...")
    k_n = 0 # experiment index number
    for n in range(n_init, n_stop + 1, n_step): # for these numbers of agents
        print("n =", n)
        print("i =   ", end='')
        sys.stdout.flush()

        wsse_vals = np.empty((1,t))
        sse_vals = np.empty((1,t))
        time_vals = np.empty((3,t))

        for i in range(t):
            print("\b"*len(str(i-1)) + str(i), end='')
            sys.stdout.flush()

            # get data
            params, votes = datasets[i]
            votes_curr = votes[:n]

            # DEFAULT: top3_full GMM (20 moments)
            time_val = time.perf_counter()
            soln, t0, t1 = gmmagg.aggregate(##rankings = votes_curr,
                                            rankings = None, # for ground-truth empirical limit
                                            algorithm = "top3_full",
                                            epsilon = None,
                                            max_iters = None,
                                            approx_step = None,
                                            ##opto = "matlab_default",
                                            opto = "matlab_emp_default", # for ground-truth empirical limit
                                            ##true_params = None
                                            true_params = params # for ground-truth empirical limit
                                           )
            time_val = time.perf_counter() - time_val
            wsse_val = stats.mix2PL_wsse(params, soln, m)
            sse_val = stats.mix2PL_sse(params, soln, m)
            wsse_vals[0][i] = wsse_val
            sse_vals[0][i] = sse_val
            time_vals[0][i] = t0
            time_vals[1][i] = t1
            time_vals[2][i] = time_val
            gmm_result = gmm_mixpl.GMMMixPLResult(num_alts = m,
                                                  ##num_votes = n,
                                                  num_votes = 0, # ground-truth empirical limit
                                                  num_mix = 2,
                                                  true_params = params,
                                                  cond = "top3_full",
                                                  ##opto = "matlab_default",
                                                  opto = "matlab_emp_default",  # ground-truth empirical limit
                                                  soln_params = soln,
                                                  momnts_runtime = t0,
                                                  opto_runtime = t1,
                                                  overall_runtime = time_val
                                                 )
            gmm_solns.append(gmm_result)


        print()
        wsse_res[k_n][0] = n
        wsse_res[k_n][1] = np.mean(wsse_vals[0]) # GMM

        sse_res[k_n][0] = n
        sse_res[k_n][1] = np.mean(sse_vals[0]) # GMM

        time_res[k_n][0] = n
        time_res[k_n][1] = np.mean(time_vals[0]) # GMM t0 (moment-calc)
        time_res[k_n][2] = np.mean(time_vals[1]) # GMM t1 (optimization)
        time_res[k_n][3] = np.mean(time_vals[2]) # GMM overall time

        # write results intermediately after a full set of trials for each n
        pickle.dump(gmm_solns, gmm_solns_file)

        k_n += 1

    pickle.dump(gmm_solns, gmm_solns_file)
    gmm_solns_file.close()
    np.savetxt(wsse_filename, wsse_res, delimiter=',', newline="\r\n")
    wsse_file.close()
    np.savetxt(sse_filename, sse_res, delimiter=',', newline="\r\n")
    sse_file.close()
    np.savetxt(time_filename, time_res, delimiter=',', newline="\r\n")
    time_file.close()

    plot.plot_error_time_data(str_error_type="MSE",
                              error_results=sse_res,
                              time_results=time_res,
                              output_img_filename=plot_filename
                             )
    plot_file.close()


if __name__ == "__main__":
    main(sys.argv)
