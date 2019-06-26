# Batch Image Resize

![screenshot](screenshot.png?raw=true)

### What is this?
This is a simple and open source tool written in
[Python](https://www.python.org/) to resize multiple images at once.

### Usage
Get the latest [release](https://github.com/over-engineer/Batch-Image-Resize/releases)
and run `bir.exe`. Click **Browse** and select the folder containing
the images you want to resize. Then enter the width, the height and
click on **Export**.

You can also select whether you want your images to be saved as a PNG
or a JPEG file or you can check the **Overwrite original** checkbox
to overwrite the original files.

### How to build it?
1. Make sure you have installed [Python 3](https://www.python.org/downloads/)
2. Get these:

    | Module                                                | Installation command      |
    | ----------------------------------------------------- | ------------------------- |
    | [Pillow](https://pypi.python.org/pypi/Pillow/3.4.2)   | `pip install Pillow`      |
    | [enum34](https://pypi.python.org/pypi/enum34)         | `pip install enum34`      |
    | [py2exe](https://pypi.python.org/pypi/py2exe/)        | `pip install py2exe`      |
    | [setuptools](https://pypi.python.org/pypi/setuptools) | `pip install setuptools`  |

3. Run `build.bat`

### Version info
I've tested this only on Windows 10. If you don't use Windows and you're
experienced with Python, it should be trivial to modify it to support
other operating systems (OS X, Linux).

### License
The MIT License, check the `LICENSE` file.
