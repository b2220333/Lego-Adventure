from Character import *
from direct.actor.Actor import Actor
from Settings import *

# Members:
#   controllerNode
#   nodePath
#   animator
#   pose
class Player(Character):
    def __init__(self, world, render, name, position):
        animator = Actor('models/Actors/lego/Bricker/Bricker3.egg',
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
        animator.setPlayRate(0.5, 'jump')
        Character.__init__(self, world, render, name, animator, position, STANDING)

    def getNodePath(self):
        return self.nodePath

    def setPosition(self, position):
        self.nodePath.setPos(position)

    def lookAt(self, position):
        self.nodePath.lookAt(position)

    def getHeight(self):
        # print("Height: ", self.nodePath.getZ())
        # return self.nodePath.getZ()
        return 10

    def getPos(self):
        return self.nodePath.getPos()

    def getcontrollerNode(self):
        return self.controllerNode

    def getPose(self):
        return self.pose

    def setPose(self, pose):
        # print("Pose:" + str(self.animator.getCurrentAnim()))
        if self.animator.getCurrentAnim() != 'jump':
            if pose == JUMPING:
                self.animator.stop()
                self.animator.play('jump')
                print("Jump")
                self.pose = JUMPING
            else:
                if self.pose != pose:
                    self.pose = pose
                    self.animator.stop()
                    if (self.pose == RUNNING):
                        self.animator.loop('run')
                        print("Run")
                    elif (self.pose == WALKING):
                        self.animator.loop('run')
                        print("Walking")
                    elif (self.pose == STANDING):
                        self.animator.pose('walk', 0)
                        print("Standing")