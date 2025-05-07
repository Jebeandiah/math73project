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
look_angle =[0.,0.,0.]
player_angle =[0.,0.,0.]

cam_angle = [0.,0.,0.]
cam_position = numpy.array([0.,0.,-5.])
cam_velocity = numpy.array([0.,0.,0.])
speed = 3
dominantplanet =0
# colors:
background_color = (240, 235, 240)
cube_color = (255, 0, 70)
circle_color = (255, 0, 70)
isgrounded = False
playerheight = 2
running = True

vertices = [ 
    [-1, -1,1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
    [-1,-1,-1],
    [1, -1,-1],
    [1, 1, -1],
    [-1, 1,-1]
            
            ] 
triangles = [[0,1,2],#index of vertices in vertices
             [3,0,2]
            ]  
planets =[[[0.,10.,0.], 5., .1]] #planet center, radius, gravity

def xrotmat(angle):
    return [
    [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]
def yrotmat(angle):
    return [
    [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
    ]
def zrotmat(angle):
    return [
    [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]

def checkplanets():
    strongestforce =0
    global cam_velocity
    global isgrounded 
    global dominantplanet
    isgrounded = False
    for i, planet in enumerate(planets):
        distance = numpy.linalg.norm(cam_position-numpy.array(planet[0]))
        force = planet[2]/(distance*distance)
        #print(distance)

        if(distance<(planet[1]+playerheight)):
            isgrounded =True
            cam_velocity = numpy.array([0.,0.,0.])
        else:
            #print(distance)
            #cam_velocity -= force*(cam_position-numpy.array(planet[0]))/fps
            ...
        #print(force*(cam_position-numpy.array(planet[0]))/(distance*fps))
        if force>strongestforce: 
            strongestforce = force
            dominantplanet = i


while running:
    pygame.mouse.set_pos = (screen_width/2, screen_height/2)
    clock.tick(fps)
    screen.fill(background_color)
    # process window events:
    checkplanets()
    
    #cam_angle[0]-=xrot
    #zrot = unit_vector(v2)
    #return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    #print(cam_angle)
    cam_position+=cam_velocity
    input_dir = numpy.array([0,0,0]) 
    anglechange = numpy.array([0,0,0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            anglechange=numpy.array(pygame.mouse.get_rel())/fps*sensitivity
            look_angle[0] = numpy.clip(look_angle[0]+math.radians(anglechange[1]), -math.pi/2.1, math.pi/2.1)
            player_angle[1]+=math.radians(anglechange[0])
            #print(look_angle[0])
            #print(cam_angle)
    rotation_matrix_x = xrotmat(cam_angle[0])
    rotation_matrix_y = yrotmat(cam_angle[1])    
    rotation_matrix_z = zrotmat(cam_angle[2])
    negrotation_matrix_y = yrotmat(-cam_angle[1])
    rotation_matrix_yz = numpy.linalg.matmul(rotation_matrix_y, rotation_matrix_z)
    rotation_matrix_xyz = numpy.linalg.matmul(rotation_matrix_x, rotation_matrix_yz)

    #print(player_angle[1])
    
    planetdir = numpy.array(planets[dominantplanet][0]-cam_position)

    #print(planetdir)
    #player_angle[0] = math.atan2(planetdir[2], planetdir[1])
    player_angle[2] = -math.atan2(planetdir[0], planetdir[1])
    #print(player_angle[1])
    #player_angle[2] = numpy.arccos(numpy.clip(numpy.dot( planetzdirnorm,numpy.array([0,1])),-1.0, 1.0))
    #print(player_angle[2])
    playerrotation_matrix_xyz = numpy.linalg.matmul(numpy.linalg.matmul(xrotmat(player_angle[0]), negrotation_matrix_y), zrotmat(player_angle[2]))

    #print(numpy.arccos(numpy.clip(numpy.dot( planetxdirnorm,numpy.array([0,1])),-1.0, 1.0)))
    #print(numpy.arccos(numpy.clip(numpy.dot( numpy.array([0,1]),planetzdirnorm),-1.0, 1.0)))
    #player_angle[1] -= numpy.arccos(numpy.clip(numpy.dot( numpy.array([0,1]),planetxdirnorm),-1.0, 1.0))
    #print(numpy.arccos(numpy.clip(numpy.dot( numpy.array([0,1]),planetxdirnorm),-1.0, 1.0)))
    #cam_angle = player_angle+look_angle
    #print(player_angle[2])
    cam_angle = numpy.array(look_angle) - numpy.array(player_angle)
    print(look_angle, end="  ")
    print(player_angle, end="  ")
    print(cam_angle)
    #print(numpy.arccos(numpy.clip(numpy.dot( numpy.array([0,1]),planetxdirnorm),-1.0, 1.0)))
    #print(cam_angle[1])
    #print (dominantplanet[0]-cam_position)
    #print(planetxdirnorm)
    #print(numpy.arccos(numpy.clip(numpy.dot( numpy.array([0,1]),planetxdirnorm),-1.0, 1.0)))
    #print(numpy.arccos(numpy.clip(numpy.dot (numpy.array([0,1]),planetxdirnorm),-1.0, 1.0)))
    #print(numpy.arccos(numpy.clip(numpy.dot(planetxdirnorm, numpy.array([0,1])),-1.0, 1.0)))
    #cam_angle[0] = numpy.arccos(numpy.clip(numpy.dot(numpy.array([planetdir[2],planetdir[1]])/numpy.linalg.norm(numpy.array([planetdir[2],planetdir[1]])), numpy.array([0,1])),-1.0, 1.0))+cam_angle[0]
    #cam_angle[0]+=xrot
    #print(numpy.array([planetdir[0],planetdir[2]])/numpy.linalg.norm(numpy.array([planetdir[0],planetdir[2]])))
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

        #print(numpy.matmul(negrotation_matrix_y,input_dir/(numpy.linalg.norm(input_dir)*fps)*speed))
        cam_position+=numpy.matmul(playerrotation_matrix_xyz,input_dir/(numpy.linalg.norm(input_dir)*fps)*speed)
        #cam_position+=input_dir/(numpy.linalg.norm(input_dir)*fps)*speed

        #print(numpy.matmul(playerrotation_matrix_xyz,input_dir/(numpy.linalg.norm(input_dir))*speed))
        #print(player_angle)
        # cam_position+=input_dir/(numpy.linalg.norm(input_dir)*fps)*speed
    #print(str(cam_position)+" "+str(cam_angle))
    #print(cam_angle)
    screen_vertices =[]
    for vertice in vertices:
        #renderedvertices = 
        worldpos = numpy.matmul( rotation_matrix_xyz, vertice-cam_position)
        if(worldpos[2]>0):
            projectedpos =(-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2)

            screen_vertices.append(projectedpos)

            pygame.draw.circle(screen, circle_color, projectedpos, 2)
        else:
            worldpos[2]=0.01
            screen_vertices.append((-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2))
        #print(worldpos)
    for i, triangle in enumerate(triangles):
        edges = [
            (screen_vertices[triangle[0]][0], screen_vertices[triangle[0]][1]),
            (screen_vertices[triangle[1]][0], screen_vertices[triangle[1]][1]),
            (screen_vertices[triangle[2]][0], screen_vertices[triangle[2]][1])
        ]
        pygame.draw.polygon(screen, (255*(i+1)/len(triangles), 100, 100 ), edges)
    for planet in planets:
        worldpos = numpy.matmul(rotation_matrix_xyz,planet[0]-cam_position)
        if(worldpos[2]>0):
            projectedpos =(-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2)
            pygame.draw.circle(screen, circle_color, projectedpos, 10000*planet[1]/(worldpos[2]*fov))


    pygame.display.update()

pygame.quit()