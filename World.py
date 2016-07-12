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
        self.jumpSpeed = 6
        self.cameraHeight = 3
        self.loadMap()
        self.loadObstacles()

    def loadMap(self):
        self.blue_sky_sphere = self.loader.loadModel(
            "models/blue_sky_sphere/blue_sky_sphere.egg")
        self.blue_sky_sphere.reparentTo(self.render)
        self.blue_sky_sphere.setScale(0.04, 0.04, 0.04)
        self.blue_sky_sphere.setPos(0, 0, 0)

        self.Ground2 = self.loader.loadModel(
            "models/Ground2/Ground2.egg")
        self.Ground2.reparentTo(self.render)
        self.Ground2.setScale(0.2, 0.2, 0.2)
        self.Ground2.setPos(0, 0, 0)

        self.addWall(Vec3(1, 100, 5), 100, 0)
        self.addWall(Vec3(1, 100, 5), -100, 0)
        self.addWall(Vec3(100, 1, 5), 0, 100)
        self.addWall(Vec3(100, 1, 5), 0, -100)

        self.addSimpleBox(boxSize=Vec3(27, 29, 15),
                          pos=Vec3(250, -250, 0),
                          scale=Vec3(0.1, 0.1, 0.1),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Junkyard/Junkyard.egg",
                          shift=Vec3(0, -2.5, 0))

        for x in xrange(1, 3):
            self.addSimpleBox(boxSize=Vec3(12, 6, 14),
                              pos=Vec3(-100 + 50 * x,
                                       90, 0),
                              scale=Vec3(0.5, 0.5, 0.5),
                              heading=180,
                              name='FarmHouse{}'.format(x),
                              modelPath="models/FarmHouse/FarmHouse.egg")

        for index in xrange(1, 10):
            style = randrange(1, 6)
            self.addSimpleBox(boxSize=Vec3(3.5, 5, 10),
                              pos=Vec3(21 * index - 100, -100, 0),
                              scale=Vec3(0.5, 0.5, 0.5),
                              heading=0,
                              name='Townhouse{}'.format(index),
                              modelPath="models/Townhouse{}/Townhouse{}.egg".format(
                style, style),
                shift=Vec3(0, 0, 0))

        # for index in xrange(1, 7):
        #     self.addSimpleBox(boxSize=Vec3(22, 22, 100),
        #                            pos=Vec3(280, 60 * index - 200, 0),
        #                            scale=Vec3(0.5, 0.5, 0.5),
        #                            heading=90,
        #                            name='Skyscraper1',
        #                            modelPath="models/Skyscraper1/Skyscraper1.egg",
        #                            shift=Vec3(0, 0, 0))

        # self.addSimpleBox(boxSize=Vec3(6, 5, 14),
        #                        pos=Vec3(0, 0, 0),
        #                        scale=Vec3(0.5, 0.5, 0.5),
        #                        heading=180,
        #                        name='funHouse',
        #                        modelPath="models/funHouse/funHouse.egg")

        # self.addSimpleBox(boxSize=Vec3(8, 12, 14),
        #                        pos=Vec3(250, 250, 0),
        #                        scale=Vec3(0.05, 0.05, 0.05),
        #                        heading=180,
        #                        name='rest station',
        #                        modelPath="models/rest station/rest station.egg",
        #                        shift=Vec3(0, 0, 11))

    def loadObstacles(self):
        self.addStairs(origin=Point3(-85, -85, 0),
                       steps=4,
                       size=Vec3(2, 4.75, 1),
                       spaceRatio=1.5,
                       alignment='y')
        self.addStairs(origin=Point3(-75, -83, 6),
                       steps=2,
                       size=Vec3(4.75, 2, 1),
                       spaceRatio=1.5,
                       alignment='x')
        self.addSimpleBox(boxSize=Vec3(15, 15, 0.2),
                          pos=Vec3(-63, -63, 9),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))
        self.addSimpleBox(boxSize=Vec3(15, 5, 0.2),
                          pos=Vec3(-29, -50, 10),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))

        self.addSimpleBox(boxSize=Vec3(3, 15, 0.2),
                          pos=Vec3(-20, -25, 11),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))

        self.addSimpleBox(boxSize=Vec3(3, 7, 0.2),
                          pos=Vec3(-20, -25, 12.5),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))

        self.addSimpleBox(boxSize=Vec3(7, 7, 0.2),
                          pos=Vec3(-10, -10, 14),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))

        self.addSimpleBox(boxSize=Vec3(2, 15, 0.2),
                          pos=Vec3(-0, 10, 15.5),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))
        self.addSimpleBox(boxSize=Vec3(2, 2, 0.2),
                          pos=Vec3(10, 10, 17),
                          scale=Vec3(0.001, 0.001, 0.001),
                          heading=0,
                          name='Junkyard',
                          modelPath="models/Ground2/Ground2.egg",
                          shift=Vec3(0, 0, 0))

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

    def addSimpleBox(self, boxSize, pos, scale, heading, name, modelPath, shift=Vec3(0, 0, 0)):
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

    def addStairs(self, origin, steps, size, spaceRatio, alignment):
        for i in range(steps):
            pos = origin + size * spaceRatio * i
            if alignment == 'x':
                pos.setX(origin.getX())
            if alignment == 'y':
                pos.setY(origin.getY())
            if alignment == 'z':
                pos.setZ(origin.getZ())
            self.stair(name="stare{}".format(i),
                       size=size,
                       pos=pos)

    def stair(self, name, size, pos):
        shape = BulletBoxShape(size * 0.5)
        stairNP = render.attachNewNode(
            BulletRigidBodyNode(name))
        stairNP.node().addShape(shape)
        stairNP.setPos(pos)
        stairNP.setCollideMask(BitMask32.allOn())
        modelNP = loader.loadModel('models/box.egg')
        modelNP.reparentTo(stairNP)
        modelNP.setPos(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0)
        modelNP.setScale(size)
        self.world.attachRigidBody(stairNP.node())

myGame = Game()
myGame.run()
