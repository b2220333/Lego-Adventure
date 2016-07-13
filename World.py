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
from Enemy import Enemy
from EnemyType1 import EnemyType1
from EnemyType2 import EnemyType2


class Game(GameBase):
    def __init__(self):
        GameBase.__init__(self)
        self.movingSpeed = 3
        self.jumpSpeed = 6
        self.cameraHeight = 3
        self.loadMap()
        self.loadStages()

    def setEnemy(self, pos):
        randNum = randrange(1, 4)
        if randNum is 3:
            EnemyType1(world=self.world,
                       render=self.render,
                       pos=pos)
        else:
            EnemyType2(world=self.world,
                       render=self.render,
                       pos=pos)

    def loadMap(self):
        self.blue_sky_sphere = self.loader.loadModel(
            "models/blue_sky_sphere/blue_sky_sphere.egg")
        self.blue_sky_sphere.reparentTo(self.render)
        self.blue_sky_sphere.setScale(0.04, 0.04, 0.04)
        self.blue_sky_sphere.setPos(0, 0, 0)

        self.garden = self.loader.loadModel(
            "models/garden/garden.egg")
        self.garden.reparentTo(self.render)
        self.garden.setScale(2, 2, 2)
        self.garden.setPos(0, 0, 0)

        self.addWall(Vec3(1, 90, 5), 80, 0)
        self.addWall(Vec3(1, 90, 5), -80, 0)
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
            self.addSimpleBox(boxSize=Vec3(12, 6, 7),
                              pos=Vec3(-100 + 50 * x,
                                       90, 0),
                              scale=Vec3(0.5, 0.5, 0.5),
                              heading=180,
                              name='FarmHouse{}'.format(x),
                              modelPath="models/FarmHouse/FarmHouse.egg")

        for index in xrange(1, 10):
            style = randrange(1, 6)
            self.addSimpleBox(boxSize=Vec3(3.5, 5, 5),
                              pos=Vec3(21 * index - 100, -100, 0),
                              scale=Vec3(0.5, 0.5, 0.5),
                              heading=0,
                              name='Townhouse{}'.format(index),
                              modelPath="models/Townhouse{}/Townhouse{}.egg".format(
                style, style))

    def loadStages(self):
        self.addStage(boxSize=Vec3(15, 15, 0.2),
                      pos=Vec3(-63, -63, 9),
                      name='Stage1',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=5)
        self.addStage(boxSize=Vec3(15, 5, 0.2),
                      pos=Vec3(-29, -50, 10),
                      name='Stage2',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=3)

        self.addStage(boxSize=Vec3(3, 15, 0.2),
                      pos=Vec3(-20, -25, 11),
                      name='Stage3',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=3)

        self.addStage(boxSize=Vec3(3, 7, 0.2),
                      pos=Vec3(-12, -25, 12.5),
                      name='Stage4',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=3)

        self.addStage(boxSize=Vec3(7, 7, 0.2),
                      pos=Vec3(-10, -10, 14),
                      name='Stage5',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=2)

        self.addStage(boxSize=Vec3(2, 15, 0.2),
                      pos=Vec3(-0, 10, 15.5),
                      name='Stage6',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=1)

        self.addStage(boxSize=Vec3(2, 2, 0.2),
                      pos=Vec3(5, 10, 17),
                      name='Stage7',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=1)

        self.addStage(boxSize=Vec3(1.0, 12, 0.2),
                      pos=Vec3(17, 22, 18),
                      name='Stage8',
                      modelPath="models/Ground2/Ground2.egg",
                      heading=-45,
                      numberOfEnemy=1)

        self.addStage(boxSize=Vec3(0.85, 12, 0.2),
                      pos=Vec3(29, 41, 19),
                      name='Stage9',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=1)

        self.addStage(boxSize=Vec3(0.7, 12, 0.2),
                      pos=Vec3(40, 62, 20),
                      name='Stage8',
                      modelPath="models/Ground2/Ground2.egg",
                      heading=-45,
                      numberOfEnemy=1)

        self.addStage(boxSize=Vec3(0.55, 12, 0.2),
                      pos=Vec3(52, 80, 21),
                      name='Stage9',
                      modelPath="models/Ground2/Ground2.egg",
                      numberOfEnemy=0)

        self.addStage(boxSize=Vec3(0.40, 12, 0.2),
                      pos=Vec3(62, 80, 22),
                      name='Stage10',
                      modelPath="models/Ground2/Ground2.egg",
                      heading=45,
                      numberOfEnemy=0)

        self.addStage(boxSize=Vec3(0.40, 100, 0.2),
                      pos=Vec3(72, 20, 23),
                      name='Stage11',
                      modelPath="models/Ground2/Ground2.egg",
                      heading=0,
                      numberOfEnemy=0)

        self.addStage(boxSize=Vec3(0.40, 120, 0.2),
                      pos=Vec3(0, 0, 24),
                      name='Stage12',
                      modelPath="models/Ground2/Ground2.egg",
                      heading=45,
                      numberOfEnemy=0)

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
        objNP.setPos(pos.getX(), pos.getY(), pos.getZ() + boxSize.getZ())
        objNP.setCollideMask(BitMask32.allOn())
        objModel = self.loader.loadModel(modelPath)
        objModel.setScale(scale.getX(), scale.getY(), scale.getZ())
        objModel.setPos(shift.getX(), shift.getY(),
                        shift.getZ() - boxSize.getZ())
        objModel.setH(heading)
        objModel.reparentTo(objNP)
        self.world.attachRigidBody(objNP.node())

    def addStage(self, boxSize, pos, name, modelPath, heading=0, numberOfEnemy=0):
        boxSize.setZ(0.01)
        shape = BulletBoxShape(boxSize)
        objNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        objNP.node().addShape(shape)
        objNP.setPos(pos.getX(), pos.getY(), pos.getZ())
        objNP.setH(heading)
        objNP.setCollideMask(BitMask32.allOn())
        objModel = self.loader.loadModel(modelPath)
        objModel.setScale(0.00174 * boxSize.getX(),
                          0.00174 * boxSize.getY(), 1)
        objModel.setPos(0, 0, 0)
        objModel.reparentTo(objNP)
        self.world.attachRigidBody(objNP.node())
        if numberOfEnemy > 0:
            for i in range(numberOfEnemy):
                enemyPos = Vec3(pos.getX() + i, pos.getY(), pos.getZ())
                self.setEnemy(enemyPos)

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
