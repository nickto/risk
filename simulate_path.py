#!/usr/bin/env python
import argparse

import numpy as np
import pandas as pd

from risk.path import simulation_summary


def main():
    parser = argparse.ArgumentParser(description="Simulate and summarise results of a path.")

    parser.add_argument("-a", "--attack",
                        type=int,
                        metavar="N",
                        dest="n_attack",
                        required=True,
                        help="number of attacking armies.")
    parser.add_argument("-d", "--defence",
                        type=int,
                        metavar="N",
                        dest="n_defence",
                        required=True,
                        nargs="+",
                        help="list of defending armies.")
    parser.add_argument("-i", "--iter",
                        type=int,
                        metavar="N",
                        dest="iter",
                        default=1000,
                        help="Number of iterations in the simulation.")
    parser.add_argument("-o", "--out",
                        type=str,
                        metavar="FILE",
                        dest="fileout",
                        help="Output file.")

    args = parser.parse_args()

    summary = simulation_summary(args.n_attack, args.n_defence, n_iter=args.iter)
    print(summary)
    if args.fileout is not None:
        summary.to_csv(args.fileout, index=True)

    return


if __name__ == "__main__":
    main()