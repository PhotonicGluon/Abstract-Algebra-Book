# IMPORTS
from pathlib import Path

from numpy import sin, cos, arange, linspace, pi
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
from tqdm import tqdm

# CONSTANTS
COVER_DIR = Path("../../book/images/cover")
COVER_PAGE_FILES = ["cover-page-background.svg", "cover-page-background.jpg"]
COVER_FULL_FILES = ["cover-full-background.svg", "cover-full-background.png", "cover-full-background.jpg"]

SCALE_FACTOR = 10
NUM_PAGES = 775

COVER_WIDTH = 155.57 * SCALE_FACTOR  # In mm
COVER_HEIGHT = 234.95 * SCALE_FACTOR
COVER_ASPECT_RATIO = COVER_HEIGHT / COVER_WIDTH
# OUTER_MARGIN_AND_BLEED = (3.17 + 3.17) * SCALE_FACTOR
OUTER_MARGIN_AND_BLEED = 19.05 * SCALE_FACTOR  # 19.05mm = Wrap area
# SPINE_WIDTH = 0.0572 * NUM_PAGES * SCALE_FACTOR
SPINE_WIDTH = 50.8 * SCALE_FACTOR
FULL_WIDTH = OUTER_MARGIN_AND_BLEED + COVER_WIDTH + SPINE_WIDTH + COVER_WIDTH + OUTER_MARGIN_AND_BLEED
FULL_HEIGHT = OUTER_MARGIN_AND_BLEED + COVER_HEIGHT + OUTER_MARGIN_AND_BLEED
DPI = 100

COVER_MIN_X = -1.15
COVER_MAX_X = 1.15
COVER_RANGE_X = COVER_MAX_X - COVER_MIN_X
PIXEL_PER_X = COVER_RANGE_X / COVER_WIDTH
MIN_X = COVER_MIN_X - (SPINE_WIDTH + COVER_WIDTH + OUTER_MARGIN_AND_BLEED) * PIXEL_PER_X
MAX_X = COVER_MAX_X + OUTER_MARGIN_AND_BLEED * PIXEL_PER_X

COVER_MIN_Y = COVER_MIN_X * COVER_ASPECT_RATIO
COVER_MAX_Y = COVER_MAX_X * COVER_ASPECT_RATIO
COVER_RANGE_Y = COVER_MAX_Y - COVER_MIN_Y
PIXEL_PER_Y = COVER_RANGE_Y / COVER_HEIGHT
MIN_Y = COVER_MIN_Y - OUTER_MARGIN_AND_BLEED * PIXEL_PER_Y
MAX_Y = COVER_MAX_Y + OUTER_MARGIN_AND_BLEED * PIXEL_PER_Y

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
print("Entered dimensions are:")
print(f"- Trim width:  {COVER_WIDTH/SCALE_FACTOR:.2f}mm")
print(f"- Trim height: {COVER_HEIGHT/SCALE_FACTOR:.2f}mm")
print(f"- Full width:  {FULL_WIDTH/SCALE_FACTOR:.2f}mm")
print(f"- Full height: {FULL_HEIGHT/SCALE_FACTOR:.2f}mm")

input("Press RETURN to continue.")
print()

# print("Creating eBook cover page...")
# plot_figure(COVER_WIDTH, COVER_HEIGHT, COVER_PAGE_FILES, (COVER_MIN_X, COVER_MAX_X), (COVER_MIN_Y, COVER_MAX_Y))
# print()

print("Creating full cover...")
plot_figure(FULL_WIDTH, FULL_HEIGHT, COVER_FULL_FILES, (MIN_X, MAX_X), (MIN_Y, MAX_Y))
print()

print("Done!")
