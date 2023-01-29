import AStarClass
from static import *
from ProjectileClass import *
from PlayerClass import *
from VectorClass import *
from CollisionClass import *
from PortalClass import *
from ObstacleClass import *
import DrawClass
import pygame
from pygame import mixer
from TextClass import Text
from math import *

pygame.init()

objSprites = pygame.sprite.Group()
playerSprites = pygame.sprite.Group()
portalSprites = pygame.sprite.Group()
projectileSprites = pygame.sprite.Group()

player = PlayerSprite("SpriteImages/Stationary.xcf", posVec.i, posVec.j)
playerSprites.add(player)

ob1 = ObstacleSprite(500, 450, 300, 300)
ob2 = ObstacleSprite(900, 750, 100, 300)
ob3 = ObstacleSprite(1000, 1000, 100, 100)
obstacles = [ob1, ob2, ob3]
objSprites.add(ob1, ob2, ob3)

portal = PortalSprite(Colours.blue)
portalSprites.add(portal)
portal2 = PortalSprite(Colours.orange)
portalSprites.add(portal2)

projectile = ProjectileSprite()
projectile2 = ProjectileSprite()

# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
size = pygame.display.Info()
screen = pygame.display.set_mode((size.current_w, size.current_h))

screenW = size.current_w
screenH = size.current_h

L1 = Line()
roof = Line(depth, depth, screenW - depth, depth)
wall1 = Line(depth, depth, depth, screenH - depth)
ground = Line(depth, screenH - depth, screenW - depth, screenH - depth)
wall2 = Line(screenW - depth, depth, screenW - depth, screenH - depth)

collisionObj = [roof, wall1, ground, wall2]
for obj in obstacles:
    collisionObj.append(Line(obj.obstacleX, obj.obstacleY, obj.obstacleX + obj.width, obj.obstacleY))
    collisionObj.append(Line(obj.obstacleX, obj.obstacleY, obj.obstacleX, obj.obstacleY + obj.height))
    collisionObj.append(Line(obj.obstacleX, obj.obstacleY + obj.height, obj.obstacleX + obj.width, obj.obstacleY + obj.height))
    collisionObj.append(Line(obj.obstacleX + obj.width, obj.obstacleY, obj.obstacleX + obj.width, obj.obstacleY + obj.height))

menuFont = pygame.font.Font("static/MainFont.otf", int(screenW / 12.5))
nodeFont = pygame.font.Font("static/MainFont.otf", int(screenW / 32.5))
background = pygame.image.load("SpriteImages/Dead (1).png")
background = pygame.transform.scale(background, (100, 100))

menuText = Text(menuFont, 'Portal Game', 70, 200)

BackgroundNoise = mixer.Sound("static/Still Alive.mp3")
backgroundMusic = pygame.mixer.Sound
click = mixer.Sound("static/buttonClick.wav")


def exitButton(leftMouse, mx, my):
    # exit button
    DrawClass.Menu.lines["xButton"].colour = Colours.black
    if DrawClass.Menu.lines["xButton"].drawing is not None and DrawClass.Menu.lines["xButton"].drawing.collidepoint(mx, my):
        DrawClass.Menu.lines["xButton"].colour = Colours.red
        if leftMouse:
            click.play()
            pygame.time.wait(160)
            quit()


def Menu():
    # one time statements
    backgroundY = 0
    BackgroundNoise.play()
    BackgroundNoise.set_volume(0.01)
    DrawClass.drawMenu(screenW, screenH)
    while True:
        # statements every frame
        leftMouse = False
        rightMouse = False
        menuChW = 50
        clock.tick(fps)
        mx, my = pygame.mouse.get_pos()
        screen.fill(Colours.white)
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left:
                    leftMouse = True
                elif event.button == right:
                    rightMouse = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        exitButton(leftMouse, mx, my)

        # draw map
        DrawClass.Menu.drawMap(screen)

        # draw static portals
        pygame.draw.ellipse(screen, Colours.blue, [screenW / 2 - depth, screenH - 69, 60, 35], 5)
        pygame.draw.ellipse(screen, Colours.orange, [screenW / 2 - depth, 34, 60, 35], 5)

        # draw falling character
        screen.blit(background, (screenW/2 - menuChW, backgroundY))
        screen.blit(background, (screenW/2 - menuChW, -screenH + backgroundY))

        if backgroundY >= screenH - 142:
            screen.blit(background, (screenW/2 - menuChW, -screenH + backgroundY))
            backgroundY = 0
        menuText.write(screen, Colours.orange)

        backgroundY += 31
        pygame.display.update()


def everyFrame():
    clock.tick(fps)
    DrawClass.Menu.drawMap(screen)
    objSprites.draw(screen)
    player.drawPlayer(screen)
    player.facingLine(20, screen)
    for obstacle in obstacles:
        obstacle.drawObstacle(screen)


def Play():
    # variables
    canShootLeft, canShootRight, canTeleport = True, True, True
    DrawClass.drawMenu(screenW, screenH)
    objSprites.update()
    intersection = []
    while True:
        # statements every frame
        leftMouse, rightMouse = False, False
        mx, my = pygame.mouse.get_pos()
        opposite = posVec.j - my
        adjacent = mx - posVec.i

        # find facing angle
        angle = player.findAngle(mx, my, opposite, adjacent)
        xChange = cos(angle)
        yChange = -sin(angle)

        everyFrame()

        AStarClass.Path.findPath((posVec.i, posVec.j))
        for node in AStarClass.nodesMap:
            node.drawNode(screen, nodeFont)

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left:
                    leftMouse = True
                elif event.button == right:
                    rightMouse = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

        exitButton(leftMouse, mx, my)

        # define walls and pointer
        L1.setCoord(posVec.i + xChange, posVec.j + yChange, xChange * mL + posVec.i, yChange * mL + posVec.j)
        for obj1 in collisionObj:
            intersection.append(L1.intersection(obj1, screen))

        # check if player moves left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            vel.add(acceleration, "i")

        if keys[pygame.K_a]:
            vel.subtract(acceleration, "i")

        # add gravity vector to velocity
        vel.add(gravity, "j")

        # check if player stops moving
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            vel.scale(deceleration, "i")

        # if player is in the air canFall = True
        if posVec.j < screenH - characterHeight - 50:
            player.canFall = True
        # if player not in air canJump = True
        else:
            posVec.j = screenH - characterHeight - 50
            vel.j = 0
            player.canJump = True

        # if player presses w or space and can jump they jump
        if player.canJump:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                vel.j = -15
                player.canJump = False
        if not keys[pygame.K_w] and not keys[pygame.K_SPACE]:
            player.canJump = True

        # stop acceleration once terminal velocity is reached
        if vel.i > terminalVel.i > 0:
            vel.limit(terminalVel, "i")
        elif vel.i < -terminalVel.i < 0:
            terminalVel.reverse("i")
            vel.limit(terminalVel, "i")
            terminalVel.reverse("i")

        # check for collisions
        player.objectCollide(objSprites, vel)
        if posVec.i <= depth:
            posVec.i = depth
            vel.i = 0
        elif posVec.i >= screenW - depth:
            posVec.i = screenW - depth
            vel.i = 0
        posVec.add(vel, "i")
        posVec.add(vel, "j")
        player.setPos(posVec.i, posVec.j)

        # if mouse button is pressed a projectile is created
        if leftMouse and canShootLeft:
            for item in intersection:
                if item is not None:
                    projectile.setAttributes(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.blue, item[0], item[1])
                    canShootLeft = False

        if rightMouse and canShootRight:
            for item2 in intersection:
                if item2 is not None:
                    projectile2.setAttributes(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.orange, item2[0], item2[1])
                    canShootRight = False

        # draw projectile to the screen
        projectile.drawProjectile(speed, screen)
        projectile2.drawProjectile(speed, screen)
        portalSprites.update(screen)
        projectile.update()
        projectile2.update()

        # if portal makes collision draw a portal
        if projectile.collision(objSprites):
            portal.setPos(projectile.getAttr("xi"), projectile.getAttr("yi"))
            canShootLeft = True

        # if portal makes collision draw a portal
        if projectile2.collision(objSprites):
            portal2.setPos(projectile2.getAttr("xi"), projectile2.getAttr("yi"))
            canShootRight = True

        # if player can teleport then check for collisions and teleport
        if canTeleport:
            portalCollide = player.portalCollide(portalSprites)
            if portalCollide == portal:
                posVec.setVec(portal2.portalX, portal2.portalY)
                canTeleport = False

            elif portalCollide == portal2:
                posVec.setVec(portal.portalX, portal.portalY)
                canTeleport = False
        if not player.portalCollide(portalSprites):
            canTeleport = True
        player.update()

        pygame.display.update()


if __name__ == '__main__':
    Play()
