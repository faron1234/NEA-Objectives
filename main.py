from static import *
from ProjectileClass import *
from PlayerClass import *
from VectorClass import *
from Collisions import *
from PortalClass import *
import DrawClass
import pygame
from pygame import mixer
from TextClass import Text
from math import *

pygame.init()

canJump = False
canFall = False
player = Player(posVec.i, posVec.j)

# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
size = pygame.display.Info()
screen = pygame.display.set_mode((size.current_w, size.current_h))

screenW = size.current_w
screenH = size.current_h

menuFont = pygame.font.Font("static/MainFont.otf", int(screenW / 12.5))
nodeFont = pygame.font.Font("static/MainFont.otf", int(screenW / 32.5))

menuText = Text(menuFont, 'Wormhole Shooting Game', 70, 200)

click = mixer.Sound("static/buttonClick.wav")


def Play():
    # variables
    projectile, projectile2, portal, portal2 = None, None, None, None
    canShootLeft, canShootRight, canTeleport = True, True, True
    global canJump
    global canFall
    DrawClass.drawMenu(screenW, screenH)
    while True:
        # statements every frame
        DrawClass.Menu.drawMap(screen)
        player.updatePos(posVec.i, posVec.j)
        allSprites.update(posVec.i, posVec.j)
        leftMouse, rightMouse = False, False
        canMoveLeft, canMoveRight = True, True
        clock.tick(fps)
        mx, my = pygame.mouse.get_pos()
        player.drawPlayer()
        allSprites.draw(screen)
        player.facingLine(20, screen)

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

        # exit button
        DrawClass.Menu.lines["xButton"].colour = Colours.black
        if DrawClass.Menu.lines["xButton"].drawing is not None and DrawClass.Menu.lines["xButton"].drawing.collidepoint(mx, my):
            DrawClass.Menu.lines["xButton"].colour = Colours.red
            if leftMouse:
                click.play()
                pygame.time.wait(160)
                quit()

        # add vectors for downward movement
        vel.add(gravity, "j")
        posVec.add(vel, "j")
        opposite = posVec.j - my
        adjacent = mx - posVec.i

        # find facing angle
        angle = player.findAngle(mx, my, opposite, adjacent)
        xChange = cos(angle)
        yChange = -sin(angle)

        # draw walls and pointer
        facing = [posVec.i + xChange, posVec.j + yChange, xChange * mL + posVec.i, yChange * mL + posVec.j]
        roof = [depth, depth, screenW - depth, depth]
        wall1 = [depth, depth, depth, screenH - depth]
        ground = [depth, screenH - depth, screenW - depth, screenH - depth]
        wall2 = [screenW - depth, depth, screenW - depth, screenH - depth]
        intersection = (Intersection((facing, roof), screen), Intersection((facing, wall1), screen), Intersection((facing, wall2), screen),
                        Intersection((facing, ground), screen))

        # check if player goes off-screen left/right
        if posVec.i <= depth:
            posVec.i = depth
            canMoveLeft = False
            vel.i = 0

        elif posVec.i >= screenW - depth:
            posVec.i = screenW - depth
            canMoveRight = False
            vel.i = 0

        # stop acceleration once terminal velocity is reached
        if vel.i > terminalVel.i > 0:
            vel.limit(terminalVel, "i")
        elif vel.i < -terminalVel.i < 0:
            terminalVel.reverse("i")
            vel.limit(terminalVel, "i")
            terminalVel.reverse("i")

        # check if player moves left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and canMoveRight:
            vel.add(acceleration, "i")
            posVec.add(vel, "i")

        elif keys[pygame.K_a] and canMoveLeft:
            vel.subtract(acceleration, "i")
            posVec.add(vel, "i")

        # check if player stops moving
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            vel.scale(deceleration, "i")
            posVec.add(vel, "i")

        # if player is in the air canFall = True
        if posVec.j < screenH - characterHeight - 50:
            canFall = True

        # if player not in air canJump = True
        else:
            posVec.j = screenH - characterHeight - 50
            vel.j = 0
            canJump = True

        # if player presses w or space and can jump they jump
        if canJump:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                vel.j = -15
                canJump = False

        # if mouse button is pressed a projectile is created
        if leftMouse and canShootLeft:
            for item in intersection:
                if item is not None:
                    projectile = Projectile(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.blue, item[0], item[1])

        if rightMouse and canShootRight:
            for item2 in intersection:
                if item2 is not None:
                    projectile2 = Projectile(angle, posVec.i + player.xChange, posVec.j + player.yChange, Colours.orange, item2[0], item2[1])

        # if a projectile has been created draw it to the screen
        if projectile is not None:
            projectile.drawProjectile(speed, screen)
            canShootLeft = False
            # if portal makes collision draw a portal
            if projectile.collision(depth, screenW, screenH):
                portal = Portal(projectile.getAttr("xi"), projectile.getAttr("yi"), Colours.blue)
                projectile = None
                canShootLeft = True

        if projectile2 is not None:
            projectile2.drawProjectile(speed, screen)
            canShootRight = False
            # if portal makes collision draw a portal
            if projectile2.collision(depth, screenW, screenH):
                portal2 = Portal(projectile2.getAttr("xi"), projectile2.getAttr("yi"), Colours.orange)
                projectile2 = None
                canShootRight = True

        # if portal exists draw it
        if portal:
            portal.drawPortal(screen)

        # if portal exists draw it
        if portal2:
            portal2.drawPortal(screen)

        pygame.display.update()


if __name__ == '__main__':
    Play()
