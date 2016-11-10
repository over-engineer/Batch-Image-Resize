@echo off
python setup.py py2exe
if exist dist (
    copy about_header.png dist/about_header.png
)
