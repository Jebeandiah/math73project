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
sensitivity = 0.09
fps = 60
fov = 30
w_angle_pspace = [0., 0., 0.]
lx = 0
cam_position = numpy.array([0., 0., -5.])
cam_velocity = numpy.array([0., 0., 0.])
speed = 8
dominantplanet = 0
targetplanet = dominantplanet

# colors
background_color = (20, 20, 20)
cube_color = (255, 0, 70)

isgrounded = False
playerheight = 2
running = True
input_dir = numpy.array([0, 0, 0])

vertices = [ 
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1]
]

triangles = [[0, 1, 2], [3, 0, 2]]

# planets: [position, radius, gravity strength, color]
planets = [
    [[0., 10., -5.], 5., 0.2, (255, 100, 100)],     # reddish
    [[10., 20., 20.], 8., 0.25, (100, 255, 100)],   # greenish
    [[0., 0., 10.], 3.5, 0.15, (100, 100, 255)]     # bluish
]

planet_colors = []

def planetdotgen():
    for planet in planets:
        for _ in range(500):
            point = numpy.random.uniform(-1, 1, (1, 3))[0]
            point = point / numpy.linalg.norm(point) * planet[1] + planet[0]
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

def xyzrotmat(angles):
    return numpy.matmul(numpy.matmul(xrotmat(angles[0]), yrotmat(angles[1])), zrotmat(angles[2]))

def drawaxes(rmat):
    origin = numpy.array([0, 0, 2])
    directions = [[0, 0, 0.2], [0.2, 0, 0], [0, 0.2, 0]]
    for i, direction in enumerate(directions):
        direction = numpy.matmul(rmat, numpy.array(direction)) + origin
        pygame.draw.line(
            screen,
            (255 * (i + 1) / 3, 0, 255),
            (-origin[0] * 10000 / (origin[2] * fov) + screen_width / 2,
             origin[1] * 10000 / (origin[2] * fov) + screen_height / 2),
            (direction[0] * 10000 / (direction[2] * fov) + screen_width / 2,
             -direction[1] * 10000 / (direction[2] * fov) + screen_height / 2),
            5
        )

my = yrotmat(0)
playerrotation = yrotmat(0)
planetdir = -cam_position + planets[dominantplanet][0]
lplanetdir = planetdir
p2wmat = yrotmat(0)
switched_planets = False

while running:
    pygame.mouse.set_pos = (screen_width / 2, screen_height / 2)
    clock.tick(fps)
    screen.fill(background_color)

    strongestforce = 0
    isgrounded = False

    for i, planet in enumerate(planets):
        distance = numpy.linalg.norm(cam_position - planet[0])
        force = planet[2] / (distance * distance)
        if distance <= planet[1] + playerheight:
            isgrounded = True
            cam_velocity = numpy.array([0., 0., 0.])
        else:
            cam_velocity -= force * (cam_position - numpy.array(planet[0]))
        if force > strongestforce:
            strongestforce = force
            dominantplanet = i

    if targetplanet != dominantplanet:
        switched_planets = True

    if isgrounded:
        cam_position = planets[dominantplanet][0] - planetdir * (planets[dominantplanet][1] + playerheight - 0.01) / numpy.linalg.norm(planetdir)

    anglechange = numpy.array([0, 0, 0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            anglechange = numpy.array(pygame.mouse.get_rel()) * sensitivity
            lx = numpy.clip(lx + math.radians(anglechange[1]), -math.pi / 2.1, math.pi / 2.1)
            my = numpy.matmul(my, yrotmat(-math.radians(anglechange[0])))

    if switched_planets and isgrounded:
        lx = 0
        dx, dy, dz = planets[dominantplanet][0] - cam_position
        lplanetdir = planets[dominantplanet][0] - cam_position
        ax = -math.atan2(dz, dy)
        dx, dy, dz = numpy.matmul(xrotmat(ax), planets[dominantplanet][0] - cam_position)
        az = -math.atan2(dx, dy)
        playerrotation = numpy.matmul(zrotmat(-az), xrotmat(ax))
        switched_planets = False
        targetplanet = dominantplanet
    else:
        if switched_planets:
            planetdir = planets[targetplanet][0] - cam_position
        movexm = xrotmat(math.acos(numpy.clip(numpy.dot(planetdir, lplanetdir) / (numpy.linalg.norm(planetdir) * numpy.linalg.norm(lplanetdir)), -1, 1)))
        lplanetdir = planetdir

        if not isgrounded:
            localmovedir = numpy.matmul(p2wmat, cam_velocity)
            moveym = numpy.matmul(yrotmat(math.atan2(+localmovedir[0], localmovedir[2])), my)
        else:
            moveym = numpy.matmul(yrotmat(math.atan2(input_dir[0], input_dir[2])), my)

        playerrotation = numpy.matmul(numpy.matmul(numpy.matmul(numpy.transpose(moveym), movexm), moveym), playerrotation)

    p2wmat = numpy.matmul(my, playerrotation)
    pmov2wmat = numpy.transpose(p2wmat)
    c2wmat = numpy.matmul(xrotmat(lx), p2wmat)

    drawaxes(numpy.transpose(numpy.matmul(my, playerrotation)))
    input_dir = numpy.array([0., 0., 0.])

    if isgrounded:
        pressed_keys = pygame.key.get_pressed()
        input_dir[2] = pressed_keys[pygame.K_w] - pressed_keys[pygame.K_s]
        input_dir[0] = pressed_keys[pygame.K_a] - pressed_keys[pygame.K_d]
        if (input_dir != numpy.array([0, 0, 0])).any():
            cam_velocity += numpy.matmul(pmov2wmat, input_dir / numpy.linalg.norm(input_dir) * speed)
        if pressed_keys[pygame.K_SPACE]:
            cam_velocity *= 0.3
            cam_velocity += planetdir / numpy.linalg.norm(planetdir) * -2

    cam_position += cam_velocity / fps
    planetdir = planets[dominantplanet][0] - cam_position

    screen_vertices = []
    for i, vertice in enumerate(vertices):
        worldpos = numpy.matmul(c2wmat, vertice - cam_position)
        if worldpos[2] > 0:
            projectedpos = (-worldpos[0] * 10000 / (worldpos[2] * fov) + screen_width / 2,
                            worldpos[1] * 10000 / (worldpos[2] * fov) + screen_height / 2)
            screen_vertices.append(projectedpos)
            if i >= 8:  # skip cube vertices
                pygame.draw.circle(screen, planet_colors[i - 8], projectedpos, numpy.clip(400 / (worldpos[2] * fov), 1, 1000))
        else:
            worldpos[2] = 0.01
            screen_vertices.append((-worldpos[0] * 10000 / (worldpos[2] * fov) + screen_width / 2,
                                    worldpos[1] * 10000 / (worldpos[2] * fov) + screen_height / 2))

    for i, triangle in enumerate(triangles):
        edges = [
            (screen_vertices[triangle[0]][0], screen_vertices[triangle[0]][1]),
            (screen_vertices[triangle[1]][0], screen_vertices[triangle[1]][1]),
            (screen_vertices[triangle[2]][0], screen_vertices[triangle[2]][1])
        ]
        pygame.draw.polygon(screen, (255 * (i + 1) / len(triangles), 100, 100), edges)

    for planet in planets:
        worldpos = numpy.matmul(c2wmat, numpy.array(planet[0]) - cam_position)
        if worldpos[2] > 0:
            projectedpos = (
                -worldpos[0] * 10000 / (worldpos[2] * fov) + screen_width / 2,
                worldpos[1] * 10000 / (worldpos[2] * fov) + screen_height / 2
            )
            radius_screen = int(10000 * planet[1] / (worldpos[2] * fov))

    pygame.display.update()

pygame.quit()
