# BCH Transmission Simulation

## Overview
This project simulates BCH (Bose-Chaudhuri-Hocquenghem) error-correcting codes, visualizes the results, and provides tools to analyze simulated transmissions. It includes scripts for generating BCH codes, running transmission simulations, and plotting the results.

---

## Setup Guide

### **Option 1: Using Terminal**

1. **Install Python**  
   Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).

2. **Navigate to the Project Folder**  
   Open a terminal or command prompt, and navigate to the `BCH_transcoder` folder:
   ```bash
   cd path/to/BCH_transcoder
   ```

3. **Set Up Virtual Environment and Dependencies**  
   Run the following commands:
   ```bash
   # Create a virtual environment
   python -m venv my_project_env

   # Activate the virtual environment
   my_project_env\Scripts\activate   # For Windows
   source my_project_env/bin/activate  # For Linux/Mac

   # Install required libraries
   pip install -r requirements.txt
   ```

### **Option 2: Using an IDE**

1. **Install Python**  
   Ensure Python is installed on your system.

2. **Open the Project in Your IDE**  
   Open the `BCH_transcoder` folder as a project in your preferred IDE (such as PyCharm, VS Code, or any other).

3. **Set Up Virtual Environment and Dependencies**  
   - **For PyCharm**:
     - You should be prompted to install the dependancies from the requirements.txt file. Press OK.
     - If the method above didn't work, press Alt+F12 to open the integrated terminal. Run `pip install -r requirements.txt`.
   - **For VS Code**:
     - Use the `Python` extension and select the interpreter by clicking on the Python version in the status bar.
     - Open the integrated terminal and run `pip install -r requirements.txt`, or use the IDE’s graphical package manager.

---

## Usage Guide

### 1. Explore individual BCH Codes  
Run one of the provided BCH code scripts to see how they handle the error-correcting process. For example:
```bash
python bch7_4.py
```

### 2. Simulate Transmission  
Run the transmission simulation script to simulate data transmission:
```bash
python transmission_simulation.py
```
This script will generate results as `.csv` files.

### 3. Plot Results  
Visualize the transmission results by running:
```bash
python plot_results.py
```
This script processes the `.csv` files generated in the previous step and creates plots in `.svg` format.

---

## Notes
- Ensure you activate the virtual environment before running any scripts if using the terminal.
- All `.csv` and `.svg` files will be created in the project directory.
- If you encounter any issues, ensure all dependencies are installed correctly using `pip install -r requirements.txt`.

