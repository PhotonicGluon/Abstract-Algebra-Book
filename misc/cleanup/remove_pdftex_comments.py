# IMPORTS
import os


# FUNCTIONS
def remove_comments(file):
    with open(file, "r") as f:
        lines = f.readlines()

    final_lines = []
    for i in range(len(lines)):
        if not lines[i].startswith("%"):
            final_lines.append(lines[i])

    if lines != final_lines:
        with open(file, "w") as f:
            for line in final_lines:
                f.write(line)

    return lines != final_lines


def remove_pdftex_comments(directory):
    dir_tree = sorted(list(os.walk(directory)), key=lambda tpl: tpl[0])
    for root, _, files in dir_tree:
        files = sorted(files)
        for file in files:
            path = os.path.join(root, file)
            extension = os.path.splitext(path)[1]
            if extension == ".pdf_tex":
                if remove_comments(path):
                    print(f"Removed comments from '{path}'")
