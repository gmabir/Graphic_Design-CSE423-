from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time, os

# --- WINDOW SETTINGS ---
W_WIDTH, W_HEIGHT = 600, 800
gameplaying = 1 
game_finish = 0
score = 0
auto = 0 
last_frame = time.time()

# DIAMOND POSITION AND LOOK
dx, dy = random.randint(50, 550), 750
dr = 15
dv = 145
diamond_color = [1.0, 1.0, 1.0]

# CATCHER SETTINGS
cx = 300
cy = 40
cw, ch = 80, 15
catcher_color = [1.0, 0.5, 1.0]
c_speed = 350

# INPUT STATUS
left = 0
right = 0

def find_the_zone(x1, y1, x2, y2):
    dx_val = x2 - x1
    dy_val = y2 - y1
    if abs(dx_val) > abs(dy_val):
        if dx_val >= 0 and dy_val >= 0: 
            return 0
        if dx_val < 0 and dy_val >= 0: 
            return 3
        if dx_val < 0 and dy_val < 0: 
            return 4
        if dx_val >= 0 and dy_val < 0: 
            return 7
    else:
        if dx_val >= 0 and dy_val >= 0: 
            return 1
        if dx_val < 0 and dy_val >= 0: 
            return 2
        if dx_val < 0 and dy_val < 0: 
            return 5
        if dx_val >= 0 and dy_val < 0: 
            return 6
    return 0

def convert_to_zone_zero(x, y, zone):
    if zone == 0: 
        return x, y
    if zone == 1: 
        return y, x
    if zone == 2: 
        return y, -x
    if zone == 3: 
        return -x, y
    if zone == 4: 
        return -x, -y
    if zone == 5: 
        return -y, -x
    if zone == 6: 
        return -y, x
    if zone == 7: 
        return x, -y

def convert_to_original_zone(x, y, zone):
    if zone == 0: 
        return x, y
    if zone == 1: 
        return y, x
    if zone == 2: 
        return -y, x
    if zone == 3: 
        return -x, y
    if zone == 4: 
        return -x, -y
    if zone == 5: 
        return -y, -x
    if zone == 6: 
        return y, -x
    if zone == 7: 
        return x, -y

def midpoint_line_algorithm(x1, y1, x2, y2, r, g, b):
    zone = find_the_zone(x1, y1, x2, y2)
    start_x, start_y = convert_to_zone_zero(x1, y1, zone)
    end_x, end_y = convert_to_zone_zero(x2, y2, zone)
    
    if start_x > end_x:
        start_x, end_x, start_y, end_y = end_x, start_x, end_y, start_y
            
    del_x = end_x - start_x
    del_y = end_y - start_y
    
    dec = 2 * del_y - del_x
    inc_EAST = 2 * del_y
    inc_NorthEast = 2 * (del_y - del_x)
    
    curr_y = start_y
    glBegin(GL_POINTS)
    glColor3f(r, g, b)
    for curr_x in range(int(start_x), int(end_x) + 1):
        orig_x, orig_y = convert_to_original_zone(curr_x, curr_y, zone)
        glVertex2i(int(orig_x), int(orig_y))
        if dec > 0:
            dec += inc_NorthEast
            curr_y += 1
        else:
            dec += inc_EAST
    glEnd()

# --- DRAWING HELPERS ---
def draw_game_objects():
    global dx, dy, dr, diamond_color, game_finish, cx, cy, catcher_color
    if game_finish == 0:
        midpoint_line_algorithm(dx, dy + dr, dx + dr - 5, dy, *diamond_color)
        midpoint_line_algorithm(dx + dr - 5, dy, dx, dy - dr, *diamond_color)
        midpoint_line_algorithm(dx, dy - dr, dx - dr + 5, dy, *diamond_color)
        midpoint_line_algorithm(dx - dr + 5, dy, dx, dy + dr, *diamond_color)

    current_c_color = catcher_color
    if game_finish == 1:
        current_c_color = [1.0, 0.0, 0.0] 
    
    midpoint_line_algorithm(cx - 35, cy - 10, cx + 35, cy - 10, *current_c_color)
    midpoint_line_algorithm(cx - 35, cy - 10, cx - 45, cy + 10, *current_c_color)
    midpoint_line_algorithm(cx + 35, cy - 10, cx + 45, cy + 10, *current_c_color)
    midpoint_line_algorithm(cx - 45, cy + 10, cx + 45, cy + 10, *current_c_color)

def drawing():
    # Adjusted for 800 height
    midpoint_line_algorithm(20, 760, 50, 760, 0.0, 0.8, 0.8)
    midpoint_line_algorithm(20, 760, 35, 780, 0.0, 0.8, 0.8)
    midpoint_line_algorithm(20, 760, 35, 740, 0.0, 0.8, 0.8)

    if gameplaying == 1:
        midpoint_line_algorithm(290, 780, 290, 740, 1.0, 0.7, 0.0)
        midpoint_line_algorithm(310, 780, 310, 740, 1.0, 0.7, 0.0)
    else:
        midpoint_line_algorithm(290, 780, 290, 740, 1.0, 0.7, 0.0)
        midpoint_line_algorithm(290, 780, 320, 760, 1.0, 0.7, 0.0)
        midpoint_line_algorithm(290, 740, 320, 760, 1.0, 0.7, 0.0)
    
    midpoint_line_algorithm(550, 780, 580, 740, 1.0, 0.0, 0.0)
    midpoint_line_algorithm(550, 740, 580, 780, 1.0, 0.0, 0.0)

def game_counter():
    global last_frame, dy, dx, cx, dv, score, game_finish, auto
    
    now = time.time()
    dt = now - last_frame
    last_frame = now
    
    if gameplaying == 0 or game_finish == 1: return

    if auto == 1:
        if cx < dx: cx += c_speed * dt
        if cx > dx: cx -= c_speed * dt
    else:
        if left: cx -= c_speed * dt
        if right: cx += c_speed * dt

    if cx < 45: cx = 45
    if cx > 555: cx = 555

    dy -= dv * dt
    if (dx + 15 > cx - 40 and dx - 15 < cx + 40 and 
        dy + 15 > cy - 10 and dy - 15 < cy + 10):
        score += 1
        print("Score:", score)
        dy = 750
        dx = random.randint(50, 550)
        dv += 10 

    if dy < 0:
        game_finish = 1
        print("Game Over. Final Score:", score)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    game_counter()
    drawing()
    draw_game_objects()
    glutSwapBuffers()

def normal_key_handler(key, x, y):
    global auto
    if key == b'c': 
        auto = 1 - auto
        print("Autopilot:", "Enabled" if auto else "Disabled")

def special_key_down(key, x, y):
    global left, right
    if key == GLUT_KEY_LEFT: left = 1
    if key == GLUT_KEY_RIGHT: right = 1

def special_key_up(key, x, y):
    global left, right
    if key == GLUT_KEY_LEFT: left = 0
    if key == GLUT_KEY_RIGHT: right = 0

def mouse_handler(button, state, x, y):
    global game_finish, gameplaying, score, dy, dv, dx
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        real_y = W_HEIGHT - y
        if 20 <= x <= 50 and 740 <= real_y <= 780:
            game_finish, score, dv, dy = 0, 0, 145, 750
            dx = random.randint(50, 550)
            print("Restarting...")
        if 280 <= x <= 325 and 740 <= real_y <= 780:
            if not game_finish: gameplaying = 1 - gameplaying
        if 540 <= x <= 590 and 740 <= real_y <= 780:
            print(f"Goodbye. Score: {score}")
            os._exit(0)

def timer_loop(v):
    glutPostRedisplay()
    glutTimerFunc(10, timer_loop, 0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutCreateWindow(b"Catch the Diamonds!")
gluOrtho2D(0, W_WIDTH, 0, W_HEIGHT)
glutDisplayFunc(display)
glutKeyboardFunc(normal_key_handler)
glutSpecialFunc(special_key_down)
glutSpecialUpFunc(special_key_up)
glutMouseFunc(mouse_handler)
glutTimerFunc(0, timer_loop, 0)
glutMainLoop()