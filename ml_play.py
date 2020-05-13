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
    preblockx = 0
    blocker_v = 0
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
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_RIGHT"})
            ball_served = True
        if side == "1P":
            ml_loop_for_1P(ball_x, ball_y, scene_info,blocker_v)
            ball_x = scene_info["ball"][0]
            ball_y = scene_info["ball"][1]
        else:
            ml_loop_for_2P(ball_x, ball_y, scene_info,blocker_v)
            ball_x = scene_info["ball"][0]
            ball_y = scene_info["ball"][1]
        blocker_v = scene_info["blocker"][0] - preblockx
        preblockx = scene_info["blocker"][0]


def ml_loop_for_1P(ball_x, ball_y, scene_info, blocker_v):
    dropx = -1
    if(scene_info["ball_speed"][1] > 0):#球往下
        if(scene_info["ball"][1]<240 and scene_info["ball_speed"][1]!=0):#球往下，球在板子上面
            hitblockx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((240-scene_info["ball"][1])//scene_info["ball_speed"][1])
            hitblocky = scene_info["ball"][1] + scene_info["ball_speed"][1] * ((240-scene_info["ball"][1])//scene_info["ball_speed"][1])
            predictblockx = scene_info["blocker"][0] + blocker_v * ((240-scene_info["ball"][1])//scene_info["ball_speed"][1])
            ballspeed = scene_info["ball_speed"][0]
            hitedge = False
            while(hitblockx > 200 or hitblockx < 0):
                if(hitblockx > 195):
                    hitblockx = 195 - ((hitblockx-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                    ballspeed = -ballspeed
                if(hitblockx < 0):
                    hitblockx = -((hitblockx)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                    ballspeed = -ballspeed
            while(predictblockx > 200 or predictblockx < 0):
                if(predictblockx > 200):
                    predictblockx = 400 - predictblockx
                if(predictblockx < 0):
                    predictblockx = -predictblockx
            nexthitblockx = hitblockx + ballspeed
            nexthitblocky = hitblocky + scene_info["ball_speed"][1]
            nextpredictblockx = predictblockx + blocker_v
            if((nextpredictblockx+30 >= nexthitblockx) and (predictblockx+30<hitblockx)):
                # if(abs((nextpredictblockx+30-nexthitblockx)/scene_info["ball_speed"][0]) >= abs((nexthitblocky-240)/scene_info["ball_speed"][1])):
                #     #print("右邊反彈")
                #     hitedge = True
                x = nextpredictblockx + 30 - nexthitblockx#正的
                y = nexthitblocky - x * scene_info["ball_speed"][1]/abs(scene_info["ball_speed"][0])
                if(y <= 260):
                    hitedge = True
                    print("右邊反彈")
                #print(y)
            # if((nextpredictblockx <= nexthitblockx+5) and (predictblockx > hitblockx+5)):
            #     if(abs((nextpredictblockx-(nexthitblockx+5))/scene_info["ball_speed"][0]) >= abs((nexthitblocky-240)/scene_info["ball_speed"][1])):
            #         #print("左邊反彈")
            #         hitedge = True
                x = nexthitblockx + 5 - nextpredictblockx#正的
                y = nexthitblocky - x * scene_info["ball_speed"][1]/abs(scene_info["ball_speed"][0])
                if(y <= 260):
                    hitedge = True
                    print("左邊反彈")
            i = 1
            while(nexthitblocky<260 and (not hitedge)):
                nexthitblockx = nexthitblockx + ballspeed
                nexthitblocky = nexthitblocky + scene_info["ball_speed"][1]
                nextpredictblockx = nextpredictblockx + blocker_v
                i = i + 1
                if((nextpredictblockx+30 >= nexthitblockx) and (predictblockx+30<hitblockx)):
                    # if(abs((nextpredictblockx+30-nexthitblockx)/scene_info["ball_speed"][0]) >= abs((nexthitblocky-240)/scene_info["ball_speed"][1]/i)):
                    #     #print("迴圈右邊反彈")
                    #     hitedge = True
                    #     break
                    x = nextpredictblockx + 30 - nexthitblockx#正的
                    y = nexthitblocky - x * scene_info["ball_speed"][1]/abs(scene_info["ball_speed"][0])
                    if(y <= 260):
                        hitedge = True
                        print("右邊反彈")
                        break
                if((nextpredictblockx <= nexthitblockx+5) and (predictblockx > hitblockx+5)):
                    # if(abs((nextpredictblockx-(nexthitblockx+5))/scene_info["ball_speed"][0]) >= abs((nexthitblocky-240)/scene_info["ball_speed"][1]/i)):
                    #     #print("迴圈左邊反彈")
                    #     hitedge = True
                    #     break
                    x = nexthitblockx + 5 - nextpredictblockx#正的
                    y = nexthitblocky - x * scene_info["ball_speed"][1]/abs(scene_info["ball_speed"][0])
                    if(y <= 260):
                        hitedge = True
                        print("左邊反彈")
                        break
            #print(hitblockx,hitblocky,predictblockx,nexthitblockx,nexthitblocky,nextpredictblockx)
            #print(nexthitblockx,nexthitblocky)
            if(hitedge):
                if((420-nexthitblocky - scene_info["ball_speed"][1])%scene_info["ball_speed"][1] == 0):
                    dropx = nexthitblockx - ballspeed + -ballspeed * ((420-nexthitblocky - scene_info["ball_speed"][1])//scene_info["ball_speed"][1])
                else:
                    dropx = nexthitblockx - ballspeed + -ballspeed * ((420-nexthitblocky - scene_info["ball_speed"][1])//scene_info["ball_speed"][1])
                print("edge predict")
            else:
                if((415-scene_info["ball"][1])%scene_info["ball_speed"][1] == 0):
                    dropx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((415-scene_info["ball"][1])//scene_info["ball_speed"][1])
                else:
                    dropx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((415-scene_info["ball"][1])//scene_info["ball_speed"][1] + 1)
            while(dropx > 200 or dropx < 0):
                if(dropx > 195):
                    dropx = 195 - ((dropx-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(dropx < 0):
                    dropx = -((dropx)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
            if(abs(dropx-scene_info["platform_1P"][0]-15) < 5.5):
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif(dropx > scene_info["platform_1P"][0]+15):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
        else:#球往下，球在板子下面
            if((415-scene_info["ball"][1])%scene_info["ball_speed"][1] == 0):
                dropx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((415-scene_info["ball"][1])//scene_info["ball_speed"][1])
            else:
                dropx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((415-scene_info["ball"][1])//scene_info["ball_speed"][1] + 1)
            while(dropx > 200 or dropx < 0):
                if(dropx > 195):
                    dropx = 195 - ((dropx-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(dropx < 0):
                    dropx = -((dropx)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
            if(abs(dropx-scene_info["platform_1P"][0]-15) < 5.5):
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif(dropx > scene_info["platform_1P"][0]+15):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
    else:#球往上
        if(scene_info["ball"][1]>260 and scene_info["ball_speed"][1]!=0):#球在板子下,球往上看球會不會反彈
            hitblockx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((260-scene_info["ball"][1])//scene_info["ball_speed"][1]+1)#球到板子位置時球會在哪
            hitblocky = scene_info["ball"][1] + scene_info["ball_speed"][1] * ((260-scene_info["ball"][1])//scene_info["ball_speed"][1])
            while(hitblockx > 200 or hitblockx < 0):
                if(hitblockx > 195):
                    hitblockx = 195 - ((hitblockx-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(hitblockx < 0):
                    hitblockx = -((hitblockx)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
            hitblockx2 = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((260-scene_info["ball"][1])//scene_info["ball_speed"][1])#球到板子位置時球會在哪
            while(hitblockx2 > 200 or hitblockx2 < 0):
                if(hitblockx2 > 195):
                    hitblockx2 = 195 - ((hitblockx2-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(hitblockx2 < 0):
                    hitblockx2 = -((hitblockx2)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
            predictblockx = scene_info["blocker"][0] + blocker_v * ((260-scene_info["ball"][1])//scene_info["ball_speed"][1] + 1)#球到板子位置時板子會在哪
            while(predictblockx > 200 or predictblockx < 0):
                if(predictblockx > 195):
                    predictblockx = 195 - ((predictblockx-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(predictblockx < 0):
                    predictblockx = -((predictblockx)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
            predictblockx2 = scene_info["blocker"][0] + blocker_v * ((260-scene_info["ball"][1])//scene_info["ball_speed"][1])#球到板子位置時板子會在哪
            while(predictblockx2 > 200 or predictblockx2 < 0):
                if(predictblockx2 > 195):
                    predictblockx2 = 195 - ((predictblockx2-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(predictblockx2 < 0):
                    predictblockx2 = -((predictblockx2)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]   
            #print(hitblockx,hitblockx2,predictblockx,predictblockx2)     
            if((hitblockx - predictblockx <= 30 and hitblockx - predictblockx >= -2.5) or (hitblockx2 - predictblockx2 <= 30 and hitblockx2 - predictblockx2 >= -2.5)):#球在板子下，球會反彈
                dropx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((260-scene_info["ball"][1])//scene_info["ball_speed"][1]) + scene_info["ball_speed"][0] * ((260-420)//scene_info["ball_speed"][1])
                while(dropx > 200 or dropx < 0):
                    if(dropx > 195):
                        dropx = 195 - ((dropx-195)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                    if(dropx < 0):
                        dropx = -((dropx)//scene_info["ball_speed"][0]) * scene_info["ball_speed"][0]
                if(abs(dropx-scene_info["platform_1P"][0]-15) < 5.5):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
                elif(dropx > scene_info["platform_1P"][0]+15):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                print("反彈") 
            else:#球在板子下,球往上不會反彈
                if(85 < scene_info["platform_1P"][0]):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                elif(75 > scene_info["platform_1P"][0]):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
        else:#球在板子上,球往上不會反彈
            if(85 < scene_info["platform_1P"][0]):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            elif(75 > scene_info["platform_1P"][0]):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
    if(scene_info["ball"][1] == 415):
        print(scene_info["ball"])
    if(dropx != -1):
        print(dropx)
    print(scene_info["ball"],scene_info["platform_1P"],scene_info["blocker"])



def ml_loop_for_2P(ball_x, ball_y, scene_info, blocker_v):#球往上
    if(scene_info["ball_speed"][1] < 0):
        dropx = scene_info["ball"][0] + scene_info["ball_speed"][0] * ((80-scene_info["ball"][1])//scene_info["ball_speed"][1])
        while(dropx > 200 or dropx < 0):
            if(dropx > 200):
                dropx = 400 - dropx
            if(dropx < 0):
                dropx = -dropx
        if(abs(dropx-scene_info["platform_2P"][0]-12.5) < 5.5):
            comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
        elif(dropx > scene_info["platform_2P"][0]+12.5):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        else:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
    else:
        if(ball_y<240 and scene_info["ball_speed"][1]!=0):
            hitblockx = ball_x + scene_info["ball_speed"][0] * (240-ball_y)/scene_info["ball_speed"][1]#球到板子位置時球會在哪
            while(hitblockx > 200 or hitblockx < 0):
                if(hitblockx > 200):
                    hitblockx = 400 - hitblockx
                if(hitblockx < 0):
                    hitblockx = -hitblockx
            predictblockx = scene_info["blocker"][0] + blocker_v * (240-ball_y)/scene_info["ball_speed"][1]#球到板子位置時板子會在哪
            while(predictblockx > 200 or predictblockx < 0):
                if(predictblockx > 200):
                    predictblockx = 400 - predictblockx
                if(predictblockx < 0):
                    predictblockx = -predictblockx            
            #print(hitblockx,predictblockx,ball_x,scene_info["blocker"][0])
            if(hitblockx - predictblockx < 30 and hitblockx - predictblockx > 0):
                dropx = ball_x + 2 * scene_info["ball_speed"][0] * (240-ball_y)/scene_info["ball_speed"][1]
                while(dropx > 200 or dropx < 0):
                    if(dropx > 200):
                        dropx = 400 - dropx
                    if(dropx < 0):
                        dropx = -dropx
                #print("反彈",dropx)
                if(dropx > scene_info["platform_2P"][0]+20):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            else:
                if(85 < scene_info["platform_2P"][0]):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                elif(75 > scene_info["platform_2P"][0]):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
        else:
            if(85 < scene_info["platform_2P"][0]):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            elif(75 > scene_info["platform_2P"][0]):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})