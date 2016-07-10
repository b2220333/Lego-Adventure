from GameBase import GameBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletDebugNode
from panda3d.core import BitMask32


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

        # self.CityTerrain = self.loader.loadModel(
        #     "models/CityTerrain/CityTerrain.egg")
        # self.CityTerrain.reparentTo(self.render)
        # self.CityTerrain.setScale(0.5, 0.5, 0.5)
        # self.CityTerrain.setPos(0, 0, 0)

        self.Ground2 = self.loader.loadModel(
            "models/Ground2/Ground2.egg")
        self.Ground2.reparentTo(self.render)
        self.Ground2.setScale(0.5, 0.5, 0.5)
        self.Ground2.setPos(0, 0, 0)
        self.addWall(Vec3(1, 290, 5), 285, 0)
        self.addWall(Vec3(1, 290, 5), -285, 0)
        self.addWall(Vec3(290, 1, 5), 0, 285)
        self.addWall(Vec3(290, 1, 5), 0, -285)
        # self.Junkyard = self.loader.loadModel(
        #     "models/Junkyard/Junkyard.egg")
        # self.Junkyard.reparentTo(self.render)
        # self.Junkyard.setScale(0.1, 0.1, 0.1)
        # self.Junkyard.setPos(0, 0, -10)

        # self.OldWestTerrain = self.loader.loadModel(
        #     "models/OldWestTerrain/OldWestTerrain.egg")
        # self.OldWestTerrain.reparentTo(self.render)
        # self.OldWestTerrain.setScale(0.03, 0.03, 0.03)
        # self.OldWestTerrain.setPos(0, 0, 0)

        # self.wintersky = self.loader.loadModel(
        #     "models/wintersky/wintersky.egg")
        # self.wintersky.reparentTo(self.render)
        # self.wintersky.setScale(0.5, 0.5, 0.5)
        # self.wintersky.setPos(0, 0, 0)

        # self.blue_sky_sphere = self.loader.loadModel(
        #     "models/blue_sky_sphere/blue_sky_sphere.egg")
        # self.blue_sky_sphere.reparentTo(self.render)
        # self.blue_sky_sphere.setScale(0.5, 0.5, 0.5)
        # self.blue_sky_sphere.setPos(0, 0, 0)

    def addWall(self, size, posX, posY):
        shape = BulletBoxShape(size)
        wallNP = self.render.attachNewNode(BulletRigidBodyNode('wall'))
        wallNP.node().addShape(shape)
        wallNP.setPos(posX, posY, size.getZ())
        wallNP.setCollideMask(BitMask32.allOn())
        if (posY is 0):
            left = -(size.getY())
            right = -left
            pos = left - 5
            while pos <= right:
                wallModel = loader.loadModel('models/fence.egg')
                wallModel.reparentTo(wallNP)
                wallModel.setPos(0, pos, -(size.getZ()))
                wallModel.setScale(1, 1, 1)
                wallModel.setH(90)
                pos += 13.5
        else:
            left = -(size.getX())
            right = -left
            pos = left - 5
            while pos <= right:
                wallModel = loader.loadModel('models/fence.egg')
                wallModel.reparentTo(wallNP)
                wallModel.setPos(pos, 0, -(size.getZ()))
                wallModel.setScale(1, 1, 1)
                pos += 13.5

        self.world.attachRigidBody(wallNP.node())


myGame = Game()
myGame.run()
