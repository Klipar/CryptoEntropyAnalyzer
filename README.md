# Crypto Entropy Analyzer 

A program for **analyzing** the internal entropy of a file, which can be useful when searching for **cryptocontainers** or other encrypted files that have been encrypted using algorithms resistant to statistical analysis.

![Python 3.6](https://img.shields.io/badge/Python-3.6-blue?logo=python)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
## Demo

![Demo of project](demo/demo.GIF)

## Usage/Examples
The program can be used in the context of **digital forensics**, specifically for searching encrypted files and **cryptocontainers**. It allows for the detection of files with suspiciously **high levels of entropy** both in file fragments and in whole files. Another use case involves **analyzing cryptographic algorithms** for resistance to statistical analysis, which enables the assessment of their effectiveness in data protection and the **identification of potential vulnerabilities** in the algorithms.
## Features


- Flexible and user-friendly interaction interface
- Creation of an entropy distribution graph in the file
- Ability to set a custom graph size
- Calculation of percentage values of entropy
- And many other metrics for file analysis ✨
## Installation

1. Make sure you have `python` version >= **3.6**:
```bash
python --version
```
2. Clone the repository by running this command:
```bash
git clone https://github.com/Klipar/CryptoEntropyAnalyzer.git
cd CryptoEntropyAnalyzer
```
3. **Optional**. Create a virtual serialization. 
If you are using `bash`:
```bash
python -m venv .venv && source .venv/bin/activate
```
Or if you use `fish`:
```fish
python -m venv .venv && source .venv/bin/activate.fish
```
After finishing the use of the program, you can **exit** the **virtual environment** by entering the following command (for `fish` & `bash`):
```
deactivate
```
4. Install the necessary libraries by running the command:
``` bash
pip install -r requirement.txt
```
5. It's **done**! 🎉 Just type to launch the program:
``` bash
python main.py
```
You can also specify the file name to be scanned when starting the program by adding the file name to the command:
``` bash
python main.py path/to/your/file
```