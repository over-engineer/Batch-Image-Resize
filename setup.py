from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": "Batch Image Resize",
            "icon_resources": [(1, "icon.ico")]
        }
    ]
)
