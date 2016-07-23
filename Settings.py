from panda3d.core import Vec3
TIME_LIMIT = 60
BOOSTED = False
JUMP_HEIGHT = 8
JUMP_SPEED = 10
LEVEL_1_POS = Vec3(-65, -65, 10)
LEVEL_2_POS = Vec3(-6, -9, 16.5)
LEVEL_3_POS = Vec3(-70, 70, 25)
MOVING_SPEED = 3
ATTACK_RAIUS = 7
PUSHING_RADIUS = 0.5
ENEMY_TURNING_RADIUS = 0.75
ENEMY_MOVING_SPEED = 1
TYPE_1_ENEMY_ATTACK_DISTANCE = 1
TYPE_1_ENEMY_PUSH_DISTANCE = -0.3
PLAYER_SPEED = 1
BOOST_TIME = 10

TYPE_1_ENEMY_POS_LIST = [Vec3(-20.67, -36.52, 11.86),
                         Vec3(-0.269259, 2.59712, 16.36)]

SPRING_LIST = [Vec3(-12, -25, 12.5),
               Vec3(5, 10, 17),
               Vec3(40, 62, 20)]

# boxSize, pos, name
STAGE_POS_LIST = [(Vec3(15, 15, 0.2), Vec3(-63, -63, 9), "stage1"),
                  (Vec3(15, 5, 0.2), Vec3(-29, -50, 10), "stage2"),
                  (Vec3(3, 15, 0.2), Vec3(-20, -25, 11), "stage3"),
                  (Vec3(3, 7, 0.2), Vec3(-12, -25, 12.5), "stage4"),
                  (Vec3(7, 7, 0.2), Vec3(-10, -10, 14), "stage5"),
                  (Vec3(2, 15, 0.2), Vec3(-0, 10, 15.5), "stage6"),
                  (Vec3(2, 2, 0.2), Vec3(5, 10, 17), "stage7"),
                  (Vec3(1.0, 12, 0.2), Vec3(17, 22, 18), "stage8"),
                  (Vec3(0.85, 12, 0.2), Vec3(29, 41, 19), "stage9"),
                  (Vec3(0.7, 12, 0.2), Vec3(40, 62, 20), "stage10"),
                  (Vec3(0.55, 12, 0.2), Vec3(52, 80, 21), "stage11"),
                  (Vec3(0.40, 12, 0.2), Vec3(62, 80, 22), "stage12"),
                  (Vec3(0.40, 80, 0.2), Vec3(72, 00, 23), "stage13"),
                  (Vec3(0.40, 100, 0.2), Vec3(0, 0, 24), "stage14")]
