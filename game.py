import arcade
 
from modal import World

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

GAME_START = 0
INSTRUCTIONS_PAGE = 1
GAME_RUNNING = 2
GAME_OVER = 3

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
 
    def draw(self):
        self.sync_with_model()
        super().draw()

class QueepWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        
        self.current_state = GAME_START
        arcade.set_background_color(arcade.color.AMAZON)
        self.intro_background = arcade.load_texture("temp/images/frontbg1.png")
        self.background = arcade.load_texture("temp/images/bg.png")
        self.instrution_background = arcade.load_texture("temp/images/instru.png")
        self.world = World(width, height) 

    def draw_instructions(self):
        arcade.draw_xywh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.instrution_background)

    def draw_game_start(self):
        arcade.draw_xywh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.intro_background)
        arcade.draw_text("Click to play", 90, 90, arcade.color.WHITE, 50, width=1000, align="center")

    def draw_game(self):
        arcade.draw_xywh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.world.main_list.draw()
        arcade.draw_text("Sheep : ", 770, self.height - 30, arcade.color.WHITE, 20, width=200, align="left")
        arcade.draw_text(str(self.world.sheep), 750, self.height - 30,arcade.color.WHITE, 20, width=200, align="right")
        arcade.draw_text("Score : ", 990, self.height - 30, arcade.color.WHITE, 20, width=1000, align="left")
        arcade.draw_text(str(self.world.score), 990, self.height - 30,arcade.color.WHITE, 20, width=200, align="right")
        if self.world.check_end:
           self.current_state = GAME_OVER

    def draw_game_over(self):
        arcade.draw_text("END GAME\n", 100, 500, arcade.color.WHITE, 80, width=1000, align="center")
        arcade.draw_text("Your Score : ", 40, 350, arcade.color.WHITE, 50, width=1000, align="center")
        arcade.draw_text(str(self.world.score),320, 350,arcade.color.WHITE, 50, width=1000, align="center")
        arcade.draw_text("Click to restart", 100, 200, arcade.color.WHITE, 50, width=1000, align="center")
 
    def on_draw(self):
        arcade.start_render()

        if self.current_state == GAME_START:
            self.draw_game_start()
        elif self.current_state == INSTRUCTIONS_PAGE:
            self.draw_instructions()
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == GAME_START:
            self.current_state = INSTRUCTIONS_PAGE
        elif self.current_state == INSTRUCTIONS_PAGE:
            self.current_state = GAME_RUNNING
            self.world.sheep = 10
        elif self.current_state == GAME_RUNNING:
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            self.world.check_end = False
            self.world.score = 0
            self.current_state = GAME_START

    def animate(self, delta):     
        if self.current_state == GAME_RUNNING:
            arcade.process_2d_physics_movement(self.world.main_list, gravity=0.6)
            arcade.process_2d_physics_collisions(self.world.main_list)         
            self.world.animate(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

if __name__ == '__main__':
    window = QueepWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()