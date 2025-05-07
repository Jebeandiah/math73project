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
look_angle = numpy.array([0.,0.,0.])
player_angle = numpy.array([0.,0.,0.])


cam_angle = [0.,0.,0.]
cam_position = numpy.array([0.,0.,-5.])
cam_velocity = numpy.array([0.,0.,0.])
speed = 3
dominantplanet = 0

# colors:
background_color = (240, 235, 240)
cube_color = (255, 0, 70)
circle_color = (255, 0, 70)
isgrounded = False
playerheight = 2
running = True

# List of vertices
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
# List of faces using vertex indices
triangles = [
    [0,1,2],
    [3,0,2]
]  

# List of planets
planets =[[[0.,10.,0.], 5., .1]] # planet center, radius, gravity

# Standard Rotation matrices
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
def rotate(angle):
    return numpy.matmul(xrotmat(angle), numpy.matmul(yrotmat(angle), zrotmat(angle)))

totalRot = numpy.matmul(xrotmat(0), numpy.matmul(yrotmat(0), zrotmat(0)))

# Checks which planet is the dominant planet (to revolve around)
def findDominantPlanet():
    strongestforce = 0
    global cam_velocity
    global isgrounded 
    global dominantplanet
    isgrounded = False
    for i, planet in enumerate(planets):
        distance = numpy.linalg.norm(cam_position-numpy.array(planet[0]))
        force = planet[2]/(distance*distance)
        if(distance<=(planet[1]+playerheight) + 0.0001):
            isgrounded = True
            cam_velocity = numpy.array([0.,0.,0.])
        else:
            cam_velocity -= force*(cam_position-numpy.array(planet[0]))
            ...
        if force > strongestforce: 
            strongestforce = force
            dominantplanet = i

# Main Loop
while running:
    pygame.mouse.set_pos = (screen_width/2, screen_height/2)
    clock.tick(fps)
    screen.fill(background_color)
    # process window events:
    findDominantPlanet()

    input_dir = numpy.array([0,0,0]) 
    anglechange = numpy.array([0,0,0])

    # Log Inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            anglechange = numpy.array(pygame.mouse.get_rel()) / fps * sensitivity
            look_angle[1] = numpy.clip(look_angle[1] + math.radians(anglechange[1]), -math.pi/2.1, math.pi/2.1)
            look_angle[0] -= math.radians(anglechange[0])

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        input_dir[2] += 1
    if pressed_keys[pygame.K_a]:
        input_dir[0] -= 1
    if pressed_keys[pygame.K_s]:
        input_dir[2] -= 1
    if pressed_keys[pygame.K_d]:
        input_dir[0] += 1

    wanted_position = cam_position + cam_velocity / fps
    bound_position = planets[dominantplanet][0] + (wanted_position - planets[dominantplanet][0]) * (planets[dominantplanet][1]+playerheight) / numpy.linalg.norm(wanted_position - planets[dominantplanet][0])
    if numpy.linalg.norm(wanted_position - planets[dominantplanet][0]) > numpy.linalg.norm(bound_position - planets[dominantplanet][0]):
        cam_position = wanted_position
    else:
        cam_position = bound_position

    if ((input_dir != numpy.array([0,0,0])).any()):
        pos_change = numpy.matmul(totalRot, input_dir/(numpy.linalg.norm(input_dir)) * speed/fps)
        cam_position -= [pos_change[0], -pos_change[1], -pos_change[2]] 
    planetdir = numpy.array(planets[dominantplanet][0] - cam_position)
    player_angle[2] = -math.atan2(planetdir[0], planetdir[1])
    # player_angle[0] = -math.atan2(planetdir[2], planetdir[1])
    cam_angle = look_angle - player_angle      

    # print(numpy.linalg.norm(cam_position - planets[dominantplanet][0]))
    # print(planetdir[2], end=" ")
    # print(planetdir[1])
  
    print(cam_position, end=" ")
    print(cam_angle)
    xrot = xrotmat(cam_angle[1])
    yrot = yrotmat(cam_angle[0])    
    zrot = zrotmat(cam_angle[2])
    yreverseRot = yrotmat(-cam_angle[0])
    yzRot = numpy.matmul(yrot, zrot)
    totalRot = numpy.matmul(xrot, yzRot)

    # Drawing to screen
    screen_vertices =[]
    for vertice in vertices:
        #renderedvertices = 
        worldpos = numpy.matmul(totalRot, vertice-cam_position)
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
        worldpos = numpy.matmul(totalRot,planet[0]-cam_position)
        if(worldpos[2]>0):
            projectedpos =(-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2)
            pygame.draw.circle(screen, circle_color, projectedpos, 10000*planet[1]/(worldpos[2]*fov))


    pygame.display.update()

pygame.quit()