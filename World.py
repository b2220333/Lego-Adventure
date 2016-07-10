from GameBase import GameBase


class Game(GameBase):
    def __init__(self):
        GameBase.__init__(self)
        self.loadMap()

    def loadMap(self):
        # self.HauntedHouse = self.loader.loadModel(
        #     "models/HauntedHouse/HauntedHouse.egg")
        # self.HauntedHouse.reparentTo(self.render)
        # self.HauntedHouse.setScale(0.25, 0.25, 0.25)
        # self.HauntedHouse.setPos(0, 0, 0)

        self.CityTerrain = self.loader.loadModel(
            "models/CityTerrain/CityTerrain.egg")
        self.CityTerrain.reparentTo(self.render)
        self.CityTerrain.setScale(0.1, 0.1, 0.1)
        self.CityTerrain.setPos(0, 0, 0)

myGame = Game()
myGame.run()
