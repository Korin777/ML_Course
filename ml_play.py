"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    ball_x = 93
    ball_y = 415
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if side == "1P":
            ml_loop_for_1P(ball_x, ball_y, scene_info)
            ball_x = scene_info["ball"][0]
            ball_y = scene_info["ball"][1]

        else:
            ml_loop_for_2P(ball_x, ball_y, scene_info)
            ball_x = scene_info["ball"][0]
            ball_y = scene_info["ball"][1]


def ml_loop_for_1P(ball_x, ball_y, scene_info):
    if(scene_info["ball_speed"][1] > 0):
        dropx = ball_x + scene_info["ball_speed"][0] * (420-ball_y)/scene_info["ball_speed"][1]
        while(dropx > 200 or dropx < 0):
            if(dropx > 200):
                dropx = 400 - dropx
            if(dropx < 0):
                dropx = -dropx
        print(dropx)
        if(dropx > scene_info["platform_1P"][0]+20):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        else:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})



def ml_loop_for_2P(ball_x, ball_y, scene_info):
    if(scene_info["ball_speed"][1] < 0):
        dropx = ball_x + scene_info["ball_speed"][0] * (80-ball_y)/scene_info["ball_speed"][1]
        while(dropx > 200 or dropx < 0):
            if(dropx > 200):
                dropx = 400 - dropx
            if(dropx < 0):
                dropx = -dropx
        print(dropx)
        if(dropx > scene_info["platform_2P"][0]+20):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        else:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})