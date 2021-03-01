import random
import os
def print_mines_layout():

    global mine_values
    global n

    print()
    print("\t\t\tMINECRAFT\n")

    st = "   "
    for i in range(n):
        st = st + "     " + str(i + 1)
    print(st)

    for r in range(n):
        st = "     "
        if r == 0:
            for col in range(n):
                st = st + "______"
            print(st)

        st = "     "
        for col in range(n):
            st = st + "|     "
        print(st + "|")

        st = "  " + str(r + 1) + "  "
        for col in range(n):
            st = st + "|  " + str(mine_values[r][col]) + "  "
        print(st + "|")

        st = "     "
        for col in range(n):
            st = st + "|_____"
        print(st + '|')

    print()

if __name__ == "__main__":

    # Size of grid
    n = 9
    # The actual values of the grid
    numbers = [[0 for y in range(n)] for x in range(n)]
    # The apparent values of the grid
    mine_values = [[' ' for y in range(n)] for x in range(n)]
    print_mines_layout()
    
