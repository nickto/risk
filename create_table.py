import pandas as pd
import argparse

from risk.probabilities import get_attacker_winning_matrix

def main():
    parser = argparse.ArgumentParser(description="Create table with probabilities of an attacker wining.")
    parser.add_argument("-m", "--max",
                        type=int,
                        metavar="N",
                        dest="max_units",
                        default=20,
                        help="Max number of units on each side.")
    parser.add_argument("-o", "--out",
                        type=str,
                        metavar="FILE",
                        dest="fileout",
                        help="Output filename.")
    parser.add_argument("-i", "--iter",
                        type=int,
                        metavar="N",
                        dest="iter",
                        default=20,
                        help="Number of iterations in the sumulation.")
    args = parser.parse_args()

    probs = get_attacker_winning_matrix(max_units=args.max_units, n_iter=args.iter, verbose=True)
    probs = pd.DataFrame(probs)
    probs.columns = range(1, args.max_units + 1)
    probs.index = probs.index + 1

    print("\nNumber of attacking units are in rows, defending - in columns.")
    print(probs.round(3))

    if args.fileout is not None:
        print("Writing results to {:s}.".format(args.fileout))
        probs.to_csv(args.fileout)
    else:
        print("File name for output not specified.")
    return


if __name__ == "__main__":
    main()