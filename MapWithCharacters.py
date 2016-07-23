from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from GameMap import GameMap
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import *
from Settings import *


class MapWithCharacters(GameMap):
    def __init__(self):
        GameMap.__init__(self)
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
        self.addSounds()

    def setupCharacters(self):
        self.addPlayer()
        self.addEnemys()

    def addPlayer(self):
        shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player-1')
        self.character.setIntoCollideMask(BitMask32.allOn())
        self.characterNP = self.render.attachNewNode(self.character)
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)
        self.actorNP = Actor('models/Actors/lego/Bricker/Bricker3.egg',
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
        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.3048)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, 0.4)
        self.runningPose = False

    def addEnemys(self):
        def addEnemy(type, pos):
            shape = BulletBoxShape(Vec3(0.3, 0.2, 0.7))
            enemyNode = BulletCharacterControllerNode(
                shape, 0.4, 'Type_{}_Enemy{}'.format(type, len(self.type_1_enemys)))
            self.world.attachCharacter(enemyNode)
            enemyNode.setIntoCollideMask(BitMask32.allOn())
            enemyNP = self.render.attachNewNode(enemyNode)
            enemyNP.setCollideMask(BitMask32.allOn())
            enemyNP.setPos(pos)
            if type is 1:
                self.type_1_enemys.append(enemyNP)
                actor = Actor('models/Actors/lego/Shield/Shield.egg',
                              {
                                  'FallbackGetup': 'models/Actors/lego/Shield/Shield-FallbackGetup.egg',
                                  'FallforwardGetup': 'models/Actors/lego/Shield/Shield-FallforwardGetup.egg',
                                  'jump': 'models/Actors/lego/Shield/Shield-jump.egg',
                                  'punch': 'models/Actors/lego/Shield/Shield-punch.egg',
                                  'walk': 'models/Actors/lego/Shield/Shield-walk.egg'
                              })
                self.type_1_enemy_actors.append(actor)
                self.type_1_enemy_is_running.append(False)
                self.type_1_enemy_is_attacking_pose.append(False)
            else:
                self.type_2_enemys.append(enemyNP)
                actor = Actor('models/Actors/lego/SecurityGuard/SecurityGuard.egg',
                              {
                                  'fallbackGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallbackGetup.egg',
                                  'fallforwardGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallforwardGetup.egg',
                                  'firegun': 'models/Actors/lego/SecurityGuard/SecurityGuard-firegun.egg',
                                  'jump': 'models/Actors/lego/SecurityGuard/SecurityGuard-jump.egg',
                                  'run': 'models/Actors/lego/SecurityGuard/SecurityGuard-run.egg',
                                  'swing': 'models/Actors/lego/SecurityGuard/SecurityGuard-swing.egg',
                                  'walk': 'models/Actors/lego/SecurityGuard/SecurityGuard-walk.egg'
                              })
                self.type_2_enemy_actors.append(actor)
                self.type_2_enemy_is_running.append(False)
                self.type_2_enemy_is_attacking_pose.append(False)
            actor.reparentTo(enemyNP)
            actor.setScale(0.3048)
            actor.setH(180)
            actor.setPos(0, 0, 0.4)

        for pos in TYPE_1_ENEMY_POS_LIST:
            addEnemy(1, pos)
        for pos in TYPE_2_ENEMY_POS_LIST:
            addEnemy(2, pos)

    def addSounds(self):
        # http://www.2gei.com/sound/
        self.completeLevelSound = base.loader.loadSfx(
            "sounds/completeLevel.mp3")
        self.deadthSound = base.loader.loadSfx("sounds/dead.wav")
        # self.completeLevelSound.setVolume(5)
        # self.completeLevelSound.play()
        self.hitSound = base.loader.loadSfx("sounds/hit.mp3")
        self.pushSound = base.loader.loadSfx("sounds/push.wav")
        self.jumpSound = base.loader.loadSfx("sounds/Jump.wav")
        self.pickupSpringSound = base.loader.loadSfx(
            "sounds/Pickup_Spring.wav")
        self.backgroundSound = base.loader.loadSfx("sounds/background.mp3")
        self.backgroundSound.setVolume(0.5)
        self.backgroundSound.setLoop(True)
        self.backgroundSound.play()