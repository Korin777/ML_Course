class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # lanes center
        self.offset = 0
        self.precom = []
        self.lane_emp = [False,False,False,False,False,False,False,False,False]
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            speed_ahead1 = 100
            speed_ahead2 = 100
            self.lane_emp = [True,True,True,True,True,True,True,True,True]
            if self.car_pos[0] <= 36 and self.car_pos[0]!=0: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 564: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    self.lane_emp[car["pos"][0]//70] = False
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 150:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -75 and x <= -40 : #-40
                        if y > 80 and y < 250:
                            grid.add(3)
                            if y < 150:
                                speed_ahead2 = car["velocity"]
                                grid.add(11) 
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y <= 80 and y >= -80:
                            grid.add(6)
                    if x < 75 and x >= 40: #40
                        if y > 80 and y < 250:
                            grid.add(1)
                            if y < 150:
                                speed_ahead1 = car["velocity"]
                                grid.add(10) 
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y <= 80 and y >= -80:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead, speed_ahead1 = speed_ahead1, speed_ahead2 = speed_ahead2)
            
        def move(grid, speed_ahead,speed_ahead1,speed_ahead2): 
            # if self.player_no == 0:

            if len(grid) == 0:
                self.precom = ["SPEED"]
                return ["SPEED"]
            else:
                if ((("MOVE_LEFT" in self.precom) or ("MOVE_RIGHT" in self.precom)) and ((self.car_pos[0]) not in self.lanes)):
                    if (5 in grid) or (("MOVE_LEFT" in self.precom) and (10 in grid and speed_ahead1 <= self.car_vel)) or (("MOVE_RIGHT" in self.precom) and (11 in grid and speed_ahead2 <= self.car_vel)):
                        if "SPEED" in self.precom:
                            self.precom.remove("SPEED")
                        if "BRAKE" not in self.precom:
                            self.precom.append("BRAKE")
                    else:
                        if "BRAKE" in self.precom:
                            self.precom.remove("BRAKE")
                        if "SPEED" not in self.precom:
                            self.precom.append("SPEED")
                    self.precom = self.precom
                    return self.precom
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    # if self.car_pos[0] > self.lanes[self.car_lane]:
                    #     self.precom = ["SPEED", "MOVE_LEFT"]
                    #     return ["SPEED", "MOVE_LEFT"]
                    # elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                    #     self.precom = ["SPEED", "MOVE_RIGHT"]
                    #     return ["SPEED", "MOVE_RIGHT"]
                    # else :
                        self.precom = ["SPEED"]
                        return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        if (4 not in grid) and (7 not in grid) and speed_ahead1>speed_ahead: # turn left 
                            if self.car_vel < speed_ahead:
                                self.precom = ["SPEED", "MOVE_LEFT"]
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                self.precom = ["BRAKE", "MOVE_LEFT"]
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) and (9 not in grid) and speed_ahead2>speed_ahead: # turn right
                            if self.car_vel < speed_ahead:
                                self.precom = ["SPEED", "MOVE_RIGHT"]
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                self.precom = ["BRAKE", "MOVE_RIGHT"]
                                return ["BRAKE", "MOVE_RIGHT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                self.precom = ["SPEED"]
                                return ["SPEED"]
                            else:
                                self.precom = ["BRAKE"]
                                return ["BRAKE"]
                    # if (self.car_pos[0] < 60 ):
                    #     self.precom = ["SPEED", "MOVE_RIGHT"]
                        # return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        self.precom = ["SPEED", "MOVE_LEFT"]
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        self.precom = ["SPEED", "MOVE_RIGHT"]
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid): # turn left 
                        self.precom = ["SPEED", "MOVE_LEFT"]
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        self.precom = ["SPEED", "MOVE_RIGHT"]
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid)  and speed_ahead1>speed_ahead: # turn left 
                        self.precom = ["MOVE_LEFT"] 
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid)  and speed_ahead2>speed_ahead: # turn right
                        self.precom = ["MOVE_RIGHT"]
                        return ["MOVE_RIGHT"]
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]
            if(0 in self.lanes):
                for i in range(0,9):
                    if((self.car_pos[0]-(35+70*i))%3==0):
                        self.offset = (self.car_pos[0]-(35+70*i))//3
                    elif(abs((self.car_pos[0]-(35+70*i))%3)==1):
                        self.offset = (self.car_pos[0]-(35+70*i))//3
                    elif(abs((self.car_pos[0]-(35+70*i))%3)==2):
                        self.offset = (self.car_pos[0]-(35+70*i))//3 + 1          
                    self.lanes[i] = self.car_pos[0] - 3*self.offset
                print(self.lanes)

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass