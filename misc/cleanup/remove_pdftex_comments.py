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

    with open(file, "w") as f:
        for line in final_lines:
            f.write(line)

    print(f"Processed '{file}'")


def remove_pdftex_comments(directory):
    dir_tree = sorted(list(os.walk(directory)), key=lambda tpl: tpl[0])
    for root, _, files in dir_tree:
        files = sorted(files)
        for file in files:
            path = os.path.join(root, file)
            extension = os.path.splitext(path)[1]
            if extension == ".pdf_tex":
                remove_comments(path)
