# LIHAO LIN Created on 07/08/2016 All right reserved
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletWorld
from panda3d.core import *
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import BitMask32
from panda3d.core import NodePath, PandaNode
from panda3d.core import Vec3, Vec4
from random import randrange
from Settings import *
import sys


class GameBase(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.jumpHeight = 5
        self.inTheAir = False
        self.cameraHeight = 5
        self.booosted = False
        self.currentLevel = 1
        self.springs = []
        self.enemys = []
        self.l1 = DirectButton(text="Level - 1",
                               scale=0.05,
                               pos=(-0.2, .4, 0),
                               command=self.startLevel1)
        self.l2 = DirectButton(text="Level - 2",
                               scale=0.05,
                               pos=(0.2, .4, 0),
                               command=self.startLevel2)

    def setupBase(self):
        self.setupWorld()
        taskMgr.add(self.update, 'update')
        taskMgr.add(self.positionCamera, 'positionCamera')
        taskMgr.add(self.enemyAttack, 'enemyAttack')

    def enemyAttack(self, task):
        for enemy in self.enemys:
            vec = self.characterNP.getPos() - enemy.getPos()
            length = vec.length()
            if length < 10:
                print length
                enemy.node().applyCentralForce(vec)
        return task.cont

    def update(self, task):
        self.processInputs()
        # do Physics process
        dt = globalClock.getDt()
        self.world.doPhysics(dt, 4, 1.0 / 240.0)
        # print "Player Position: {}".format(self.characterNP.getPos())
        return task.cont

    def processInputs(self):
        if inputState.isSet('cameraHigher'):
            self.cameraHeight += 1
        if inputState.isSet('cameraLower'):
            self.cameraHeight -= 1

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
        if inputState.isSet('jump') and self.inTheAir is False:
            self.runningPose = False
            self.actorNP.play("jump")
            if self.booosted:
                self.character.setMaxJumpHeight(self.jumpHeight * 2)
                self.character.setJumpSpeed(JUMP_SPEED * 2)
            else:
                self.character.setMaxJumpHeight(self.jumpHeight)
                self.character.setJumpSpeed(JUMP_SPEED)
            self.character.doJump()
            self.inTheAir = True
            taskMgr.add(self.resetInTheAir, "resetInTheAir")
        if inputState.isSet('turnLeft'):
            turningAngle = 120.0
            isMovingDirection = True
        if inputState.isSet('turnRight'):
            turningAngle = -120.0
            isMovingDirection = True

        if self.inTheAir:
            pass
        else:
            if isMovingDirection:
                if self.runningPose is False:
                    self.actorNP.loop("run")
                    self.runningPose = True
            else:
                if self.runningPose:
                    self.actorNP.stop()
                    self.actorNP.pose("walk", 0)
                    self.runningPose = False
        self.character.setLinearMovement(movingDirection * MOVING_SPEED, True)
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
        self.addEnemys()

    def addGround(self):
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode('Ground'))
        floorNP.node().addShape(shape)
        floorNP.setPos(0, 0, 0)
        floorNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(floorNP.node())

    def addPlayer(self):
        shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player-1')
        self.characterNP = self.render.attachNewNode(self.character)
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

    def resetInTheAir(self, task):
        if task.time < 1.2:
            return task.cont
        else:
            self.inTheAir = False
            return task.done

    def resetJumpHeight(self, task):
        if task.time < 10:
            return task.cont
        else:
            self.booosted = False
            return task.done

    def Exit(self):
        # self.cleanup()
        sys.exit(1)

    def Debug(self):
        print "Debug Mode Toggled"
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def startLevel1(self):
        self.level = 1
        self.startGame()
        # self.run()

    def startLevel2(self):
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
            self.characterNP.setPos(LEVEL_2_POS)
        taskMgr.add(self.checkCollectable, "checkCollectable")
        taskMgr.add(self.checkPosition, "checkPosition")
        self.timeBar = DirectWaitBar(text="Time",
                                     value=0,
                                     range=60,
                                     pos=(0, .4, .9),
                                     scale=(1, 0.5, 0.2))
        self.resetCharacterPosition()

    def checkCollectable(self, task):
        for spring in self.springs:
            contactResult = self.world.contactTestPair(
                self.character, spring.node())
            if len(contactResult.getContacts()) > 0:
                print "Sphere is in contact with: ", spring.getName()
                spring.node().removeAllChildren()
                self.world.removeGhost(spring.node())
                taskMgr.add(self.resetJumpHeight, "resetJumpHeight")
                if self.booosted is False:
                    self.booosted = True
                    self.boostBar = DirectWaitBar(text="Boost",
                                                  value=5,
                                                  range=BOOST_TIME,
                                                  pos=(0, 1, 0.8),
                                                  scale=(0.5, 0.5, 0.2))
                    taskMgr.add(self.updateBoostStatus, 'updateBoostStatus')
        return task.cont

    def updateBoostStatus(self, task):
        if task.time < BOOST_TIME:
            self.boostBar["value"] = task.time
            return task.cont
        else:
            self.boostBar.destroy()
            return task.done

    def checkPosition(self, task):
        height = self.characterNP.getZ()
        if height < 5:
            print "player deaded"
            self.booosted = False
            self.resetCharacterPosition()
        else:
            if self.level is 1:
                vec = self.characterNP.getPos() - LEVEL_2_POS
                if vec.length() < 3:
                    print "Compeleted level 1"
                    self.level = 2
                # print "{} until level 1 check point".format(vec.length())
            else:
                vec = self.characterNP.getPos() - LEVEL_3_POS
                if vec.length() < 3:
                    print "Compeleted level 2"
                # print "{} until compelete check point".format(vec.length())
        return task.cont

    def resetCharacterPosition(self):
        if self.level is 1:
            self.characterNP.setPos(LEVEL_1_POS)
        else:
            self.characterNP.setPos(LEVEL_2_POS)
        taskMgr.add(self.countDown, 'countDown')

    def countDown(self, task):
        if task.time < 60:
            self.timeBar['value'] = task.time
            return task.cont
        else:
            print "Time over, Game Restart"
            self.resetCharacterPosition()
            return task.done

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
        for pos in SpringList:
            self.addSpring(pos)

    def loadStages(self):
        for stage in STAGE_POS_LIST:
            self.addStage(boxSize=stage[0],
                          pos=stage[1],
                          name=stage[2],
                          modelPath=stage[3],
                          heading=stage[4])

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

    def addStage(self, boxSize, pos, name, modelPath, heading=0):
        shape = BulletBoxShape(boxSize)
        objNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        objNP.node().addShape(shape)
        objNP.setPos(pos.getX(), pos.getY(), pos.getZ())
        objNP.setH(heading)
        objNP.setCollideMask(BitMask32.allOn())
        objModel = self.loader.loadModel(modelPath)
        objModel.setScale(2 * boxSize.getX(),
                          2 * boxSize.getY(),
                          2 * boxSize.getZ())
        objModel.setPos(0, 0, boxSize.getZ() / -1)
        objModel.reparentTo(objNP)
        self.world.attachRigidBody(objNP.node())

    def addSpring(self, pos):
        print "add spring #{} at: {}".format(len(self.springs), pos)
        shape = BulletBoxShape(Vec3(0.3, 0.3, 0.8))
        node = BulletGhostNode('Spring' + str(len(self.springs)))
        node.addShape(shape)
        springNP = self.render.attachNewNode(node)
        springNP.setCollideMask(BitMask32.allOff())
        springNP.setPos(pos.getX(), pos.getY(), pos.getZ() + 3.4)
        modelNP = loader.loadModel('models/spring/spring.egg')
        modelNP.reparentTo(springNP)
        modelNP.setScale(1, 1, 1)
        modelNP.setPos(0, 0, -1)
        self.world.attachGhost(node)
        self.springs.append(springNP)

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

    def addEnemys(self):
        for pos in ENEMY_POS_LIST:
            self.addEnemy(pos)

    def addEnemy(self, pos):
        print "enemy pos: ", pos
        type = randrange(1, 4)
        shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
        enemy = BulletRigidBodyNode("Enemy" + str(len(self.enemys)))
        enemy.setMass(0.3)
        enemy.addShape(shape)
        characterNP = render.attachNewNode(enemy)
        characterNP.setPos(pos)
        characterNP.setH(45)
        characterNP.setCollideMask(BitMask32.allOn())
        self.enemys.append(characterNP)
        self.world.attachRigidBody(enemy)
        if type is 1:
            actorNP = Actor('models/Actors/lego/Shield/Shield.egg',
                            {
                                'fallbackGetup': 'models/Actors/lego/Shield/Shield-FallbackGetup.egg',
                                'fallforwardGetup': 'models/Actors/lego/Shield/Shield-FallforwardGetup.egg',
                                'jump': 'models/Actors/lego/Shield/Shield-jump.egg',
                                'punching': 'models/Actors/lego/Shield/Shield-punching.egg',
                                'walk': 'models/Actors/lego/Shield/Shield-walk.egg'
                            })
        else:
            actorNP = Actor('models/Actors/lego/SecurityGuard/SecurityGuard.egg',
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

        actorNP.reparentTo(characterNP)
        actorNP.setScale(0.3048)
        actorNP.setH(180)
        actorNP.setPos(0, 0, 0.4)


myGame = GameBase()
myGame.run()
myGame.getLevel()
