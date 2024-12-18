# BCH Transmission Simulation

## Overview
This project simulates BCH (Bose-Chaudhuri-Hocquenghem) error-correcting codes, visualizes the results, and provides tools to analyze simulated transmissions. It includes scripts for generating BCH codes, running transmission simulations, and plotting the results.

# Setup guide
1. Install Python from [python.org](https://www.python.org/).
2. Open a terminal/command prompt, and navigate to the BCH_transcoder folder.
3. Run the following commands in console:
```
python -m venv my_project_env       # Create a virtual environment
my_project_env\Scripts\activate     # Activate it (Windows version)
source my_project_env/bin/activate  # Activate it (Linux/Mac version)
pip install -r requirements.txt     # Install dependencies
```

# Usage guide
a) Run one of the provided BCH code files, for example:
```
python bch7_4.py
```
b) Run the transmission simulation by typing:
```
python transmission_simulation.py
```
It will write the results to a few .csv files, which can be plotted to plots in .csv format by running:
```
python plot_results.py
```
