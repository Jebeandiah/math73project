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
w_angle_pspace = [0., 0., 0.]
ay =0
lx =0
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
planets =[[[0.,-10.,-5.], 5., .1]] #planet center, radius, gravity

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

def xyzrotmat(angles):
    return numpy.matmul(numpy.matmul(xrotmat(angles[0]), yrotmat(angles[1])), zrotmat(angles[2]))
def drawaxes(rmat):
    #origin = numpy.matmul(rmat, numpy.array([0,0,2]))
    origin = numpy.array([0,0,2])
    directions = [[0,0,0.2],[0.2,0,0],[0,0.2,0] ]
    for i, direction in enumerate(directions):
        # Draw a red line from (0, 0) to (500, 500) with a thickness of 5 pixels
        direction = numpy.matmul(rmat,numpy.array(direction))+origin
        pygame.draw.line(screen,(255*(i+1)/3, 0, 255), (-origin[0]*10000/(origin[2]*fov)+screen_width/2, origin[1]*10000/(origin[2]*fov)+screen_height/2), (direction[0]*10000/(direction[2]*fov)+screen_width/2, -direction[1]*10000/(direction[2]*fov)+screen_height/2), 5)

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
            cam_velocity -= force*(cam_position-numpy.array(planet[0]))
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
    cam_position+=cam_velocity/fps
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
            lx = numpy.clip(lx+math.radians(anglechange[1]), -math.pi/2.1, math.pi/2.1)
            ay-=math.radians(anglechange[0])
            #print(look_angle[0])
            #print(cam_angle)
    #negrotation_matrix_xyz = numpy.linalg.matmul(numpy.matmul(xrotmat(0*cam_angle[0]), yrotmat(-cam_angle[1])), zrotmat(0*cam_angle[2]))
    #print(player_angle[1])
    
    dx, dy, dz = planets[dominantplanet][0]-cam_position
    ax=-math.atan2(dz, dy)
    dx, dy, dz = numpy.matmul(xrotmat(ax),planets[dominantplanet][0]-cam_position)
    az = -math.atan2(dx, dy)
    p2wmat=numpy.matmul(numpy.matmul(yrotmat(ay), zrotmat(-az)), xrotmat(ax))
    pmov2wmat = numpy.transpose(p2wmat)
    #pmov2wmat = numpy.transpose((numpy.matmul(numpy.matmul(zrotmat(-ay), xrotmat(ax)), zrotmat(az))))
    c2wmat = numpy.matmul(xrotmat(lx),p2wmat )
   
    drawaxes(pmov2wmat)
    

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
        cam_position+=numpy.matmul(pmov2wmat,input_dir/(numpy.linalg.norm(input_dir)*fps)*speed)
        #print(numpy.matmul(playerrotation_matrix_xyz,input_dir/(numpy.linalg.norm(input_dir))*speed))
    screen_vertices =[]
    for vertice in vertices:
        #renderedvertices = 
        worldpos = numpy.matmul( c2wmat, vertice-cam_position)
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
        worldpos = numpy.matmul(c2wmat,planet[0]-cam_position)
        if(worldpos[2]>0):
            projectedpos =(-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2)
            pygame.draw.circle(screen, circle_color, projectedpos, 10000*planet[1]/(worldpos[2]*fov))


    pygame.display.update()

pygame.quit()