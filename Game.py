# Panda3d Library
from direct.gui.DirectGui import *
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import ClockObject
# My Game Classes
from GameScene import *
from Settings import *
from FireBalls import FireBalls

class Game(GameScene):
    def __init__(self):
        GameScene.__init__(self)
        self.chooseLevel()
        self.booosted = False
        # TODO: REMOVE THESE
        self.pushed = False

    def chooseLevel(self):
        self.buttons = []
        button = DirectButton(text="Level - 1",
                               scale=0.05,
                               pos=(-0.2, .4, 0),
                               command=lambda : self.startGame(1))
        self.buttons.append(button)
        button = DirectButton(text="Level - 2",
                               scale=0.05,
                               pos=(0.2, .4, 0),
                               command=lambda : self.startGame(2))
        self.buttons.append(button)


    def startGame(self, level):
        # Set level to start
        self.level = level
        # List of balls in Game Scene
        self.sphereNodes = []

        # Remove buttons from the screen
        for button in self.buttons:
            button.destroy()
        self.buttons = []

        # Setup Game Scene
        self.setupScene()
        # Setup Guard Weapon: Fire Ball
        self.fireballs = FireBalls(self.world, self.render, self.loader)
        # Setup Player Control
        self.setupControls()
        # TODO: Remove this
        self.placePlayer()

        # Add status indicator onto screen
        self.timeBar = DirectWaitBar(text="Time",
                                     value=0,
                                     range=TIME_LIMIT,
                                     pos=(0, .4, .95),
                                     scale=(1, 1, 0.45))

        self.healthBar = DirectWaitBar(text="health",
                                       value=HEALTH_LIMIT,
                                       range=HEALTH_LIMIT,
                                       pos=(0, 0.4, 0.85),
                                       scale=(1, 1, 0.45))

        # Begin tasks
        taskMgr.add(self.physicsUpdateTask, 'physicsUpdateTask')
        taskMgr.add(self.inputProcessingTask, 'inputProcessingTask')
        taskMgr.add(self.cameraFollowingTask, 'cameraFollowingTask')
        taskMgr.add(self.attackingTask, 'attackingTask')
        taskMgr.add(self.collectableCheckTask, "collectableCheckTask")
        taskMgr.add(self.hitCheckTask, "hitCheckTask")
        taskMgr.add(self.playerHealthCheckTask, "playerHealthCheckTask")


    def setupControls(self):
        def Exit():
            sys.exit(1)

        def Debug():
            print "Debug Mode Toggled"
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()

        base.disableMouse()
        self.accept('escape', Exit)
        self.accept('t', Debug)
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')
        inputState.watchWithModifiers('jump', 'space')
        inputState.watchWithModifiers('cameraHigher', 'q')
        inputState.watchWithModifiers('cameraLower', 'e')

    def placePlayer(self):
        print("Level:", self.level, " Player @", PLAYER_POSITIONS[self.level])
        self.player.setPosition(PLAYER_POSITIONS[self.level])
        self.player.lookAt(Vec3(0, 0, 0))
        self.health = HEALTH_LIMIT
        self.isMoving = False
        taskMgr.add(self.gameTimmerTask, 'gameTimmerTask')


# ==========    Tasks running when game start

    def gameTimmerTask(self, task):
        if task.time < TIME_LIMIT:
            self.timeBar['value'] = task.time
            return task.cont
        else:
            print "Time over, Game Restart"
            self.placePlayer()
            return task.done

    def boostTimmerTask(self, task):
        if self.booosted and task.time < BOOST_TIME:
            self.boostBar["value"] = task.time
            return task.cont
        else:
            self.boostBar.destroy()
            return task.done

    def playerFallingTimmerTask(self, task):
        if task.time < PLAYER_FALLING_POSE_TIME:
            return task.cont
        else:
            self.inTheAir = False
            return task.done

    def hitCheckTask(self, task):
        for ball in self.sphereNodes:
            contactResult = self.world.contactTestPair(
                self.player.getControllerNode(), ball)
            if len(contactResult.getContacts()) > 0:
                self.health -= 1
                self.healthBar['value'] = self.health
                self.hitSound.play()
        return task.cont

    def collectableCheckTask(self, task):
        for spring in self.springs:
            contactResult = self.world.contactTestPair(
                self.player.getControllerNode(), spring.node())
            if len(contactResult.getContacts()) > 0:
                self.pickupSpringSound.play()
                # print "Sphere is in contact with: ", spring.getName()
                spring.node().removeAllChildren()
                self.world.removeGhost(spring.node())
                taskMgr.add(self.boostTimmerTask, "boostTimmerTask")
                if self.booosted is False:
                    self.booosted = True
                    self.boostBar = DirectWaitBar(text="Boost",
                                                  value=BOOST_TIME,
                                                  range=BOOST_TIME,
                                                  pos=(0, 1, 0.75),
                                                  scale=(0.5, 0.5, 0.2))
                    taskMgr.add(self.boostTimmerTask, 'boostTimmerTask')
        return task.cont

    def boostTimmerTask(self, task):
        if task.time < BOOST_TIME:
            return task.cont
        else:
            self.booosted = False
            return task.done

    def playerHealthCheckTask(self, task):
        height = self.player.getHeight()
        # print("Health: ", self.health, " Height: ", height)
        if height < 5 or self.health < 0:
            self.deadthSound.play()
            self.booosted = False
            self.placePlayer()
        else:
            if self.level is 1:
                vec = self.player.getPosition() - LEVEL_2_POS
                if vec.length() < 3:
                    print "Completed level 1"
                    self.level = 2
                    self.completeLevelSound.play()
            else:
                vec = self.player.getPosition() - LEVEL_3_POS
                if vec.length() < 3:
                    print "Completed level 2"
        return task.cont

    def cameraFollowingTask(self, task):
        base.camera.setX(self.player.getNodePath(), 0)
        base.camera.setY(self.player.getNodePath(), -10)
        base.camera.setZ(self.player.getNodePath(), self.cameraHeight)
        position = self.player.getPosition()
        position.setZ(position.getZ() + 2)
        base.camera.lookAt(position)
        return task.cont

    def attackingTask(self, task):
        for shield in self.shields:
            shield.lookAt(self.player.getPosition())
            vectorToPlayer = self.player.getPosition() - shield.getPosition()
            vectorFromHome = shield.getPosition() - self.player.getPosition()
            okayToAttack = False
            if (vectorToPlayer.getZ() < 0.1 and vectorToPlayer.length() < SHIELD_ATTACKING_RADIUS):
                okayToAttack = True
            else:
                shield.setPose(STANDING)

            if okayToAttack:

            else:
                shield.goBackHome()


        for guard in self.guards:
            guard.lookAt(self.player.getPosition())
            vectorToPlayer = self.player.getPosition() - guard.getPosition()
            vectorFromHome = guard.getPosition() - self.player.getPosition()
            okayToAttack = False
            if (vectorToPlayer.getZ() < 0.1 and vectorToPlayer.length() < GUARD_ATTACKING_RADIUS):
                okayToAttack = True
            else:
                guard.setPose(STANDING)
            if (task.time - guard.getShootingTime()) < GUARD_SHOOTING_TIME_INTERVAL:
                okayToAttack = False

            if okayToAttack:
                print("guard attacking")
                self.fireballs.fire(guard.getPosition(), self.player.getPosition())
                guard.setPose(SWINGING)
                guard.saveShootingTime(task.time)
            # if (vectorFromHome.length() > GUARD_MAX_DISTANCE_FROM_HOME):
                # guard.goBackHome()
        return task.cont

    def physicsUpdateTask(self, task):
        self.world.doPhysics(globalClock.getDt(), 4, 1.0 / 240.0)
        return task.cont

    def inputProcessingTask(self, task):
        # Camera Control Keys
        if inputState.isSet('cameraHigher'):
            self.cameraHeight += 0.1
        if inputState.isSet('cameraLower'):
            self.cameraHeight -= 0.1


        move = Vec3(0, 0, 0)
        turningAngle = 0.0

        # Character Movements
        if inputState.isSet('forward'):
            move.setY(PLAYER_SPEED)
            self.isMoving = True
        elif inputState.isSet('reverse'):
            move.setY(-PLAYER_SPEED)
            self.isMoving = True

        if inputState.isSet('turnLeft'):
            turningAngle = 120.0
            self.isMoving = True
        elif inputState.isSet('turnRight'):
            turningAngle = -120.0
            self.isMoving = True

        if self.isMoving is False:
            self.player.setPose(STANDING)
        else:
            self.player.setPose(WALKING)
        self.isMoving = False

        if inputState.isSet('jump'):
            self.player.setPose(JUMPING)
            if self.booosted:
                self.player.getControllerNode().setMaxJumpHeight(JUMP_HEIGHT * 2)
                self.player.getControllerNode().setJumpSpeed(JUMP_SPEED * 2)
            else:
                self.player.getControllerNode().setMaxJumpHeight(JUMP_HEIGHT)
                self.player.getControllerNode().setJumpSpeed(JUMP_SPEED)
            self.player.getControllerNode().doJump()

        if self.pushed:
            move.setY(TYPE_1_ENEMY_PUSH_DISTANCE)
            self.pushed = False
        self.player.getControllerNode().setLinearMovement(move, True)
        self.player.getControllerNode().setAngularMovement(turningAngle)
        return task.cont