import numpy as np

from helper import gradient_path

class Board:
    def __init__(self, width=100, height=100, *a, **k ):
        """Initialize the board with dimensions and cell size."""
        self.width = width
        self.height = height
        mid_height = height//2
        self.entrance_pos = mid_height,0
        self.exit_pos = mid_height,width-1
        self.walkable_array = np.zeros((height,width,))
        self.update_walk_guide_array()
        
    def update_walk_guide_array(self,gradient_array=None):
        if gradient_array is None:
            gradient_array = gradient_path(self.walkable_array,self.exit_pos,unwalkable=1)
        self.walk_guide_array = gradient_array
        
def grid_dfs(grid, entry, exit):
    stack, visited = [entry], {entry}
    while stack:
        x, y = stack.pop()
        if (x, y) == exit: return True
        for dx, dy in [(0,1),(0,-1),(-1,0),(1,0)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<len(grid) and 0<=ny<len(grid[0]) and grid[nx][ny] is None and (nx, ny) not in visited:
                stack.append((nx, ny))
                visited.add((nx, ny))
    return False

        
class GridBoard(Board):
    def __init__(self, cell_size=(10,10) ,*a,**k):
        super().__init__(*a,**k)
        self.cell_size = cell_size
        self.cell_size_width,self.cell_size_height = cell_size
        self.tower_array = [[None]*self.cell_size_width for i in range(self.cell_size_height)]
        self.walkable_array[:] = 1
        self.walkable_array[:,self.grid_width//2::self.grid_width]=0
        self.walkable_array[self.grid_height//2::self.grid_height,::]=0
        top,left,buttom,right = self.get_grid_bounding_box(*self.entrance_grid)
        self.walkable_array[top:buttom,left:right] = 0
        top,left,buttom,right = self.get_grid_bounding_box(*self.exit_grid)
        self.walkable_array[top:buttom,left:right] = 0
        self.update_walk_guide_array()

    def placable(self,h,w):
        if (h,w) == self.entrance_grid:return False
        if (h,w) == self.exit_grid:return False
        if self.tower_array[h][w] is not None:return False
        return True

    def add_tower(self,h,w,tower_data):
        if self.placable(h,w):
            top,left,buttom,right = self.get_grid_bounding_box(h,w)
            tmp = self.walkable_array.copy()
            tmp[top:buttom,left:right] = 1
            entrance_h,entrance_w = self.entrance_pos
            gradient_array = gradient_path(tmp,self.exit_pos,unwalkable=1)
            if gradient_array[entrance_h,entrance_w]==0:return False
            self.walkable_array[:] = tmp
            self.tower_array[h][w] = tower_data
            self.update_walk_guide_array(gradient_array)
            return True
        else:return False
        
    def get_grid_from_pos(self,h,w):
        return h//self.grid_height,w//self.grid_width
    def get_pos_from_grid(self,y,x):
        return y*self.grid_height,x*self.grid_width
    def get_grid_bounding_box(self,y,x):
        top,left = self.get_pos_from_grid(y,x)
        buttom,right = top+self.grid_height,left+self.grid_width
        return top,left,buttom,right
    def get_occupied_grid_array(self):
        return [[None if self.tower_array[i][j] is None else True for j in range(self.cell_size_width)] for i in range(self.cell_size_height)]
    @property
    def grid_width(self):
        return self.width//self.cell_size_width
    @property
    def grid_height(self):
        return self.height//self.cell_size_height
    @property
    def entrance_grid(self):
        return self.get_grid_from_pos(*self.entrance_pos)
    @property
    def exit_grid(self):
        return self.get_grid_from_pos(*self.exit_pos)