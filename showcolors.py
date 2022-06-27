#! /usr/bin/python3
import sys
import truecolor
import os

colors = []

if len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print("""Show the givern colors in the terminal.
The terminal must support truecolor.
Usage: showcolors.py [color...] [-] [-h]
    color: one or more color hex code, e.g. '#ff0000'.
    -h: show this help.
    -: read colors from stdin, can be combined with color.""")
    sys.exit(0)

for arg in sys.argv[1:]:
    if arg == "-":
        for line in sys.stdin.read().splitlines():
            for word in line.split(" "):
                colors.append(word)
    else:
        colors.append(arg)


class Item:
    def __init__(self, color, foreground):
        self.color = truecolor.hex_to_rgb(color)
        self.foreground = truecolor.hex_to_rgb(foreground)
        self.raw_color = color


items = []
maxwidth = 0

for color in colors:
    # Here we find the average value or R, G and B.
    average_value = sum(truecolor.hex_to_rgb(color)) / 3
    # We then see if this is > or <= 127(256/2 - 1)
    # (to see if it is dark or light)
    # We then find the color between black and white that will be
    # most readable on the background.
    foreground = '#000000' if average_value > 127 else '#FFFFFF'
    items.append(Item(color, foreground))
    maxwidth = max(maxwidth, len(color))

x = 0

for item in items:
    print(truecolor.color_text(item.raw_color +
                               " "*(maxwidth-len(item.raw_color)),
                               foreground=item.foreground,
                               background=item.color),
          end="")

    x += maxwidth
    if x+maxwidth > os.get_terminal_size()[0]:
        print()
        x = 0

print()
