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


class EnemyType2(Enemy):
    def __init__(self, world, render, pos):
        nodePath = Actor('models/Actors/lego/SecurityGuard/SecurityGuard.egg',
                         {
                             'fallbackGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallbackGetup.egg',
                             'fallforwardGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallforwardGetup.egg',
                             'firegun': 'models/Actors/lego/SecurityGuard/SecurityGuard-firegun.egg',
                             'jump': 'models/Actors/lego/SecurityGuard/SecurityGuard-jump.egg',
                             'run': 'models/Actors/lego/SecurityGuard/SecurityGuard-run.egg',
                             'swing': 'models/Actors/lego/SecurityGuard/SecurityGuard-swing.egg',
                             'walk': 'models/Actors/lego/SecurityGuard/SecurityGuard-walk.egg',
                             'SecurityGuard': 'models/Actors/lego/SecurityGuard/SecurityGuard.egg'
                         })
        Enemy.__init__(self, nodePath, world, render, pos)
