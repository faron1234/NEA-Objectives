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

objectSprites = pygame.sprite.Group()
playerSprites = pygame.sprite.Group()
portalSprites = pygame.sprite.Group()
projectileSprites = pygame.sprite.Group()

player = PlayerSprite(posVec.i, posVec.j)
playerSprites.add(player)

ob1 = ObstacleSprite("rect", (500, 450), (300, 301))
ob2 = ObstacleSprite("rect", (900, 750), (100, 300))
ob3 = ObstacleSprite("rect", (1000, 1000), (100, 100))
ob4 = ObstacleSprite("polygon", (500, 500), ((200, 100), (400, 100), (400, 250), (300, 250), (300, 200), (200, 200), (200, 100)))
obstacles = [ob1, ob2, ob3, ob4]

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
    if obj.type == "polygon":
        corners = obj.corners
        for index in range(len(corners)-1):
            collisionObj.append(Line(corners[index][0], corners[index][1], corners[index+1][0], corners[index+1][1]))
    if obj.type == "rect":
        collisionObj.append(Line(obj.x, obj.y, obj.x + obj.width, obj.y))
        collisionObj.append(Line(obj.x, obj.y, obj.x, obj.y + obj.height))
        collisionObj.append(Line(obj.x, obj.y + obj.height, obj.x + obj.width, obj.y + obj.height))
        collisionObj.append(Line(obj.x + obj.width, obj.y, obj.x + obj.width, obj.y + obj.height))
    objectSprites.add(obj)

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
    player.movingRight, player.movingLeft = False, False
    DrawClass.Menu.drawMap(screen)
    objectSprites.draw(screen)
    player.drawPlayer(screen)
    player.facingLine(20, screen)
    for obstacle in obstacles:
        obstacle.drawObstacle(screen)


def getShortestCollision(intersections):
    shortest = inf
    shortestCoord = None
    for item in intersections:
        if item:
            distance = dist((item[0], item[1]), (player.x, player.y))
            if distance < shortest:
                shortest = distance
                shortestCoord = item[0], item[1]

    return shortestCoord


def Play():
    # variables
    canShootLeft, canShootRight, canTeleport = True, True, True
    DrawClass.drawMenu(screenW, screenH)
    objectSprites.update()
    while True:
        # statements every frame
        leftMouse, rightMouse = False, False
        mx, my = pygame.mouse.get_pos()
        opposite = posVec.j - my
        adjacent = mx - posVec.i
        intersectionPoints = []

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
            pygame.draw.line(screen, Colours.black, (obj1.x1, obj1.y1), (obj1.x2, obj1.y2), 3)
            intersectionPoints.append(L1.intersection(obj1, screen))

        # check if player moves left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            vel.add(acceleration, "i")

        if keys[pygame.K_a]:
            vel.subtract(acceleration, "i")

        if vel.i > 0.3:
            player.movingRight = True

        if vel.i < -0.3:
            player.movingLeft = True

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
        player.objectCollide(objectSprites, vel)
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
            shortestCollision = getShortestCollision(intersectionPoints)
            if shortestCollision:
                projectile.setAttributes(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.blue, shortestCollision[0], shortestCollision[1])
            canShootLeft = False

        if rightMouse and canShootRight:
            shortestCollision = getShortestCollision(intersectionPoints)
            if shortestCollision:
                projectile2.setAttributes(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.orange, shortestCollision[0], shortestCollision[1])
            canShootRight = False

        # draw projectile to the screen
        projectile.drawProjectile(speed, screen)
        projectile2.drawProjectile(speed, screen)
        portalSprites.update(screen)
        projectile.update()
        projectile2.update()

        # if portal makes collision draw a portal
        if projectile.collision(objectSprites):
            portal.setPos(projectile.getAttr("xi"), projectile.getAttr("yi"))
            canShootLeft = True

        # if portal makes collision draw a portal
        if projectile2.collision(objectSprites):
            portal2.setPos(projectile2.getAttr("xi"), projectile2.getAttr("yi"))
            canShootRight = True

        # if player can teleport then check for collisions and teleport
        if canTeleport:
            portalCollide = player.portalCollide(portalSprites)
            if portalCollide == portal and portal2.portalX is not None:
                posVec.setVec(portal2.portalX, portal2.portalY)
                vel.reverse("j")
                canTeleport = False

            elif portalCollide == portal2 and portal.portalX is not None:
                posVec.setVec(portal.portalX, portal.portalY)
                canTeleport = False
        if not player.portalCollide(portalSprites):
            canTeleport = True
        player.update()

        pygame.display.update()


if __name__ == '__main__':
    Play()
