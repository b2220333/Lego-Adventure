# Import packages from panda3d to save 3d vectors
from panda3d.core import Vec3

# Constants
DEFAULT_ANIMATOR_HEIGHT = 180
DEFAULT_ANIMATOR_SCALE  = 0.3048
DEFAULT_NODEPATH_HEIGHT = 45
DEFAULT_ANIMATOR_OFFSET = Vec3(0, 0, 0.4)
DEFAULT_CAMERA_HEIGHT   = 3.5
ATTACKING = 0
RUNNING   = 1
STANDING  = 2
WALKING   = 3
JUMPING   = 4

PLAYER_FALLING_POSE_TIME = 1.2
HEALTH_LIMIT = 500
TIME_LIMIT = 90
JUMP_HEIGHT = 8
JUMP_SPEED = 10
PLAYER_SPEED = 3
BOOST_TIME = 10

GUARD_ATTACKING_RADIUS =  20
GUARD_MAX_DISTANCE_FROM_HOME = 5
GUARD_MOVING_SPEED  = 1
GUARD_SHOOTING_TIME_INTERVAL = 0.8
GUARD_FIREBALL_LIMITE = 5
SHIELD_ATTACKING_RADIUS  = 8
SHIELD_MAX_DISTANCE_FROM_HOME = 3
SHIELD_MOVING_SPEED = 0.75
SHIELD_PUSHING_DISTANCE = 0.8
SHILED_PUSHING_POWER = 20

PLAYER_POSITIONS = [Vec3(0, 0, 0),
                    Vec3(-65, -65, 10),
                    Vec3(-6, -9, 16.5),
                    Vec3(73.5, -43.0, 46.8)]

SHIELD_POSITIONS = [Vec3(-20.4551, -32.5579, 12),
                    Vec3(-0.269259, 2.59712, 16.36),
                    Vec3(29.4766, 42.2148, 19.86),
                    Vec3(39.9572, 71.1687, 21)]

GUARD_POSITIONS = [Vec3(-16.296, -54.2117, 11),
                   Vec3(-11.2137, -5.56247, 15),
                   Vec3(16.9461, 31.4267, 19),
                   Vec3(34.8673, 41.6622, 21),
                   Vec3(34.7589, 51.4396, 20.86),
                   Vec3(56.4356, 59.0785, 22),
                   Vec3(72, 0, 30),
                   Vec3(72, -10, 34),
                   Vec3(72, -20, 38),
                   Vec3(72, -30, 42),
                   Vec3(72, -40, 46),
                   Vec3(72, -80, 50),
                   Vec3(61.7531, 80.0794, 23)]

# Positions of Collectable on the map
SPRING_LIST = [Vec3(-12, -25, 12.5),
               Vec3(5, 10, 17),
               Vec3(40, 62, 20)]

# Positions of Platform on the map
STAGE_POS_LIST = [(Vec3(15, 15, 0.2), Vec3(-63, -63, 9), "stage1"),
                  (Vec3(15, 5, 0.2), Vec3(-29, -50, 10), "stage2"),
                  (Vec3(3, 15, 0.2), Vec3(-20, -25, 11), "stage3"),
                  (Vec3(3, 7, 0.2), Vec3(-12, -25, 12.5), "stage4"),
                  (Vec3(7, 7, 0.2), Vec3(-10, -10, 14), "stage5"),
                  (Vec3(2, 15, 0.2), Vec3(-0, 10, 15.5), "stage6"),
                  (Vec3(2, 2, 0.2), Vec3(8.5, 10, 17), "stage7"),
                  (Vec3(1.0, 12, 0.2), Vec3(17, 22, 18), "stage8"),
                  (Vec3(1.0, 1.0, 0.2), Vec3(23, 28, 18.5), "stage9"),
                  (Vec3(0.85, 12, 0.2), Vec3(29, 41, 19), "stage10"),
                  (Vec3(0.85, 12, 0.2), Vec3(35, 51, 20), "stage11"),
                  (Vec3(0.7, 12, 0.2), Vec3(40, 62, 20), "stage12"),
                  (Vec3(0.7, 12, 0.2), Vec3(45, 70, 20), "stage13"),
                  (Vec3(0.55, 12, 0.2), Vec3(49, 75, 21), "stage14"),
                  (Vec3(5.5, 12, 0.2), Vec3(60, 70, 21), "stage15"),
                  (Vec3(1.40, 12, 0.2), Vec3(64, 75, 23), "stage16"),
                  (Vec3(0.40, 12, 0.2), Vec3(68, 80, 26), "stage17"),
                  (Vec3(3.40, 80, 0.2), Vec3(72, 80, 28.5), "stage18"),
                  (Vec3(5, 5, 0.2), Vec3(72, 0, 30), "stage19"),
                  (Vec3(5, 5, 0.2), Vec3(72, -10, 34), "stage20"),
                  (Vec3(5, 5, 0.2), Vec3(72, -20, 38), "stage21"),
                  (Vec3(5, 5, 0.2), Vec3(72, -30, 42), "stage22"),
                  (Vec3(5, 5, 0.2), Vec3(72, -40, 46), "stage23"),
                  (Vec3(5, 5, 0.2), Vec3(72, -80, 50), "stage24")]
# OLD Settings

# # Behavior Settings
# ENEMY_TURNING_RADIUS = 0.75
# LEVEL_1_POS = Vec3(-65, -65, 10)
# LEVEL_2_POS = Vec3(-6, -9, 16.5)
# LEVEL_3_POS = Vec3(73.5, -43.0, 46.8)
# TYPE_1_ENEMY_ATTACK_DISTANCE = 1
# TYPE_1_ENEMY_ATTACK_RAIUS = 7
# TYPE_1_ENEMY_MOVING_SPEED = 0.3
# TYPE_1_ENEMY_PUSH_DISTANCE = -1
# TYPE_2_ENEMY_ATTACK_RAIUS = 20


# # TODO: Remove this
# # Positions of Type 1 Enemy on the map
# TYPE_1_ENEMY_POS_LIST = [Vec3(-20.4551, -32.5579, 12),
#                          Vec3(-0.269259, 2.59712, 16.36),
#                          Vec3(29.4766, 42.2148, 19.86),
#                          Vec3(39.9572, 71.1687, 21)]

# # Positions of Type 2 Enemy on the map
# TYPE_2_ENEMY_POS_LIST = [Vec3(-16.296, -54.2117, 11),
#                          Vec3(-11.2137, -5.56247, 15),
#                          Vec3(16.9461, 31.4267, 19),
#                          Vec3(34.8673, 41.6622, 21),
#                          Vec3(34.7589, 51.4396, 20.86),
#                          Vec3(56.4356, 59.0785, 22),
#                          Vec3(72, 0, 30),
#                          Vec3(72, -10, 34),
#                          Vec3(72, -20, 38),
#                          Vec3(72, -30, 42),
#                          Vec3(72, -40, 46),
#                          Vec3(72, -80, 50),
#                          Vec3(61.7531, 80.0794, 23)]

