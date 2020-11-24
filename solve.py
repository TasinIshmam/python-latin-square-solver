#!/usr/bin/python3 
# Useful link: https://levelup.gitconnected.com/csp-algorithm-vs-backtracking-sudoku-304a242f96d0


import sys
from pprint import pprint
from qcpboard import QcpBoard

def read_input_board(casename):
    input_file = open("data/" + casename)

    if input_file is None:
        raise Exception("File not found: " + casename)

    input_lines = input_file.read().splitlines()

    n = input_lines[0].split('=')[1]   # "N=10;"" gets parsed to "10;"
    n =  int (n[:-1])  # n gets parsed to th integer value of 10. 

    board = []

    for idx in range(3, len(input_lines)):
        # remove non integer characters.
        line = input_lines[idx].replace('|','').replace('[','').replace(']','').replace(';','') 

        if(not line.strip()): # skip empty line
            continue

        # convert comma separated numbers into list 
        number_arr = [int(s.strip()) for s in line.split(',')]  

        board.append(number_arr)
    
    # pprint(board)
    return board

input_files = ['d-10-01.txt.txt', 'd-10-06.txt.txt', 'd-10-07.txt.txt', 'd-10-08.txt.txt', 'd-10-09.txt.txt']
input_files_2 = ['d-15-01.txt.txt']
for file_name in input_files_2:
    print(file_name)
    matrix = read_input_board(file_name)
    board = QcpBoard(matrix)
    board.solveSimpleBackTracking()
    board.print_state()

# def solveSimpleBackTracking(self):
#     location = self.getNextLocation()
#     if location is empty:
#         return True
#     else:
#         self.expandedNodes += 1
#         for choice in range(1,self.dim+1):
#             if self.isSafe(location[0],location[1],choice):  #location[0] is x, location[1] is y
#                 self.board[location[0]][location[1]] = str(choice)
#                 if self.solveSimpleBackTracking():
#                     return True
#                 self.board[location[0]][location[1]] = ‘0’  #resetting choice 
#     return False