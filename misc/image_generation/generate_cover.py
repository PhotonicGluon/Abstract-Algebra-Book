# IMPORTS
from pathlib import Path

from numpy import sin, cos, arange, linspace, pi
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
from tqdm import tqdm

# CONSTANTS
COVER_DIR = Path("../../book/images/cover")
# COVER_PAGE_FILES = ["cover-page-background.svg", "cover-page-background.jpg"]
COVER_PAGE_FILES = ["cover-page-background.jpg"]
# COVER_FULL_FILES = ["cover-full-background.svg", "cover-full-background.png", "cover-full-background.jpg"]
COVER_FULL_FILES = ["cover-full-background.jpg"]

NUM_PAGES = 764

BODY_WIDTH = 123.825  # In mm, 123.825 mm = 4.875"
BODY_HEIGHT = 203.20  # In mm, 203.20 mm = 8"
ASPECT_RATIO = BODY_HEIGHT / BODY_WIDTH

SAFETY_MARGIN_BASE = 12.70  # In mm, 12.70 mm = 0.5"
SAFETY_MARGIN_BLEED = 3.175  # In mm, 3.175 mm = 0.125"
SAFETY_MARGIN = SAFETY_MARGIN_BASE + SAFETY_MARGIN_BLEED

TRIM_WIDTH = SAFETY_MARGIN + BODY_WIDTH + SAFETY_MARGIN  # In mm
TRIM_HEIGHT = SAFETY_MARGIN + BODY_HEIGHT + SAFETY_MARGIN  # In mm

WRAP_AREA = 19.05  # In mm, 19.05 mm = 0.75"
SPINE_WIDTH = 50.80  # In mm, 50.80 mm = 2"

FULL_WIDTH = WRAP_AREA + TRIM_WIDTH + SPINE_WIDTH + TRIM_WIDTH + WRAP_AREA
FULL_HEIGHT = WRAP_AREA + TRIM_HEIGHT + WRAP_AREA

DPI = 100
SCALE_PX_TO_MM = 10  # Num pixels representing 1 mm
TRIM_WIDTH_SCALED = TRIM_WIDTH * SCALE_PX_TO_MM  # In px
TRIM_HEIGHT_SCALED = TRIM_HEIGHT * SCALE_PX_TO_MM  # In px
FULL_WIDTH_SCALED = FULL_WIDTH * SCALE_PX_TO_MM  # In px
FULL_HEIGHT_SCALED = FULL_HEIGHT * SCALE_PX_TO_MM  # In px

BODY_MIN_X = -1
BODY_MAX_X = 1
BODY_RANGE_X = BODY_MAX_X - BODY_MIN_X
PIXEL_PER_X = BODY_RANGE_X / BODY_WIDTH
TRIM_MIN_X = BODY_MIN_X - SAFETY_MARGIN * PIXEL_PER_X
TRIM_MAX_X = BODY_MAX_X + SAFETY_MARGIN * PIXEL_PER_X
FULL_MIN_X = TRIM_MIN_X - (SPINE_WIDTH + TRIM_WIDTH + WRAP_AREA) * PIXEL_PER_X
FULL_MAX_X = TRIM_MAX_X + WRAP_AREA * PIXEL_PER_X

BODY_MIN_Y = BODY_MIN_X * ASPECT_RATIO
BODY_MAX_Y = BODY_MAX_X * ASPECT_RATIO
BODY_RANGE_Y = BODY_MAX_Y - BODY_MIN_Y
PIXEL_PER_Y = BODY_RANGE_Y / BODY_HEIGHT
TRIM_MIN_Y = BODY_MIN_Y - SAFETY_MARGIN * PIXEL_PER_Y
TRIM_MAX_Y = BODY_MAX_Y + SAFETY_MARGIN * PIXEL_PER_Y
FULL_MIN_Y = TRIM_MIN_Y - WRAP_AREA * PIXEL_PER_Y
FULL_MAX_Y = TRIM_MAX_Y + WRAP_AREA * PIXEL_PER_Y

# NUM_LINES = 2500
# LINES_ALPHA = 0.125
NUM_LINES = 250
LINES_ALPHA = 0.25
NUM_CUSPS = 7  # Number of cusps to draw for the epicycloid
OFFSET = 1.5 * pi / NUM_CUSPS  # Offset for the first plotted point
# OFFSET = pi / NUM_CUSPS  # Offset for the first plotted point

POLYGON_LINE_COLOUR = "white"
POLYGON_LINE_ALPHA = 0
POLYGON_LINE_THICKNESS = 5
# POLYGON_FILL_COLOUR = "black"
POLYGON_FILL_COLOUR = "white"
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
    # draw_epicycloid(NUM_CUSPS, offset=OFFSET, alpha=LINES_ALPHA, n=NUM_LINES)
    # draw_inscribed_polygon(
    #     NUM_CUSPS,
    #     offset=OFFSET,
    #     line_colour=POLYGON_LINE_COLOUR,
    #     line_alpha=POLYGON_LINE_ALPHA,
    #     line_thickness=POLYGON_LINE_THICKNESS,
    #     fill_colour=POLYGON_FILL_COLOUR,
    #     fill_alpha=POLYGON_FILL_ALPHA,
    # )

    plt.axvline(color="white")
    plt.axhline(color="white")

    plt.axvline(x=BODY_MIN_X, color="blue")
    plt.axvline(x=BODY_MAX_X, color="blue")

    plt.axhline(y=BODY_MIN_Y, color="red")
    plt.axhline(y=BODY_MAX_Y, color="red")

    # Save result
    if isinstance(filenames, str):
        filenames = [filenames]

    for filename in tqdm(filenames, desc="Saving Files"):
        plt.savefig(COVER_DIR / filename)

    plt.close()


# MAIN CODE
print("Entered dimensions are:")
print(f"- Body width:  {BODY_WIDTH:.2f} mm = {BODY_WIDTH / 25.4:.2f} in")
print(f"- Body height: {BODY_HEIGHT:.2f} mm = {BODY_HEIGHT / 25.4:.2f} in")
print(f"- Trim width:  {TRIM_WIDTH:.2f} mm = {TRIM_WIDTH / 25.4:.2f} in")
print(f"- Trim height: {TRIM_HEIGHT:.2f} mm = {TRIM_HEIGHT / 25.4:.2f} in")
print(f"- Full width:  {FULL_WIDTH:.2f} mm = {FULL_WIDTH / 25.4:.2f} in")
print(f"- Full height: {FULL_HEIGHT:.2f} mm = {FULL_HEIGHT / 25.4:.2f} in")

input("Press RETURN to continue.")
print()

print("Creating eBook cover page...")
plot_figure(TRIM_WIDTH_SCALED, TRIM_HEIGHT_SCALED, COVER_PAGE_FILES, (TRIM_MIN_X, TRIM_MAX_X), (TRIM_MIN_Y, TRIM_MAX_Y))
print()

print("Creating full cover...")
plot_figure(FULL_WIDTH_SCALED, FULL_HEIGHT_SCALED, COVER_FULL_FILES, (FULL_MIN_X, FULL_MAX_X), (FULL_MIN_Y, FULL_MAX_Y))
print()

print("Done!")
