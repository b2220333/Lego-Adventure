from GameBase import GameBase


class Game(GameBase):
    def __init__(self):
        GameBase.__init__(self)

myGame = Game()
myGame.run()
