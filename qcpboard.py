from typing import * 
from pprint import pprint 
import random 
from copy import deepcopy
import functools


class QcpBoard: 
    
    def __init__(self, board) -> None: 
        self.board = board
        self.original_board = deepcopy(board) 
        self.board_len = len(board)
        self.expanded_nodes = 0
        self.backtracks_done = 0
        self.variable_domain_map = {}  
        self.variable_dynamic_degree_map = {} 
        self.set_variable_domains_all()  
        self.set_dynamic_degree_all()
    

    def set_variable_domains_all(self) -> None:
        for row in range(0, self.board_len):
            for col in range(0, self.board_len):
                self.variable_domain_map[(row,col)] = self.find_domain_for_variable(row, col)



    def set_variable_domains_for_specific_row_col(self, row: int, col: int) -> None:
        # across row
        for idx in range(0, self.board_len):
            self.variable_domain_map[(row,idx)] = self.find_domain_for_variable(row,idx)

        # across col
        for idx in range(0, self.board_len):
            self.variable_domain_map[(idx,col)] = self.find_domain_for_variable(idx,col)

    def find_variable_with_smallest_domain_heuristic(self) -> Optional[tuple]:
        min_entry = (-1,-1)
        min_domain_size = self.board_len + 1

        for key, domain in self.variable_domain_map.items():
            if domain == [-1]:  # skip entries that are already filled up. 
                continue 

            if (len(domain) < min_domain_size): # found variable with smaller domain. 
                min_domain_size = len(domain)
                min_entry = key 

        if min_entry == (-1,-1): # No entries to add. 
            return None, None

        return min_entry, self.variable_domain_map[min_entry]
        

    def find_domain_for_variable(self, row: int,  col: int) -> list: 
        if not (0 <= row < self.board_len) or not (0 <= col < self.board_len) :
            raise Exception("Invalid row or col values. Row: " + str(row) + "Col: " + str(col))

        if self.board[row][col] != 0: # Value already set. So no point in calculating domain. 
            return [-1] #[-1] used to indicate board entry already assigned in variable domain map. 

        domain_set = set([idx for idx in range(1, self.board_len + 1)])

        ## iterate across fixed row/x axis
        for idx in range(0, self.board_len):
            if (idx == col): 
                continue
            if self.board[row][idx] in domain_set:
                domain_set.remove(self.board[row][idx])

        ## iterate across fixed colum/y axis
        for idx in range(0, self.board_len):
            if (idx == row): 
                continue
            if self.board[idx][col] in domain_set:
                domain_set.remove(self.board[idx][col])
        
        # whatever is left in domain_set is the domain of (x,y) on the board. 
        # note: domain set can be empty [] if there's no options 
        return list(domain_set)  

    def find_dynamic_degre_for_variable(self, row, col):
        dynamic_degree = 0
        #iterate across single row
        for idx in range(self.board_len):
            if idx != col and self.board[row][idx] == 0:
                dynamic_degree += 1
        #iterate across single column
        for idx in range(self.board_len):
            if idx != row and self.board[idx][col] == 0:
                dynamic_degree += 1

        return dynamic_degree
    
    def set_dynamic_degree_all(self):
        for row in range (self.board_len):
            for col in range (self.board_len):
                self.variable_dynamic_degree_map[(row,col)] = self.find_dynamic_degre_for_variable(row, col)

    def set_dynamic_degree_specific_row_col(self, row, col):
        # across row
        for idx in range(0, self.board_len):
            self.variable_dynamic_degree_map[(row,idx)] = self.find_dynamic_degre_for_variable(row,idx)

        # across col
        for idx in range(0, self.board_len):
            self.variable_dynamic_degree_map[(idx,col)] = self.find_dynamic_degre_for_variable(idx,col)
                
    def find_variable_with_brelaz_heuristic(self):
        # brelaz sorts by domain length, and then breaks ties with maximum dynamic degree. 
        variable_list = []

        for row in range (self.board_len):
            for col in range (self.board_len): 
                if self.board[row][col] == 0:
                    variable_list.append(((row,col), self.variable_domain_map[(row,col)], self.variable_dynamic_degree_map[(row,col)])) 
        
        if len(variable_list) == 0: # no unfilled variables. 
            return None, None 

        variable_list.sort(key = functools.cmp_to_key(QcpBoard.brelaz_comparator))

        return variable_list[0][0], variable_list[0][1] # return (row,col) , [domain_list]

    @staticmethod
    def brelaz_comparator (first, second):
        if len(first[1]) == len (second[1]):
            return  first[2] - second[2] ## Might be inaccurate. According to monmoy second - first hobe.
        else:
            return len(first[1]) - len(second[1])

            

    def set_variable_in_board(self, row: int, col: int, value: int):
        if not (0 <= row < self.board_len) or not (0 <= col < self.board_len) :
            raise Exception("Invalid row or col values. Row: " + str(row) + "Col: " + str(col))
       
        if self.board[row][col] != 0:
            raise Exception("Error. Trying to rewrite already existing variable. Row: " + str(row) + "Col: " + str(col))

        self.board[row][col] = value
        self.set_variable_domains_for_specific_row_col(row, col)
        self.set_dynamic_degree_specific_row_col(row, col)


    def reset_variable_in_board(self, row: int, col: int):
        if not (0 <= row < self.board_len) or not (0 <= col < self.board_len) :
            raise Exception("Invalid row or col values. Row: " + str(row) + "Col: " + str(col))
       
        if self.board[row][col] == 0:
            raise Exception("Error. Trying to reset already empty variable. Row: " + str(row) + "Col: " + str(col))

        self.board[row][col] = 0
        self.set_variable_domains_for_specific_row_col(row, col)
        self.set_dynamic_degree_specific_row_col(row, col)



    def is_complete(self) -> bool:
        for row in range(0, self.board_len):
            for col in range(0, self.board_len):
                if self.board[row][col] == 0:
                    return False
    
        return True 


    def _print_variable_domain_map(self) -> None:
        for pair in self.variable_domain_map.items():
            print(pair) 

    def print_state(self):
        # print("\n-----------Original Board State------------")
        # pprint(self.original_board)
        # print("-----------Original Board State------------\n")
        # print("-----------Current Board State------------")
        # pprint(self.board)
        # print("-----------Current Board State------------\n")
        print("Expanded Nodes: ", self.expanded_nodes)
        print("Backtracks Done: ", self.backtracks_done)
        print("\n")



    def solveSimpleBackTracking(self):
        if self.is_complete():
            return True
        
        min_entry, domain = self.find_variable_with_smallest_domain_heuristic()
        
        if min_entry is None:
            raise Exception("No domain entries found even though board is not complete.")

        self.expanded_nodes += 1

        if self.expanded_nodes % 10000 == 0:
            self.print_state()

        # random.shuffle(domain)
        for domain_choice in domain:
            if domain_choice == [-1]:
                raise Exception("Invalid domain marker [-1] added to domain map")

            self.set_variable_in_board(min_entry[0], min_entry[1], domain_choice)
            if self.solveSimpleBackTracking():
                return True
            else: #not sure if this should be here. 
                self.reset_variable_in_board(min_entry[0], min_entry[1])  #resetting domain_choice 
                self.backtracks_done += 1  # resetting a variable basically means going back/backtracking. 

        return False

            
    def reset_board(self) -> None:    # Sets board to original state. 
        self.board = deepcopy(self.original_board)
        self.expanded_nodes = 0
        self.backtracks_done = 0
        self.variable_domain_map = {}  
        self.set_variable_domains_all()  
           




    


        

        
    
            
        
         
        



    
