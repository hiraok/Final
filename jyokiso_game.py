import pyxel
import math
import random

class Player():
    def __init__(self):
        self.x=100
        self.y=240
        self.dead = False
        self.clear = False
        self.angle_to_enemy = None
    def movement(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -=1.5
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x +=1.5
        if pyxel.btn(pyxel.KEY_UP):
            self.y -=1.5
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y +=1.5

    def enemy_hit(self,enemy):
        self.distance = math.sqrt((abs(self.x - enemy.enemy_x))**2 + (abs(self.y - enemy.enemy_y))**2)
        self.angle_to_enemy = math.atan2(enemy.enemy_y - self.y,self.x - enemy.enemy_x)
        if self.angle_to_enemy < 0:
            self.angle_to_enemy = math.pi*2 + self.angle_to_enemy

        if self.distance <= enemy.view_radius and self.angle_to_enemy > enemy.tmp_angle - enemy.view_width_half and self.angle_to_enemy< enemy.tmp_angle + enemy.view_width_half:

            self.dead = True

    def wall_collision(self,wall):
        if wall.wall_x + wall.wall_width -5 <= self.x <= wall.wall_x + wall.wall_width                      and self.y >= wall.wall_y and self.y <= wall.wall_y + wall.wall_height:
            return 'Left'
        if wall.wall_x <= (self.x + 10) <= wall.wall_x +5                                                         and self.y >= wall.wall_y and self.y <= wall.wall_y + wall.wall_height:
            return 'Right'
        if wall.wall_y <= (self.y + 10)<= wall.wall_y + 5                                                          and self.x >= wall.wall_x and self.x <= wall.wall_x + wall.wall_width:
            return 'Up'
        if wall.wall_y + wall.wall_height - 5 <= self.y <= wall.wall_y + wall.wall_height                     and self.x >= wall.wall_x and self.x <= wall.wall_x + wall.wall_width:
            return 'Down'
        
    def edge_stop(self):
        if self.x <= 0:
            self.x =0
        if self.x >= 190:
            self.x = 190
        if self.y <= 0:
            self.y =0
        if self.y >= 190:
            self.y = 190



class Wall():
    def __init__(self,x,y,w,h):
        self.wall_x = x
        self.wall_y = y
        self.wall_width = w
        self.wall_height = h

class Enemy():
    def __init__(self,x,y):
        self.view_radius=35
        #初期値　角度
        self.view_angle= math.radians(random.randint(0,7)*45)
        self.view_width_half = math.radians(45/2)

        self.start_point_x=self.view_radius * math.cos(self.view_angle - self.view_width_half)
        self.start_point_y=self.view_radius * math.sin(self.view_angle - self.view_width_half)

        self.end_point_x=self.view_radius * math.cos(self.view_angle + self.view_width_half)
        self.end_point_y=self.view_radius * math.sin(self.view_angle + self.view_width_half)

        self.enemy_x=x
        self.enemy_y=y

        self.enemy_x_direction=math.cos(self.view_angle)
        self.enemy_y_direction=-math.sin(self.view_angle)

        self.enemy_move_size=0.5

        self.start_frame = 0
        self.move_duration = 0

        self.tmp_angle = self.view_angle

        self.turn_direction = 1

        self.stop_time = 0

        self.tmp_frame = 0

        self.reflection_turning = False

        self.wall_side = None 


    def movement(self,Wall_hit = None):
        if self.enemy_x <= 0 or self.enemy_x >= 200 or self.enemy_y <= 0 or self.enemy_y >= 200 or Wall_hit != None:
            if Wall_hit != None:
                self.wall_side = Wall_hit

            self.reflection()

        elif pyxel.frame_count - self.start_frame >= self.move_duration and pyxel.frame_count > 120:

            self.start_frame = pyxel.frame_count

            self.tmp_angle = self.view_angle

            self.view_angle = math.radians(random.randint(0,7)*45)

            if (self.view_angle - self.tmp_angle) >= 0 and (self.view_angle - self.tmp_angle) <= math.pi:
                self.turn_direction = 1
            elif(self.view_angle - self.tmp_angle) >= 0 and (self.view_angle - self.tmp_angle) > math.pi:
                self.turn_direction = -1
            elif(self.view_angle - self.tmp_angle) < 0 and abs(self.view_angle - self.tmp_angle) <= math.pi:
                self.turn_direction = -1
            else:
                self.turn_direction = 1

            self.stop_time=min(abs(self.tmp_angle - self.view_angle),2*math.pi-abs(self.tmp_angle - self.view_angle))/(math.pi/90)

            self.enemy_x_direction=math.cos(self.view_angle)
            self.enemy_y_direction=-math.sin(self.view_angle)

            self.move_duration = random.randint(60,90) + self.stop_time

        
        if pyxel.frame_count - self.start_frame >= self.stop_time:
            #movement
            self.enemy_x += self.enemy_move_size * self.enemy_x_direction
            self.enemy_y += self.enemy_move_size * self.enemy_y_direction
            self.reflection_turning = False
        elif self.reflection_turning == False:
            #field of view 
            self.tmp_angle += math.radians(2)*self.turn_direction
            self.end_angle = self.tmp_angle + math.radians(45)

            self.start_point_x=self.view_radius * math.cos(self.tmp_angle - self.view_width_half)
            self.start_point_y=self.view_radius * math.sin(self.tmp_angle - self.view_width_half)
            
            self.end_point_x=self.view_radius * math.cos(self.tmp_angle + self.view_width_half)
            self.end_point_y=self.view_radius * math.sin(self.tmp_angle + self.view_width_half)

    def reflection(self):
        #edge reflection
        if self.reflection_turning == False:
            self.direction_list=()     

            if self.enemy_x <= 0 or self.wall_side == 'Left':
                self.direction_list = (0,1,7)
            elif self.enemy_x >= 200 or self.wall_side == 'Right':
                self.direction_list = (3,4,5)
            elif self.enemy_y <= 0 or self.wall_side == 'Down':
                self.direction_list = (5,6,7)
            elif self.enemy_y >= 200 or self.wall_side == 'Up':
                self.direction_list = (1,2,3)


            self.start_frame = pyxel.frame_count

            self.tmp_angle = self.view_angle

            self.view_angle = math.radians(random.choice(self.direction_list)*45)

            if (self.view_angle - self.tmp_angle) >= 0 and (self.view_angle - self.tmp_angle) <= math.pi:
                self.turn_direction = 1
            elif(self.view_angle - self.tmp_angle) >= 0 and (self.view_angle - self.tmp_angle) > math.pi:
                self.turn_direction = -1
            elif(self.view_angle - self.tmp_angle) < 0 and abs(self.view_angle - self.tmp_angle) <= math.pi:
                self.turn_direction = -1
            else:
                self.turn_direction = 1

            self.stop_time=min(abs(self.tmp_angle - self.view_angle),2*math.pi-abs(self.tmp_angle - self.view_angle))/(math.pi/90)
            self.enemy_x_direction=math.cos(self.view_angle)
            self.enemy_y_direction=-math.sin(self.view_angle)

            self.move_duration = random.randint(60,120) + self.stop_time
            self.reflection_turning = True

        #field of view 
        self.tmp_angle += math.radians(2)*self.turn_direction
        self.end_angle = self.tmp_angle + math.radians(45)

        self.start_point_x=self.view_radius * math.cos(self.tmp_angle - self.view_width_half)
        self.start_point_y=self.view_radius * math.sin(self.tmp_angle - self.view_width_half)
            
        self.end_point_x=self.view_radius * math.cos(self.tmp_angle + self.view_width_half)
        self.end_point_y=self.view_radius * math.sin(self.tmp_angle + self.view_width_half)  

    def wall_collision(self,wall):
        if wall.wall_x + wall.wall_width <= self.enemy_x <= wall.wall_x + wall.wall_width + 1                       and self.enemy_y >= wall.wall_y and self.enemy_y <= wall.wall_y + wall.wall_height:
            return 'Left'
        if wall.wall_x - 1 <= self.enemy_x <= wall.wall_x                                                           and self.enemy_y >= wall.wall_y and self.enemy_y <= wall.wall_y + wall.wall_height:
            return 'Right'
        if wall.wall_y <= self.enemy_y <= wall.wall_y + 1                                                           and self.enemy_x >= wall.wall_x and self.enemy_x <= wall.wall_x + wall.wall_width:
            return 'Up'
        if wall.wall_y + wall.wall_height - 1 <= self.enemy_y <= wall.wall_y + wall.wall_height                     and self.enemy_x >= wall.wall_x and self.enemy_x <= wall.wall_x + wall.wall_width:
            return 'Down'     

class Goal():
    def __init__(self):
        self.x = 166
        self.y = 30

class App:
    def __init__(self):
        self.player=Player()
        self.goal = Goal()
        self.Enemies = []
        self.Walls1 = []
        self.Walls2 = []
        self.Walls3 = []
        pyxel.init(200, 200)

        pyxel.load('img.pyxres')



        #enemy make
        self.Enemies.append(Enemy(20,30))
        self.Enemies.append(Enemy(25,95))
        self.Enemies.append(Enemy(70,95))
        self.Enemies.append(Enemy(25,130))
        self.Enemies.append(Enemy(125,30))
        self.Enemies.append(Enemy(124,100))
        self.Enemies.append(Enemy(165,30))
        self.Enemies.append(Enemy(165,80))



        
        #wall make
        self.Walls1.append(Wall(8,8,136,8)) 
        self.Walls1.append(Wall(152,8,40,8))
        self.Walls1.append(Wall(48,64,48,8))
        self.Walls1.append(Wall(8,112,48,8))
        self.Walls1.append(Wall(144,104,8,8))
        self.Walls1.append(Wall(48,160,144,8))


        self.Walls2.append(Wall(96,64,8,88))
        self.Walls2.append(Wall(144,8,8,96))
        self.Walls2.append(Wall(0,8,8,192))
        self.Walls2.append(Wall(192,8,8,192))
        

        self.Walls3.append(Wall(0,0,200,8))
        self.Walls3.append(Wall(48,56,56,8))
        self.Walls3.append(Wall(0,104,56,8))
        self.Walls3.append(Wall(48,152,152,8))







        self.Walls = self.Walls1 + self.Walls2 + self.Walls3

        pyxel.run(self.update, self.draw)

    def update(self):

        if self.player.clear or self.player.dead:
            pass
        else:
            self.player.movement()
            if pyxel.frame_count > 30:
                for enemy in self.Enemies:
                    for wall in self.Walls:
                        tmp = enemy.wall_collision(wall)
                        if tmp:
                            break
                    enemy.movement(tmp)
                    self.player.enemy_hit(enemy)


    
            for wall in self.Walls:
                tmp = self.player.wall_collision(wall)
                if tmp:
                    if tmp == 'Up':
                        self.player.y = wall.wall_y - 10
                    if tmp == 'Down':
                        self.player.y = wall.wall_y + wall.wall_height
                    if tmp == 'Left':
                        self.player.x = wall.wall_x + wall.wall_width
                    if tmp == 'Right':
                        self.player.x = wall.wall_x - 10
            
            self.player.edge_stop()
            
            
            
            for enemy in self.Enemies:
                side = None
                for wall in self.Walls:
                    side = enemy.wall_collision(wall)
                    if side!=None:
                        break

    def draw(self):
        pyxel.bltm(0, 0, 1, 0, 0, 200, 200)

        if self.player.dead:
            pyxel.text(90,90,"GameOver",0)
        if self.player.clear:
            pyxel.text(90,90,"Clear",0)
        else:
            if (self.goal.x < self.player.x + 12 and  self.goal.x + 10 > self.player.x and self.goal.y < self.player.y + 12 and  self.goal.y + 9 > self.player.y):     
                self.player.clear = True

            for a in self.Enemies:
                pyxel.tri(a.enemy_x,a.enemy_y,
                        a.enemy_x + a.start_point_x, a.enemy_y - a.start_point_y,
                        a.enemy_x + a.end_point_x,   a.enemy_y - a.end_point_y, 8)
                pyxel.blt(a.enemy_x-4,a.enemy_y-4,0,0,16,8,8,7)

            pyxel.blt(self.player.x ,self.player.y,0,16,16,12,12,7)            

            pyxel.blt(self.goal.x,self.goal.y,0,0,1,10,9,0)

App()













