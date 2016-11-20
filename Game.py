from GameScene import *
from direct.gui.DirectGui import *
from direct.showbase.InputStateGlobal import inputState
from Settings import *

class Game(GameScene):
    def __init__(self):
        GameScene.__init__(self)
        self.chooseLevel()
        # TODO: REMOVE THESE
        self.inTheAir = False
        self.booosted = False
        self.currentLevel = 1
        self.type_1_enemys = []
        self.type_1_enemy_actors = []
        self.type_1_enemy_is_running = []
        self.type_1_enemy_is_attacking_pose = []
        self.type_2_enemys = []
        self.type_2_enemy_actors = []
        self.type_2_enemy_is_running = []
        self.type_2_enemy_is_attacking_pose = []
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
        taskMgr.add(self.shieldAttackingTask, 'shieldAttackingTask')
        taskMgr.add(self.guardAttachingTask, 'guardAttachingTask')
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
        self.player.setPos(PLAYER_POSITIONS[self.level])
        self.player.lookAt(Vec3(0, 0, 0))
        self.health = HEALTH_LIMIT
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
                self.player.getcontrollerNode(), ball)
            if len(contactResult.getContacts()) > 0:
                self.health -= 1
                self.healthBar['value'] = self.health
                self.hitSound.play()
        return task.cont

    def collectableCheckTask(self, task):
        for spring in self.springs:
            contactResult = self.world.contactTestPair(
                self.player.getcontrollerNode(), spring.node())
            if len(contactResult.getContacts()) > 0:
                self.pickupSpringSound.play()
                # print "Sphere is in contact with: ", spring.getName()
                spring.node().removeAllChildren()
                self.world.removeGhost(spring.node())
                taskMgr.add(self.boostTimmerTask, "boostTimmerTask")
                if self.booosted is False:
                    self.booosted = True
                    self.boostBar = DirectWaitBar(text="Boost",
                                                  value=5,
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
        if height < 5 or self.health < 0:
            self.deadthSound.play()
            self.booosted = False
            self.placePlayer()
        else:
            if self.level is 1:
                vec = self.player.getPos() - LEVEL_2_POS
                if vec.length() < 3:
                    print "Compeleted level 1"
                    self.level = 2
                    self.completeLevelSound.play()
            else:
                vec = self.player.getPos() - LEVEL_3_POS
                if vec.length() < 3:
                    print "Compeleted level 2"
        return task.cont

    def cameraFollowingTask(self, task):
        base.camera.setX(self.player.getNodePath(), 0)
        base.camera.setY(self.player.getNodePath(), -10)
        base.camera.setZ(self.player.getNodePath(), self.cameraHeight)
        position = self.player.getPos()
        position.setZ(position.getZ() + 2)
        base.camera.lookAt(position)
        return task.cont

    def shieldAttackingTask(self, task):
        for index, enemy in enumerate(self.type_1_enemys):
            target = self.player.getPos()
            target.setZ(enemy.getZ())
            enemy.lookAt(target)
            vec = self.player.getPos() - enemy.getPos()
            distance = vec.length()
            heightDelta = vec.getZ()
            if (distance < TYPE_1_ENEMY_ATTACK_RAIUS) and (abs(heightDelta) < 0.1):
                if not self.type_1_enemy_is_running[index]:
                    self.type_1_enemy_actors[index].loop('walk')
                    self.type_1_enemy_is_running[index] = True

                if not self.type_1_enemy_is_attacking_pose[index] and distance < TYPE_1_ENEMY_ATTACK_DISTANCE:
                    self.type_1_enemy_actors[index].play('punch')
                    self.pushSound.play()
                    self.type_1_enemy_is_attacking_pose[index] = True
                    taskMgr.add(self.resetPoseTask, 'resetAttackPose')
                if distance > TYPE_1_ENEMY_ATTACK_DISTANCE and not self.type_1_enemy_is_attacking_pose[index]:
                    enemy.node().setLinearMovement(Vec3(0, TYPE_1_ENEMY_MOVING_SPEED, 0), True)
                else:
                    enemy.node().setLinearMovement(Vec3(0, 0, 0), True)
                    self.pushed = True
                    self.pushedDirection = vec
                vec.normalize()
            else:
                if self.type_1_enemy_is_running[index]:
                    self.type_1_enemy_actors[index].stop()
                    self.type_1_enemy_actors[index].pose('walk', 0)
                    self.type_1_enemy_is_running[index] = False
                enemy.node().setLinearMovement(Vec3(0, 0, 0), True)
        return task.cont

    def guardAttachingTask(self, task):
        if (task.time % 0.2) < 0.01:
            for index, enemy in enumerate(self.type_2_enemys):
                heading = enemy.getH()
                enemy.lookAt(self.player.getPos())
                if abs(heading - enemy.getH()) > 1:
                    if not self.type_2_enemy_is_running[index]:
                        self.type_2_enemy_actors[index].loop('walk')
                    self.type_2_enemy_is_running[index] = True
                else:
                    if self.type_2_enemy_is_running[index]:
                        self.type_2_enemy_actors[index].stop()
                        self.type_2_enemy_actors[index].pose('walk', 0)
                        self.type_2_enemy_is_running[index] = False

        if (task.time % 2) < 0.01:
            for index, enemy in enumerate(self.type_2_enemys):
                target = self.player.getPos()
                vec = self.player.getPos() - enemy.getPos()
                distance = vec.length()
                if distance < TYPE_2_ENEMY_ATTACK_RAIUS:
                    self.type_2_enemy_actors[index].play('swing')
                    # throw new ball
                    pos = enemy.getPos()
                    shooting_direction = self.player.getPos() - pos
                    shooting_direction.normalize()
                    print "shotting at: ", shooting_direction
                    sphereNode = BulletRigidBodyNode('Ball')
                    sphereNode.setMass(1.0)
                    sphereNode.addShape(BulletSphereShape(0.2))
                    sphere = self.render.attachNewNode(sphereNode)
                    pos.setZ(pos.getZ() + 1)
                    sphere.setPos(pos)
                    smileyFace = self.loader.loadModel("models/smiley")
                    smileyFace.setScale(0.2)
                    smileyFace.reparentTo(sphere)
                    self.world.attachRigidBody(sphereNode)
                    sphereNode.applyCentralForce(shooting_direction * 1000)
                    self.sphereNodes.append(sphereNode)
        return task.cont

    def physicsUpdateTask(self, task):
        self.world.doPhysics(globalClock.getDt(), 4, 1.0 / 240.0)
        return task.cont

    def resetPoseTask(self, task):
        if task.time < 1:
            return task.cont
        else:
            for index in range(len(self.type_1_enemy_is_attacking_pose)):
                self.type_1_enemy_is_attacking_pose[index] = False
                self.type_1_enemy_is_running[index] = False
            return task.done

    def inputProcessingTask(self, task):
        if inputState.isSet('cameraHigher'):
            self.cameraHeight += 0.1
        if inputState.isSet('cameraLower'):
            self.cameraHeight -= 0.1

        movingDirection = Vec3(0, 0, 0)
        turningAngle = 0.0
        isMovingDirection = False
        if inputState.isSet('forward'):
            movingDirection.setY(PLAYER_SPEED)
            isMovingDirection = True
        if inputState.isSet('reverse'):
            movingDirection.setY(-PLAYER_SPEED)
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
                self.player.getcontrollerNode().setMaxJumpHeight(JUMP_HEIGHT * 2)
                self.player.getcontrollerNode().setJumpSpeed(JUMP_SPEED * 2)
            else:
                self.player.getcontrollerNode().setMaxJumpHeight(JUMP_HEIGHT)
                self.player.getcontrollerNode().setJumpSpeed(JUMP_SPEED)
            self.player.getcontrollerNode().doJump()
            self.jumpSound.play()
            self.inTheAir = True
            taskMgr.add(self.playerFallingTimmerTask,
                        "playerFallingTimmerTask")
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
                if self.player.getPose != RUNNING:
                    self.player.setPos(RUNNING)
                    # self.actorNP.loop('run')
                    # self.runningPose = True
            else:
                if self.player.getPose() == RUNNING:
                    self.player.setPos(WALKING)
                    # self.actorNP.stop()
                    # self.actorNP.pose("walk", 0)
                    # self.runningPose = False

        if self.pushed:
            movingDirection.setY(TYPE_1_ENEMY_PUSH_DISTANCE)
            self.pushed = False
        self.player.getcontrollerNode().setLinearMovement(movingDirection, True)
        self.player.getcontrollerNode().setAngularMovement(turningAngle)
        return task.cont