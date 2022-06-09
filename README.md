# Logic Simulatior App

## Goal
The aim of our project is to design a logic simulator. The logic network is defined by a circuit definition text file which is to be uploaded by the user. A detailed specification for the language of the circuit definition, using the Extended Backus Naur Form (EBNF) notation, has also been provided in `grammer.ebnf`. The functionality of the logic simulator is to simulate the operations of an electrical circuit computationally, which provides a time-saving way to test the functionalities of circuits designed.



## Installation to run on Linux

A conda virtual environment is recommended to run the software to ensure the correct dependencies are included. The list of requirements is provides in **requirements.txt**. The enviroment can be created with the required dependencies by running the following bash commands using anaconda shell within the project directory.


```bash
conda create --name <name_of_environment> --file requirements.txt
source activate <name of environment>
```
The packages should be automatically installed in the environment. Note that the environment creation can take some time to install all the dependencies.


## Installing PyOpenGL
### Windows
Download an unofficial Windows binary of PyOpenGL from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl). You need to make sure you download the compatible version with your environment.  

Then navigate to the folder containing the downloaded .whl file and run the command 
```python
pip install PyOpenGL-***.whl
```

# Mac
In your Python terminal, run the command 
```python
pip install PyOpenGL
```
If you are using Anaconda, run the command
```python
conda install PyOpenGL
```
For Anaconda distributions only, type 
```python
conda install python.app. 
```
To allow Anaconda to access graphics, scripts must be run using the command pythonw filename.py rather than the usual python3 filename.py.

### Linux
On most Linux distributions, PyOpenGL can be installed as a system package.

## Run

To launch the command-line user interface:

```python
python -m logsim -c path_to_definition_file

```

To use the logsim App Graphical User Interface(GUI):

```python
python logsim.py
```
### GUI Simulation Actions
Start by clicking `Menu`, then choose `Open`. Upload your circuit definition file from your local computer.
Set the number of cycles to run in the spin control box and click `run` to see the signal displayed.
Click `continue` to run more cycles from the current point or `Rerun` to start the simulation fresh. Click `Clear Console` to clear the user messages displayed in the console output.

### GUI Switch and Monitor Settings
To change the signals to be dislayed, click `Choose Monitor` and select the signals you wish to display on screen by ticking the checkbox near them. To change the state of the switches in the network, click `Choose Switch` and select the switches you wish to be in the state of OPEN.

### GUI File Functions
Save the canvas plot as an image file by clicking `Menu`, then choose `Save Canvas`. Save the text file containing the console output messages by cllicking `Menu`, then choose `Save Console`. A dialogue box will pop up where you can choose the local destination for the canvas image or text file to be saved to.

## Code Conventions
All files are fully compliant with PEP 8 and PEP 257. Code styles are autoformatted with `black` and checked with `pycodestyle` and `pydocstyle`.

## Contributors
This project is developed by Nikodem, Youjing and Gleb in collaboration.

