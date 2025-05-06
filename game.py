import pygame
import math
import numpy

screen_width, screen_height = 800, 600

# init pygame settings:
pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
sensitivity = 10
fps = 240
fov = 30
cam_angle = [0,0]
cam_position = numpy.array([0.,0.,-5.])
speed = 3
# colors:
background_color = (240, 235, 240)
cube_color = (255, 0, 70)
circle_color = (255, 0, 70)

running = True

vertices = [ [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1]
            
            ] 
triangles = [[0,1,2],#index of vertices in vertices
             [3,0,2]
            ]  
renderedvertices = []

while running:
    pygame.mouse.set_pos = (screen_width/2, screen_height/2)
    clock.tick(fps)
    screen.fill(background_color)
    # process window events:
    input_dir = numpy.array([0,0,0]) 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mmov = pygame.mouse.get_rel()
            anglechange=numpy.array(mmov)/fps*sensitivity
            cam_angle = numpy.array([cam_angle[0]-math.radians(anglechange[0]), numpy.clip(cam_angle[1]+math.radians(anglechange[1]), -math.pi/2.1, math.pi/2.1)])
            print(cam_angle)
    rotation_matrix_x =[
    [1, 0, 0],
        [0, math.cos(cam_angle[1]), -math.sin(cam_angle[1])],
        [0, math.sin(cam_angle[1]), math.cos(cam_angle[1])]
    ]

    rotation_matrix_y = [
        [math.cos(cam_angle[0]), 0, -math.sin(cam_angle[0])],
        [0, 1, 0],
        [math.sin(cam_angle[0]), 0, math.cos(cam_angle[0])]
    ]
    negrotation_matrix_y = [
        [math.cos(-cam_angle[0]), 0, -math.sin(-cam_angle[0])],
        [0, 1, 0],
        [math.sin(-cam_angle[0]), 0, math.cos(-cam_angle[0])]
    ]
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        input_dir[2]+=1
    if pressed_keys[pygame.K_a]:
        input_dir[0]+=1
    if pressed_keys[pygame.K_s]:
        input_dir[2]-=1
    if pressed_keys[pygame.K_d]:
        input_dir[0]-=1
    if((input_dir!=numpy.array([0,0,0])).any() ):

        cam_position+=numpy.matmul(negrotation_matrix_y, input_dir/(numpy.linalg.norm(input_dir)*fps)*speed)
        # cam_position+=input_dir/(numpy.linalg.norm(input_dir)*fps)*speed
    #print(str(cam_position)+" "+str(cam_angle))
    #print(cam_angle)
    screen_vertices =[]
    for vertice in vertices:
        #renderedvertices = 
        worldpos = numpy.matmul( numpy.matmul(rotation_matrix_x, rotation_matrix_y), vertice-cam_position)
        projectedpos =(-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2)
        if(worldpos[2]>0):
            screen_vertices.append(projectedpos)

            pygame.draw.circle(screen, circle_color, projectedpos, 2)
        else:
            worldpos[2]=0.01
            screen_vertices.append((-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2))
        #print(worldpos)
    for triangle in triangles:
        edges = [
            (screen_vertices[triangle[0]][0], screen_vertices[triangle[0]][1]),
            (screen_vertices[triangle[1]][0], screen_vertices[triangle[1]][1]),
            (screen_vertices[triangle[2]][0], screen_vertices[triangle[2]][1])
        ]
        pygame.draw.polygon(screen, (100 , 100, 100 ), edges)
    #pygame.draw.circle(screen, circle_color, (0, 0+screen_height/2), 2)

    pygame.display.update()

pygame.quit()