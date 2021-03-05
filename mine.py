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
    mine_values[0][8] = 'T'
    mine_values[0][0] = 'F'
    mine_values[0][2] = 'I'
    mine_values[2][1] = 'g'
    mine_values[2][3] = 'w'
    mine_values[4][0] = 'G'
    mine_values[7][1] = 'g'
    mine_values[8][0] = 'W'
    mine_values[8][4] = 'I'
    mine_values[6][8] = 'w'
    mine_values[2][6] = 'S'
    mine_values[2][7] = 'S'
    mine_values[2][8] = 'S'
    mine_values[3][6] = 'S'
    mine_values[3][7] = 'S'
    mine_values[3][8] = 'S'
    mine_values[4][6] = 'S'
    mine_values[4][7] = 'S'
    mine_values[4][8] = 'S'
    mine_values[5][6] = 'S'
    mine_values[5][7] = 'S'
    mine_values[5][8] = 'S'
        
    print_mines_layout()
    
    
