import random
from collections import deque

class Board:
    def __init__(self, rows=5, cols=6):
        # 初始化遊戲盤面
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]

    def initialize_board(self,initstring=None):
        # 實現遊戲盤面的初始化邏輯
        if initstring is None:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.board[row][col] = self.generate_random_gem()
        else:
            
            if len(initstring)==self.rows*self.cols:
                for row in range(self.rows):
                    for col in range(self.cols):
                        self.board[row][col] = initstring[col+row*self.cols]
            else:
                print("error",len(initstring),self.rows*self.cols)

    def generate_random_gem(self):
        # 生成隨機珠子的邏輯，這裡假設有6種不同的珠子
        gem_types = ["A", "B", "C", "D", "E", "F"]
        return random.choice(gem_types)

    def display_board(self):
        # 顯示遊戲盤面的當前狀態
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is None:
                    print("-", end=" ")
                else:
                    print(self.board[row][col], end=" ")
            print()  # 換行

    def is_valid_move(self, row, col):
        # 檢查移動是否有效
        pass

    def make_move(self, row, col):
        # 實現移動操作
        pass

    def check_matches(self):
        matches = []

        # 檢查橫向匹配
        for row in range(self.rows):
            for col in range(self.cols - 2):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] != None:
                    matches.append((row, col))
                    matches.append((row, col + 1))
                    matches.append((row, col + 2))

        # 檢查縱向匹配
        for col in range(self.cols):
            for row in range(self.rows - 2):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] != None:
                    matches.append((row, col))
                    matches.append((row + 1, col))
                    matches.append((row + 2, col))

        return matches

    def remove_matches(self):
        combo_count = 0     # 連擊數量
        ball_count = 0      # 珠子數量
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        matches = self.check_matches()
        for row, col in matches:
            if not visited[row][col]:
                color = self.board[row][col]
                combo_count += 1

                # 使用BFS來搜索連擊珠子
                queue = deque([(row, col)])
                visited[row][col] = True

                while queue:
                    current_row, current_col = queue.popleft()

                    # 檢查四個方向的相鄰珠子
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = current_row + dr, current_col + dc

                        # 檢查邊界和顏色是否相同
                        if 0 <= new_row < self.rows and 0 <= new_col < self.cols and not visited[new_row][new_col] and self.board[new_row][new_col] == color and (new_row,new_col) in matches:
                            queue.append((new_row, new_col))
                            visited[new_row][new_col] = True
                            

                            # 在這裡你可以根據需要執行其他操作，比如增加分數等

        # 將連擊珠子設置為None
        for r in range(self.rows):
            for c in range(self.cols):
                if visited[r][c]:
                    self.board[r][c] = None
                    ball_count += 1
        
        print(combo_count,ball_count)
        return combo_count,ball_count

    def fill_board(self):
        for col in range(self.cols):
            empty_cells = 0
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] is None:
                    empty_cells += 1
                elif empty_cells > 0:
                    self.board[row + empty_cells][col] = self.board[row][col]
                    self.board[row][col] = None



    def play_game(self):
        # 遊戲主循環
        pass


def main():
    seed_value = 1234
    random.seed(seed_value)
    board = Board()
    board.initialize_board()
    board.display_board()
    print("----------------------------")
    
    board.remove_matches()
    board.display_board()
    print("----------------------------")

    
if __name__ == "__main__":
    main()