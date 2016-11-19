from direct.actor.Actor import Actor
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import *
from Settings import *

class Character():
    def __init__(self, world, render, name, animator, pose):
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
