from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random, time

window_width = 1000
window_height = 800
GRID_LENGTH = 600

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def set_range(val, low, high):
    if val < low:
        return low
    if val > high:
        return high
    return val

def angle_difference(a, b):
    diff = a - b
    while diff > 180:
        diff -= 360
    while diff < -180:
        diff += 360
    return diff

player_x, player_y, player_z = 0, 0, 0
enemies = []
enemy_speed = 50

def enemy_generate():
    while True:
        spawn_limit = GRID_LENGTH - 50
        rx = random.uniform(-spawn_limit, spawn_limit)
        ry = random.uniform(-spawn_limit, spawn_limit)
        dx = rx - player_x
        dy = ry - player_y
        if dx*dx + dy*dy > 90000:
            return rx, ry

tick = 0
facing_dic = 0
bullets = []
bullet_speed = 500
bullets_missed = 0
shoot_cooldown = 0
cheat_mode = False
cheat_vision = False
score = 0
life = 5
game_over = False
fp_lock = False
fp_lock_angle = 0

def restart():
    global player_x, player_y, player_z, facing_dic, bullets
    global bullets_missed, shoot_cooldown, enemies
    global score, life, game_over, cheat_mode
    global cheat_vision, tick, fp_lock, fp_lock_angle

    player_x = player_y = player_z = 0
    facing_dic = 0
    bullets.clear()
    bullets_missed = 0
    shoot_cooldown = 0
    score = 0
    tick = 0
    fp_lock_angle = 0
    life = 5
    game_over = False
    cheat_mode = cheat_vision = fp_lock = False

    enemies.clear()
    for _ in range(5):
        x, y = enemy_generate()
        enemies.append([x, y, 30])

    print("Game RESTARTED")

camera_angle = 0
camera_height = 500
camera_radius = 900
first_person = False

def camara_angle():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, 1.25, 0.1, 2000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person:
        if fp_lock == True:
            angle = fp_lock_angle
        else:
            angle = facing_dic
        rad = math.radians(angle)
        lx, ly = math.cos(rad), math.sin(rad)

        gluLookAt(player_x + lx * 50, player_y + ly * 50, 200,
                  player_x + lx * 300, player_y + ly * 300, 20,
                  0, 0, 1)
    else:
        rad = math.radians(camera_angle)
        gluLookAt(math.cos(rad) * camera_radius,
                  math.sin(rad) * camera_radius,
                  camera_height,
                  0, 0, 0,
                  0, 0, 1)

def draw_wall():
    l = GRID_LENGTH
    h = 70
    glBegin(GL_QUADS)

    glColor3f(0.2, 0.5, 1)
    glVertex3f(-l, -l, 0); glVertex3f(-l, l, 0)
    glVertex3f(-l, l, h); glVertex3f(-l, -l, h)
    glColor3f(0, 1, 0.3)
    glVertex3f(l, -l, 0); glVertex3f(l, l, 0)
    glVertex3f(l, l, h); glVertex3f(l, -l, h)
    glColor3f(.8, 1, 0.7)
    glVertex3f(-l, -l, 0); glVertex3f(l, -l, 0)
    glVertex3f(l, -l, h); glVertex3f(-l, -l, h)
    glColor3f(0.7, 1, 1)
    glVertex3f(-l, l, 0); glVertex3f(l, l, 0)
    glVertex3f(l, l, h); glVertex3f(-l, l, h)

    glEnd()

tiles_size = 100
def draw_floor():
    glBegin(GL_QUADS)
    for y in range(-GRID_LENGTH, GRID_LENGTH, tiles_size):
        for x in range(-GRID_LENGTH, GRID_LENGTH, tiles_size):
            if ((x // tiles_size) + (y // tiles_size)) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.9)
            glVertex3f(x, y, 0)
            glVertex3f(x+tiles_size, y, 0)
            glVertex3f(x+tiles_size, y+tiles_size, 0)
            glVertex3f(x, y+tiles_size, 0)
    glEnd()

def draw_player():
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)
    
    if game_over:
        glRotatef(90, 1, 0, 0)
    else:
        glRotatef(facing_dic, 0, 0, 1)

    q = gluNewQuadric()
    glPushMatrix()
    glColor3f(0.2, 0.4, 0.2)
    glTranslatef(0, 0, 110)
    glScalef(80, 55, 90) 
    glutSolidCube(1)    
    glPopMatrix()

    # Head
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(0, 0, 155)
    gluSphere(q, 30, 15, 15)
    glPopMatrix()

    
    # Left Leg
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(-20, 15, 0)
    glScalef(0.4, 0.4, 1.2)
    gluCylinder(q, 15, 45, 55, 10, 10)
    glPopMatrix()

    # Right Leg
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(-20, -15, 0)
    glScalef(0.4, 0.4, 1.2)
    gluCylinder(q, 15, 45, 55, 10, 10)
    glPopMatrix()

    # Right Arm 
    glPushMatrix()
    glColor3f(0.25, 0.22, 0.19)
    glTranslatef(40, -25, 110)
    glRotatef(90, 0, 1, 0)
    glScalef(0.5, 0.4, 1.2)
    gluCylinder(q, 15, 10, 60, 10, 10)
    glPopMatrix()

    # Gun 
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, -5, 110)
    glRotatef(90, 0, 1, 0)
    glScalef(0.5, 0.4, 1.2)
    gluCylinder(q, 20, 5, 200, 10, 10)
    glPopMatrix()

    glPopMatrix()
def enemy_drawing(ex, ey, base_r):
    s = 1 + 0.2 * math.sin(tick * 3)

    glPushMatrix()
    glTranslatef(ex, ey, 0)

    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 35)
    glScalef(s, s, s)
    gluSphere(gluNewQuadric(), base_r, 20, 20)
    glPopMatrix()

    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 95)
    glScalef(s, s, s)
    gluSphere(gluNewQuadric(), base_r * 0.65, 20, 20)
    glPopMatrix()

    glPopMatrix()



def ene_movenment(dt):
    global life, game_over
    if game_over:
        return

    for e in enemies:
        dx = player_x - e[0]
        dy = player_y - e[1]
        dist = math.hypot(dx, dy)

        if dist > 0:
            e[0] += dx/dist * enemy_speed * dt
            e[1] += dy/dist * enemy_speed * dt

        if dist < 50:
            life -= 1
            e[0], e[1] = enemy_generate()
            if life <= 0:
                game_over = True

def drawing_enemies():
    for ex, ey, r in enemies:
        enemy_drawing(ex, ey, r)                

def draw_bullets():
    glColor3f(0.8, 0, 0)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], b[2])
        glutSolidCube(20)
        glPopMatrix()

def firing():
    global shoot_cooldown
    if game_over or shoot_cooldown > 0:
        return

    rad = math.radians(facing_dic)
    vx = math.cos(rad) * bullet_speed
    vy = math.sin(rad) * bullet_speed

    bullets.append([
        player_x + math.cos(rad)*150,
        player_y + math.sin(rad)*150,
        100, vx, vy
    ])
    shoot_cooldown = 0.1
    print("Bullet fired")
def bullet_motion(dt):
    global shoot_cooldown, bullets, bullets_missed, game_over, score

    shoot_cooldown = max(0, shoot_cooldown - dt)

    if game_over:
        return

    i = 0
    while i < len(bullets):
        b = bullets[i]
        b[0] += b[3] * dt
        b[1] += b[4] * dt
        if abs(b[0]) > 650 or abs(b[1]) > 650:
            bullets_missed += 1
            bullets.pop(i)

            if bullets_missed >= 10:
                game_over = True
            continue
        hit = False
        for e in enemies:
            dx = b[0] - e[0]
            dy = b[1] - e[1]

            if math.sqrt(dx*dx + dy*dy) <= 50:
                score += 1
                e[0], e[1] = enemy_generate()
                hit = True
                break

        if hit:
            bullets.pop(i)
        else:
            i += 1
def cheat(dt):
    global facing_dic

    if cheat_mode == False or game_over == True:
        return
    
    move_amount = 500 * dt
    facing_dic = (facing_dic + move_amount)
    if facing_dic >= 360:
        facing_dic -= 360
        
    for item in enemies:
        tx = item[0]
        ty = item[1]
        
        dx = tx - player_x
        dy = ty - player_y

        if dx == 0 and dy == 0:
            continue

        my_rad = (facing_dic * 3.14159) / 180.0
        look_x = math.cos(my_rad)
        look_y = math.sin(my_rad)

        check_val = (look_x * dy) - (look_y * dx)
        enemy_front = (look_x * dx) + (look_y * dy)

        if enemy_front > 0:
            if check_val < 0:
                check_val = -check_val
            
            if check_val < 40:
                firing()
                break

def keyboardListener(key,x,y):
    global player_x, player_y, facing_dic, cheat_mode

    if key == b'r':
        restart()
        return

    if game_over:
        return

    rad = math.radians(facing_dic)
    if key == b'w':
        player_x += math.cos(rad)*40
        player_y += math.sin(rad)*40
    elif key == b's':
        player_x -= math.cos(rad)*40
        player_y -= math.sin(rad)*40
    boundary = GRID_LENGTH - 50

    player_x = max(-boundary, min(boundary, player_x))
    player_y = max(-boundary, min(boundary, player_y))    

    if key == b'a':
        facing_dic += 5
    elif key == b'd':
        facing_dic -= 5

    if key == b'c':
        cheat_mode = not cheat_mode
def specialKeyListener(key, x, y):
    global camera_angle, camera_height

    if key == GLUT_KEY_LEFT:
        camera_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5
    elif key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10

    camera_height = set_range(camera_height, 200, 1000)

    glutPostRedisplay()        

def mouseListener(button,state,x,y):
    global first_person
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            firing()
        elif button == GLUT_RIGHT_BUTTON:
            first_person = not first_person

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,window_width,window_height)

    camara_angle()
    draw_floor()
    draw_wall()
    drawing_enemies()
    draw_bullets()
    draw_player()

    draw_text(10, window_height-30, f"Life: {life:}")
    draw_text(10, window_height-60, f"Score: {score:}")
    draw_text(10, window_height-90, f"Missed: {bullets_missed:}")

    glutSwapBuffers()

last_time = 0
def idle():
    global last_time, tick
    now = time.time()
    if last_time == 0:
        last_time = now

    dt = min(now - last_time, 0.05)
    last_time = now

    tick += dt

    cheat(dt)
    ene_movenment(dt)
    bullet_motion(dt)

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Assignment 3")

    glEnable(GL_DEPTH_TEST)

    restart()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__":
    main()