from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

class GameProject:
    def __init__(self):
        # Window size
        self.W_W = 500
        self.W_H = 700
        
        # Game states (using integer flags instead of is_something)
        self.play_state = 1 # 1 for play, 0 for pause
        self.dead_flag = 0  # 1 for game over
        self.points = 0
        self.hacker_mode = 0 # 1 for cheat on
        self.prev_time = time.time()
        
        # Diamond stuff
        self.diam_x = random.randint(40, 460)
        self.diam_y = 650
        self.diam_r = 15
        self.diam_v = 140
        self.diam_rgb = [1.0, 1.0, 1.0]
        
        # Catcher stuff
        self.c_x = 250
        self.c_y = 35
        self.c_width = 75
        self.c_height = 12
        self.c_rgb = [1.0, 1.0, 1.0]
        self.c_v = 380
        
        # Keys
        self.L_key = False
        self.R_key = False
        
        # Buttons
        self.btn_h = 40
        self.y_top = 680
        self.y_low = 640
        self.left_x = 20
        self.mid_x = 235
        self.right_x = 440

    # -------------------------------------------------------------------------
    # MIDPOINT LINE ALGORITHM - MANUAL IMPLEMENTATION
    # -------------------------------------------------------------------------
    
    def get_zone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            if dx >= 0:
                if dy >= 0:
                    return 0
                else:
                    return 7
            else:
                if dy >= 0: 
                    return 3
                else: 
                    return 4
        else:
            if dy >= 0:
                if dx >= 0: 
                    return 1
                else: 
                    return 2
            else:
                if dx >= 0: 
                    return 6
                else: 
                    return 5

    def to_0(self, x, y, z):
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

    def from_0(self, x, y, z):
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

    def draw_line(self, x1, y1, x2, y2, r, g, b):
        z = self.get_zone(x1, y1, x2, y2)
        x1_0, y1_0 = self.to_0(x1, y1, z)
        x2_0, y2_0 = self.to_0(x2, y2, z)
        
        if x1_0 > x2_0:
            x1_0, x2_0 = x2_0, x1_0
            y1_0, y2_0 = y2_0, y1_0
            
        dx = x2_0 - x1_0
        dy = y2_0 - y1_0
        d = 2 * dy - dx
        inc_E = 2 * dy
        inc_NE = 2 * (dy - dx)
        
        y_ptr = y1_0
        glBegin(GL_POINTS)
        glColor3f(r, g, b)
        for x_ptr in range(int(x1_0), int(x2_0) + 1):
            px, py = self.from_0(x_ptr, y_ptr, z)
            glVertex2i(int(px), int(py))
            if d > 0:
                d += inc_NE
                y_ptr += 1
            else:
                d += inc_E
        glEnd()

    # -------------------------------------------------------------------------
    # SHAPE DRAWING
    # -------------------------------------------------------------------------

    def render_buttons(self):
        # Restart (Teal)
        c1 = [0.1, 0.7, 0.7]
        mid_y = (self.y_top + self.y_low) // 2
        self.draw_line(self.left_x, mid_y, self.left_x + 35, mid_y, *c1)
        self.draw_line(self.left_x, mid_y, self.left_x + 15, self.y_top, *c1)
        self.draw_line(self.left_x, mid_y, self.left_x + 15, self.y_low, *c1)

        # Play/Pause (Amber)
        c2 = [1.0, 0.6, 0.0]
        if self.play_state == 1: # Show Pause Icon
            self.draw_line(self.mid_x + 10, self.y_top, self.mid_x + 10, self.y_low, *c2)
            self.draw_line(self.mid_x + 25, self.y_top, self.mid_x + 25, self.y_low, *c2)
        else: # Show Play Icon
            self.draw_line(self.mid_x, self.y_top, self.mid_x, self.y_low, *c2)
            self.draw_line(self.mid_x, self.y_top, self.mid_x + 30, mid_y, *c2)
            self.draw_line(self.mid_x, self.y_low, self.mid_x + 30, mid_y, *c2)

        # Close (Red)
        self.draw_line(self.right_x, self.y_top, self.right_x + 35, self.y_low, 1.0, 0.0, 0.0)
        self.draw_line(self.right_x, self.y_low, self.right_x + 35, self.y_top, 1.0, 0.0, 0.0)

    def render_objects(self):
        # Diamond
        if self.dead_flag == 0:
            rgb = self.diam_rgb
            cx, cy = int(self.diam_x), int(self.diam_y)
            r = self.diam_r
            self.draw_line(cx, cy + r, cx + r - 3, cy, *rgb)
            self.draw_line(cx + r - 3, cy, cx, cy - r, *rgb)
            self.draw_line(cx, cy - r, cx - r + 3, cy, *rgb)
            self.draw_line(cx - r + 3, cy, cx, cy + r, *rgb)

        # Catcher
        crgb = self.c_rgb
        if self.dead_flag == 1:
            crgb = [1.0, 0.0, 0.0]
        
        cur_x = int(self.c_x)
        cur_y = self.c_y
        w = self.c_width // 2
        h = self.c_height // 2
        
        self.draw_line(cur_x - w, cur_y - h, cur_x + w, cur_y - h, *crgb)
        self.draw_line(cur_x - w, cur_y - h, cur_x - w - 8, cur_y + h, *crgb)
        self.draw_line(cur_x + w, cur_y - h, cur_x + w + 8, cur_y + h, *crgb)
        self.draw_line(cur_x - w - 8, cur_y + h, cur_x + w + 8, cur_y + h, *crgb)

    # -------------------------------------------------------------------------
    # GAME ENGINE
    # -------------------------------------------------------------------------

    def update(self):
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        
        if self.play_state == 0 or self.dead_flag == 1:
            return

        # Catcher control
        if self.hacker_mode == 1:
            if self.c_x < self.diam_x: self.c_x += self.c_v * dt
            if self.c_x > self.diam_x: self.c_x -= self.c_v * dt
        else:
            if self.L_key: self.c_x -= self.c_v * dt
            if self.R_key: self.c_x += self.c_v * dt

        if self.c_x < 45: self.c_x = 45
        if self.c_x > 455: self.c_x = 455

        # Fall
        self.diam_y -= self.diam_v * dt

        # Hit detection
        d_lx, d_rx = self.diam_x - 15, self.diam_x + 15
        d_by, d_ty = self.diam_y - 15, self.diam_y + 15
        
        c_lx, c_rx = self.c_x - 40, self.c_x + 40
        c_by, c_ty = self.c_y - 10, self.c_y + 10
        
        if d_rx > c_lx and d_lx < c_rx and d_by < c_ty and d_ty > c_by:
            self.points += 1
            print("Score now:", self.points)
            self.diam_x = random.randint(50, 450)
            self.diam_y = 660
            self.diam_rgb = [random.random(), random.random(), random.random()]
            self.diam_v += 12 # get faster

        if self.diam_y < 0:
            self.dead_flag = 1
            print("Final Score:", self.points)
            print("!!! GAME OVER !!!")

    def start_again(self):
        print("Restarting Game...")
        self.points = 0
        self.diam_v = 140
        self.dead_flag = 0
        self.play_state = 1
        self.diam_x = random.randint(50, 450)
        self.diam_y = 660

# --- Global instances ---
G = GameProject()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    G.update()
    G.render_buttons()
    G.render_objects()
    glutSwapBuffers()

def key_press(k, x, y):
    if k == b'c':
        if G.hacker_mode == 0: G.hacker_mode = 1
        else: G.hacker_mode = 0

def special_dn(k, x, y):
    if k == GLUT_KEY_LEFT: 
        G.L_key = True
    if k == GLUT_KEY_RIGHT: 
        G.R_key = True

def special_up(k, x, y):
    if k == GLUT_KEY_LEFT:
        G.L_key = False
    if k == GLUT_KEY_RIGHT:
        G.R_key = False

def click(b, s, x, y):
    if b == GLUT_LEFT_BUTTON and s == GLUT_DOWN:
        mx, my = x, G.W_H - y
        # Check restart
        if G.left_x <= mx <= G.left_x + 40 and G.y_low <= my <= G.y_top:
            G.start_again()
        # Check pause
        if G.mid_x <= mx <= G.mid_x + 40 and G.y_low <= my <= G.y_top:
            if G.dead_flag == 0:
                if G.play_state == 1: G.play_state = 0
                else: G.play_state = 1
        # Check quit
        if G.right_x <= mx <= G.right_x + 40 and G.y_low <= my <= G.y_top:
            print("Goodbye! Final score was:", G.points)
            glutLeaveMainLoop()

def frame_timer(v):
    glutPostRedisplay()
    glutTimerFunc(10, frame_timer, 0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(G.W_W, G.W_H)
glutCreateWindow(b"Midpoint Diamond Catcher")
gluOrtho2D(0, G.W_W, 0, G.W_H)
glutDisplayFunc(display)
glutKeyboardFunc(key_press)
glutSpecialFunc(special_dn)
glutSpecialUpFunc(special_up)
glutMouseFunc(click)
glutTimerFunc(0, frame_timer, 0)
glutMainLoop()