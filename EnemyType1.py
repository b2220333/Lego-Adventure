from Enemy import Enemy
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


class EnemyType1(Enemy):
    def __init__(self, world, render, pos):
        nodePath = Actor('models/Actors/lego/Shield/Shield.egg',
                         {
                             'fallbackGetup': 'models/Actors/lego/Shield/Shield-FallbackGetup.egg',
                             'fallforwardGetup': 'models/Actors/lego/Shield/Shield-FallforwardGetup.egg',
                             'jump': 'models/Actors/lego/Shield/Shield-jump.egg',
                             'punching': 'models/Actors/lego/Shield/Shield-punching.egg',
                             'walk': 'models/Actors/lego/Shield/Shield-walk.egg'
                         })
        Enemy.__init__(self, nodePath, world, render, pos)
