from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletWorld
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import BitMask32
from panda3d.core import BitMask32
from panda3d.core import NodePath, PandaNode
from panda3d.core import Vec3
from random import randrange


class Obstacle():
    def __init__(self):
        self.objects = []
        self.objectsMoving = []

    # def move(self, task):
    #     print "moving obj"
    #     for obj in self.objects:
    #         obj.setY(obj, 0.01)

    #     return task.cont
    def move(self, task):
        for index, obj in enumerate(self.objects):
            moveVec = Vec3(0, 1, 0)
            if obj.getY() > 2 or obj.getY() < -2:
                self.objectsMoving[index] *= -1
            obj.setY(obj, self.objectsMoving[index])
        return task.cont

    def stair(self, world, render, name, size, pos):
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
        self.objects.append(stairNP)
        self.objectsMoving.append(randrange(0, 5) * 1.0 / 100)
        world.attachRigidBody(stairNP.node())
