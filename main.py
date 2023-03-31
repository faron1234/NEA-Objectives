from static import *
from ProjectileClass import *
from VectorClass import *
from ObstacleClass import *
from DrawClass import backgroundDrawing, createBackground
import pygame
from pygame import mixer

pygame.init()

# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
size = pygame.display.Info()
screen = pygame.display.set_mode((size.current_w, size.current_h))

screenW = size.current_w
screenH = size.current_h

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
    createBackground(screenW, screenH)
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

        backgroundDrawing.drawMap(screen)
        player.facingLine(20, screen)
        ObstacleSprite.drawObstacle(gameMap.obstacles, screen)

        for obstacle in collisionObj:
            obstacle.drawObstacle()

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
        vel.limit("i")

        if player.canJump and keys[pygame.K_w] or keys[pygame.K_SPACE]:
            vel.j = -16
            player.canJump = False
        # if player presses w or space and can jump they jump
        if collide:
            player.canJump = True

        # draw projectile to the screen
        projectile.drawProjectile(speed, screen)
        projectile2.drawProjectile(speed, screen)
        objectSprites.update(screen)
        invisibleSprites.update(screen)
        projectile.update()
        projectile2.update()
        player.update(screen)

        projectile.startProjectile(angle, "left", Colours.blue)
        projectile2.startProjectile(angle, "right", Colours.orange)

        # if player can teleport then check for collisions and teleport
        player.reset()

        pygame.display.update()


if __name__ == '__main__':
    Play()
