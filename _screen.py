import turtle
import _turtle

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
        self.turtle = _turtle.TurtleController("#435", scale)
        self.turtle.goto(x, y)

    def ht(self):
        self.turtle.ht()

    def changeColor(self, color):
        self.turtle.st()
        self.turtle.color(color)

if __name__ == "__main__":
    import main