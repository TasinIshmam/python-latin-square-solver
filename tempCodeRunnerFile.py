
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