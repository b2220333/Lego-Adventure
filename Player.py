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
        Character.__init__(self, world, render, name, animator, position, STANDING)

    def getNodePath(self):
        return self.nodePath

    def setPos(self, position):
        self.nodePath.setPos(position)

    def lookAt(self, position):
        self.nodePath.lookAt(position)

    def getHeight(self):
        return self.nodePath.getZ()

    def getPos(self):
        return self.nodePath.getPos()

    def getcontrollerNode(self):
        return self.controllerNode

    def getPose(self):
        return self.pose

    def setPose(self, pose):
        self.pose = pose
        self.animator.stop()
        if (self.pose == RUNNING):
            self.animator.loop('run')
        elif (self.pose == WALKING):
            self.animator.loop('run')

