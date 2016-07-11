# LIHAO LIN Created on 07/08/2016 All right reserved
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
import sys


class GameBase(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.movingSpeed = 1
        self.jumpHeight = 3
        self.jumpSpeed = 3
        self.setupWorld()
        self.cameraHeight = 5
        taskMgr.add(self.update, 'update')
        taskMgr.add(self.positionCamera, 'positionCamera')

    def update(self, task):
        self.processInputs()
        # do Physics process
        dt = globalClock.getDt()
        self.world.doPhysics(dt, 4, 1.0 / 240.0)
        return task.cont

    def processInputs(self):
        # input tests
        # if inputState.isSet('fallbackGetup'):
        #     print "fallbackGetup is playing"
        #     self.actorNP.play('fallbackGetup')
        # if inputState.isSet('fallforwardGetup'):
        #     print "fallforwardGetup is playing"
        #     self.actorNP.play('fallforwardGetup')
        # if inputState.isSet('fireball'):
        #     print "fireball is playing"
        #     self.actorNP.play('fireball')
        # if inputState.isSet('jump'):
        #     print "jump is playing"
        #     self.actorNP.play('jump')
        # if inputState.isSet('punching'):
        #     print "punching is playing"
        #     self.actorNP.play('punching')
        # if inputState.isSet('run'):
        #     print "run is playing"
        #     self.actorNP.play('run')
        # if inputState.isSet('superpunch'):
        #     print "superpunch is playing"
        #     self.actorNP.play('superpunch')
        # if inputState.isSet('walk'):
        #     print "walk is playing"
        #     self.actorNP.play('walk')

        if inputState.isSet('cameraHigher'):
            self.cameraHeight += 1
            print "new camera height {}".format(self.cameraHeight)
        if inputState.isSet('cameraLower'):
            self.cameraHeight -= 1
            print "new camera height {}".format(self.cameraHeight)
        # input test end

        movingDirection = Vec3(0, 0, 0)
        turningAngle = 0.0
        isMovingDirection = False
        if inputState.isSet('forward'):
            movingDirection.setY(2.0)
            isMovingDirection = True
        if inputState.isSet('reverse'):
            movingDirection.setY(-2.0)
            isMovingDirection = True
        if inputState.isSet('left'):
            movingDirection.setX(-2.0)
            isMovingDirection = True
        if inputState.isSet('right'):
            movingDirection.setX(2.0)
            isMovingDirection = True
        if inputState.isSet('jump'):
            self.runningPose = False
            self.actorNP.play("jump")
            self.character.setMaxJumpHeight(self.jumpHeight)
            self.character.setJumpSpeed(self.jumpSpeed)
            self.character.doJump()
        if inputState.isSet('turnLeft'):
            turningAngle = 120.0
            isMovingDirection = True
        if inputState.isSet('turnRight'):
            turningAngle = -120.0
            isMovingDirection = True

        if isMovingDirection:
            if self.runningPose is False:
                self.actorNP.loop("run")
                self.runningPose = True
                print "movingDirection"
        else:
            if self.runningPose:
                self.actorNP.stop()
                self.actorNP.pose("walk", 0)
                self.runningPose = False
        self.character.setLinearMovement(
            movingDirection * self.movingSpeed, True)
        self.character.setAngularMovement(turningAngle)

    def positionCamera(self, task):
        base.camera.setX(self.characterNP, 0)
        base.camera.setY(self.characterNP, -10)
        base.camera.setZ(self.characterNP, self.cameraHeight)
        position = self.characterNP.getPos()
        position.setZ(position.getZ() + 2)
        base.camera.lookAt(position)
        return task.cont

    # Setup functions for Game
    def setupWorld(self):
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)
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
        self.addGround()
        self.addPlayer()

    def addGround(self):
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode('Ground'))
        floorNP.node().addShape(shape)
        floorNP.setPos(0, 0, 0)
        floorNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(floorNP.node())

    def addPlayer(self):
        shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.characterNP = self.render.attachNewNode(self.character)
        self.characterNP.setPos(0, 0, 0)
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)
        self.actorNP = Actor('models/Actors/lego/Bricker/Bricker3.egg',
                             {
                                 'fallbackGetup': 'models/Actors/lego/Bricker/Bricker-FallbackGetup.egg',
                                 'fallforwardGetup': 'models/Actors/lego/Bricker/Bricker-FallforwardGetup.egg',
                                 'fireball': 'models/Actors/lego/Bricker/Bricker-fireball.egg',
                                 'jump': 'models/Actors/lego/Bricker/Bricker-jump.egg',
                                 'punching': 'models/Actors/lego/Bricker/Bricker-punching.egg',
                                 'run': 'models/Actors/lego/Bricker/Bricker-run.egg',
                                 'superpunch': 'models/Actors/lego/Bricker/Bricker-superpunch.egg',
                                 'walk': 'models/Actors/lego/Bricker/Bricker-walk.egg'
                             })
        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.3048)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, 0.4)
        self.runningPose = False

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
        base.disableMouse()
        self.accept('escape', self.Exit)
        # self.accept('r', self.Reset)
        self.accept('t', self.Debug)
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')
        inputState.watchWithModifiers('jump', 'space')
        inputState.watchWithModifiers('cameraHigher', 'q')
        inputState.watchWithModifiers('cameraLower', 'e')

        # action tests
        inputState.watchWithModifiers('fallbackGetup', '1')
        inputState.watchWithModifiers('fallforwardGetup', '2')
        inputState.watchWithModifiers('fireball', '3')
        inputState.watchWithModifiers('jump', '4')
        inputState.watchWithModifiers('punching', '5')
        inputState.watchWithModifiers('run', '6')
        inputState.watchWithModifiers('superpunch', '7')
        inputState.watchWithModifiers('walk', '8')
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
