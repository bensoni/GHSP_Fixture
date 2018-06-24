## Python & PyQt5 Installation 
Install the following dependencies for Python 3 and Qt5.


[Python 3.6.5](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)

`pip3 install PyQt5`

## Create GUI
Create GUI using Qt Designer. This will create the .ui file which can later be converted to a python file.

Command to convert .ui to .py
```python
pyuic5 -x noise.ui -o noise.py
```

`pyuic5` should be installed along with Python.


## python-can Installation

https://python-can.readthedocs.io/en/2.1.0/installation.html

'pip install python-can' 


The installation comes with a frame logger module:

https://python-can.readthedocs.io/en/2.1.0/bin.html

I got it working with the VN1630A by calling this in command line: 'python -m can.logger -c 0 -i vector'

-c is the channel, in this case it's Channel 1 on the CAN case
-v is the backend interface to use, which in this case is vector.




