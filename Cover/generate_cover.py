# IMPORTS
from numpy import sin, cos, linspace, pi
import matplotlib.pyplot as plt
from tqdm import tqdm

# CONSTANTS
WIDTH = 1760
HEIGHT = 2500
ASPECT_RATIO = HEIGHT / WIDTH
DPI = 100

MIN_X = -1.15
MAX_X = -MIN_X

NUM_LINES = 2500
LINES_ALPHA = 0.125
NUM_CUSPS = 7  # Number of cusps to draw for the epicycloid
OFFSET = 1.5 * pi / 7  # Offset for the first plotted point

COLOURS = [
    "lightcoral",  # Red
    "peachpuff",  # Orange
    "khaki",  # Yellow
    "palegreen",  # Green
    "lightblue",  # Blue
    "orchid",  # Purple
    "lightpink"  # Pink
]


# FUNCTIONS
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
        plt.axline((x1, y1), (x2, y2), color=COLOURS[i % len(COLOURS)], linestyle="-", alpha=alpha)


# MAIN CODE
# Initialize plotting figure
plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor="black")
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.xlim(MIN_X, MAX_X)
plt.ylim(ASPECT_RATIO * MIN_X, ASPECT_RATIO * MAX_X)
plt.axis("off")

draw_epicycloid(NUM_CUSPS, offset=OFFSET, alpha=LINES_ALPHA, n=NUM_LINES)

plt.show()
plt.close()
