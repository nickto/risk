#!/usr/bin/env python
import numpy as np
import pandas as pd
from battle import battle


def path(n_attack: int, n_defence_list: list, verbose: bool = False) -> dict:
    """Simulate a path.

    Args:
        n_attack:       number of armies attacking.
        n_defence_list: list of number of armies defending.
        verbose:        verbosity.

    Returns:
        The list of outcomes of each individual battle.
    """

    # Simulate a path
    outcomes = []
    for i, n_defence in enumerate(n_defence_list):
        if verbose:
            print(n_attack, n_defence_list)
        outcome = battle(n_attack, n_defence, verbose=False)
        outcome["step"] = i + 1
        outcomes.append(outcome)

        n_attack = outcome["armies"]["attack"] - 1
        if n_attack < 0:
            n_attack = 0

    return outcomes


def simulation(n_attack: int, n_defence_list: list, n_iter: int = 1000, verbose: bool = False) -> pd.DataFrame:
    """Simulate a path multiple times.

    Args:
        n_attack:       number of armies attacking.
        n_defence_list: list of number of armies defending.
        n_iter:         number of times to repeat simulation.
        verbose:        verbosity.

    Returns:
        List of each path results.
    """
    outcomes = []
    for i in range(n_iter):
        outcome = path(n_attack=n_attack, n_defence_list=n_defence_list.copy(), verbose=False)
        outcomes.append(outcome)

        if verbose:
            print(outcome)

    return outcomes


def summarise_simulation(simulation_outcomes: list) -> dict:
    """Process simulation.

    Args:
        simulation_outcomes:  result of simulation function.

    Returns:
        Dict with summary of a simulation: expected wins and expected number of armies.
    """
    summary = np.zeros(shape=(len(simulation_outcomes[0]), 4))
    for outcome in simulation_outcomes:
        for i, step in enumerate(outcome):
            assert i + 1 == step["step"]
            summary[i, 0] += step["armies"]["attack"]
            summary[i, 1] += step["armies"]["defence"]
            summary[i, 2] += step["winner"]["attack"]
            summary[i, 3] += step["winner"]["defence"]
    summary = summary / len(simulation_outcomes)
    summary = pd.DataFrame(summary)
    summary.columns = ["n_attack", "n_defence", "attack_wins", "defence_wins"]
    summary.index += 1

    return summary


def simulation_summary(n_attack: int, n_defence_list: list, n_iter: int = 1000, verbose: bool = False) -> dict:
    """Simulate a path multiple times and summarise the results.

    Args:
        n_attack:       number of armies attacking.
        n_defence_list: list of number of armies defending.
        n_iter:         number of times to repeat simulation.
        verbose:        verbosity.
    Returns:
        Dict with summary of a simulation: expected wins and expected number of armies.
    """
    outcome = simulation(n_attack, n_defence_list, n_iter, verbose)

    return summarise_simulation(outcome)


def main():
    # print(path(10, [5, 5, 5], False))
    # simulation_outcomes = simulation(10, [10, 1], 100, False)
    # print(summarise_simulation(simulation_outcomes))
    print(simulation_summary(10, [2, 2, 2, 2, 2], 1000, False))
    return


if __name__ == "__main__":
    main()