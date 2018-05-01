import numpy as np

def attack(n_attack, n_defence, verbose=False):

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

        # Remove the dice that playe
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


def main():
    attack(n_attack=6, n_defence=1, verbose=True)
    return


if __name__ == "__main__":
    main()