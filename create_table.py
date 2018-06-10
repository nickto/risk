#!/usr/bin/env python
import argparse

import numpy as np
import pandas as pd

from risk.battle import simulation_summary


def reindex_from_one(array: np.array) -> pd.DataFrame:
    """Convert array to data frame and reindex from 1 (not from 0).

    Args:
        array: array to reindex.

    Returns:
        Reindexed data frame.
    """
    df = pd.DataFrame(array)
    df.columns = df.columns + 1
    df.index = df.index + 1
    return df


def get_summary_matrices(n_max: int = 10, n_iter: int = 1000) -> dict:
    """Run simulation for different combinations of armies and summarise results.

    Args:
        n_max:  maximum number of armies to consider.
        n_iter: number of times to repeat each simulation.

    Returns:
        Dict with matrices.
    """
    # Pre-allocate
    summaries = {
        "attack_wins": np.zeros(shape=(n_max, n_max)),
        "defence_wins": np.zeros(shape=(n_max, n_max)),
        "n_attack": np.zeros(shape=(n_max, n_max)),
        "n_defence": np.zeros(shape=(n_max, n_max)),
    }
    for key, value in summaries.items():
        summaries[key][:] = np.nan

    for n_attack in range(1, n_max + 1):
        for n_defence in range(1, n_max + 1):
            summary = simulation_summary(n_attack, n_defence, n_iter=n_iter)
            for key, value in summary.items():
                summaries[key][n_attack - 1, n_defence - 1] = value

    return summaries


def main():
    parser = argparse.ArgumentParser(description="Create table with probabilities of an attacker wining.")
    parser.add_argument("-m", "--max",
                        type=int,
                        metavar="N",
                        dest="max_armies",
                        default=20,
                        help="Max number of armies on each side.")
    parser.add_argument("-o", "--out",
                        type=str,
                        metavar="PREFIX",
                        dest="fileout",
                        help="Output file prefix (with path).")
    parser.add_argument("-i", "--iter",
                        type=int,
                        metavar="N",
                        dest="iter",
                        default=1000,
                        help="Number of iterations in the simulation.")
    args = parser.parse_args()

    summaries = get_summary_matrices(n_max=args.max_armies, n_iter=args.iter)

    print("Attack armies are in rows, defence armies are in columns")
    for key, summary in summaries.items():
        summary = reindex_from_one(summary)
        print("\n" + key + ":")
        print(summary)
        if args.fileout is not None:
            filename = "{prefix}_{suffix}.csv".format(prefix=args.fileout, suffix=key)
            summary.to_csv(filename, index=True)

    return


if __name__ == "__main__":
    main()