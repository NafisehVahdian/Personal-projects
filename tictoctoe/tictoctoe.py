import random


class TicTacToe:
    def __init__(self, ):
        self.board =  [' '] * 10   #list(map(str, range(10)))  # index 0 is unused
        self.player_turn = self.get_random_first_player()

    def get_random_first_player(self):
        return random.choice(['X', 'O'])

    def show_board(self):
        print('\n')
        print(self.board[1] + ' | ' + self.board[2] + ' | ' + self.board[3])
        print('---------')
        print(self.board[4] + ' | ' + self.board[5] + ' | ' + self.board[6])
        print('---------')
        print(self.board[7] + ' | ' + self.board[8] + ' | ' + self.board[9])        
        print('\n')


    def swap_player_turn(self):
        self.player_turn = 'O' if self.player_turn == 'X' else 'X'
        return self.player_turn
    

    def is_board_filled(self):
        return ' ' not in self.board[1:]
    
    def fix_spot(self, cell, player):
        self.board[cell] = player


    def has_player_won(self, player):
        win_combinations = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # horizontal
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # vertical
            (1, 5, 9), (3, 5, 7)              # diagonal
        ]   
        for combo in win_combinations:
            if all(self.board[cell] == player for cell in combo):
                return True
        return False
    def start(self):
        while True:
            self.show_board()
            print(f"Player {self.player_turn}'s turn. Choose a cell (1-9):")
            try:
                cell = int(input())
                if cell < 1 or cell > 9 or self.board[cell] != ' ':
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
                continue
            
            self.fix_spot(cell, self.player_turn)
            
            if self.has_player_won(self.player_turn):
                self.show_board()
                print(f"Player {self.player_turn} won!")
                break
            
            if self.is_board_filled():
                self.show_board()
                print("It's a draw!")
                break
            
            self.swap_player_turn()
            self.show_board()
            print(f"Player {self.player_turn}'s turn")
            cell = int(input('Enter a cell number (1-9): '))
            if self.board[cell] == ' ' and cell in range(1, 10):
                self.fix_spot(cell, self.player_turn)

                if self.has_player_won(self.player_turn):
                    self.show_board()
                    print(f"Player {self.player_turn} won!")

                    break
            elif self.is_board_filled():
                self.show_board()
                print("It's a draw!")
                break
            
            else:
                print("Invalid move. Try again.")
            self.swap_player_turn()
            


if __name__ == "__main__":
    game = TicTacToe()
    game.start()
