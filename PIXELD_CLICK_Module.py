from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
all_moving_points = [] 
movement_speed = 0.6
pause_flag = False
blink_status = False
is_visible = True
time_counter = 0
blink_threshold = 200

def is_out_of_bounds(position, limit):
    if position >= limit or position <= 0:
        return True
    return False
def update_point(point_data):
    point_data[0] = point_data[0] + (point_data[2] * movement_speed)
    point_data[1] = point_data[1] + (point_data[3] * movement_speed)
    #  (Width = 1500)
    if is_out_of_bounds(point_data[0], 1500):
        point_data[2] = point_data[2] * -1      
    #  (Height = 800)
    if is_out_of_bounds(point_data[1], 800):
        point_data[3] = point_data[3] * -1 
def convert_mouse_to_gl(y_coordinate): 
    return 800 - y_coordinate
def get_new_point_colors():
    red = random.random()
    green = random.random()
    blue = random.random()
    return red, green, blue
def my_mouse_input_handler(button, state, x, y):
    global blink_status, all_moving_points
    
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            gl_y = convert_mouse_to_gl(y)
            directions = [-1, 1]
            dx = random.choice(directions)
            dy = random.choice(directions)
            r, g, b = get_new_point_colors()
            
            new_point = [x, gl_y, dx, dy, r, g, b]
            all_moving_points.append(new_point)
            
        elif button == GLUT_LEFT_BUTTON:
            if blink_status == True:
                blink_status = False
            else:
                blink_status = True

def my_keyboard_input_handler(key, x, y):
    global pause_flag
    if key == b' ':
        if pause_flag == False:
            pause_flag = True
        else:
            pause_flag = False

def my_special_keys_handler(key, x, y):
    global movement_speed
    if pause_flag == False:
        if key == GLUT_KEY_UP:
            movement_speed = movement_speed + 0.3
        elif key == GLUT_KEY_DOWN:
            movement_speed = movement_speed - 0.3
            if movement_speed < 0.3: 
                movement_speed = 0.3
    glutPostRedisplay()
def physics_and_animation_logic():
    global time_counter, is_visible, all_moving_points, movement_speed, pause_flag
    if pause_flag == True:
        glutPostRedisplay()
        return
    if blink_status == True:
        time_counter = time_counter + 1
        if time_counter >= blink_threshold:
            is_visible = not is_visible
            time_counter = 0
    for p in all_moving_points:
        update_point(p)
        
    glutPostRedisplay()
def draw_the_frame():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Projection setup
    glViewport(0, 0, 1500, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 1500, 0, 800, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if blink_status == True and is_visible == False:
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(1500, 0)
        glVertex2f(1500, 800)
        glVertex2f(0, 800)
        glEnd()
    else:
        glPointSize(10)  
        glBegin(GL_POINTS)
        for p in all_moving_points:
            glColor3f(p[4], p[5], p[6])
            glVertex2f(p[0], p[1])
        glEnd()

    glutSwapBuffers()
def initialize_program():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(1500, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Task 2 - Modular Moving Points")
    
    glutDisplayFunc(draw_the_frame)
    glutIdleFunc(physics_and_animation_logic)
    glutMouseFunc(my_mouse_input_handler)
    glutKeyboardFunc(my_keyboard_input_handler)
    glutSpecialFunc(my_special_keys_handler)
    
    glClearColor(0, 0, 0, 1)
    glutMainLoop()

if __name__ == "__main__":
    initialize_program()