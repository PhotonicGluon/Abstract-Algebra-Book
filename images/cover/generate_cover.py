# IMPORTS
from numpy import sin, cos, arange, linspace, pi
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
from tqdm import tqdm

# CONSTANTS
WIDTH = 1760
HEIGHT = 2500
ASPECT_RATIO = HEIGHT / WIDTH
DPI = 100

MIN_X = -1.15
MAX_X = -MIN_X

NUM_LINES = 2000
LINES_ALPHA = 0.125
LINES_SATURATION = 0.75
LINES_VALUE = 1.
NUM_CUSPS = 7  # Number of cusps to draw for the epicycloid
OFFSET = 1.5 * pi / NUM_CUSPS  # Offset for the first plotted point
# OFFSET = pi / NUM_CUSPS  # Offset for the first plotted point

POLYGON_LINE_COLOUR = "white"
POLYGON_LINE_ALPHA = 0
POLYGON_LINE_THICKNESS = 5
POLYGON_FILL_COLOUR = "black"
POLYGON_FILL_ALPHA = 0.35

COLOURS = [
    "lightcoral",
    "peachpuff",
    "palegreen",
    "green",
    "lightblue",
    "blue",
    "orchid",
    "lightpink"
]


# FUNCTIONS
def get_colour(i, num_colours=7, saturation=1., value=1.):
    return COLOURS[i % len(COLOURS)]

    # import colorsys
    # return colorsys.hsv_to_rgb((i % num_colours) / num_colours, saturation, value)


def epicycloid_point(num_cusps, theta, offset=pi / 7):
    x = (num_cusps + 1) / (num_cusps + 2) * cos(theta + offset) + 1 / (num_cusps + 2) * cos(
        (num_cusps + 1) * theta + offset)
    y = (num_cusps + 1) / (num_cusps + 2) * sin(theta + offset) + 1 / (num_cusps + 2) * sin(
        (num_cusps + 1) * theta + offset)

    return x, y


def draw_epicycloid(num_cusps, num_colours=7, saturation=0.5, value=1., offset=pi / 7, alpha=0.1, n=200,
                    tolerance=1e-8):
    # Generate the thetas to sample the points at
    thetas = linspace(0, 2 * pi, n)

    # Plot the 'tangent' lines
    for i, theta in enumerate(tqdm(thetas, desc="Drawing Lines")):
        # Generate the two points
        x1 = cos(theta + offset)
        y1 = sin(theta + offset)
        x2 = cos((num_cusps + 1) * theta + offset)
        y2 = sin((num_cusps + 1) * theta + offset)

        # If too close, skip them
        if abs(x1 - x2) < tolerance and abs(y1 - y2) < tolerance:
            continue

        # Draw a line connecting the two points
        plt.axline(
            (x1, y1), (x2, y2),
            color=get_colour(i, num_colours=num_colours, saturation=saturation, value=value),
            linestyle="-",
            alpha=alpha
        )


def draw_inscribed_polygon(num_cusps, offset=pi / 7, line_colour="#ffffff", line_alpha=0.5, line_thickness=3,
                           fill_colour="#ffffff", fill_alpha=0.3):
    # Get the points on the heptagon
    thetas = arange(pi / num_cusps, 2 * pi, 2 * pi / num_cusps)
    points = [epicycloid_point(num_cusps, theta, offset) for theta in thetas]

    points_x = [pt[0] for pt in points]
    points_y = [pt[1] for pt in points]

    plt.fill(points_x, points_y, edgecolor=mcolors.to_rgba(line_colour, line_alpha),
             facecolor=mcolors.to_rgba(fill_colour, fill_alpha), linewidth=line_thickness,
             zorder=1e6)  # High z-order to make polygon be on top


# MAIN CODE
# Initialize plotting figure
plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor="black")
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.xlim(MIN_X, MAX_X)
plt.ylim(ASPECT_RATIO * MIN_X, ASPECT_RATIO * MAX_X)
plt.axis("off")

# Draw things
draw_epicycloid(NUM_CUSPS, saturation=LINES_SATURATION, value=LINES_VALUE, offset=OFFSET, alpha=LINES_ALPHA,
                n=NUM_LINES)
draw_inscribed_polygon(NUM_CUSPS, offset=OFFSET, line_colour=POLYGON_LINE_COLOUR, line_alpha=POLYGON_LINE_ALPHA,
                       line_thickness=POLYGON_LINE_THICKNESS, fill_colour=POLYGON_FILL_COLOUR,
                       fill_alpha=POLYGON_FILL_ALPHA)

# Show result
plt.show()
plt.close()