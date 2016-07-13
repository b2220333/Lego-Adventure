from direct.actor.Actor import Actor
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletWorld
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import BitMask32
from panda3d.core import NodePath, PandaNode
from panda3d.core import Vec3, Vec4


class Enemy:
    def __init__(self, nodePath, world, render, pos):
        shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.characterNP = render.attachNewNode(self.character)
        self.characterNP.setPos(pos)
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        world.attachCharacter(self.character)
        self.actorNP = nodePath
        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.3048)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, 0.4)
