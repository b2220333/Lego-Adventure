from GameBase import GameBase
from panda3d.core import Vec3, Point3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletDebugNode
from panda3d.core import BitMask32
from random import randrange


class Game(GameBase):
    def __init__(self):
        GameBase.__init__(self)
        self.movingSpeed = 3
        # self.jumpHeight = 1
        self.jumpSpeed = 6

        self.loadMap()
        self.loadObstacles()

    def loadMap(self):
        self.blue_sky_sphere = self.loader.loadModel(
            "models/blue_sky_sphere/blue_sky_sphere.egg")
        self.blue_sky_sphere.reparentTo(self.render)
        self.blue_sky_sphere.setScale(0.084, 0.084, 0.084)
        self.blue_sky_sphere.setPos(0, 0, 0)

        self.Ground2 = self.loader.loadModel(
            "models/Ground2/Ground2.egg")
        self.Ground2.reparentTo(self.render)
        self.Ground2.setScale(0.8, 0.8, 0.8)
        self.Ground2.setPos(0, 0, 0)

        self.addWall(Vec3(1, 290, 5), 285, 0)
        self.addWall(Vec3(1, 290, 5), -285, 0)
        self.addWall(Vec3(290, 1, 5), 0, 285)
        self.addWall(Vec3(290, 1, 5), 0, -285)

        self.addSimpleBuilding(boxSize=Vec3(27, 29, 15),
                               pos=Vec3(250, -250, 0),
                               scale=Vec3(0.1, 0.1, 0.1),
                               heading=0,
                               name='Junkyard',
                               modelPath="models/Junkyard/Junkyard.egg",
                               shift=Vec3(0, -2.5, 0))

        for row in xrange(0, 1):
            for x in xrange(1, 10):
                self.addSimpleBuilding(boxSize=Vec3(12, 6, 14),
                                       pos=Vec3(-280 + 50 * x,
                                                280 - 60 * row, 0),
                                       scale=Vec3(0.5, 0.5, 0.5),
                                       heading=180,
                                       name='FarmHouse{}-{}'.format(row, x),
                                       modelPath="models/FarmHouse/FarmHouse.egg")
        for row in xrange(0, 1):
            for x in xrange(1, 10):
                self.addSimpleBuilding(boxSize=Vec3(12, 6, 14),
                                       pos=Vec3(-205 + 50 * x,
                                                250 - 60 * row, 0),
                                       scale=Vec3(0.5, 0.5, 0.5),
                                       heading=180,
                                       name='FarmHouse{}-{}'.format(row, x),
                                       modelPath="models/FarmHouse/FarmHouse.egg")

        for index in xrange(1, 70):
            style = randrange(1, 6)
            self.addSimpleBuilding(boxSize=Vec3(3.5, 5, 10),
                                   pos=Vec3(7 * index - 280, -270, 0),
                                   scale=Vec3(0.5, 0.5, 0.5),
                                   heading=0,
                                   name='Townhouse{}'.format(index),
                                   modelPath="models/Townhouse{}/Townhouse{}.egg".format(
                                       style, style),
                                   shift=Vec3(0, 0, 0))

        for index in xrange(1, 7):
            self.addSimpleBuilding(boxSize=Vec3(22, 22, 100),
                                   pos=Vec3(280, 60 * index - 200, 0),
                                   scale=Vec3(0.5, 0.5, 0.5),
                                   heading=90,
                                   name='Skyscraper1',
                                   modelPath="models/Skyscraper1/Skyscraper1.egg",
                                   shift=Vec3(0, 0, 0))

        # self.addSimpleBuilding(boxSize=Vec3(6, 5, 14),
        #                        pos=Vec3(0, 0, 0),
        #                        scale=Vec3(0.5, 0.5, 0.5),
        #                        heading=180,
        #                        name='funHouse',
        #                        modelPath="models/funHouse/funHouse.egg")

        self.addSimpleBuilding(boxSize=Vec3(8, 12, 14),
                               pos=Vec3(250, 250, 0),
                               scale=Vec3(0.05, 0.05, 0.05),
                               heading=180,
                               name='rest station',
                               modelPath="models/rest station/rest station.egg",
                               shift=Vec3(0, 0, 11))

    def loadObstacles(self):
        origin = Point3(2, 0, 0)
        size = Vec3(2, 4.75, 1)
        shape = BulletBoxShape(size * 0.55)
        for i in range(10):
            pos = origin + size * i
            pos.setY(0)
            stairNP = self.render.attachNewNode(
                BulletRigidBodyNode('Stair%i' % i))
            stairNP.node().addShape(shape)
            stairNP.setPos(pos)
            stairNP.setCollideMask(BitMask32.allOn())

            modelNP = loader.loadModel('models/box.egg')
            modelNP.reparentTo(stairNP)
            # modelNP.setPos(0, 0, 0)
            modelNP.setPos(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0)
            modelNP.setScale(size)
            self.world.attachRigidBody(stairNP.node())

        for i in range(10):
            pos = origin + size * i
            pos.setY(0)
            pos.setX(pos.getX() * -1)
            stairNP = self.render.attachNewNode(
                BulletRigidBodyNode('Stair%i' % i))
            stairNP.node().addShape(shape)
            stairNP.setPos(pos)
            stairNP.setCollideMask(BitMask32.allOn())

            modelNP = loader.loadModel('models/box.egg')
            modelNP.reparentTo(stairNP)
            modelNP.setPos(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0)
            modelNP.setScale(size)

            self.world.attachRigidBody(stairNP.node())

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

    def addSimpleBuilding(self, boxSize, pos, scale, heading, name, modelPath, shift=Vec3(0, 0, 0)):
        shape = BulletBoxShape(boxSize)
        objNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        objNP.node().addShape(shape)
        objNP.setPos(pos.getX(), pos.getY(), pos.getZ())
        objNP.setCollideMask(BitMask32.allOn())
        objModel = self.loader.loadModel(modelPath)
        objModel.setScale(scale.getX(), scale.getY(), scale.getZ())
        objModel.setPos(shift.getX(), shift.getY(), shift.getZ())
        objModel.setH(heading)
        objModel.reparentTo(objNP)
        self.world.attachRigidBody(objNP.node())

myGame = Game()
myGame.run()
