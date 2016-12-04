


class FireBalls():
    def __init__(self, world, render, loader, shooterPosition, shootingDirection):
        self.render = render
        self.world = world
        self.loader = loader
        self.fireballs = []

    def fire(self, shooterPosition, shootingDirection):
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
        sphereBRBN.applyCentralForce(shooting_direction.normalize() * 1000)
        self.fireballs.append(sphereBRBN)

    def cleanUp(self):
        # TODO: rewrite clean up
        if self.fireballs.size > 100:
            self.fireballs.remove()