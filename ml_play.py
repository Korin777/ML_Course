"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False #有沒有發球
    ball_x = 93
    ball_y = 93
    preball_y = 93

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready() #保留

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False


            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            preball_x = ball_x
            if preball_y > ball_y :
                up = True
            else :
                up = False
            preball_y = ball_y
            ball_x = scene_info.ball[0] + 2.5
            if preball_x > ball_x :
                left = True
            else :
                left = False
            ball_y = scene_info.ball[1] + 2.5
            platform_x = scene_info.platform[0] + 20
            if up :
                if platform_x == 95 :
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                elif platform_x > 95 :
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                else :
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else :
                    if left :
                        if ball_x - (397.5 - ball_y) < 0 :
                            drop_x = -(ball_x - (397.5 - ball_y))
                        else :
                            drop_x = ball_x - (397.5 - ball_y)
                    else :
                        if ball_x + (397.5 - ball_y) > 200 :
                            drop_x = 400 - (ball_x + (397.5 - ball_y))
                        else :
                            drop_x = ball_x + (397.5 - ball_y)
                    if platform_x > drop_x + 3.5 :
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_x < drop_x  - 3.5:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    else :
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE)              
            # else :
            #     if platform_x > ball_x :
            #         comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            #     elif platform_x < ball_x :
            #         comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            #     else :
            #         comm.send_instruction(scene_info.frame, PlatformAction.NONE) 

                