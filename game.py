# LIHAO LIN Created on 07/08/2016 All right reserved
import sys
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec3, Vec4, Point3
from panda3d.core import BitMask32
from panda3d.core import NodePath, PandaNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSoftBodyNode
from panda3d.bullet import BulletSoftBodyConfig
from panda3d.bullet import ZUp


class LegoAdventure(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupWorld()

        taskMgr.add(self.update, 'update')

    def update(self, task):
        self.processInputs()
        # do Physics process
        dt = globalClock.getDt()
        self.world.doPhysics(dt, 4, 1.0 / 240.0)
        # reposition the camera
        camvec = self.characterNP.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec * (camdist - 10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec * (5 - camdist))
            camdist = 5.0
        self.floater.setPos(self.characterNP.getPos())
        self.floater.setZ(self.characterNP.getZ() + 2.0)
        # base.camera.lookAt(self.floater)
        return task.cont

    def processInputs(self):
        pass

    # Setup functions for Game
    def setupWorld(self):
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)
        # setup environment
        # self.environ = self.loader.loadModel("models/environment")
        # self.environ.reparentTo(self.render)
        # self.environ.setScale(0.25, 0.25, 0.25)
        # self.environ.setPos(-8, 42, 0)
        # setup debugNode
        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()
        # created Bullet Physics World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        # add debugNode to the world
        self.world.setDebugNode(self.debugNP.node())
        # other setups
        self.setupLights()
        self.setupControlKeys()
        # Floor
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode('Floor'))
        floorNP.node().addShape(shape)
        floorNP.setPos(0, 0, 0)
        floorNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(floorNP.node())
        self.addPlayer()

    def addPlayer(self):
        # Character
        h = 1.75
        w = 0.4
        # TODO: Change the Shape of the character in physics world
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        #    self.character.setMass(1.0)
        self.characterNP = self.render.attachNewNode(self.character)
        self.characterNP.setPos(-2, 0, 14)
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)
        self.actorNP = Actor('models/Actors/lego/Brawler/Brawler.egg', {
            'run': 'models/Actors/lego/Brawler/Brawler-walk.egg',
            'walk': 'models/Actors/lego/Brawler/Brawler-walk.egg',
            'jump': 'models/Actors/lego/Brawler/Brawler-jump.egg'})
        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.3048)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, 0.4)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

    def setupLights(self):
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)
        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)
        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(dlightNP)
        print "Done Setup Light"

    def setupControlKeys(self):
        self.accept('escape', self.Exit)
        # self.accept('r', self.Reset)
        self.accept('t', self.Debug)
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')
        inputState.watchWithModifiers('jump', 'space')
        print "Done Setup Control"

    def Exit(self):
        # self.cleanup()
        sys.exit(1)

    def Debug(self):
        print "Debug Mode Toggled"
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

game = LegoAdventure()
game.run()
