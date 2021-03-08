import random
import os
from tabulate import tabulate

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
    n = 9
    numbers = [[0 for y in range(n)] for x in range(n)]
    mine_values = [[' ' for y in range(n)] for x in range(n)]

    #mine_values[3][5] = 'A'

    mine_values[0][0] = 'e'
    mine_values[0][8] = 'b'
    mine_values[8][0] = 'c'

    mine_values[2][3] = 'a'
    mine_values[6][8] = 'a'

    mine_values[0][2] = 'f'
    mine_values[8][4] = 'f'

    mine_values[2][1] = 'd'
    mine_values[7][1] = 'd'

    for r in range(2,6):
        for col in range(6,9):
            mine_values[r][col] = 's'

print_mines_layout()
#print(mine_values)
print()

l = [["a", "got_wood"], ["b", "used_toolshed"], ["c", "used_workbench"],["d", "got_grass"],
["e", "used_factory"], ["f", "got_iron"],["s","at_shelter"]]
table = tabulate(l, headers=['Propositions', 'Events'], tablefmt='orgtbl')
print(table)
print()

r, col = input("Enter a mine location for Agent: ").split()

if mine_values[int(r)][int(col)] == "a":
    print("Event Detected : got_wood")
if mine_values[int(r)][int(col)] == "b":
    print("Event Detected : used_toolshed")
if mine_values[int(r)][int(col)] == "c":
    print("Event Detected : used_workbench")
if mine_values[int(r)][int(col)] == "d":
    print("Event Detected : got_grass")
if mine_values[int(r)][int(col)] == "e":
    print("Event Detected : used_factory")
if mine_values[int(r)][int(col)] == "f":
    print("Event Detected : got_iron")
if mine_values[int(r)][int(col)] == "s":
    print("Event Detected : at_shelter")
mine_values[int(r)][int(col)]= "A"

print_mines_layout()

"""

if mine_values[int(r)][int(col)] != "a" and "b" and "c" and "d" and "e" and "f" and "s":
    print("Location Empty!")

l = [["a", "got_wood"], ["b", "used_toolshed"], ["c", "used_workbench"],["d", "got_grass"],
["e", "used_factory"], ["f", "got_iron"],["s","at_shelter"]]
table = tabulate(l, headers=['Propositions', 'Events'], tablefmt='orgtbl')
print(table)

"""
