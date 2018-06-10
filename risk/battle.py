#!/usr/bin/env python
import numpy as np
import pandas as pd


def roll_dice(n_attack: int, n_defence: int, verbose: bool = False) -> (int, int):
    """Simulate a single dice roll.

    Args:
        n_attack:  number of armies attacking.
        n_defence: number of armies defending.
        verbose:   verbosity.

    Returns:
        Tuple of the number of attacking and defending armies after the dice roll.
    """
    if verbose:
        print("Before battle:")
        print("Armies attacking: {},\tArmies defending {}.".format(n_attack, n_defence))

    # Throw dice
    dice_attack = np.random.randint(low=1, high=6, size=np.min([3, n_attack]))
    dice_defence = np.random.randint(low=1, high=6, size=np.min([2, n_defence]))

    dice_attack = np.flip(np.sort(dice_attack), axis=0)
    dice_defence = np.flip(np.sort(dice_defence), axis=0)

    if verbose:
        print("Attacking dice: " + str(list(dice_attack)) + "\tDefending dice: " + str(list(dice_defence)))

    for i in range(2):
        # Check that both arrays of dice results are not empty
        if dice_attack.shape[0] == 0 or dice_defence.shape[0] == 0:
            if verbose:
                print("Ran out of dice.")
                print("After battle:")
                print("Armies attacking: {},\tArmies defending {}.".format(n_attack, n_defence))
            return n_attack, n_defence

        # Fight
        if dice_attack[0] > dice_defence[0]:
            if verbose:
                print("Attacker kills 1 army")
            n_defence -= 1
        else:
            n_attack -= 1
            if verbose:
                print("Defender kills 1 army")

        # Remove one dice from each side that has just played
        dice_attack = dice_attack[1:]
        dice_defence = dice_defence[1:]

        # Check if one of the sides is dead
        if n_attack == 0 or n_defence == 0:
            if verbose:
                if n_attack == 0:
                    print("Attacker is dead.")
                else:
                    print("Defender is dead.")
                print("After battle:")
                print("Armies attacking: {},\tArmies defending {}.".format(n_attack, n_defence))
            return n_attack, n_defence

    if verbose:
        print("After battle:")
        print("Armies attacking: {},\tArmies defending {}.".format(n_attack, n_defence))

    return n_attack, n_defence


def battle(n_attack: int, n_defence: int, verbose: bool = False) -> dict:
    """Simulate a battle till one side wins.

    Args:
        n_attack:  number of armies attacking.
        n_defence: number of armies defending.
        verbose:   verbosity.

    Returns:
        The winning side and the number of remaining armies.
    """

    roll_counter = 0
    while True:
        roll_counter += 1
        if verbose:
            print("\nDice roll: {}".format(roll_counter))

        n_attack, n_defence = roll_dice(n_attack, n_defence, verbose=verbose)

        if n_attack == 0 or n_defence == 0:
            break

    if n_attack == 0:
        winner = "defender"
    else:
        winner = "attacker"

    if verbose:
        print("\nBattle winner: {}. N attack: {}, N defence: {}".format(winner, n_attack, n_defence))
        print("-" * 20 + "\n")

    outcome = {"armies": {
        "attack": n_attack,
        "defence": n_defence}
    }
    if winner == "attacker":
        outcome["winner"] = {"attack": True, "defence": False}
    else:
        outcome["winner"] = {"attack": False, "defence": True}

    return outcome


def simulation(n_attack: int, n_defence: int, n_iter: int = 1000, verbose: bool = False) -> pd.DataFrame:
    """Simulate a battle multiple times.

    Args:
        n_attack:  number of armies attacking.
        n_defence: number of armies defending.
        n_iter:    number of times to repeat simulation.
        verbose:   verbosity.

    Returns:
        Data frame with results of each battle.
    """
    battle_list = []
    for i in range(n_iter):
        battle_outcome = battle(n_attack=n_attack, n_defence=n_defence, verbose=verbose)
        battle_list.append({
            "n_attack": battle_outcome["armies"]["attack"],
            "n_defence": battle_outcome["armies"]["defence"],
            "attack_wins": battle_outcome["winner"]["attack"],
            "defence_wins": battle_outcome["winner"]["defence"]
        })
    outcomes = pd.DataFrame(battle_list)
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


def simulation_summary(n_attack: int, n_defence: int, n_iter: int = 1000, verbose: bool = False) -> dict:
    """Simulate a battle multiple times and summarise the results.

    Args:
        n_attack:  number of armies attacking.
        n_defence: number of armies defending.
        n_iter:    number of times to repeat a simulation.
        verbose:   verbosity.

    Returns:
        Dict with summary of a simulation: expected wins and expected number of armies.
    """
    outcome = simulation(n_attack, n_defence, n_iter, verbose)

    return summarise_simulation(outcome)


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
    # print(roll_dice(n_attack=5, n_defence=5, verbose=True))
    # print(battle(n_attack=5, n_defence=5, verbose=True))
    # print(simulation(n_attack=10, n_defence=1, n_iter=100))
    print(simulation_summary(n_attack=5, n_defence=5))
    # print(get_summary_matrices(n_max=5, n_iter=1000))
    return


if __name__ == "__main__":
    main()
