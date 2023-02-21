import curses
from PIL import Image
import time
import random


class Pokemon:
    def __init__(self, name, hp, atk, defense, level=5, hp_max=100, speed=10):
        self.name = name
        self.hp = hp
        self.hp_max = hp_max
        self.atk = atk
        self.defense = defense
        self.level = level

    def attack(self, enemy):
        enemy.hp -= self.atk

    @staticmethod
    def growl(enemy):
        enemy.atk -= 1
        if enemy.atk < 0:
            enemy.atk = 0

    def __str__(self):
        return f"{self.name} - HP: {self.hp} - ATK: {self.atk}"


def main(stdscr):
    # Load the image file
    option = 0
    size_x_white = 110
    size_y_white = 30

    def draw_image(stdscr, img_file, x_pos, y_pos, size_x=50, size_y=20):
        img = Image.open(img_file)
        curses.start_color()
        # Get the size of the image
        (width, height) = img.size

        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        curses.init_pair(7, curses.COLOR_WHITE, -1)
        curses.init_pair(8, curses.COLOR_BLACK, -1)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Scale the image down to fit the terminal size
        if height > curses.LINES or width > curses.COLS:
            aspect_ratio = 2
            new_height = curses.LINES
            new_width = int(new_height * aspect_ratio)
            if new_width > curses.COLS:
                new_width = curses.COLS
                new_height = int(new_width / aspect_ratio)
            img = img.resize((size_x, size_y), Image.LANCZOS)

        # Convert the image to a list of RGB values
        pixels = list(img.getdata())
        pixels = [pixels[i * img.width:(i + 1) * img.width] for i in range(img.height)]
        i = 1
        # Draw the image in the terminal
        for y, row in enumerate(pixels):
            for x, pixel in enumerate(row):
                try:
                    (r, g, b) = pixel
                except ValueError:
                    (r, g, b, _) = pixel

                if r >= 150 and g >= 150 and b >= 150:
                    color = 7  # White
                elif r >= 128 and g >= 128 and b < 50:
                    color = 3  # Yellow
                elif r >= 128 and b >= 128 and g < 50:
                    color = 5  # Magenta
                elif g >= 128 and b >= 128:
                    color = 6  # Cyan
                elif r >= 128:
                    color = 1  # Red
                elif g >= 128:
                    color = 2  # Green
                elif b >= 128:
                    color = 4  # Blue
                elif r < 100 and g < 100 and b < 100:
                    color = 8
                else:
                    color = 0
                stdscr.addstr(y + y_pos, x + x_pos, "\u2588", curses.color_pair(color))

        # Refresh the screen

    def idle_animation(stdscr):
        draw_image(stdscr, "charmander.png", 0, 10)
        stdscr.refresh()
        time.sleep(0.3)
        draw_image(stdscr, "charmander.png", 0, 9)
        stdscr.refresh()
        time.sleep(0.3)

    def attack_animation(stdscr):
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "charmander.png", 10, 10)
        stdscr.refresh()
        time.sleep(0.1)
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "charmander.png", 0, 10)
        stdscr.refresh()

    def attack_animation_enemy(stdscr):
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "bulbinha.png", 60, 0, size_x=30, size_y=20)
        stdscr.refresh()
        time.sleep(0.1)
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "bulbinha.png", 70, 0, size_x=30, size_y=20)
        stdscr.refresh()

    def draw_hp_bar(stdscr, hp, x, y):
        hp_bar = ""
        hp_bar += "HP: "
        hp_bar += str(hp)
        hp_bar += "/"
        color = 2
        stdscr.addstr(y, x, "\u2588" * (hp // 10) * 2, curses.color_pair(color))

    def draw_status(stdscr, pokemon, x, y):
        stdscr.addstr(y - 1, x - 2, pokemon.name.upper(), curses.color_pair(9))
        draw_hp_bar(stdscr, pokemon.hp, x, y)
        stdscr.addstr(y - 1, x + 17, f"Lv{pokemon.level}", curses.color_pair(9))
        stdscr.addstr(y + 1, x + 13, f"{pokemon.hp}/{pokemon.hp_max}", curses.color_pair(9))

    def draw_growl(stdscr, x, y):
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "growl.png", x, y, size_x=30, size_y=20)
        stdscr.refresh()
        time.sleep(0.1)

    def attack_options(stdscr, pokemon, x, y):
        stdscr.addstr(y + 1, x, "TACLKE", curses.color_pair(9))
        stdscr.addstr(y + 1, x + 10, "GROWL", curses.color_pair(9))
        nonlocal option

        if c == curses.KEY_RIGHT:
            option = 1
        elif c == curses.KEY_LEFT:
            option = 0

        if option == 0:
            stdscr.addstr(y + 1, x - 2, ">", curses.color_pair(9))
            stdscr.addstr(y + 1, x + 8, " ", curses.color_pair(9))
        if option == 1:
            stdscr.addstr(y + 1, x - 2, " ", curses.color_pair(9))
            stdscr.addstr(y + 1, x + 8, ">", curses.color_pair(9))

    draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
    bulbasaur = Pokemon("Bulbasaur", 100, 10, 10)
    charmander = Pokemon("Charmander", 100, 10, 10)
    current_pokemon = bulbasaur
    moved = False

    while True:
        idle_animation(stdscr)
        draw_image(stdscr, "bulbinha.png", 70, 0, size_x=30, size_y=20)
        stdscr.nodelay(True)
        c = stdscr.getch()

        if c == ord('g'):
            attack_animation_enemy(stdscr)

        elif c == ord('q'):
            import sys
            sys.exit(0)
        if (c == curses.KEY_ENTER or c == 10 or c == 13) and option == 0 and current_pokemon == charmander:
            attack_animation(stdscr)
            charmander.attack(bulbasaur)
            moved = True
        elif (c == curses.KEY_ENTER or c == 10 or c == 13) and option == 1 and current_pokemon == charmander:
            charmander.growl(bulbasaur)
            draw_growl(stdscr, 60, 0)
            moved = True

        if current_pokemon == bulbasaur and moved:
            if random.randint(0, 10) > 7:
                draw_growl(stdscr, 0, 10)
                bulbasaur.growl(charmander)
                time.sleep(0.3)
            else:
                attack_animation_enemy(stdscr)
                bulbasaur.attack(charmander)
            moved = False

        # change turn
        if moved:
            current_pokemon = bulbasaur
        else:
            current_pokemon = charmander

        draw_hp_bar(stdscr, bulbasaur.hp, 30, 5)
        draw_status(stdscr, bulbasaur, 30, 5)
        draw_status(stdscr, charmander, 60, 22)
        attack_options(stdscr, charmander, 60, 25)

        if bulbasaur.hp <= 0:
            draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
            idle_animation(stdscr)
            stdscr.addstr(20, 60, f"{bulbasaur.name.upper()} FAINTED", curses.color_pair(9))
            stdscr.refresh()
            time.sleep(10)
            # break
        elif charmander.hp <= 0:
            draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
            draw_image(stdscr, "bulbinha.png", 70, x, size_x=30, size_y=20)
            stdscr.addstr(20, 60, f"{charmander.name.upper()} FAINTED", curses.color_pair(9))
            stdscr.refresh()
            time.sleep(10)


if __name__ == "__main__":
    curses.wrapper(main)
