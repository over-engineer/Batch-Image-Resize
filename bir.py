#! /usr/bin/env python

# Batch Image Resize
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

import os
import PIL.Image
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class Application(Frame):
    def set_properties_defaults(self):
        """
        Set the default values for our class properties
        """

        self.selected_directory.set("No directory selected")
        self.export_properties["width"].set("width px")
        self.export_properties["height"].set("height px")
        self.export_properties["type"].set("PNG")  # default export type
        self.overwrite_original.set(False)  # default is disabled

    def confirm_settings(self):
        """
        Display a confirmation dialog with the current settings

        :return:    whether we want to continue exporting or cancel it
                    Return `True` if we want to export, or `False` if we don't
        """

        confirm_msg = "You are about to export with these settings:"
        confirm_msg += "\nDirectory: " + self.selected_directory.get()
        confirm_msg += "\nResize images to: " + self.export_properties["width"].get()
        confirm_msg += "x" + self.export_properties["height"].get() + " px"
        confirm_msg += "\nOverwrite original: "
        if self.overwrite_original.get():
            confirm_msg += "YES"
        else:
            confirm_msg += "NO"
        confirm_msg += "\nSave as: " + self.export_properties["type"].get()
        confirm_msg += "\n\nAre you sure you want to continue?"

        return messagebox.askyesno("Export confirmation", confirm_msg)

    def is_image(self, filename):
        """
        Checks if a filename is an image (png, jpg or jpeg, case insensitive)

        :param filename: The filename (as a string)
        :return: `True` if the given filename is an image, or `False` if it's not
        """

        file = filename.lower()
        return file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg")

    def get_filename_with_type(self, filename, file_type, suffix=""):
        """
        Get a filename and return it with the given suffix and the correct file extension for the given type

        :param filename: The filename (e.g. "image_file.jpg")
        :param file_type: The file type (e.g. "PNG")
        :param suffix: An optional string to place between the name and the extension of the file (default is "")
        :return: the filename with the correct extension for the given type (e.g. "image_file.png")
        """

        extension = filename.split(".")[-1]
        return filename[:-(len(extension) + 1)] + suffix + "." + file_type.lower()

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

        # open the given image and resize it
        img = PIL.Image.open(img_path)
        img = img.resize((width, height), PIL.Image.ANTIALIAS)

        # set the destination image file we want to save
        dest_img_name = self.get_filename_with_type(name, export_type, "_resized")
        if overwrite:
            dest_img_name = name

        # save the resized/converted image
        img.save(os.path.join(path, dest_img_name))

    def init_export(self):
        """
        Export all the images in the selected directory

        When `self.init_export()` is called, everything is ready to resize and export images
        This loops through all the files in the given directory and calls `self.export_file()`
        for the actual opening, resizing and saving of the files
        """

        # final export settings
        directory_path = self.selected_directory.get()
        width = int(self.export_properties["width"].get())
        height = int(self.export_properties["height"].get())
        export_type = self.export_properties["type"].get()
        overwrite = self.overwrite_original.get()

        # loop through the files in the given directory and export any image files
        for path, subdirs, files in os.walk(directory_path):
            for name in files:
                if self.is_image(name):
                    # TODO: Add a new window with a progress bar while exporting images
                    self.export_file(path, name, width, height, export_type, overwrite)

        # at this point, we are done with our exports, display a success message
        messagebox.showinfo("Exports completed", "All images were exported successfully")

    def export_button_handler(self):
        """
        The handler of the Export button
        """

        selected_directory = self.selected_directory.get()

        # Check if we are ready to export
        if selected_directory == "No directory selected":
            # No directory selected
            messagebox.showerror("Invalid directory", "You have to select a directory first")
        else:
            # Directory selected
            if not os.path.isdir(selected_directory):
                # Directory does not exist
                messagebox.showerror("Invalid directory",
                                     "The directory \"" + selected_directory + "\" does not exist")
            else:
                # Directory exists
                if (not self.export_properties["width"].get().isdigit()) or \
                        (not self.export_properties["height"].get().isdigit()):
                    # Dimensions are not digits
                    messagebox.showerror("Invalid dimensions",
                                         "Width and height must be integers")
                else:
                    # Dimensions are digits
                    if self.confirm_settings():
                        # Settings confirmed, we are ready to export
                        self.init_export()

    def browse_for_directory(self):
        """
        Browse using `filedialog` for the images directory and store it at `self.selected_directory`
        Gets called when we click the Browse button
        """

        self.selected_directory.set(filedialog.askdirectory())

    def toggle_save_as_dropdown(self):
        """
        Change the state of `self.save_as_dropdown` based on `self.overwrite_original`

        The dropdown should be enabled when `self.overwrite_original` is set to `False`
        and disabled when `self.overwrite_original` is set to `True`
        """

        if self.overwrite_original.get():
            self.save_as_dropdown.configure(state="disabled")
        else:
            self.save_as_dropdown.configure(state="enabled")

    def create_widgets(self):
        """
        Create the UI elements
        """

        # Fonts
        font_big = ("Segoe UI", 24)
        font_medium = ("Segoe UI", 10)
        font_small = ("Segoe UI", 8)

        main_container = Frame(self)
        main_container.grid(row=0, column=0, padx=20)

        # Header/title
        label = Label(main_container, text="Batch Image Resize", font=font_big)
        label.grid(row=0, column=0, columnspan=3, pady=8)

        # Browse
        browse_field = ttk.Entry(main_container, textvariable=self.selected_directory)
        browse_field.grid(row=1, column=0, columnspan=2, sticky="we", padx=2)

        browse_btn = ttk.Button(main_container, text="Browse", command=self.browse_for_directory)
        browse_btn.grid(row=1, column=2, sticky="we", padx=2)

        # Resize to
        resize_to_label = Label(main_container, text="Resize to:", font=font_medium)
        resize_to_label.grid(row=2, column=0, sticky="e")

        resize_width_field = ttk.Entry(main_container, textvariable=self.export_properties["width"])
        resize_width_field.grid(row=2, column=1, padx=2)

        resize_height_field = ttk.Entry(main_container, textvariable=self.export_properties["height"])
        resize_height_field.grid(row=2, column=2, padx=3)

        # Save as
        save_as_label = Label(main_container, text="Save as:", font=font_medium)
        save_as_label.grid(row=3, column=0, sticky="e")

        self.save_as_dropdown = ttk.OptionMenu(main_container,
                                          self.export_properties["type"],
                                          self.export_properties["type"].get(),
                                          "PNG",
                                          "JPEG")
        self.save_as_dropdown.grid(row=3, column=1, sticky="we", padx=2)

        # Overwrite original
        overwrite_checkbox = ttk.Checkbutton(main_container,
                                             text="Overwrite original",
                                             variable=self.overwrite_original,
                                             onvalue=True,
                                             offvalue=False,
                                             command=self.toggle_save_as_dropdown)
        overwrite_checkbox.grid(row=4, column=0, columnspan=2, sticky="w")

        # Export
        export_btn = ttk.Button(main_container, text="Export", command=self.export_button_handler)
        export_btn.grid(row=3, column=2, rowspan=2, sticky="nesw", padx=2)

        # Copyright
        copyright_label = Label(main_container, text="Copyright (c) 2016 dn0z | v0.1", font=font_small)
        copyright_label.grid(row=5, column=0, columnspan=3, sticky="we", pady=20)

    def __init__(self, parent=None):
        """
        The constructor of the Application class
        """

        # super class call
        Frame.__init__(self, parent)

        # properties
        self.save_as_dropdown = None

        self.selected_directory = StringVar(self)
        self.overwrite_original = BooleanVar(self)
        self.export_properties = {
            "width": StringVar(self),
            "height": StringVar(self),
            "type": StringVar(self)
        }

        # call methods
        self.grid()
        self.set_properties_defaults()
        self.create_widgets()


def main():
    """
    The main function
    """

    root = Tk()

    root.title("Batch Image Resize")
    root.geometry("360x210")
    root.resizable(0, 0)

    style = ttk.Style()
    style.theme_use("vista")

    app = Application(parent=root)
    app.mainloop()


if __name__ == "__main__":
    main()
