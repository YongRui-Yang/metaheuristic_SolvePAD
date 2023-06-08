from board import Board
import random
def yield_make_path(start):
    # BFS 窮舉會有大量撞牆的解與回頭解
    path_list = []
    if start<=0:
        path_list.append(0)
        yield ''.join(str(x) for x in path_list)
    else:
        while start>0:
            tmpi = start%4
            path_list.append(tmpi)
            start = start//4
        yield ''.join(str(x) for x in path_list)
    while True:
        path_list[0] += 1
        # 檢查是否要進位
        checkid = 0
        while path_list[checkid]>=4:
            path_list[checkid]=0
            if checkid+1>=len(path_list):
                path_list.append(1)
            else:
                path_list[checkid+1]+=1
            checkid+=1
        yield ''.join(str(x) for x in path_list)

        
def main():
    seed_value = 11
    random.seed(seed_value)
    board = Board()
    board.initialize_board("DEDDEEBBEDFEBADCBAEFFAEDDFFEFB")
    best_path = "#"
    best_score = -1e10
    sol=yield_make_path(0)


    

    for i in range(100):
        
        path=next(sol)
        board.reset_board()
        board.make_move(0,0,path)
        score = board.cpmpute_scroce()
        if score>best_score:
            best_score = score
            best_path = path
            print(best_score)
             
    board.reset_board()
    board.make_move(0,0,best_path)
    board.cpmpute_scroce()
    board.display_board()
    
if __name__ == "__main__":
    main()