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
        The winning side and the number of remaining armies.
    """

    # Simulate a path
    outcomes = []
    success = True  # True if attacker wins
    for i, n_defence in enumerate(n_defence_list):
        if verbose:
            print(n_attack, n_defence_list)
        outcome = battle(n_attack, n_defence, verbose=False)
        outcomes.append(outcome)

        n_attack = outcome["armies"]["attack"]
        n_defence_list[i] = outcome["armies"]["defence"]

        if outcome["winner"]["defence"]:
            success = False
            break

    if verbose:
        print(n_attack, n_defence_list)
        if success:
            print("Attack succeeded.")
        else:
            print("Attack failed.")

    path_outcome = {"armies": {
        "attack": n_attack,
        "defence": n_defence_list}
    }

    if success:
        path_outcome["winner"] = {"attack": True, "defence": False}
    else:
        path_outcome["winner"] = {"attack": False, "defence": True}

    return path_outcome


def simulation(n_attack: int, n_defence_list: list, n_iter: int = 1000, verbose: bool = False) -> pd.DataFrame:
    """Simulate a path multiple times.

    Args:
        n_attack:       number of armies attacking.
        n_defence_list: list of number of armies defending.
        n_iter:         number of times to repeat simulation.
        verbose:        verbosity.

    Returns:
        Data frame with results of each path.
    """
    path_list = []
    for i in range(n_iter):
        path_outcome = path(n_attack=n_attack, n_defence_list=n_defence_list.copy(), verbose=False)

        if verbose:
            print(path_outcome)

        entry = {
            "n_attack": path_outcome["armies"]["attack"],
            "attack_wins": path_outcome["winner"]["attack"],
            "defence_wins": path_outcome["winner"]["defence"]
        }

        for step, n_defence in enumerate(path_outcome["armies"]["defence"]):
            key = "step_{:d}".format(step + 1)
            entry[key] = n_defence

        path_list.append(entry)

    outcomes = pd.DataFrame(path_list)
    return outcomes


def summarise_simulation(simulation_outcome: pd.DataFrame) -> dict:
    """Process simulation.

    Args:
        simulation_outcome:  result of simulation function.

    Returns:
        Dict with summary of a simulation: expected wins and expected number of armies.
    """
    summary = dict(pd.Series(np.mean(simulation_outcome, axis=0)).to_dict())
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
    print(path(10, [10, 1], False))
    simulation_outcome = simulation(10, [10, 1], 100, False)
    print(summarise_simulation(simulation_outcome))
    print(simulation_summary(10, [10, 1], 1000, False))
    return


if __name__ == "__main__":
    main()