#!/usr/bin/python3 

import sys
from pprint import pprint
from qcpboard import QcpBoard
from config import Config 

def read_input_board(casename):
    input_file = open("data/" + casename)

    if input_file is None:
        raise Exception("File not found: data/" + casename)

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

# grid sized 10
input_files = ['d-10-01.txt.txt', 'd-10-06.txt.txt', 'd-10-07.txt.txt', 'd-10-08.txt.txt', 'd-10-09.txt.txt'] 
# grid sized 15
input_files_2 = ['d-15-01.txt.txt'] 
# all cases 
input_files_all = input_files + input_files_2 

print("Using algorithm: " + Config.algorithm + "\n")
print("Using variable ordering heuristic: " + Config.variable_ordering + "\n")



for file_name in input_files_all:
    print(file_name)
    matrix = read_input_board(file_name)
    board = QcpBoard(matrix)

    if Config.algorithm == Config.algorithm_choices[1]:
        board.solve_forward_checking()
    elif Config.algorithm == Config.algorithm_choices[0]:
        board.solve_backtracking() 
    else:
        raise Exception("No valid algorithm specified")
    board.print_state()

