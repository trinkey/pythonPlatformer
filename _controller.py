import turtle
import time
import json
import _turtle

class Controller:
    def __init__(self, startingMapNumber, playerObject, screenObject):
        self.turtle = _turtle.TurtleController("white")
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

if __name__ == "__main__":
    import main