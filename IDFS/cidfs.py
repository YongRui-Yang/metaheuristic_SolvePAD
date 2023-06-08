from board import Board
import random

board = Board()
best_path = ""
best_score = 0
find_max_sol = 10000
find_sol = 0
def dfs_make_path(nowrow,nowcol,nowpath,targetlan):
    # DFS 窮舉解
    global find_sol
    if find_sol>=find_max_sol:
        return
    elif len(nowpath)==targetlan:
        global board,best_path,best_score
        find_sol +=1
        board.reset_board()
        board.make_move(0,0,nowpath)
        score = board.cpmpute_scroce()
        if score>best_score:
            best_score = score
            best_path = nowpath
            print(best_score)
    else:
        if len(nowpath)!=0:
            endstep = nowpath[-1]
        else:
            endstep = "#"
        # 0 上
        if nowrow+1<5 and endstep!="2":
            dfs_make_path(nowrow+1,nowcol,nowpath+'0',targetlan)
        # 1 右
        if nowcol+1<6 and endstep!="3":
            dfs_make_path(nowrow,nowcol+1,nowpath+'1',targetlan)
        # 2 下
        if nowrow-1>=0 and endstep!="0":
            dfs_make_path(nowrow-1,nowcol,nowpath+'2',targetlan)
        # 3 左
        if nowcol-1>=0 and endstep!="1":
            dfs_make_path(nowrow,nowcol-1,nowpath+'3',targetlan)
        
def main():
    seed_value = 11
    random.seed(seed_value)
    global board,best_path,best_score,find_sol
    board.initialize_board("DEDDEEBBEDFEBADCBAEFFAEDDFFEFB")
    
    # 進行c次 IDFS
    c = 3
    idfs_deepmax = 12
    for j in range(c):
        tmp_best_path = best_path
        tmp_best_score = best_score
        for i in range(1,idfs_deepmax):
            dfs_make_path(0,0,tmp_best_path,len(tmp_best_path)+i)
            find_sol = 0
        board.reset_board()
        board.make_move(0,0,best_path)
        board.cpmpute_scroce()
        board.display_board()
        print(len(best_path)-len(tmp_best_path),best_score-tmp_best_score)
    print(len(best_path),best_score)
if __name__ == "__main__":
    main()
