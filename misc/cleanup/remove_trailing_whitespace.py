# IMPORTS
import os


# FUNCTIONS
def remove_trailing_whitespace(file):
    changed_file = False
    with open(file, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        original = lines[i]
        lines[i] = f"{lines[i].rstrip()}\n"

        if lines[i] != original:
            changed_file = True

    if changed_file:
        with open(file, "w") as f:
            for line in lines:
                f.write(line)

    return changed_file


def strip_trailing_whitespace(directory):
    dir_tree = sorted(list(os.walk(directory)), key=lambda tpl: tpl[0])
    for root, _, files in dir_tree:
        files = sorted(files)
        for file in files:
            path = os.path.join(root, file)
            extension = os.path.splitext(path)[1]
            if extension in {".tex", ".bib"}:
                if remove_trailing_whitespace(path):
                    print(f"Removed trailing whitespace from '{path}'")
