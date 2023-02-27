import AStarClass
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


def button(leftMouse, mx, my, buttonName, colourChange, function):
    # exit button
    backgroundDrawing.lines[buttonName].colour = Colours.black
    if not backgroundDrawing.lines[buttonName].drawing.collidepoint(mx, my):
        return
    backgroundDrawing.lines[buttonName].colour = colourChange
    if leftMouse:
        click.play()
        pygame.time.wait(160)
        function()


# event loop
def eventLoop():
    leftMouse, rightMouse = False, False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
            leftMouse = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == right:
            rightMouse = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()
    return leftMouse, rightMouse


def teleport(canTeleport):
    portalCollide = player.portalCollide(portalSprites)
    if not player.portalCollide(portalSprites):
        return True
    if not canTeleport:
        return False
    if portalCollide == portal and portal2.x is not None:
        posVec.setVec(portal2.x, portal2.y)
        vel.i = -vel.j
        vel.j = 0
        return False

    elif portalCollide == portal2 and portal.x is not None:
        posVec.setVec(portal.x, portal.y)
        return False


def createProjectile(leftMouse, rightMouse, canShootLeft, canShootRight, angle):
    # if mouse button is pressed a projectile is created
    if leftMouse and canShootLeft:
        intersectionLine = L1.intersection(collisionObj, 1)
        if intersectionLine:
            projectile.setAttributes(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.blue, intersectionLine)
        canShootLeft = False
    if rightMouse and canShootRight:
        intersectionLine1 = L1.intersection(collisionObj, 2)
        if intersectionLine1:
            projectile2.setAttributes(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.orange, intersectionLine1)
        canShootRight = False
    return canShootLeft, canShootRight


def Play():
    # variables
    canShootLeft, canShootRight, canTeleport = True, True, True
    backgroundDrawing.lines['startButton'].doDraw = False
    backgroundDrawing.lines['scoresButton'].doDraw = False
    Path, nodesMap = AStarClass.createNodes(screenW, screenH)
    while True:
        # set fps
        clock.tick(fps)

        # check for mouse attributes
        leftMouse, rightMouse = eventLoop()
        mx, my = pygame.mouse.get_pos()

        # find facing angle
        opposite = posVec.j - my
        adjacent = mx - posVec.i
        angle = player.findAngle(mx, my, opposite, adjacent)
        xChange = cos(angle)
        yChange = -sin(angle)

        player.movingRight, player.movingLeft = False, False
        backgroundDrawing.drawMap(screen)
        player.drawPlayer(screen)
        player.facingLine(20, screen)
        ObstacleSprite.drawObstacle(gameMap.obstacles, screen)
        for line in collisionObj:
            pygame.draw.line(screen, Colours.red, [line.x1, line.y1], [line.x2, line.y2])

        button(leftMouse, mx, my, "xButton", Colours.red, quit)

        Path.findPath(player)
        for node in nodesMap:
            node.drawNode(screen, nodeFont, Path, nodesMap[-1])

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
        collide = player.objectCollide((objectSprites, invisibleSprites), vel, canTeleport)
        posVec.add(vel, 'i')
        posVec.add(vel, 'j')
        player.setPos(posVec.i, posVec.j)

        if player.canJump and (keys[pygame.K_w] or keys[pygame.K_SPACE]):
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

        canShootLeft, canShootRight = createProjectile(leftMouse, rightMouse, canShootLeft, canShootRight, angle)

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
        if projectile.collision(portalSprites):
            canShootLeft = True
        if projectile.collision(objectSprites, invisibleSprites) and projectile.intersectionLine:
            canShootLeft = True
            portal.setPos(projectile)
            portal.setLine(projectile.intersectionLine)

        # if portal makes collision draw a portal
        if projectile2.collision(portalSprites):
            canShootRight = True
        if projectile2.collision(objectSprites, invisibleSprites) and projectile2.intersectionLine:
            canShootRight = True
            portal2.setPos(projectile2)
            portal2.setLine(projectile2.intersectionLine)

        # if player can teleport then check for collisions and teleport
        canTeleport = teleport(canTeleport)

        pygame.display.update()


def Menu():
    # one time statements
    backgroundY = 0
    BackgroundNoise.play()
    BackgroundNoise.set_volume(0.00)
    createBackground(screenW, screenH)
    while True:
        # statements every frame
        leftMouse, rightMouse = eventLoop()
        mx, my = pygame.mouse.get_pos()
        screen.fill(Colours.white)
        clock.tick(fps)
        # draw map
        backgroundDrawing.drawMap(screen)

        button(leftMouse, mx, my, "xButton", Colours.red, quit)
        button(leftMouse, mx, my, "startButton", Colours.orange, Play)
        button(leftMouse, mx, my, "scoresButton", Colours.blue, "")

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
