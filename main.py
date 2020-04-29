import arcade
import random

# Constants
SCREEN_WIDTH: int = 300
SCREEN_HEIGHT: int = 600
SCREEN_TITLE: str = "Arcade Shooter"
SPRITE_SCALE_FACTOR: int = 2


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_sprite = None
        self.bullet_list = None
        self.alien_list = None
        self.score = None
        self.game_over = None

        self.time_elapsed: float = 0.0
        self.player_speed: float = 2.0
        self.alien_speed: float = 2.0
        self.bullet_speed: float = 6.0

        self.alien_spawn_rate: float = 2.0

    def setup(self):

        # Load sprites
        self.player_sprite = arcade.Sprite("ship.png", SPRITE_SCALE_FACTOR)
        self.player_sprite.center_x = self.player_sprite.center_y = 50

        self.bullet_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()

        self.score: int = 0
        self.game_over: bool = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player_sprite.change_x = -self.player_speed
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player_sprite.change_x = self.player_speed

        # Shooting bullets
        if symbol == arcade.key.SPACE:
            bullet_sprite = arcade.Sprite("bullet.png", SPRITE_SCALE_FACTOR)
            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = 50
            bullet_sprite.change_y = self.bullet_speed
            self.bullet_list.append(bullet_sprite)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A or \
           symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_draw(self):
        arcade.start_render()
        self.player_sprite.draw()
        self.bullet_list.draw()
        self.alien_list.draw()

        # Draw game score
        if not self.game_over:
            arcade.draw_text("Score: " + str(self.score), 8, SCREEN_HEIGHT - 24, arcade.color.WHEAT)
        else:
            arcade.set_background_color(arcade.color.GRANNY_SMITH_APPLE)
            arcade.draw_text("Game Over!\nFinal score:" + str(self.score),
                             8, SCREEN_HEIGHT - 16 * 6, arcade.color.ALABAMA_CRIMSON, 16)

    def on_update(self, delta_time: float):

        # Freeze the game when the game is over
        if self.game_over:
            return

        # Speed up game as time progresses
        self.player_speed += delta_time * 0.1
        self.alien_speed += delta_time * 0.1
        self.bullet_speed += delta_time * 0.1 * 3
        self.alien_spawn_rate -= delta_time * 0.1 * 0.25

        # Keep player's ship within the screen limits
        if self.player_sprite.center_x < 24:
            self.player_sprite.center_x = 24
        elif self.player_sprite.center_x > SCREEN_WIDTH - 24:
            self.player_sprite.center_x = SCREEN_WIDTH - 24

        # Spawn alien-enemies
        self.time_elapsed += delta_time
        if self.time_elapsed > self.alien_spawn_rate:
            alien_sprite = arcade.Sprite("alien.png", SPRITE_SCALE_FACTOR)
            alien_sprite.center_x = int(random.randrange(64, SCREEN_WIDTH - 64))
            alien_sprite.center_y = SCREEN_HEIGHT + 50
            alien_sprite.change_y = -self.alien_speed
            self.alien_list.append(alien_sprite)
            self.time_elapsed = 0

        # Update sprites
        self.player_sprite.update()
        self.bullet_list.update()
        self.alien_list.update()

        # Loop through bullets
        for bullet in self.bullet_list:

            # Bullet hit enemy
            collisions = arcade.check_for_collision_with_list(bullet, self.alien_list)
            if collisions:
                bullet.remove_from_sprite_lists()

            for alien in collisions:
                alien.remove_from_sprite_lists()
                self.score += 1

            # Off screen
            if bullet.center_y > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Game over
        for alien in self.alien_list:
            if alien.center_y < 32:
                self.game_over = True




# Main game function
def main():
    game = Game()
    game.setup()
    arcade.run()


main()
