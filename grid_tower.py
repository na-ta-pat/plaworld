class GridTower:
    def __init__(self, damage, position, speed = 10, image = "./images/default.png", ):
        self.damage = damage
        self.speed = speed
        self.image = image
        self.position = position
        self.tick_count=0

    def tick(self,*a,**k):
        self.hit(*a,**k)
    def hit(self,board,enemies):
        pass

class GoldenFish(GridTower):

    def __init__(self,*a,**k):
        super().__init__(*a,**k)

    def hit(self,board,enemies):
        cur_grid = board.get_grid_from_pos(*self.position)
        for enemy in enemies:
            enemy_grid = board.get_grid_from_pos(*enemy.position)
            if (cur_grid[0]-enemy_grid[0])**2+(cur_grid[1]-enemy_grid[1])**2<=1:
                enemy.health-=self.damage