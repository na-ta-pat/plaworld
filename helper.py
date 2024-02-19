import numpy as np

move_l = [(0, 1),(-1, 0),(0, -1),(1, 0)]
def gen_move(x,y):
    return [(x+xx,y+yy) for xx,yy in move_l]

def gradient_path(array,exit=None,unwalkable=1,walkable=None):

    array = np.array(array)
    
    mask = np.zeros(array.shape)
    if unwalkable is not None:
        mask[array==unwalkable]= np.inf
    if walkable is not None:
        mask[:] = np.inf
        mask[array==walkable]=0

    arr = mask

    assert exit is not None
    
    l = [exit]
    x,y = exit
    arr[x,y] = 1
    cnt = 2
    cnt_log = 0
    while l:
        # print(cnt_log)
        next_l=[]
        while l:
            cnt_log +=1
            x,y = l.pop()
            for x,y in gen_move(x,y):
                if not 0<=x<arr.shape[0] or not 0<=y<arr.shape[1]:continue
                if not arr[x,y]:
                    arr[x,y] = cnt
                    next_l.append((x,y))
        
        l=next_l
        cnt+=1

    return arr
    

    

    




if __name__=="__main__":
    array = np.array([
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0]  # Exit is implicitly defined at (4, 4)
    ])
    exit = (4, 4)
    unwalkable = 1
    walkable = None  # This parameter is not used in this test case

    result = gradient_path(array, exit=exit, unwalkable=unwalkable, walkable=walkable)
    print(result)
