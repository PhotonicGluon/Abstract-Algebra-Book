# IMPORTS
import os


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


def strip_trailing_whitespace(directory):
    dir_tree = sorted(list(os.walk(directory)), key=lambda tpl: tpl[0])
    for root, _, files in dir_tree:
        files = sorted(files)
        for file in files:
            path = os.path.join(root, file)
            extension = os.path.splitext(path)[1]
            if extension in {".tex", ".bib"}:
                remove_trailing_whitespace(path)
