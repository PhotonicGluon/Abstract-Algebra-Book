# IMPORTS
import os

# CONSTANTS
DIRECTORY = ".."

# FUNCTIONS
def remove_trailing_whitespace(file):
    with open(file, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()

    with open(file, "w") as f:
        for line in lines:
            f.write(f"{line}\n")

    print(f"Processed '{file}'")


def process_tex_files_in_dir(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if os.path.splitext(path)[1] == ".tex":
                remove_trailing_whitespace(path)


# MAIN CODE
process_tex_files_in_dir(DIRECTORY)
