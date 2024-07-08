import Path_Traversal
import pygame as py
import Graphics
import GameMap
import NPC
import random as rand

# Constants
SCREENWIDTH = 480
SCREENHEIGHT = 600
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)
FRAMERATE = 30
SCREENCOLOR = (0, 0, 0)

# Set up pygame
clock = py.time.Clock()
screen = py.display.set_mode(SCREENSIZE)
py.display.set_caption("NPC Path Finding and Daily Schedule")
py.init()

# Initialize game components
game_map = GameMap.Map("./Maps/Map2/map2_image.png", "./Maps/Map2/map2_paths.json")
path_finder = Path_Traversal.Dijkstra(game_map)
graphics = Graphics.GraphicsManager(screen, game_map)
key_nodes = game_map.get_key_nodes()

# Create and load test NPCs for demo
# TODO: Create manager for NPCs
speeds = [1, 1, 1, 1, 1, 1, 1.2, 1.5, 1.5, 1.6]
npcs = []
npc_count = 30
for i in range(npc_count):
    start_node = rand.choice(list(game_map.Nodes.keys()))
    num_key_locs = rand.randint(3, 10)
    speed = rand.choice(speeds)
    try:
        npcs.append(
            NPC.NpcCharacter(path_finder,
                             start_node,
                             [rand.choice(key_nodes) for i in range(num_key_locs)],
                             speed)
        )
    except Exception as ex:
        print("Failed to create NPC")

for n in npcs:
    r = rand.randint(50, 250)
    g = rand.randint(50, 250)
    b = rand.randint(50, 250)
    color = (r, g, b)
    graphics.npc_graphics.add_npc(n, color)

# controls
show_overlay = True
pause = False


def on_space_key_pressed():
    global show_overlay
    show_overlay = not show_overlay


def on_p_key_pressed():
    global pause
    pause = not pause


keydown_events = {py.K_SPACE: on_space_key_pressed, py.K_p: on_p_key_pressed}

# Main Game Loop

app_running = True
while app_running:
    # Handle Events
    for event in py.event.get():
        if event.type == py.QUIT:
            app_running = False
        if event.type == py.KEYDOWN:
            pressed_key = event.key
            if pressed_key in keydown_events:
                keydown_events[pressed_key]()

    if pause:
        continue

    # Draw graphics
    screen.fill(SCREENCOLOR)
    
    graphics.background_graphics.draw_background()
    if show_overlay:
        graphics.node_graphics.draw_overlay()
    graphics.npc_graphics.draw_npcs()
    graphics.background_graphics.draw_outside_block()
    
    if pause:
        continue

    # TODO: move this to NPCs manager when created
    for n in npcs:
        n.move_to_target()
    py.display.flip()
    clock.tick(FRAMERATE)

py.quit()
