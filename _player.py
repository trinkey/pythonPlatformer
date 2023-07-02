import turtle
import keyboard
import _turtle

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
        self.turtle   = _turtle.TurtleController()

        self.turtleW  = _turtle.TurtleController()
        self.turtleWA = _turtle.TurtleController()
        self.turtleA  = _turtle.TurtleController()
        self.turtleAS = _turtle.TurtleController()
        self.turtleS  = _turtle.TurtleController()
        self.turtleSD = _turtle.TurtleController()
        self.turtleD  = _turtle.TurtleController()
        self.turtleDW = _turtle.TurtleController()

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

def key(key: str) -> bool:
    return keyboard.is_pressed(key)

if __name__ == "__main__":
    import main