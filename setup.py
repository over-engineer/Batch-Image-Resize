from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": "LoL Skype DnD.py",
            "icon_resources": [(1, "icon.ico")]
        }
    ]
)
