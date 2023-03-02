import AStarClass
import Dijkstra
from static import *
from ProjectileClass import *
from PlayerClass import *
from VectorClass import *
from CollisionClass import *
from PortalClass import *
from ObstacleClass import *
from DrawClass import backgroundDrawing, createBackground
import pygame
from pygame import mixer
from TextClass import Text
from math import *

pygame.init()

# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
size = pygame.display.Info()
screen = pygame.display.set_mode((size.current_w, size.current_h))

screenW = size.current_w
screenH = size.current_h

menuFont = pygame.font.Font('static/MainFont.otf', int(screenW / 6.5))
nodeFont = pygame.font.Font('static/MainFont.otf', int(screenW / 32.5))

menuText = Text(menuFont, Colours.orange, 'Portal', 70, 35)
menuText2 = Text(menuFont, Colours.orange, 'Game', 70, menuText.height)

BackgroundNoise = mixer.Sound('static/Still Alive.mp3')
click = mixer.Sound('static/buttonClick.wav')


def button(mx, my, buttonName, colourChange, function):
    # exit button
    backgroundDrawing.lines[buttonName].colour = Colours.black
    if not backgroundDrawing.lines[buttonName].drawing.collidepoint(mx, my):
        return
    backgroundDrawing.lines[buttonName].colour = colourChange
    if player.leftMouse:
        click.play()
        pygame.time.wait(160)
        function()


# event loop
def eventLoop():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
            player.leftMouse = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == right:
            player.rightMouse = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()


def Play():
    # variables
    backgroundDrawing.lines['startButton'].doDraw = False
    backgroundDrawing.lines['scoresButton'].doDraw = False
    PathA, nodesMap = AStarClass.createNodes()
    PathD = Dijkstra.createPath(nodesMap)
    frame = 0
    while True:
        # set fps
        clock.tick(fps)
        frame += 1
        # check for mouse attributes
        eventLoop()
        mx, my = pygame.mouse.get_pos()

        # find facing angle
        angle = player.findAngle(mx, my)
        xChange = cos(angle)
        yChange = -sin(angle)

        backgroundDrawing.drawMap(screen)
        player.drawPlayer(screen)
        player.facingLine(20, screen)
        ObstacleSprite.drawObstacle(gameMap.obstacles, screen)
        for line in collisionObj:
            pygame.draw.line(screen, Colours.red, [line.x1, line.y1], [line.x2, line.y2])

        button(mx, my, "xButton", Colours.red, quit)
        if frame % 10 == 0:
            PathA.findPath(player)
        # PathD.findPath(player)
        for node in nodesMap:
            node.drawNode(screen, nodeFont, PathA, nodesMap[-1])

        # define walls and pointer
        L1.setCoord(posVec.i + xChange, posVec.j + yChange, xChange * mL + posVec.i, yChange * mL + posVec.j)

        # check if player moves left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            vel.add(acceleration, 'i')

        if keys[pygame.K_a]:
            vel.subtract(acceleration, 'i')

        if vel.i > 0.01:
            player.movingRight = True
            player.lastMoved = "right"

        if vel.i < -0.01:
            player.movingLeft = True
            player.lastMoved = "left"

        # add gravity vector to velocity
        vel.add(gravity, 'j')

        # check if player stops moving
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            vel.scale(deceleration, 'i')

        # check for collisions
        collide = player.objectCollide((objectSprites, invisibleSprites))
        posVec.add(vel, 'i')
        posVec.add(vel, 'j')
        player.setPos(posVec.i, posVec.j)

        if player.canJump and keys[pygame.K_w] or keys[pygame.K_SPACE]:
            vel.j = -16
            player.canJump = False
        # if player presses w or space and can jump they jump
        if collide:
            player.canJump = True

        # stop acceleration once terminal velocity is reached
        if vel.i > terminalVel.i > 0:
            vel.limit(terminalVel, 'i')
        elif vel.i < -terminalVel.i < 0:
            terminalVel.reverse('i')
            vel.limit(terminalVel, 'i')
            terminalVel.reverse('i')

        # draw projectile to the screen
        projectile.drawProjectile(speed, screen)
        projectile2.drawProjectile(speed, screen)
        portalSprites.update(screen)
        objectSprites.update(screen)
        invisibleSprites.update(screen)
        projectile.update()
        projectile2.update()
        player.update()

        # if portal makes collision draw a portal
        projectile.collision("left", portal, portalSprites)
        projectile.collision("left", portal, objectSprites, invisibleSprites)
        # if portal makes collision draw a portal
        projectile2.collision("right", portal2, portalSprites)
        projectile2.collision("right", portal2, objectSprites, invisibleSprites)

        projectile.startProjectile(angle, "left", L1, Colours.blue)
        projectile2.startProjectile(angle, "right", L1, Colours.orange)

        # if player can teleport then check for collisions and teleport
        player.portalCollide()
        player.reset()

        pygame.display.update()


def Menu():
    # one time statements
    backgroundY = 0
    BackgroundNoise.play()
    BackgroundNoise.set_volume(0.00)
    createBackground(screenW, screenH)
    while True:
        # statements every frame
        eventLoop()
        mx, my = pygame.mouse.get_pos()
        screen.fill(Colours.white)
        clock.tick(fps)
        # draw map
        backgroundDrawing.drawMap(screen)

        button(mx, my, "xButton", Colours.red, quit)
        button(mx, my, "startButton", Colours.orange, Play)
        button(mx, my, "scoresButton", Colours.blue, "")

        # draw static portals
        pygame.draw.ellipse(screen, Colours.blue, [screenW / 2 - depth, screenH - 69, 60, 35], 5)
        pygame.draw.ellipse(screen, Colours.orange, [screenW / 2 - depth, 34, 60, 35], 5)

        # draw falling character
        screen.blit(fallSprite, (screenW/2 - fsWidth/1.5, backgroundY))
        screen.blit(fallSprite, (screenW/2 - fsWidth/1.5, -screenH + backgroundY))

        if backgroundY >= screenH - fsWidth:
            screen.blit(fallSprite, (screenW/2 - fsWidth, -screenH + backgroundY))
            backgroundY = 0
        menuText.write(screen)
        menuText2.write(screen)

        backgroundY += 25
        pygame.display.update()


if __name__ == '__main__':
    Menu()
