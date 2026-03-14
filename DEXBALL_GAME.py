from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time

# --- WINDOW SETTINGS ---
W_WIDTH, W_HEIGHT = 500, 700
gameplaying = 1 
game_finish = 0
score = 0
auto = 0 
last_frame = time.time()

# DIAMOND POSITION AND LOOK
dx, dy = random.randint(30, 470), 650
dr = 15
dv = 145
d_color = [1.0, 1.0, 1.0]

# CATCHER SETTINGS
cx = 250
cy = 40
cw, ch = 80, 15
c_color = [1.0, 1.0, 1.0]
c_speed = 350

# INPUT STATUS
left = 0
right = 0

# --- LINE ALGORITHM (MIDPOINT) ---
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

def convert_to_zero(x, y, z):
    if z == 0: 
        return x, y
    if z == 1: 
        return y, x
    if z == 2: 
        return y, -x
    if z == 3: 
        return -x, y
    if z == 4: 
        return -x, -y
    if z == 5: 
        return -y, -x
    if z == 6: 
        return -y, x
    if z == 7: 
        return x, -y

def convert_back(x, y, z):
    if z == 0: 
        return x, y
    if z == 1: 
        return y, x
    if z == 2: 
        return -y, x
    if z == 3: 
        return -x, y
    if z == 4: 
        return -x, -y
    if z == 5: 
        return -y, -x
    if z == 6: 
        return y, -x
    if z == 7: 
        return x, -y

def m_line(x1, y1, x2, y2, r, g, b):
    zone = find_the_zone(x1, y1, x2, y2)
    # Mapping points
    x1_0, y1_0 = convert_to_zero(x1, y1, zone)
    x2_0, y2_0 = convert_to_zero(x2, y2, zone)
    
    if x1_0 > x2_0:
        x1_0, x2_0, y1_0, y2_0 = x2_0, x1_0, y2_0, y1_0
            
    dx0 = x2_0 - x1_0
    dy0 = y2_0 - y1_0
    d_start = 2 * dy0 - dx0
    dE = 2 * dy0
    dNE = 2 * (dy0 - dx0)
    
    y_current = y1_0
    glBegin(GL_POINTS)
    glColor3f(r, g, b)
    for x_current in range(int(x1_0), int(x2_0) + 1):
        actual_x, actual_y = convert_back(x_current, y_current, zone)
        glVertex2i(int(actual_x), int(actual_y))
        if d_start > 0:
            d_start += dNE
            y_current += 1
        else:
            d_start += dE
    glEnd()

# --- DRAWING HELPERS ---
def show_stuff():
    global dx, dy, dr, d_color, game_finish, cx, cy, cw, ch, c_color
    if game_finish == 0:
        m_line(dx, dy + dr, dx + dr - 5, dy, d_color[0], d_color[1], d_color[2])
        m_line(dx + dr - 5, dy, dx, dy - dr, d_color[0], d_color[1], d_color[2])
        m_line(dx, dy - dr, dx - dr + 5, dy, d_color[0], d_color[1], d_color[2])
        m_line(dx - dr + 5, dy, dx, dy + dr, d_color[0], d_color[1], d_color[2])

    draw_c = c_color
    if game_finish == 1:
        draw_c = [1.0, 0.0, 0.0] 
    
    # Bucket shape
    m_line(cx - 35, cy - 10, cx + 35, cy - 10, *draw_c)
    m_line(cx - 35, cy - 10, cx - 45, cy + 10, *draw_c)
    m_line(cx + 35, cy - 10, cx + 45, cy + 10, *draw_c)
    m_line(cx - 45, cy + 10, cx + 45, cy + 10, *draw_c)

def draw_top_icons():
    m_line(20, 660, 50, 660, 0.0, 0.8, 0.8)
    m_line(20, 660, 35, 680, 0.0, 0.8, 0.8)
    m_line(20, 660, 35, 640, 0.0, 0.8, 0.8)

    if gameplaying == 1:
        m_line(240, 680, 240, 640, 1.0, 0.7, 0.0)
        m_line(260, 680, 260, 640, 1.0, 0.7, 0.0)
    else:
        # Play button (Triangle)
        m_line(240, 680, 240, 640, 1.0, 0.7, 0.0)
        m_line(240, 680, 270, 660, 1.0, 0.7, 0.0)
        m_line(240, 640, 270, 660, 1.0, 0.7, 0.0)
    m_line(450, 680, 480, 640, 1.0, 0.0, 0.0)
    m_line(450, 640, 480, 680, 1.0, 0.0, 0.0)

# --- ENGINE ---
def game_tick():
    global last_frame, dy, dx, cx, dv, score, game_finish, d_color, auto
    
    now = time.time()
    step = now - last_frame
    last_frame = now
    
    if gameplaying == 0 or game_finish == 1: return

    if auto == 1:
        if cx < dx: cx += c_speed * step
        if cx > dx: cx -= c_speed * step
    else:
        if left: cx -= c_speed * step
        if right: cx += c_speed * step

    # Border check
    if cx < 45: 
        cx = 45
    if cx > 455: 
        cx = 455

    # Diamond movement
    dy -= dv * step

    # Check collision (AABB)
    if (dx + 15 > cx - 40 and dx - 15 < cx + 40 and 
        dy + 15 > cy - 10 and dy - 15 < cy + 10):
        score += 1
        print("Score:", score)
        dy = 650
        dx = random.randint(50, 450)
        dv += 10
        d_color = [random.random(), random.random(), random.random()]

    # Miss check
    if dy < 0:
        game_finish = 1
        print("Game Over. Final Score:", score)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    game_tick()
    draw_top_icons()
    show_stuff()
    glutSwapBuffers()

# --- INPUTS ---
def normal_key(k, x, y):
    global auto
    if k == b'c': 
        auto = 1 - auto
        print("Cheat:", "ON" if auto else "OFF")

def spec_dn(k, x, y):
    global left, right
    if k == GLUT_KEY_LEFT: 
        left = 1
    if k == GLUT_KEY_RIGHT:
        right = 1

def spec_up(k, x, y):
    global left, right
    if k == GLUT_KEY_LEFT: 
        left = 0
    if k == GLUT_KEY_RIGHT: 
        right = 0

def mouse_click(btn, state, x, y):
    global game_finish, gameplaying, score, dy, dv, dx
    if btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        real_y = W_HEIGHT - y
        # Reset button
        if 20 <= x <= 50 and 640 <= real_y <= 680:
            print("Starting Over...")
            game_finish, score, dv, dy = 0, 0, 145, 650
            dx = random.randint(50, 450)
        # Pause button
        if 235 <= x <= 275 and 640 <= real_y <= 680:
            if not game_finish: 
                gameplaying = 1 - gameplaying
        # Exit button
        if 445 <= x <= 485 and 640 <= real_y <= 680:
            print("Goodbye. Score:", score)
            glutLeaveMainLoop()

def timer(v):
    glutPostRedisplay()
    glutTimerFunc(10, timer, 0)

# --- INIT ---
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutCreateWindow(b"Diamond Game")
gluOrtho2D(0, W_WIDTH, 0, W_HEIGHT)
glutDisplayFunc(display)
glutKeyboardFunc(normal_key)
glutSpecialFunc(spec_dn)
glutSpecialUpFunc(spec_up)
glutMouseFunc(mouse_click)
glutTimerFunc(0, timer, 0)
glutMainLoop()