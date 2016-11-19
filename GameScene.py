from Guard import *
from Shield import *
from Player import *
from direct.actor.Actor import Actor
from panda3d.bullet import BulletWorld
from direct.showbase.ShowBase import ShowBase

class GameScene(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupScene()

    def setupScene(self):
        # Set Scene Background Color
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)

        # Create Physics World
        self.world = BulletWorld()



    def addPlayer(self):
        # TODO: remove test statements
        shield = Shield(self.world, self.render, "s1")
        guard = Guard(self.world, self.render, "g1")
        player = Player(self.world, self.render, "p1")