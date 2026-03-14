from OpenGL.GL import *     # Core OpenGL functions (drawing, colors, etc.)
from OpenGL.GLUT import *   # GLUT library (window creation, display, loop)
from OpenGL.GLU import *    # OpenGL Utility Library (projection utilities)
import random
# --- Global coordinates of the point ---
x, y = 500,1000
bridgeness_level=0

# ===== Function to draw a single point =====
def draw_image(x, y):
    glPointSize(5)          
    glBegin(GL_POINTS)      
    glVertex2f(x, y)        
    glEnd()                 
    ## sky ===========================================
    glColor3f(bridgeness_level, bridgeness_level,bridgeness_level)
    
    glBegin(GL_QUADS)    
    glVertex2f(0, 375)    
    glVertex2f(1000, 375)  
    glVertex2f(1000, 500)  
    glVertex2f(0, 500)    
    glEnd()               
    
    ##ground===========================================
    glBegin(GL_TRIANGLES)  
    glColor3f(0.4, 0.2, 0.10)  
    glVertex2f(0,0)   
    glVertex2f(1000,0)   
    glVertex2f(0,375)    
    glEnd()


    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.10)    
    glVertex2f(0,375)
    glVertex2f(1000,0)    
    glVertex2f(1000,375)    
    glEnd()            
    
    
    ## Grass=================================================================
    glBegin(GL_TRIANGLES)
    glColor3f(0.1, 0.8, 0.2) 
    glVertex2f(0, 300)
    glVertex2f(66, 300)
    glVertex2f(33, 375)
    glVertex2f(66, 300)
    glVertex2f(133, 300)
    glVertex2f(100, 375)
    glVertex2f(133, 300)
    glVertex2f(200, 300)
    glVertex2f(166, 375)
    glVertex2f(200, 300)
    glVertex2f(266, 300)
    glVertex2f(233, 375)
    glVertex2f(266, 300)
    glVertex2f(333, 300)
    glVertex2f(300, 375)
    glVertex2f(333, 300)
    glVertex2f(400, 300)
    glVertex2f(366, 375)
    glVertex2f(400, 300)
    glVertex2f(466, 300)
    glVertex2f(433, 375)
    glVertex2f(466, 300)
    glVertex2f(533, 300)
    glVertex2f(500, 375)
    glVertex2f(533, 300)
    glVertex2f(600, 300)
    glVertex2f(566, 375)
    glVertex2f(600, 300)
    glVertex2f(666, 300)
    glVertex2f(633, 375)
    glVertex2f(666, 300)
    glVertex2f(733, 300)
    glVertex2f(700, 375)
    glVertex2f(733, 300)
    glVertex2f(800, 300)
    glVertex2f(766, 375)
    glVertex2f(800, 300)
    glVertex2f(866, 300)
    glVertex2f(833, 375)
    glVertex2f(866, 300)
    glVertex2f(933, 300)
    glVertex2f(900, 375)
    glVertex2f(933, 300)
    glVertex2f(1000, 300)
    glVertex2f(966, 375)
    glEnd()


#house drawing ===========================================
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.0, 0.5) 
    glVertex2f(350, 275)
    glVertex2f(650, 275)
    glVertex2f(500, 400)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.75, 0.75, 0.85) 
    glVertex2f(350, 75)
    glVertex2f(650, 75)
    glVertex2f(350, 275)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(650, 75)
    glVertex2f(650, 275)
    glVertex2f(350, 275)
    glEnd()
###window and door=================================================================
    # Door
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.6, 1.0) 
    glVertex2f(460, 75)
    glVertex2f(540, 75)
    glVertex2f(460, 180)
    glVertex2f(540, 75)
    glVertex2f(540, 180)
    glVertex2f(460, 180)
    glEnd()

    # Left Window
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.6, 1.0) 
    glVertex2f(380, 150)
    glVertex2f(430, 150)
    glVertex2f(380, 200)
    glVertex2f(430, 150)
    glVertex2f(430, 200)
    glVertex2f(380, 200)
    glEnd()

    # Left Window line
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0) 
    glVertex2f(405, 150)
    glVertex2f(405, 200)
    glVertex2f(380, 175)
    glVertex2f(430, 175)
    glEnd()

    # Right Window
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.6, 1.0) 
    glVertex2f(570, 150)
    glVertex2f(620, 150)
    glVertex2f(570, 200)
    glVertex2f(620, 150)
    glVertex2f(620, 200)
    glVertex2f(570, 200)
    glEnd()

    # Right Window line
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0) 
    glVertex2f(595, 150)
    glVertex2f(595, 200)
    glVertex2f(570, 175)
    glVertex2f(620, 175)
    glEnd()

    # Door point
    glPointSize(8)          
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 0.0) 
    glVertex2f(520, 120)   
    glEnd()
def keyboard_listener(key, x, y):
    global bridgeness_level
    
    if key == b'w': 
        if bridgeness_level < 1.0:       ###Keyboared listener for white 'w' and for black 'b'
            bridgeness_level += 0.05
    elif key == b'b':
        if bridgeness_level > 0.0:
            bridgeness_level -= 0.05
            
    glutPostRedisplay()




rain_position=[]
angle=0    ###setting the angle of the rain
speed=30       
def raining():
    global rain_position
    rain_position=[]
    for i in range(150):
        a = random.randint(0, 1000)
        b = random.randint(0, 500)
        rain_position.append([a,b])
def rain_drawing():
    glColor3f(0.6, 0.8, 1.0) 
    glLineWidth(1)
    glBegin(GL_LINES)
    for p in rain_position:
        glVertex2f(p[0], p[1])
        glVertex2f(p[0] + (angle * 2), p[1] - 25)  
    glEnd()
def animate():
    global rain_position
    for drp in rain_position:
        drp[1] -= speed  # Move down
        drp[0] += angle * 0.1 
        if drp[1] < 0:
            drp[1] = 500  
            drp[0] = random.randint(0, 1000) 
        if drp[0] > 1000:
            drp[0] = 0
        if drp[0] < 0: 
            drp[0] = 1000
            
    glutPostRedisplay()
def special_key_listener(key, x, y):
    global angle
    if key==GLUT_KEY_LEFT:      
        angle-=2
    elif key==GLUT_KEY_RIGHT:   
        angle+=2
    glutPostRedisplay()


# ===== Set up 2D coordinate system =====
def setup_projection():
    glViewport(0, 0, 1000, 500)     # Define the portion of the window to render to
    glMatrixMode(GL_PROJECTION)    # Switch to the projection matrix
    glLoadIdentity()               # Reset the projection matrix
    glOrtho(0.0, 1000, 0.0, 500, 0.0, 1.0)  # Define a 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)     # Switch back to the modelview matrix


# ===== Display callback =====
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer
    glLoadIdentity()                                    # Reset transformations
    setup_projection()                                  # Set up coordinate system
    glColor3f(0.1, 0.1, 0.3)                            # Set color (R, G, B) → Yellow
    draw_image(x, y)
    rain_drawing()                                   # Draw the point
    glutSwapBuffers()                                   # Swap buffers (double buffering)


# ===== Main entry point =====
def main():
    glutInit()                               # Initialize GLUT
    glutInitDisplayMode(GLUT_RGBA)           # Set display mode: RGBA color
    glutInitWindowSize(1000, 500)             # Set window size (width, height)
    glutInitWindowPosition(0, 0)             # Set window position (top-left corner)
    glutCreateWindow(b"OpenGL 2D Point")     # Create window with a title
    glutDisplayFunc(display) 
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutIdleFunc(animate)
    raining()                
    glutMainLoop()   
    

# ===== Run the program =====
if __name__ == "__main__":
    main()
