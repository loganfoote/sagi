# SAGI summer school python lectures and exercises
Put introduction here

## Installation

To get started with this project, you need to have [list any prerequisites] installed on your machine. Follow the instructions below to set up the project.

## Setting Up Anaconda

1. **Download Anaconda:**
   - Visit the [Anaconda Distribution](https://www.anaconda.com/products/distribution) page.
   - Download the installer for your operating system (Windows, macOS, or Linux).

2. **Install Anaconda:**
   - Run the downloaded installer and follow the prompts.
   - During installation, make sure to check the option to add Anaconda to your PATH environment variable.

3. **Verify Installation:**
   - Open a terminal (or Anaconda Prompt on Windows) and type:
     ```sh
     conda --version
     ```
   - You should see the version of Anaconda printed out, confirming that the installation was successful.

## Running Jupyter Notebooks

1. **Create a Conda Environment:**
   - In your terminal, create a new Conda environment by running:
     ```sh
     conda create -n sagi python=3.11
     ```
   - `sagi` is the name of the environment we will use for the lessons.

2. **Activate the Environment:**
   - Activate your environment by running:
     ```sh
     conda activate myenv
     ```

3. **Install Jupyter Notebook:**
   - With your environment activated, install Jupyter Notebook by running:
     ```sh
     conda install jupyter
     ```

4. **Start Jupyter Notebook:**
   - In your terminal, start Jupyter Notebook by running:
     ```sh
     jupyter notebook
     ```
   - This will open Jupyter Notebook in your default web browser.

5. **Open and Run Notebooks:**
   - Navigate to the notebook files in this repository and open them in Jupyter Notebook.
   - You can now run the cells in the notebook to execute the code.

## Install this repository -> This is a work in progress

1. **Activate the Environment**
- Activate your environment by running:
  ```sh
  conda activate myenv
  ```
2. **Clone this repository:**
   ```sh
   git clone https://github.com/loganfoote/citkid
   ```
3. **Navigate to the repository directory**
4. **Install the package using pip:**
   ```sh
   python -m pip install .
   ```
