import arcade.key
from random import randint, random
import math

class Sheep:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.angle = -90

    def init_sheep(self):
        self.sheeps = []
        for i in range(1,3):
            sheep_c = Sheep(self,randint(200, 1050),randint(350, 500))
            self.sheeps.append(sheep_c)
        return self.sheeps

    def rotate_sheep(self, delta, hit):
        if hit:
            self.angle += 180

class Walls:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def init_wall(self,width,height):
        self.walls = []

        for i in range(25, 200,25): 
            wall = Walls(self, i, 115 - (i - 165) * 0.5)
            self.walls.append(wall)

        for i in range(440, 750,25):
            if i <= 515:
                wall = Walls(self, i, 110 + (i - 440) * 0.5)
            elif i >= 650:
                wall = Walls(self, i, 130 - (i - 700) * 0.5)
            else:
                wall = Walls(self, i, 140)
            self.walls.append(wall)

        for i in range(1000 , width - 50, 25):
            wall = Walls(self, i, 115 + (i - 1000) * 0.5)
            self.walls.append(wall)
        
        return self.walls


class Spikes:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
    
    def random_number(self):
        self.numx = []
        self.numy = []

        for i in range(20):
            self.numx.append(randint(200, 1050))
            self.numy.append(randint(350, 500))

        for i in range(19):
            for j in range(20):
                if math.fabs((self.numx[i] + self.numy[i]) - (self.numx[j] + self.numy[j])) < 50:
                    self.numx[i] += ((self.numx[i] + self.numy[i]) - (self.numx[j] + self.numy[j]))
                    self.numy[i] += ((self.numx[i] + self.numy[i]) - (self.numx[j] + self.numy[j]))     
        
    def init_spike(self):
        self.spikes = []
        for i in range(6):
            for j in range(4):
                spike = Spikes(self, 350 + i * 100, 300 + j * 100)
                self.spikes.append(spike)
        return self.spikes

class Flippers:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def init_flipper_left_1(self):
        self.flippers = []    
        for i in range(200,275 ,10): #195
            flipper = Flippers(self, i, 110)
            self.flippers.append(flipper)
        return self.flippers
    
    def init_flipper_right_1(self):
        self.flippers = []
        for i in range(415,340 ,-10): #420
            flipper = Flippers(self, i, 110)
            self.flippers.append(flipper)
        return self.flippers
    
    def init_flipper_left_2(self):
        self.flippers = []    
        for i in range(765,840 ,10):
            flipper = Flippers(self, i, 110)
            self.flippers.append(flipper)
        return self.flippers

    def init_flipper_right_2(self,width):
        self.flippers = []
        for i in range(980,905 ,-10): #420
            flipper = Flippers(self, i, 110)
            self.flippers.append(flipper)
        return self.flippers
        

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sheep = 10
        self.score = 0   

        self.flipper_left_1_state = 0
        self.flipper_right_1_state = 0
        self.flipper_left_2_state = 0
        self.flipper_right_2_state = 0
        self.check_end = False

        self.sound_sheep = arcade.sound.load_sound("temp/sounds/sheep.mp3")
        self.sound_lose = arcade.sound.load_sound("temp/sounds/fail2.wav")

        self.walls = Walls.init_wall(self,width,height)        
        self.spikes = Spikes.init_spike(self)
        self.flippers_left_1 = Flippers.init_flipper_left_1(self)
        self.flippers_right_1 = Flippers.init_flipper_right_1(self)
        self.flippers_left_2 = Flippers.init_flipper_left_2(self)
        self.flippers_right_2 = Flippers.init_flipper_right_2(self,width)

        self.main_list = arcade.SpriteList()
        self.sheep_list = arcade.SpriteList()
        self.flipper_left_1_list = arcade.SpriteList()
        self.flipper_right_1_list = arcade.SpriteList()
        self.flipper_left_2_list = arcade.SpriteList()
        self.flipper_right_2_list = arcade.SpriteList()

        for wall in self.walls:
            wall_l = arcade.PhysicsAABB("temp/images/block.png", [wall.x, wall.y], [25, 25], [0, 0], 1.5, 100, 0.001)
            wall_l.static = True
            self.main_list.append(wall_l)

        for spike in self.spikes:
            spike_l = arcade.PhysicsCircle("temp/images/hay.png", [spike.x, spike.y], 15,[0, 0], 1.5, 100, 0.001)
            spike_l.static = True
            self.main_list.append(spike_l)

        World.generate_flipper(self,self.flippers_left_1, self.flipper_left_1_list)
        World.generate_flipper(self,self.flippers_right_1, self.flipper_right_1_list)
        World.generate_flipper(self,self.flippers_left_2, self.flipper_left_2_list)
        World.generate_flipper(self,self.flippers_right_2, self.flipper_right_2_list)
    
    def generate_flipper(self, flipper_o, flipper_l):
        for flipper in flipper_o:
            flipper_c = arcade.PhysicsAABB("temp/images/block.png", [flipper.x, flipper.y], [10, 10], [0, 0], 1.5, 100, 0.001)
            flipper_c.static = True
            self.main_list.append(flipper_c)
            flipper_l.append(flipper_c)

    def animate(self, delta):     
        for sheep in self.sheep_list:
            for spike in self.spikes:
                if math.fabs(sheep.center_y - spike.y) < 25 and math.fabs(sheep.center_x - spike.x) < 25:
                    arcade.sound.play_sound(self.sound_sheep)
                    self.score += 10

            if sheep.center_x < 50:
                sheep.velocity = [5, 0]
            if sheep.center_x > self.width - 50:
                sheep.velocity = [-5, 0]  
            if sheep.center_y > self.height - 50:
                sheep.velocity = [0, -5]            

            if (sheep.center_y < 50):
                sheep.kill()
            
            if(len(self.sheep_list) < 1 and self.sheep == 0):
                self.check_end = True
                arcade.sound.play_sound(self.sound_lose)
        
        World.control_flipper(self,self.flipper_left_1_state, self.flipper_left_1_list)
        World.control_flipper(self,self.flipper_right_1_state, self.flipper_right_1_list)
        World.control_flipper(self,self.flipper_left_2_state, self.flipper_left_2_list)
        World.control_flipper(self,self.flipper_right_2_state, self.flipper_right_2_list)

    def control_flipper(self, flipper_s, flipper_l):
        if flipper_s == 1 and flipper_l[len(flipper_l) - 1].center_y < 200:
            y = 2
            y_change = 2
            for sprite in flipper_l:
                sprite.change_y = y
                y += y_change
                sprite.frozen = False
            
        elif flipper_s == 0 and flipper_l[len(flipper_l) - 1].center_y > 60:
            y = -2
            y_change = -2
            for sprite in flipper_l:
                sprite.change_y = y
                y += y_change
                sprite.frozen = False
        
        else:
            for sprite in flipper_l:
                sprite.change_y = 0
                sprite.frozen = True

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE: 
            if not(self.check_end):
                if self.sheep > 0 and len(self.sheep_list) < 2:
                    self.sheep -= 2
                    sheep_o = Sheep.init_sheep(self)
                    for sheep_b in sheep_o:
                        sheep_l = arcade.PhysicsCircle("temp/images/sheep.png", [sheep_b.x, sheep_b.y], 15, [0, -5], 1, 0.30, 0.001)
                        self.main_list.append(sheep_l)
                        self.sheep_list.append(sheep_l)                
            else :
                self.sheep = 10

        if key == arcade.key.Z:
            self.flipper_right_1_state = 1
            
        if key == arcade.key.X:
            self.flipper_left_1_state = 1

        if key == arcade.key.PERIOD:
            self.flipper_right_2_state = 1

        if key == arcade.key.SLASH:
            self.flipper_left_2_state = 1
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.Z:
            self.flipper_right_1_state = 0

        if key == arcade.key.X:
            self.flipper_left_1_state = 0
            
        if key == arcade.key.PERIOD:
            self.flipper_right_2_state = 0            

        if key == arcade.key.SLASH:
            self.flipper_left_2_state = 0