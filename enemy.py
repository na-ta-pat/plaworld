from helper import gen_move
from random import shuffle

class Enemy:
    def __init__(self, health, speed, shield, image = "./images/default.png", position = None):
        self.full_health = self.health = health
        self.speed = speed
        self.shield = shield
        self.image = image
        self._position = position

    def move(self, board):
        for _ in range(self.speed):self.single_move(board)

    def single_move(self, board):
        # Base move method, to be overridden based on speed
        pass

    def deploy(self, position):
        self.position = position
        
    def clone(self):
        return type(self)(self.health, self.speed, self.shield, self.image, self.position)

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,position):
        self._last_position = self.position
        self._position = position
        if self._last_position is None:self._last_position = self.position
    @property
    def position_diff(self):return self.position[0]-self._last_position[0],self.position[1]-self._last_position[1],



class FlyingEnemy(Enemy):
    
    def __init__(self,*a,**k):
        super().__init__(*a,**k)

    def single_move(self, board):
        walkable_array = board.walkable_array
        _, y = self.position
        self.position = (self.position[0], y + 1 if y + 1 < walkable_array.shape[1] else y)

            
class WiseEnemy(Enemy):
    
    def __init__(self,*a,**k):
        super().__init__(*a,**k)

    def single_move(self,board):
        walk_guide_array = board.walk_guide_array
        x,y = self.position
        cur_val = walk_guide_array[x,y]
        
        moves = gen_move(x,y)
        shuffle(moves)

        for x,y in moves:
            if not 0<=x<walk_guide_array.shape[0] or not 0<=y<walk_guide_array.shape[1]:continue
            if walk_guide_array[x,y]<cur_val:
                self.position = x,y
                break

