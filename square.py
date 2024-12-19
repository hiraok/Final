import pyxel

class Square:
    def __init__(self, x, y):
        self.sx = x
        self.sy = y
        self.ex = x
        self.ey = y
        self.mode = 1

    def end(self, x, y):
        if self.mode == 1:
            self.ex = x
            self.ey = y
            self.mode = 0

    def draw(self):
        if self.mode == 1:
            pyxel.rect(self.sx, self.sy, pyxel.mouse_x - self.sx, pyxel.mouse_y - self.sy, 5)
        else:
            pyxel.rect(self.sx, self.sy, self.ex - self.sx, self.ey - self.sy, 0)

class App:
    def __init__(self):
        pyxel.init(200,165)
        pyxel.mouse(True)
        self.squares = []
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.squares.append(Square(pyxel.mouse_x, pyxel.mouse_y))
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            for square in self.squares:
                square.end(pyxel.mouse_x, pyxel.mouse_y)

    def draw(self):
        pyxel.cls(7)
        for square in self.squares:
            square.draw()

App()