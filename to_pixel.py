import curses
from PIL import Image
import time

attack_animation_bool = False
def main(stdscr):
    # Load the image file
    #curses.use_default_colors()

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
                    color = 7 # White
                elif r >= 128 and g >= 128 and b < 50:
                    color = 3 # Yellow
                elif r >= 128 and b >= 128 and g < 50:
                    color = 5 # Magenta
                elif g >= 128 and b >= 128:
                    color = 6 # Cyan
                elif r >= 128:
                    color = 1 # Red
                elif g >= 128:
                    color = 2 # Green
                elif b >= 128:
                    color = 4 # Blue
                elif r < 100 and g < 100 and b < 100:
                    color = 8
                else:
                    color = 0
                stdscr.addstr(y+y_pos, x+x_pos, "\u2588", curses.color_pair(color))
    size_x_white = 110
    size_y_white = 30
        # Refresh the screen
    def idle_animation(stdscr):
        draw_image(stdscr, "charmander.png", 0, 10)
        stdscr.refresh()
        time.sleep(0.3)
        draw_image(stdscr, "charmander.png", 0, 9)
        stdscr.refresh()
        time.sleep(0.3)

    def atack_animation(stdscr):
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "charmander.png", 10, 10)
        stdscr.refresh()
        time.sleep(0.1)
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "charmander.png", 0, 10)
        stdscr.refresh()

    def atack_animation_enemy(stdscr):
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "bulbinha.png", 60, 0, size_x=30, size_y=20)
        stdscr.refresh()
        time.sleep(0.1)
        draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
        draw_image(stdscr, "bulbinha.png", 70, 0, size_x=30, size_y=20)
        stdscr.refresh()

    x = 0
    draw_image(stdscr, "white.png", 0, 0, size_x=size_x_white, size_y=size_y_white)
    while True:
        idle_animation(stdscr)
        draw_image(stdscr, "bulbinha.png", 70, x, size_x=30, size_y=20)

        stdscr.nodelay(True)
        c = stdscr.getch()

        if c == ord('x'):
            x += 10
            stdscr.clear()
        if c == ord('z'):
            x -= 10
            stdscr.clear()
        if c == ord('f'):
            atack_animation(stdscr)
        if c == ord('g'):
            atack_animation_enemy(stdscr)



        elif c == ord('q'):
            import sys
            sys.exit(0)






if __name__ == "__main__":
    curses.wrapper(main)