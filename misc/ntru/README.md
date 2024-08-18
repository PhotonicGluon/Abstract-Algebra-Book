# NTRU Implementation

This is a sample implementation of the NTRU cryptosystem as described in chapter 28 of the book.

You will require Python 3 installed (e.g., Python 3.11).

## Setup

Download the `ntru` files and navigate into the directory in a terminal.
- For example, in Linux/macOS this can be done by executing `cd misc/ntru`.

Create a new virtual environment:

```bash
python3 -m venv venv
```

> [!IMPORTANT]
> If the above command fails, try using `python` instead of `python3`.

Activate the virtual environment.
- Linux/macOS: `source venv/bin/activate`
- Windows: `venv/Scripts/activate`

Install all needed dependencies:

```bash
pip install -r requirements.txt
```

Then run the NTRU example:
```bash
python3 run_ntru.py
```

## Licence

This NTRU implementation is licenced under [The Unlicense](LICENSE).
- Do note that the source code of [the rest of the book](/) is covered by a different license.
