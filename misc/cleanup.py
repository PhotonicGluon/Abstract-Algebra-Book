# IMPORTS
from cleanup import strip_trailing_whitespace, remove_pdftex_comments

# CONSTANTS
DIRECTORY = ".."

# MAIN PROCESSES
print("=" * 50)
print("Stripping trailing whitespace from files.".upper())
print("=" * 50)
strip_trailing_whitespace(DIRECTORY)
print()

print("=" * 50)
print("Removing PDFTEX Comments".upper())
print("=" * 50)
remove_pdftex_comments(DIRECTORY)
print()

print("Done!")
