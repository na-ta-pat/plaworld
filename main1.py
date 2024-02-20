import pygame
import numpy as np
from board import GridBoard
from enemy import FlyingEnemy, WiseEnemy
from grid_tower import GoldenFish
from random import choice

_cache = {}
def load_img(path):
    if path not in _cache:
        image = pygame.image.load(path)
        orig_width, orig_height = image.get_size()
        scale_factor = min(grid_board.grid_width/orig_width,grid_board.grid_height/orig_height)
        scale_factor = (grid_board.grid_height/orig_height)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        image = pygame.transform.scale(image, (new_width,new_height))
        _cache[path] = image
    return _cache[path]

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 960
BOARD_WIDTH, BOARD_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
CELL_SIZE = (9, 9)  # Pixel dimensions of each grid cell
FPS = 60

# Colors
BACKGROUND_COLOR = (30, 30, 30)
WALKABLE_COLOR = (50, 150, 50)
TOWER_COLOR = (0, 0, 200)
ENEMY_COLOR = (200, 50, 50)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

# Game Variables
grid_board = GridBoard(width=BOARD_WIDTH, height=BOARD_HEIGHT, cell_size=CELL_SIZE)
enemies = [
    WiseEnemy(20,5,0),
    WiseEnemy(20,3,1),
    WiseEnemy(70,1,2),
]*49+[FlyingEnemy(70,1,2,image=r"./images/default_flying_unit.png"),]*2

def draw_grid():
    for row in range(grid_board.cell_size_height):
        for col in range(grid_board.cell_size_width):
            x,y = grid_board.get_pos_from_grid(col,row)
            rect = pygame.Rect(x,y, grid_board.grid_height, grid_board.grid_width)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Draw grid lines

def draw_towers():
    for tower in deployed_towers:
        grid = grid_board.get_grid_from_pos(*tower.position)
        top,left = grid_board.get_pos_from_grid(*grid)
        screen.blit(load_img(tower.image), (left,top,))

def draw_enemies():
    for enemy in sorted(deployed_enemies,key=lambda e:e.position[0]):
        HEALTH_BOX_SIZE = 1
        pos = enemy.position
        center = pos[::-1]
        center=center[0],center[1]-grid_board.grid_height
        center=center[0]-grid_board.grid_width//4,center[1]+grid_board.grid_height//2
        screen.blit(load_img(enemy.image), center)
        #    draw health bar
        pygame.draw.rect(screen, (255,0,0), (center,(enemy.full_health*HEALTH_BOX_SIZE,HEALTH_BOX_SIZE)))
        pygame.draw.rect(screen, (0,255,0), (center,(enemy.health*HEALTH_BOX_SIZE,HEALTH_BOX_SIZE)))

def draw_walkable_array():

    walkable_array = grid_board.walkable_array
    
    # Transform the walkable_array into an RGB format for Pygame's surface
    height, width = walkable_array.shape
    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Set walkable areas to yellow (255, 255, 0) and non-walkable areas to another color
    rgb_array[walkable_array == 1] = [255, 255, 0]  # Yellow for walkable
    rgb_array[walkable_array == 0] = [0, 0, 0]  # Black for non-walkable
    
    # Convert the RGB array to a Pygame surface
    walkable_surface = pygame.surfarray.make_surface(rgb_array.transpose((1, 0, 2)))
    
    # Draw the surface onto the screen
    screen.blit(walkable_surface, (0, 0))


def handle_click(pos):
    pos = pos[::-1]
    grid_y, grid_x = grid_board.get_grid_from_pos(*pos)
    if grid_board.add_tower(grid_y, grid_x, 1):  # Assuming tower data is 1
        deployed_towers.append(GoldenFish(.1,(pos),image = './images/golden_fish.png'))
        print(f"Tower added at grid ({grid_y}, {grid_x})")
    else:
        print(f"Cannot place tower at grid ({grid_y}, {grid_x})")

deployed_enemies = []  # Keep track of all deployed enemies
deployed_towers = []  # Keep track of all deployed enemies

def spawn_enemy(enemy_list):
    enemy = choice(enemy_list)
    if 1:
        cloned_enemy = enemy.clone()
        cloned_enemy.deploy(grid_board.entrance_pos)
        deployed_enemies.append(cloned_enemy)

def game_loop():
    running = True
    spawn_event = pygame.USEREVENT + 1  # Custom event for spawning enemies
    move_event = pygame.USEREVENT + 2  # Custom event for moving enemies
    pygame.time.set_timer(spawn_event, 100)  # Spawn every 100 milliseconds (.1 second)
    pygame.time.set_timer(move_event, 100)  # Move every 100 milliseconds (.1 second)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                handle_click(event.pos)
            elif event.type == spawn_event:
                spawn_enemy(enemies)  # Assume `enemies` is a list of enemy templates
            elif event.type == move_event:
                to_remove = []
                for enemy in deployed_enemies:
                    enemy.move(grid_board)  # Assuming `move` requires the board's walkable array
                    if enemy.health<=0:to_remove.append(enemy)
                for enemy in to_remove:
                    deployed_enemies.remove(enemy)
                for tower in deployed_towers:
                    tower.tick(grid_board,deployed_enemies)
                

        screen.fill(BACKGROUND_COLOR)

        # draw_walkable_array()
        draw_grid()
        draw_towers()
        draw_enemies()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
