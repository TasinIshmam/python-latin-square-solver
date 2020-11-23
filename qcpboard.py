

class QcpBoard: 
    
    def __init__(self, board) -> None: 
        self.board = board
        self.board_len = len(board)
        self.is_completed = False
        self.expanded_nodes = 0
        self.backtracks_done = 0
        self.variable_domain_map = {}    
    
    def set_variable_domains_all(self) -> None:
        for row in range(0, self.board_len):
            for col in range(0, self.board_len):
                self.variable_domain_map[(row,col)] = self.find_domain_for_variable(row, col)

    def _print_variable_domain_map(self) -> None:
        for pair in self.variable_domain_map.items():
            print(pair) 

    def find_domain_for_variable(self, row,  col) -> list: 
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
        
        # whatever is left in domain_set is the domain of the (x,y) on the board. 
        return list(domain_set)


            
        




    


        

        
    
            
        
         
        



    
