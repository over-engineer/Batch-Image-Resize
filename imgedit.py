#! /usr/bin/env python

# Batch Image Resize - imgedit module
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

import os
import PIL.Image


def is_image(filename):
    """
    Checks if a filename is an image (png, jpg or jpeg, case insensitive)

    :param filename: The filename (as a string)
    :return: `True` if the given filename is an image, or `False` if it's not
    """

    file = filename.lower()
    return file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg")


def get_filename_with_type(filename, file_type, suffix=""):
    """
    Get a filename and return it with the given suffix and the correct file extension for the given type

    :param filename: The filename (e.g. "image_file.jpg")
    :param file_type: The file type (e.g. "PNG")
    :param suffix: An optional string to place between the name and the extension of the file (default is "")
    :return: the filename with the correct extension for the given type (e.g. "image_file.png")
    """

    extension = filename.split(".")[-1]
    return filename[:-(len(extension) + 1)] + suffix + "." + file_type.lower()


def export_file(path, name, width, height, export_type, overwrite):
    """
    Open, resize and save an image with the given properties

    :param path: The path to the directory where the image is located (without the image filename)
    :param name: The filename of the image we want to export
    :param width: The new width we want to resize to
    :param height: The new height we want to resize to
    :param export_type: The file type we want to save to (we ignore it if `overwrite` is `True`)
    :param overwrite: Whether we want to overwrite the original files or not
    """

    img_path = os.path.join(path, name)

    # open the given image and resize it
    img = PIL.Image.open(img_path)
    img = img.resize((width, height), PIL.Image.ANTIALIAS)

    # set the destination image file we want to save
    dest_img_name = get_filename_with_type(name, export_type, "_resize")
    if overwrite:
        dest_img_name = name

    # save the resized/converted image
    img.save(os.path.join(path, dest_img_name))


def export_all_in_dir(selected_dir, width, height, export_type, overwrite):
    """
    Export all the images in the selected directory

    When `self.init_export()` is called, everything is ready to resize and export images
    This loops through all the files in the given directory and calls `self.export_file()`
    for the actual opening, resizing and saving of the files

    :param selected_dir: The path to the directory containing all the images to resize
    :param width: The new width we want to resize to
    :param height: The new height we want to resize to
    :param export_type: The file type we want to save to (we ignore it if `overwrite` is `True`)
    :param overwrite: Whether we want to overwrite the original files or not
    :return: `True` if all images were exported successfully or `False` if there was an error
    """

    for path, subdirs, files in os.walk(selected_dir):
        for name in files:
            if is_image(name):
                # TODO: Add a new window with a progress bar while exporting images
                export_file(path, name, width, height, export_type, overwrite)

    return True
