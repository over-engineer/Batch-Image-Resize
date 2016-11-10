from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": "bir.py",
            "icon_resources": [(1, "icon.ico")]
        }
    ]
)
