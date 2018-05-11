#!/usr/bin/env python
import numpy as np
import progressbar


def dice_roll(n_attack: int, n_defence: int, verbose: bool = False) -> (int, int):
    """Simulate a single dice roll.

    Args:
        n_attack:  number of units attacking.
        n_defence: number of units defending.
        verbose:   verbosity.

    Returns:
        Tuple of the number of attacking and defending units after the dice roll.
    """
    if verbose:
        print("Before battle:")
        print("Units attacking: {},\tUnits defending {}.".format(n_attack, n_defence))

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
                print("Units attacking: {},\tUnits defending {}.".format(n_attack, n_defence))
            return n_attack, n_defence

        # Fight
        if dice_attack[0] > dice_defence[0]:
            if verbose:
                print("Attacker kills 1 unit.")
            n_defence -= 1
        else:
            n_attack -= 1
            if verbose:
                print("Defender kills 1 unit.")

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
                print("Units attacking: {},\tUnits defending {}.".format(n_attack, n_defence))
            return n_attack, n_defence

    if verbose:
        print("After battle:")
        print("Units attacking: {},\tUnits defending {}.".format(n_attack, n_defence))

    return n_attack, n_defence


def attacker_wins(n_attack: int, n_defence: int, verbose: bool = False) -> bool:
    """Simulate a battle till one side wins.

    Args:
        n_attack:  number of units attacking.
        n_defence: number of units defending.
        verbose:   verbosity.

    Returns:
        True if attacker wins.
     """

    roll_counter = 0
    while True:
        roll_counter += 1
        if verbose:
            print("\nDice roll: {}".format(roll_counter))

        n_attack, n_defence = dice_roll(n_attack, n_defence, verbose=verbose)

        if n_attack == 0 or n_defence == 0:
            break

    if n_attack == 0:
        winner = "defender"
    else:
        winner = "attacker"

    if verbose:
        print("\nBattle winner: {}.".format(winner))
        print("-" * 20 + "\n")

    if winner == "attacker":
        return True
    else:
        return False


def get_attacker_winning_probability(n_attack: int, n_defence: int, n_iter: int = 1000, verbose: bool = False) -> float:
    """Compute probability of attacker winning the battle.

    Args:
        n_attack:  number of units attacking.
        n_defence: number of units defending.
        n_iter:    number of iterations in the simulation.
        verbose:   verbosity.

    Returns:
        Probability of attacker winning.
    """

    attacker_victories = []
    for i in range(n_iter):
        attacker_victories.append(attacker_wins(n_attack, n_defence, verbose))

    prob = float(np.mean(attacker_victories))

    if verbose:
        print("Probability of attacker winning: {0:.2f}.".format(prob))

    return prob


def get_attacker_winning_matrix(max_units: int = 20, n_iter: int = 1000, verbose: bool = False) -> np.array:
    """Compute attacker winning probabilities for different number of attacking/defending units.

    Args:
        max_units:  maximum number of units on both sides.
        n_iter:     number of iterations in the simulation.
        verbose:    verbosity.

    Returns:
        Matrix with probability of attacker winning, attacker units are in rows.
    """

    probs = np.zeros((max_units, max_units))
    probs[:] = np.nan

    if verbose:
        counter = 0
        bar = progressbar.ProgressBar(max_value=max_units * max_units)

    for attacker_units in range(1, max_units + 1):
        for defender_units in range(1, max_units + 1):
            # print(attacker_units, defender_units, get_attacker_winning_probability(
            #     n_attack=attacker_units,
            #     n_defence=defender_units,
            #     n_iter=n_iter,
            #     verbose=False))
            probs[attacker_units - 1, defender_units - 1] = get_attacker_winning_probability(
                n_attack=attacker_units,
                n_defence=defender_units,
                n_iter=n_iter,
                verbose=False)

            if verbose:
                counter += 1
                bar.update(counter)

    return probs

def main():
    print("Probability of attacker winning: {0:.2f}.".
          format(get_attacker_winning_probability(n_attack=1, n_defence=1, n_iter=1000, verbose=False)))
    print("\nTable of probabilities:")
    print(get_attacker_winning_matrix(max_units=5, n_iter=100, verbose=False))
    return


if __name__ == "__main__":
    main()
