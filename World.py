from GameBase import GameBase
# from panda3d.core import Vec3, Point3
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
from direct.gui.DirectGui import *
from panda3d.core import *
from MapData import Stages
from panda3d.bullet import BulletGhostNode



class Game(GameBase):
    def __init__(self):
        GameBase.__init__(self)
        self.movingSpeed = 3
        self.jumpSpeed = 6
        self.cameraHeight = 3
        self.level = 1
        self.springs = []
        self.l1 = DirectButton(text="Level - 1",
                               scale=0.05,
                               pos=(-0.2, .4, 0),
                               command=self.setLevel1)
        self.l2 = DirectButton(text="Level - 2",
                               scale=0.05,
                               pos=(0.2, .4, 0),
                               command=self.setLevel2)

    def setLevel1(self):
        self.level = 1
        self.startGame()
        # self.run()

    def setLevel2(self):
        self.level = 2
        self.startGame()
        # self.run()

    def startGame(self):
        self.l1.destroy()
        self.l2.destroy()
        self.setupBase()
        self.loadMap()
        self.loadStages()
        if self.level is 2:
            self.characterNP.setPos(Vec3(-6, -9, 16.5))
        # self.run()

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

    def loadStages(self):
        stageFilePath = "models/Ground2/Ground2.egg"
        for stage in Stages:
            self.addStage(boxSize=stage[0],
                          pos=stage[1],
                          name=stage[2],
                          modelPath=stage[3],
                          heading=stage[4],
                          numberOfEnemy=stage[5])

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
        self.addSpring(pos)

    def addSpring(self, pos):
            shape = BulletBoxShape(Vec3(0.3, 0.3, 0.8))
            node = BulletGhostNode('Spring')
            node.addShape(shape)
            springNP = self.render.attachNewNode(node)
            springNP.setCollideMask(BitMask32.allOff())
            springNP.setPos(pos.getX(), pos.getY(), pos.getZ()+3.4)
            modelNP = loader.loadModel('models/spring/spring.egg')
            modelNP.reparentTo(springNP)
            modelNP.setScale(1, 1, 1)
            modelNP.setPos(0, 0, -1)
            self.world.attachGhost(node)
            self.springs.append(node)

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
myGame.getLevel()
# myGame.startGame()
