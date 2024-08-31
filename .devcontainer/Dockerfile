FROM qmcgaw/latexdevcontainer:latest
WORKDIR /workspace
COPY . .

# Install python
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-venv

# Install needed packages
RUN tlmgr update --self
RUN tlmgr install `cat latex-packages.txt`
RUN texhash
