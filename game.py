import pygame
import math
import numpy

screen_width, screen_height = 1200, 800

# init pygame settings:
pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
sensitivity = 0.09
fps = 60
fov = 30
w_angle_pspace = [0., 0., 0.]
cx =0
cam_position = numpy.array([0.,0.,0.])
cam_velocity = numpy.array([0.,0.,2.])
speed = 8
dominantplanet =0
targetplanet = dominantplanet

# colors:
#background_color = (240, 235, 240)
background_color = (20, 15, 25)
cube_color = (255, 0, 70)
circle_color = (255, 0, 70)
isgrounded = False
playerheight = 2
running = True
input_dir = numpy.array([0,0,0])
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
planets = [
    [[0., 10., -5.], 5., 0.2, (255, 100, 100)],     # reddish
    [[10., 20., 20.], 8., 0.25, (100, 255, 100)],   # greenish
    [[0., 0., 10.], 3.5, 0.15, (100, 100, 255)]     # bluish
]
planet_colors = []

#[[10.,20.,20.], 8., 0.25],[[0.,0.,10.], 3.5, 0.15]
def planetdotgen():
    for planet in planets:
        for i in range(500):
            point = numpy.random.uniform(-1, 1,(1,3))[0]
            point = point/numpy.linalg.norm(point)*planet[1]+planet[0] 
            #print(point)
            vertices.append(point)
            planet_colors.append(planet[3])


planetdotgen()
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

def drawaxes(rmat):
    #origin = numpy.matmul(rmat, numpy.array([0,0,2]))
    origin = numpy.array([0,0,2])
    directions = [[0,0,0.2],[0.2,0,0],[0,0.2,0] ]
    for i, direction in enumerate(directions):
        # Draw a red line from (0, 0) to (500, 500) with a thickness of 5 pixels
        direction = numpy.matmul(rmat,numpy.array(direction))+origin
        pygame.draw.line(screen,(255*(i+1)/3, 0, 255), (-origin[0]*10000/(origin[2]*fov)+screen_width/2, origin[1]*10000/(origin[2]*fov)+screen_height/2), (direction[0]*10000/(direction[2]*fov)+screen_width/2, -direction[1]*10000/(direction[2]*fov)+screen_height/2), 5)

my = yrotmat(0)
playerrotation = yrotmat(0)
planetdir = -cam_position + planets[dominantplanet][0]
lplanetdir = planetdir
p2wmat = numpy.eye(3)
switched_planets = True
lcamvel =numpy.array([0,0,2])
apy=0
lmovang =0
landingangle =0
lmovdir = numpy.array([0,0,1])
R = numpy.eye(3)
nullvoffset =0
while running:

    pygame.mouse.set_pos = (screen_width/2, screen_height/2)
    clock.tick(fps)
    screen.fill(background_color)

    strongestforce =0
    wasgrounded = isgrounded
    isgrounded = False
    #print(str(lcamvel)+" hehe", end=" ")

    for i, planet in enumerate(planets):
        distance = numpy.linalg.norm(cam_position-planet[0])
        force = planet[2]/(distance*distance)
        if(distance <= planet[1]+playerheight):
            isgrounded =True
            
        else:
            cam_velocity -= force*(cam_position-numpy.array(planet[0]))
        if force>strongestforce: 
            strongestforce = force
            dominantplanet = i
    if(targetplanet!=dominantplanet):
        #print("switch")
        switched_planets = True
    if(isgrounded):
        targetplanet = dominantplanet
        switched_planets = False
        cam_velocity = numpy.array([0.,0.,0.])
        cam_position = planets[dominantplanet][0] - planetdir * (planets[dominantplanet][1] + playerheight -.01) / numpy.linalg.norm(planetdir)
    #print(switched_planets)
    #print(lcamvel)

    anglechange = numpy.array([0,0,0])
    dpy = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_rel()
            cx = numpy.clip(cx+math.radians(mouse[1]*sensitivity), -math.pi/2., math.pi/2.)
            dpy -=math.radians(mouse[0]*sensitivity)
            #print(mouse, end=" ")
           # print(py, end=" ")
            #my= yrotmat(-math.radians(anglechange[0]))
            #my = yrotmat(math.pi/2)
    
    input_dir = numpy.array([0.,0.,0.]) 
    if (isgrounded):
        nullvoffset =0
        pressed_keys = pygame.key.get_pressed()
        input_dir[2] = pressed_keys[pygame.K_w] - pressed_keys[pygame.K_s]
        input_dir[0] = pressed_keys[pygame.K_a] - pressed_keys[pygame.K_d]
        if((input_dir!=numpy.array([0,0,0])).any() ):
            apy =0
            cam_velocity += numpy.matmul(pmov2wmat,input_dir/(numpy.linalg.norm(input_dir))*speed)
            lmovdir = input_dir
            lmovang = -math.atan2(input_dir[0], input_dir[2])
            #print(lcamvel)
            #lcamvel = cam_velocity/fps
        if pressed_keys[pygame.K_SPACE] and wasgrounded:
            
            cam_velocity *= 0.3
            cam_velocity += planetdir/numpy.linalg.norm(planetdir)*-2
    cam_position += cam_velocity/fps
    if((input_dir==numpy.array([0,0,0])).all()):
        #print(apy)
        apy+= dpy
    
    yoffset = dpy+apy +lmovang
    #print(anglechange)S
    #lcamvel = numpy.matmul(numpy.transpose(my), lcamvel)
    #lcamvel = numpy.matmul(my, lcamvel)
    tpdir = planetdir = planets[targetplanet][0] - cam_position

    newup = tpdir / numpy.linalg.norm(tpdir)
   
    newf =cam_velocity -numpy.dot(cam_velocity,newup)*newup

    if numpy.linalg.norm(newf) <  1e-6:
        newf = lcamvel-numpy.dot(lcamvel,newup)*newup

    else:
        lcamvel = numpy.copy(cam_velocity)
    #print(newf)
    newf /= numpy.linalg.norm(newf)
    #print(newf)
    #print(yoffset)
    
    

    if isgrounded:

        f = yrotmat(yoffset) @ numpy.array([0, 0, 1])
        up = numpy.array([0, 1, 0])
        # if not isgrounded:
        #     print(newf, end=" ")
        #     newf = newf-numpy.dot(newf,p2wmat.T@l)*p2wmat.T@newup
        #     print(newf)
        #     newf /= numpy.linalg.norm(newf)
        if  not wasgrounded:
            wasgrounded = True
            f= numpy.array([0, 0, 1])
            l= numpy.array([1, 0, 0])
            olddir = c2wmat.T@f
            newf = olddir - numpy.dot(olddir, newup)*newup
            #newlook = olddir - numpy.dot(olddir, l)*l
            newf/=numpy.linalg.norm(newf)
            lcamvel = numpy.copy(newf)
            cam_velocity = numpy.copy(newf)
            apy -= yoffset
           #cx=-math.acos(numpy.clip(numpy.dot(newlook, newup)/(numpy.linalg.norm(newf)*numpy.linalg.norm(newlook)),-1, 1 ))+math.pi/2
            cx = math.acos(numpy.clip(numpy.dot(olddir, newf)/(numpy.linalg.norm(olddir)),-1, 1 ))
            print(cx)
        l = numpy.cross(f, up)


        lmy = my
        #print(newf, end=" ")
        newl = numpy.cross(newf, newup)
        U = numpy.column_stack((f, up, l))
        V = numpy.column_stack((newf, newup, newl))
        # if numpy.sign(numpy.linalg.det(V)) != numpy.sign(numpy.linalg.det(U)):
        #     U[:, 2] *= -1  


        p2wmat = U @ V.T
        #olddir = p2wmat@c2wmat@p2wmat.T@f
        #ydif = yrotmat(-math.atan2(olddir[0], 1))
        #print(olddir, end = " ")
        #print(f)

      
        playerrotation = yrotmat(-apy)@p2wmat

    else:
        movexm = xrotmat(math.acos(numpy.clip(numpy.dot(planetdir, lplanetdir)/(numpy.linalg.norm(planetdir)*numpy.linalg.norm(lplanetdir)),-1, 1 )))
        localmovedir = numpy.matmul(p2wmat, lcamvel)
        moveym = yrotmat(math.atan2(+localmovedir[0],localmovedir[2])+apy)
  
        playerrotation = numpy.matmul(numpy.matmul(numpy.matmul(numpy.transpose(moveym),movexm ), moveym), playerrotation)
        #playerrotation = p2wmat@movexm@p2wmat.T@playerrotation

        p2wmat = numpy.matmul(yrotmat(apy), playerrotation)
    lplanetdir = planetdir        

    # planetdir = planets[dominantplanet][0]-cam_position
    # movexm = xrotmat(math.acos(numpy.clip(numpy.dot(planetdir, lplanetdir)/(numpy.linalg.norm(planetdir)*numpy.linalg.norm(lplanetdir)),-1, 1 )))
    # moveym = numpy.matmul(yrotmat(math.atan2(input_dir[0], input_dir[2])), my)
    # lplanetdir = planetdir
    # if not numpy.array_equal(input_dir,numpy.array([0,0,0])):
    #     playerrotation = numpy.matmul(numpy.matmul(numpy.matmul(numpy.transpose(moveym),movexm ), moveym), playerrotation)
   
    # p2wmat = numpy.matmul(my, playerrotation)
    pmov2wmat = p2wmat.T
    #pmov2wmat = p2wmat
    c2wmat = numpy.matmul(xrotmat(cx),p2wmat )
    drawaxes(pmov2wmat)
    
   
    
    planetdir = planets[dominantplanet][0] - cam_position


    screen_vertices =[]
    for i, vertice in enumerate(vertices):
        #renderedvertices = 
        worldpos = numpy.matmul( c2wmat, vertice-cam_position)
        if(worldpos[2]>0):
            projectedpos =(-worldpos[0]*10000/(worldpos[2]*fov)+screen_width/2, worldpos[1]*10000/(worldpos[2]*fov)+screen_height/2)

            screen_vertices.append(projectedpos)
            if i >= 8:  # skip cube vertices
                pygame.draw.circle(screen, planet_colors[i - 8], projectedpos, numpy.clip(400 / (worldpos[2] * fov), 1, 1000))
            else:
                pygame.draw.circle(screen, circle_color, projectedpos, numpy.clip(400/(worldpos[2]*fov),1, 1000))
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
            #pygame.draw.circle(screen, circle_color, projectedpos, 10000*planet[1]/(worldpos[2]*fov))


    pygame.display.update()
    # if not wasgrounded and isgrounded:
    #     wasgrounded = True
    #     clock.tick(0.6)

pygame.quit()