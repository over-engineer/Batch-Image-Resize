#! /usr/bin/env python

# Batch Image Resize - imgedit module
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

import os
import PIL.Image
import PIL.ImageTk


class HelpingMethods(object):
    @staticmethod
    def is_image(filename):
        """
        Checks if a filename is an image (png, jpg or jpeg, case insensitive)

        :param filename: The filename (as a string)
        :return: `True` if the given filename is an image, or `False` if it's not
        """

        file = filename.lower()
        return file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg")

    @staticmethod
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

    @staticmethod
    def get_imagetk(filename):
        """
        Open an image and return it as an `ImageTk` object

        :param filename: the filename of the image we want to open
        :return: the `ImageTk` object
        """

        return PIL.ImageTk.PhotoImage(PIL.Image.open(filename))


class ImgEdit(object):
    def export_file(self, path, name, width, height, export_type, overwrite):
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

        # set the destination image file we want to save
        dest_img_name = HelpingMethods.get_filename_with_type(name, export_type, "_resize")
        if overwrite:
            dest_img_name = name

        try:
            # open the given image, resize and save it
            img = PIL.Image.open(img_path)
            img = img.resize((width, height), PIL.Image.ANTIALIAS)
            img.save(os.path.join(path, dest_img_name))
        except IOError:
            return False

        return True

    def export_all_in_dir(self, selected_dir, width, height, export_type, overwrite, q):
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

        # reset default values
        self.num_of_exported_images = 0
        self.num_of_images_to_export = None

        # loop through all the files in the given directory and store the
        # path and the filename of image files in a list
        images = []
        for path, subdirs, files in os.walk(selected_dir):
            for name in files:
                if HelpingMethods.is_image(name):
                    images.append({
                        "path": path,
                        "name": name
                    })
        self.num_of_images_to_export = len(images)

        # loop through the images list to open, resize and save them
        all_exported_successfully = True
        for img in images:
            # export and check if everything went okay
            exported_successfully = self.export_file(img["path"], img["name"], width, height, export_type, overwrite)
            if not exported_successfully:
                all_exported_successfully = False

            self.num_of_exported_images += 1

        q.put(all_exported_successfully)

    def __init__(self):
        self.num_of_exported_images = 0
        self.num_of_images_to_export = None
