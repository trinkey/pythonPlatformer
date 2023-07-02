import turtle

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

if __name__ == "__main__":
    import main