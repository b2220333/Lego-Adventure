from direct.gui.DirectGui import *
from direct.showbase.InputStateGlobal import inputState
from MapWithCharacters import MapWithCharacters
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletRigidBodyNode, BulletSphereShape
from panda3d.core import *
from Settings import *
import sys


class GameBase(MapWithCharacters):
    def __init__(self):
        MapWithCharacters.__init__(self)
        self.cameraHeight = 5
        self.chooseLevel()
        self.sphereNodes = []
        self.health = HEALTH_LIMIT

# ======================================================
# =======       GAME FLOW CONTROL FUNCTIONS     ========
    def chooseLevel(self):
        def startLevel1():
            self.level = 1
            self.startGame()

        def startLevel2():
            self.level = 2
            self.startGame()

        self.l1 = DirectButton(text="Level - 1",
                               scale=0.05,
                               pos=(-0.2, .4, 0),
                               command=startLevel1)
        self.l2 = DirectButton(text="Level - 2",
                               scale=0.05,
                               pos=(0.2, .4, 0),
                               command=startLevel2)

    def startGame(self):
        # remove the menu
        self.l1.destroy()
        self.l2.destroy()
        # add game tasks
        self.addTasks()
        # setup map for game
        self.setupMap()
        # setup controlls
        self.setupControls()
        # setup chatacters
        self.setupCharacters()
        self.placePlayer()
        # add countdown timebar
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

    def addTasks(self):
        taskMgr.add(self.physicsUpdateTask, 'physicsUpdateTask')
        taskMgr.add(self.inputProcessTask, 'inputProcessTask')
        taskMgr.add(self.cameraPositionTask, 'cameraPositionTask')
        taskMgr.add(self.type_1_enemy_attack_task, 'type_1_enemy_attack_task')
        taskMgr.add(self.type_2_enemy_attack_task, 'type_2_enemy_attack_task')
        taskMgr.add(self.collectableCheckTask, "collectableCheckTask")
        taskMgr.add(self.hitCheckTask, "hitCheckTask")
        taskMgr.add(self.playerPositionCheckTask, "playerPositionCheckTask")

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
        print "Done Setup Control"

    def placePlayer(self):
        if self.level is 1:
            self.characterNP.setPos(LEVEL_1_POS)
            self.characterNP.lookAt(Vec3(0, 0, 0))
            self.health = HEALTH_LIMIT
        else:
            self.characterNP.setPos(LEVEL_2_POS)
            self.characterNP.lookAt(Vec3(0, 0, 0))
        taskMgr.add(self.countDownTask, 'countDownTask')

# ==============================================================
# =======       TASKS FOR RUNNING THE GAME        ============

    def countDownTask(self, task):
        if task.time < TIME_LIMIT:
            self.timeBar['value'] = task.time
            return task.cont
        else:
            print "Time over, Game Restart"
            self.placePlayer()
            return task.done

    def updateBoostBarTask(self, task):
        if self.booosted and task.time < BOOST_TIME:
            self.boostBar["value"] = task.time
            return task.cont
        else:
            self.boostBar.destroy()
            return task.done

    def resetCharacterStatusTask(self, task):
        if task.time < 1.2:
            return task.cont
        else:
            self.inTheAir = False
            return task.done

    def hitCheckTask(self, task):
        for ball in self.sphereNodes:
            contactResult = self.world.contactTestPair(
                self.character, ball)
            if len(contactResult.getContacts()) > 0:
                # self.pickupSpringSound.play()
                print "hit"
                self.health -= 1
                self.healthBar['value'] = self.health
        return task.cont

    def collectableCheckTask(self, task):
        for spring in self.springs:
            contactResult = self.world.contactTestPair(
                self.character, spring.node())
            if len(contactResult.getContacts()) > 0:
                self.pickupSpringSound.play()
                # print "Sphere is in contact with: ", spring.getName()
                spring.node().removeAllChildren()
                self.world.removeGhost(spring.node())
                taskMgr.add(self.boostResetTask, "boostResetTask")
                if self.booosted is False:
                    self.booosted = True
                    self.boostBar = DirectWaitBar(text="Boost",
                                                  value=5,
                                                  range=BOOST_TIME,
                                                  pos=(0, 1, 0.75),
                                                  scale=(0.5, 0.5, 0.2))
                    taskMgr.add(self.updateBoostBarTask, 'updateBoostBarTask')
        return task.cont

    def boostResetTask(self, task):
        if task.time < BOOST_TIME:
            return task.cont
        else:
            self.booosted = False
            return task.done

    def playerPositionCheckTask(self, task):
        height = self.characterNP.getZ()
        if height < 5:
            print "player deaded"
            self.deadthSound.play()
            self.booosted = False
            self.placePlayer()
        else:
            if self.level is 1:
                vec = self.characterNP.getPos() - LEVEL_2_POS
                if vec.length() < 3:
                    print "Compeleted level 1"
                    self.level = 2
                    self.completeLevelSound.play()
            else:
                vec = self.characterNP.getPos() - LEVEL_3_POS
                if vec.length() < 3:
                    print "Compeleted level 2"
        return task.cont

    def cameraPositionTask(self, task):
        base.camera.setX(self.characterNP, 0)
        base.camera.setY(self.characterNP, -10)
        base.camera.setZ(self.characterNP, self.cameraHeight)
        position = self.characterNP.getPos()
        position.setZ(position.getZ() + 2)
        base.camera.lookAt(position)
        return task.cont

    def type_1_enemy_attack_task(self, task):
        for index, enemy in enumerate(self.type_1_enemys):
            target = self.characterNP.getPos()
            target.setZ(enemy.getZ())
            enemy.lookAt(target)
            vec = self.characterNP.getPos() - enemy.getPos()
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

    def type_2_enemy_attack_task(self, task):
        if (task.time % 0.2) < 0.01:
            for index, enemy in enumerate(self.type_2_enemys):
                heading = enemy.getH()
                enemy.lookAt(self.characterNP.getPos())
                if abs(heading - enemy.getH()) > 0.1:
                    if not self.type_2_enemy_is_running[index]:
                        self.type_2_enemy_actors[index].loop('walk')
                    self.type_2_enemy_is_running[index] = True
                else:
                    if self.type_2_enemy_is_running[index]:
                        self.type_2_enemy_actors[index].stop()
                        self.type_2_enemy_actors[index].pose('walk', 0)
                        self.type_2_enemy_is_running[index] = False

        if (task.time % 2) < 0.01:
            # clean up old balls
            for ball in self.sphereNodes:
                ball.removeAllChildren()
                self.world.removeRigidBody(ball)
            # for every enemy
            for index, enemy in enumerate(self.type_2_enemys):
                target = self.characterNP.getPos()
                vec = self.characterNP.getPos() - enemy.getPos()
                distance = vec.length()
                if distance < TYPE_2_ENEMY_ATTACK_RAIUS:
                    self.type_2_enemy_actors[index].play('swing')
                    # throw new ball
                    pos = enemy.getPos()
                    shooting_direction = self.characterNP.getPos() - pos
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

    def inputProcessTask(self, task):
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
                self.character.setMaxJumpHeight(JUMP_HEIGHT * 2)
                self.character.setJumpSpeed(JUMP_SPEED * 2)
            else:
                self.character.setMaxJumpHeight(JUMP_HEIGHT)
                self.character.setJumpSpeed(JUMP_SPEED)
            self.character.doJump()
            self.jumpSound.play()
            self.inTheAir = True
            taskMgr.add(self.resetCharacterStatusTask,
                        "resetCharacterStatusTask")
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
                    self.actorNP.loop('run')
                    self.runningPose = True
            else:
                if self.runningPose:
                    self.actorNP.stop()
                    self.actorNP.pose("walk", 0)
                    self.runningPose = False

        if self.pushed:
            movingDirection.setY(TYPE_1_ENEMY_PUSH_DISTANCE)
            self.pushed = False
        self.character.setLinearMovement(movingDirection, True)
        self.character.setAngularMovement(turningAngle)
        return task.cont

myGame = GameBase()
myGame.run()
myGame.getLevel()
