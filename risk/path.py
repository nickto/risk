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
        print(outcome)

        n_attack = outcome["armies"]["attack"]
        n_defence_list[i] = outcome["armies"]["defence"]

        print(n_attack, n_defence_list)

        if outcome["winner"]["defence"]:
            success = False
            break

    if verbose:
        print(n_attack, n_defence_list)
        if success:
            print("Attack succeeded.")
        else:
            print("Attack failed.")

    path_outcome = {
        "armies": {
            "attack": n_attack,
            "defence": n_defence_list
        },
        "attack_success": success
    }

    return path_outcome

def main():
    path(10, [5, 4], True)
    return


if __name__ == "__main__":
    main()