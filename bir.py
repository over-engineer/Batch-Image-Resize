#! /usr/bin/env python

# Batch Image Resize
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

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
        self.export_properties["type"].set("PNG")   # default export type
        self.overwrite_original.set(False)          # default is disabled

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
        if self.overwrite_original:
            confirm_msg += "YES"
        else:
            confirm_msg += "NO"
        confirm_msg += "\nSave as: " + self.export_properties["type"].get()
        confirm_msg += "\n\nAre you sure you want to continue?"

        return messagebox.askyesno("Export confirmation", confirm_msg)

    def export_button_handler(self):
        """
        The handler of the Export button
        """

        print(self.confirm_settings())

    def browse_for_directory(self):
        """
        Browse using `filedialog` for the images directory and store it at `self.selected_directory`
        Gets called when we click the Browse button
        """

        self.selected_directory.set(filedialog.askdirectory())

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

        save_as_dropdown = ttk.OptionMenu(main_container,
                                          self.export_properties["type"],
                                          self.export_properties["type"].get(),
                                          "PNG",
                                          "JPEG")
        save_as_dropdown.grid(row=3, column=1, sticky="we", padx=2)

        # Overwrite original
        overwrite_checkbox = ttk.Checkbutton(main_container,
                                             text="Overwrite original",
                                             variable=self.overwrite_original,
                                             onvalue=True,
                                             offvalue=False)
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

    style = ttk.Style()
    style.theme_use("vista")

    app = Application(parent=root)
    app.mainloop()


if __name__ == "__main__":
    main()
