from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSphereShape
from Settings import GUARD_FIREBALL_LIMITE

class FireBalls():
    def __init__(self, world, render, loader):
        self.render = render
        self.world = world
        self.loader = loader
        self.fireballs = []

    def fire(self, shooterPosition, targetPosition):
        print("fire balls")
        # create bullet rigid body node
        sphereBRBN = BulletRigidBodyNode('Ball')
        # set physics properties
        sphereBRBN.setMass(1.0)
        sphereBRBN.addShape(BulletSphereShape(0.2))
        # attach to render and get a nodePath in render hierarchic
        sphere = self.render.attachNewNode(sphereBRBN)

        # set starting position of fire ball
        pos = shooterPosition
        pos.setZ(pos.getZ() + 1)
        sphere.setPos(pos)
        # load texture of fireball and set size then add to nodePath
        smileyFace = self.loader.loadModel("models/smiley")
        smileyFace.setScale(0.2)
        smileyFace.reparentTo(sphere)

        # add rigid body to physics world
        self.world.attachRigidBody(sphereBRBN)
        # apply the force so it moves
        shootingDirection = targetPosition - pos
        shootingDirection.normalize()
        sphereBRBN.applyCentralForce(shootingDirection * 1000)
        self.fireballs.append(sphereBRBN)
        self.cleanUp()

    def getFireballsList(self):
        return self.fireballs

    def cleanUp(self):
        if len(self.fireballs) > GUARD_FIREBALL_LIMITE:
            ball = self.fireballs[0]
            ball.removeAllChildren()
            self.world.removeRigidBody(ball)
            self.fireballs.remove(ball)