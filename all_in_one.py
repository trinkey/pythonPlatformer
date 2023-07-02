import turtle
import time
import json
import turtle
import keyboard

class Screen:
    def __init__(self):
        # Constants
        self.BACKGROUND_COLOR = "#625"
        self.PLATFORM_COLOR = "#000"
        self.ALT_COLOR = "#222"
        self.WIN_TILE_COLOR = "#d48"
        self.DEATH_COLOR = "#f00"
        self.BOUNCY_BLOCK_COLOR = "#00a"
        self.TILE_SCALE = 2.5

        # Screen setup
        self.screen = turtle.Screen()
        self.screen.setup(500, 500)
        self.screen.bgcolor(self.BACKGROUND_COLOR)
        self.screen.tracer(0)

        # Setup tile list
        self.tiles = []
        for i in range(100):
            self.tiles.append(BackgroundTile(
                scale=self.TILE_SCALE,
                x=(i % 10) * 20 * self.TILE_SCALE - 225,
                y=(9 - (i // 10)) * 20 * self.TILE_SCALE - 225
            ))

    def update(self):
        self.screen.update()

    def loadMap(self, levelMap: list):
        self.levelMap = levelMap
        for i in range(100):
            if self.levelMap[i] in [0, 4]:
                self.tiles[i].ht()
            elif self.levelMap[i] == 1:
                self.tiles[i].changeColor(self.PLATFORM_COLOR)
            elif self.levelMap[i] == 2:
                self.tiles[i].changeColor(self.ALT_COLOR)
            elif self.levelMap[i] == 3:
                self.tiles[i].changeColor(self.WIN_TILE_COLOR)
            elif self.levelMap[i] == 5:
                self.tiles[i].changeColor(self.DEATH_COLOR)
            elif self.levelMap[i] == 6:
                self.tiles[i].changeColor(self.BOUNCY_BLOCK_COLOR)

class BackgroundTile:
    def __init__(self, scale, x, y):
        self.turtle = TurtleController("#435", scale)
        self.turtle.goto(x, y)

    def ht(self):
        self.turtle.ht()

    def changeColor(self, color):
        self.turtle.st()
        self.turtle.color(color)

class TurtleController:
    def __init__(self, color="green", scale=1, shape="square"):
        # Turtle setup
        self.turtle = turtle.Turtle()
        self.turtle.pu()
        self.turtle.speed(0)
        self.turtle.shape(shape)
        self.turtle.color(color)
        self.turtle.turtlesize(scale)

    def goto(self, x: float, y: float):
        self.turtle.goto(x, y)

    def color(self, color: str):
        self.turtle.color(color)

    def ht(self):
        self.turtle.ht()

    def st(self):
        self.turtle.st()

    def xcor(self) -> float:
        return self.turtle.xcor()

    def ycor(self) -> float:
        return self.turtle.ycor()

    def write(self, text, align, font):
        self.turtle.write(text, align=align, font=font)

    def clear(self):
        self.turtle.clear()

class Player:
    def __init__(self, x: float, y: float, levelMap):
        # Constants
        self.SCREEN_SIZE = 500
        self.X_MOVEMENT_PER_SECOND = 500
        self.Y_MOVEMENT_PER_SECOND = 400
        self.COLLISION_PER_FRAME = 5
        self.PLAYER_HEIGHT = 20
        self.PLAYER_WIDTH = 20
        self.TILE_SCALE = 2.5
        self.MAX_Y_VELOCITY = 1200
        self.MAX_X_VELOCITY = 1200

        # Other variables
        self.levelMap = levelMap
        self.xVelocity = 0
        self.yVelocity = 0

        # Turtle setup
        self.turtle   = TurtleController()

        self.turtleW  = TurtleController()
        self.turtleWA = TurtleController()
        self.turtleA  = TurtleController()
        self.turtleAS = TurtleController()
        self.turtleS  = TurtleController()
        self.turtleSD = TurtleController()
        self.turtleD  = TurtleController()
        self.turtleDW = TurtleController()

        self.goto(x, y)

    def goto(self, x: float, y: float):
        self.turtle.goto(x, y)

        self.turtleW .goto(x                   , y + self.SCREEN_SIZE)
        self.turtleWA.goto(x - self.SCREEN_SIZE, y + self.SCREEN_SIZE)
        self.turtleA .goto(x - self.SCREEN_SIZE, y)
        self.turtleAS.goto(x - self.SCREEN_SIZE, y - self.SCREEN_SIZE)
        self.turtleS .goto(x                   , y - self.SCREEN_SIZE)
        self.turtleSD.goto(x + self.SCREEN_SIZE, y - self.SCREEN_SIZE)
        self.turtleD .goto(x + self.SCREEN_SIZE, y)
        self.turtleDW.goto(x + self.SCREEN_SIZE, y + self.SCREEN_SIZE)

        self.xPos = self.turtle.xcor()
        self.yPos = self.turtle.ycor()

    def movement(self, frameDelta: float):
        # Detect keystrokes
        if key("r"):
            self.loadMap(self.levelMap)

        if key("w") or key("space") or key("up"):
            if self.onGround():
                self.yVelocity = self.Y_MOVEMENT_PER_SECOND

        if key("a") or key("left"):
            self.xVelocity -= self.X_MOVEMENT_PER_SECOND * frameDelta
            if self.xVelocity > 0 and self.onGround():
                self.xVelocity -= self.X_MOVEMENT_PER_SECOND * frameDelta

        if key("d") or key("right"):
            self.xVelocity += self.X_MOVEMENT_PER_SECOND * frameDelta
            if self.xVelocity < 0 and self.onGround():
                self.xVelocity += self.X_MOVEMENT_PER_SECOND * frameDelta

        if self.xVelocity > self.MAX_X_VELOCITY:
            self.xVelocity = self.MAX_X_VELOCITY
        if self.yVelocity > self.MAX_Y_VELOCITY:
            self.yVelocity = self.MAX_Y_VELOCITY

        if self.xVelocity < -self.MAX_X_VELOCITY:
            self.xVelocity = -self.MAX_X_VELOCITY
        if self.yVelocity < -self.MAX_Y_VELOCITY:
            self.yVelocity = -self.MAX_Y_VELOCITY

        # Detect bouncy blocks
        if self.onBouncy():
            self.yVelocity = self.MAX_Y_VELOCITY / 2

        # Set turtle position
        for i in range(self.COLLISION_PER_FRAME):
            self.goto(
                self.xPos + (self.xVelocity * frameDelta * (1 / self.COLLISION_PER_FRAME)),
                self.yPos + (self.yVelocity * frameDelta * (1 / self.COLLISION_PER_FRAME))
            )
            self.wrapPlayer()

            if self.checkCollision(): # If not able to go x and y
                self.goto(
                    self.xPos - (self.xVelocity * frameDelta * (1 / self.COLLISION_PER_FRAME)),
                    self.yPos
                )
                self.wrapPlayer()

                if self.checkCollision(): # If not able to go just y
                    self.goto(
                        self.xPos + (self.xVelocity * frameDelta * (1 / self.COLLISION_PER_FRAME)),
                        self.yPos - (self.yVelocity * frameDelta * (1 / self.COLLISION_PER_FRAME))
                    )
                    self.wrapPlayer()
                    self.yVelocity = 0

                    if self.checkCollision(): # If not able to go just x
                        self.goto(
                            self.xPos - (self.xVelocity * frameDelta * (1 / self.COLLISION_PER_FRAME)),
                            self.yPos
                        )
                        self.wrapPlayer()
                        self.xVelocity = 0

                else:
                    self.xVelocity = 0

            if self.checkDie():
                self.loadMap(self.levelMap)

        # Friction
        if self.onGround():
            self.xVelocity *= 0.2 ** frameDelta

        # Gravity
        self.yVelocity -= self.Y_MOVEMENT_PER_SECOND * frameDelta * 2

    def returnSurroundings(self, i: int) -> list[int]:
        return [
            w := i - 10 if i > 9      else i + 90, # Top
                 i - 1  if i % 10     else i + 9,  # Left
            s := i + 10 if i < 90     else i - 90, # Bottom
                 i + 1  if (i+1) % 10 else i - 9,  # Right

                 w - 1 if w % 10     else w + 9, # Top left
                 w + 1 if (w+1) % 10 else w - 9, # Top Right
                 s - 1 if w % 10     else s + 9, # Bottom Left
                 s + 1 if (w+1) % 10 else s - 9, # Bottom Right

                 i # Center
        ]

    def wrapPlayer(self):
        if self.xPos >= self.SCREEN_SIZE / 2:
            self.goto(self.xPos - self.SCREEN_SIZE, self.yPos)
        if self.xPos <= -self.SCREEN_SIZE / 2:
            self.goto(self.xPos + self.SCREEN_SIZE, self.yPos)
        if self.yPos >= self.SCREEN_SIZE / 2:
            self.goto(self.xPos, self.yPos - self.SCREEN_SIZE)
        if self.yPos <= -self.SCREEN_SIZE / 2:
            self.goto(self.xPos, self.yPos + self.SCREEN_SIZE)

    def getI(self) -> int:
        return int((self.xPos + 250) / 20 / self.TILE_SCALE // 1 + (5 - (self.yPos) / 20 / self.TILE_SCALE) // 1 * 10)

    def coreCollisionCheck(self, x: callable, xCoyote: float, y: callable, yCoyote: float, passthrough: float) -> bool:
        # Check main player
        if self.checkWithinRange(x(passthrough), self.xPos, xCoyote) and \
           self.checkWithinRange(y(passthrough), self.yPos, yCoyote):
            return 1

        # Check top player
        elif self.checkWithinRange(x(passthrough), self.xPos, xCoyote) and \
             self.checkWithinRange(y(passthrough), self.yPos + self.SCREEN_SIZE, yCoyote):
            return 1
        # Check left player
        elif self.checkWithinRange(x(passthrough), self.xPos - self.SCREEN_SIZE, xCoyote) and \
             self.checkWithinRange(y(passthrough), self.yPos, yCoyote):
            return 1
        # Check down player
        elif self.checkWithinRange(x(passthrough), self.xPos, xCoyote) and \
             self.checkWithinRange(y(passthrough), self.yPos - self.SCREEN_SIZE, yCoyote):
            return 1
        # Check right player
        elif self.checkWithinRange(x(passthrough), self.xPos + self.SCREEN_SIZE, xCoyote) and \
             self.checkWithinRange(y(passthrough), self.yPos, yCoyote):
            return 1
        return 0

    def checkCollision(self) -> bool:
        for i in self.returnSurroundings(self.getI()):
            # Check main player
            if self.levelMap[i] in [1, 2, 6] and self.coreCollisionCheck(
                lambda i: (i % 10) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE + 10,
                lambda i: (9 - (i // 10)) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE + 10,
                i
            ):
                return 1
        return 0

    def checkDie(self) -> bool:
        for i in self.returnSurroundings(self.getI()):
            if self.levelMap[i] == 5 and self.coreCollisionCheck(
                lambda i: (i % 10) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE,
                lambda i: (9 - (i // 10)) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE,
                i
            ):
                return 1
        return 0

    def onGround(self) -> bool:
        for i in self.returnSurroundings(self.getI()):
            if self.levelMap[i] in [1, 2] and self.coreCollisionCheck(
                lambda i: (i % 10) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE + 10,
                lambda i: (9 - (i // 10)) * 20 * self.TILE_SCALE - 225 + 10 * self.TILE_SCALE,
                11,
                i
            ):
                return 1
        return 0

    def onBouncy(self) -> bool:
        for i in self.returnSurroundings(self.getI()):
            if self.levelMap[i] == 6 and self.coreCollisionCheck(
                lambda i: (i % 10) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE + 5,
                lambda i: (9 - (i // 10)) * 20 * self.TILE_SCALE - 225 + 10 * self.TILE_SCALE,
                11,
                i
            ):
                return 1
        return 0

    def loadMap(self, levelMap: list):
        self.levelMap = levelMap
        for i in range(100):
            if self.levelMap[i] == 4:
                self.xVelocity = 0
                self.yVelocity = 0
                self.goto(
                    (i % 10) * 20 * self.TILE_SCALE - 225,
                    (9 - (i // 10)) * 20 * self.TILE_SCALE - 225
                )
                break

    def checkForWin(self) -> bool:
        for i in self.returnSurroundings(self.getI()):
            if self.levelMap[i] == 3 and self.coreCollisionCheck(
                lambda i: (i % 10) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE + 10,
                lambda i: (9 - (i // 10)) * 20 * self.TILE_SCALE - 225,
                10 * self.TILE_SCALE + 10,
                i
            ):
                return 1
        return 0

    def checkWithinRange(self, num1: float, num2: float, coyote: float) -> bool:
        return num1 > num2 - coyote and num1 < num2 + coyote

class Controller:
    def __init__(self, startingMapNumber, playerObject, screenObject):
        self.turtle = TurtleController("white")
        self.turtle.ht()

        self.player = playerObject
        self.screen = screenObject

        self.level = startingMapNumber
        self.maps = json.loads(open("maps.json").read())

    def loadNewLevel(self):
        self.turtle.clear()
        self.map = self.maps[str(self.level)]["map"]

        self.player.loadMap(self.map)
        self.screen.loadMap(self.map)

        for i in self.maps[str(self.level)]["commands"]:
            exec(i)

        self.level += 1

    def start(self):
        self.loadNewLevel()
        self.frameStart = time.time()
        self.screen.update()
        while True:
            self.newFrameStart = time.time()
            x = time.time() - self.frameStart
            self.player.movement(x if x else 0.00001)
            self.screen.loadMap(self.map)
            # # Debug physics check locations:
            # for i in self.player.returnSurroundings(self.player.getI()):
            #     self.screen.tiles[i].changeColor("orange")
            self.screen.update()
            if self.player.checkForWin():
                self.loadNewLevel()
            self.frameStart = self.newFrameStart

def key(key: str) -> bool:
    return keyboard.is_pressed(key)

screen = Screen()
player = Player(0, 0, [])
controller = Controller(1, player, screen)

controller.start()