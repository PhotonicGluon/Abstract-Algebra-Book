# IMPORTS
from pathlib import Path

from numpy import sin, cos, arange, linspace, pi
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
from tqdm import tqdm

# CONSTANTS
COVER_DIR = Path("../../book/images/cover/front-only")
COVER_FILES = ["cover-page-background.svg", "cover-page-background.jpg"]

NUM_PAGES = 763

TRIM_WIDTH = 152.40  # In mm, 152.40 mm = 6"
TRIM_HEIGHT = 228.60  # In mm, 228.60 mm = 9"
ASPECT_RATIO = TRIM_HEIGHT / TRIM_WIDTH

DPI = 100
SCALE_PX_TO_MM = 10  # Num pixels representing 1 mm
TRIM_WIDTH_SCALED = TRIM_WIDTH * SCALE_PX_TO_MM  # In px
TRIM_HEIGHT_SCALED = TRIM_HEIGHT * SCALE_PX_TO_MM  # In px

TRIM_MIN_X = -1.25
TRIM_MAX_X = 1.25
TRIM_RANGE_X = TRIM_MAX_X - TRIM_MIN_X
PIXEL_PER_X = TRIM_RANGE_X / TRIM_WIDTH

TRIM_MIN_Y = TRIM_MIN_X * ASPECT_RATIO
TRIM_MAX_Y = TRIM_MAX_X * ASPECT_RATIO
TRIM_RANGE_Y = TRIM_MAX_Y - TRIM_MIN_Y
PIXEL_PER_Y = TRIM_RANGE_Y / TRIM_HEIGHT

NUM_LINES = 2500
LINES_ALPHA = 0.125
NUM_CUSPS = 7  # Number of cusps to draw for the epicycloid
OFFSET = 1.5 * pi / NUM_CUSPS  # Offset for the first plotted point
# OFFSET = pi / NUM_CUSPS  # Offset for the first plotted point

POLYGON_LINE_COLOUR = "white"
POLYGON_LINE_ALPHA = 0
POLYGON_LINE_THICKNESS = 5
POLYGON_FILL_COLOUR = "black"
POLYGON_FILL_ALPHA = 0.35

COLOURS = ["lightcoral", "peachpuff", "palegreen", "green", "lightblue", "blue", "orchid", "lightpink"]


# FUNCTIONS
def get_colour(i):
    return COLOURS[i % len(COLOURS)]


def epicycloid_point(num_cusps, theta, offset=pi / 7):
    x = (num_cusps + 1) / (num_cusps + 2) * cos(theta + offset) + 1 / (num_cusps + 2) * cos(
        (num_cusps + 1) * theta + offset
    )
    y = (num_cusps + 1) / (num_cusps + 2) * sin(theta + offset) + 1 / (num_cusps + 2) * sin(
        (num_cusps + 1) * theta + offset
    )

    return x, y


def draw_epicycloid(num_cusps, offset=pi / 7, alpha=0.1, n=200, tolerance=1e-8):
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
        plt.axline((x1, y1), (x2, y2), color=get_colour(i), linestyle="-", alpha=alpha)


def draw_inscribed_polygon(
    num_cusps,
    offset=pi / 7,
    line_colour="#ffffff",
    line_alpha=0.5,
    line_thickness=3,
    fill_colour="#ffffff",
    fill_alpha=0.3,
):
    # Get the points on the heptagon
    thetas = arange(pi / num_cusps, 2 * pi, 2 * pi / num_cusps)
    points = [epicycloid_point(num_cusps, theta, offset) for theta in thetas]

    points_x = [pt[0] for pt in points]
    points_y = [pt[1] for pt in points]

    plt.fill(
        points_x,
        points_y,
        edgecolor=mcolors.to_rgba(line_colour, line_alpha),
        facecolor=mcolors.to_rgba(fill_colour, fill_alpha),
        linewidth=line_thickness,
        zorder=1e6,
    )  # High z-order to make polygon be on top


def plot_figure(width, height, filenames, x_range, y_range):
    # Initialize plotting figure
    plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI, facecolor="black")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.axis("off")

    # Draw things
    draw_epicycloid(NUM_CUSPS, offset=OFFSET, alpha=LINES_ALPHA, n=NUM_LINES)
    draw_inscribed_polygon(
        NUM_CUSPS,
        offset=OFFSET,
        line_colour=POLYGON_LINE_COLOUR,
        line_alpha=POLYGON_LINE_ALPHA,
        line_thickness=POLYGON_LINE_THICKNESS,
        fill_colour=POLYGON_FILL_COLOUR,
        fill_alpha=POLYGON_FILL_ALPHA,
    )

    # Save result
    if isinstance(filenames, str):
        filenames = [filenames]

    for filename in tqdm(filenames, desc="Saving Files"):
        plt.savefig(COVER_DIR / filename)

    plt.close()


# MAIN CODE
print("Creating front-only page...")
plot_figure(TRIM_WIDTH_SCALED, TRIM_HEIGHT_SCALED, COVER_FILES, (TRIM_MIN_X, TRIM_MAX_X), (TRIM_MIN_Y, TRIM_MAX_Y))
print()

print("Done!")
