# Logic Simulatior App

### Goal
The aim of our project is to design a logic simulator. The logic network is defined by a circuit definition text file which is to be uploaded by the user. A detailed specification for the language of the circuit definition, using the Extended Backus Naur Form (EBNF) notation, has also been provided. 



### Installation

You can install required packages by running the following command


```python
python -m pip install --upgrade pip
pip install -r requirements.txt
```
The packages should be automatically installed in the environment. Alternatively, you can install packages following the requirement list below.


## Requirements

```python
atomicwrites==1.4.0
attrs==21.4.0
colorama==0.4.4
iniconfig==1.1.1
numpy==1.22.3
packaging==21.3
Pillow==9.1.0
pluggy==1.0.0
py==1.11.0
python==3.7.13
pycodestyle==2.8.0
pydocstyle==6.1.1
pyparsing==3.0.9
pytest==7.1.2
six==1.16.0
snowballstemmer==2.2.0
tomli==2.0.1
wxPython==4.1.1

```

## Installing PyOpenGL
# Windows
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

# Linux
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

Start by click Menu, then choose Open. Upload your circuit definition file from your local computer.

Choose the number of cycles to run 

## Contributors
This project is developed by Nikodem, Youjing and Gleb in collaboration.

