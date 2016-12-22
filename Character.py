# Panda3d Library
from direct.actor.Actor import Actor
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import *
# My Game Classes
from Settings import *
# Members:
#   controllerNode
#   nodePath
#   animator
#   pose

class Character():
    def __init__(self, world, render, name, animator, position, pose):
        # Create a box shape
        shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
        # Create a Controller Node with the shape
        self.controllerNode = BulletCharacterControllerNode(shape, 0.4, name)
        self.controllerNode.setIntoCollideMask(BitMask32.allOn())
        # Attach the Controller Node to the world
        world.attachCharacter(self.controllerNode)

        # Attach Controller Node to the render and get a NodePath
        self.nodePath = render.attachNewNode(self.controllerNode)
        # Setup the nodePath
        self.nodePath.setCollideMask(BitMask32.allOn())
        self.nodePath.setH(DEFAULT_NODEPATH_HEIGHT)
        self.nodePath.setPos(position)

        # Set the actor of the Character
        self.animator = animator

        # Add animator to NodePath so it can be rendered
        self.animator.reparentTo(self.nodePath)
        # Configure the animator
        self.animator.setScale(DEFAULT_ANIMATOR_SCALE)
        self.animator.setH(DEFAULT_ANIMATOR_HEIGHT)
        self.animator.setPos(DEFAULT_ANIMATOR_OFFSET)

        # Set Current Character Pose
        self.pose = pose

        # Save home position
        self.home = position

    # ==========    Character Controls
    def lookAt(self, position):
        position.setZ(self.getPosition().getZ())
        self.nodePath.lookAt(position)

    def movement(self, vector):
        self.controllerNode.setLinearMovement(vector, True)

    # ==========    Getters
    def getNodePath(self):
        return self.nodePath

    def getHeight(self):
        return self.nodePath.getZ()

    def getPosition(self):
        return self.nodePath.getPos()

    def getPose(self):
        return self.pose

    def getControllerNode(self):
        return self.controllerNode

    def getCurrentPoseName(self):
        return self.getCurrentAnim()

    def getHomePosition(self):
        return self.home

    # ==========    Setters
    def setPosition(self, position):
        self.nodePath.setPos(position)

    def setPose(self, pose):
        if self.animator.getCurrentAnim() != 'jump':
            if pose == JUMPING:
                self.animator.stop()
                self.animator.play('jump')
                self.pose = JUMPING
            else:
                if self.pose != pose:
                    self.pose = pose
                    self.animator.stop()
                    if (self.pose == RUNNING):
                        self.animator.loop('run')
                    elif (self.pose == WALKING):
                        self.animator.loop('run')
                    elif (self.pose == STANDING):
                        self.animator.pose('walk', 0)
                    elif (self.pose == ATTACKING):
                        self.animator.loop('attack')
                        self.pose == STANDING

    # ==========    Boolean Functions
    def isWalking(self):
        animate = self.animator.getCurrentAnim()
        return animate == 'walk' or animate == 'run'

    def isAttacking(self):
        animate = self.animator.getCurrentAnim()
        return animate == 'attack'

    def goBackHome(self):
        return
        # print("TODO: Go back to self.position")