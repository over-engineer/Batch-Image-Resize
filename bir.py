#! /usr/bin/env python

# Batch Image Resize
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

import imgedit
import os

from enum import Enum
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class SettingsStatus(Enum):
    """
    An enumeration of the settings statuses
    """

    # valid settings
    valid_settings = 1

    # invalid settings
    directory_not_selected = 2
    directory_does_not_exist = 3
    invalid_dimensions = 4


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

    def increase_progress_bar_value(self):
        """
        Increase the progress bar value by one
        """

        self.progress_bar["value"] += 1
        print("Increased progress bar value by one")

    def clear_progress_window(self):
        """
        Clear the progress window
        """

        if self.progress_window is not None:
            self.progress_window.destroy()

    def display_progress_window(self, progress_maximum=100):
        """
        Display the progress window

        :param progress_maximum: The maximum value of the progress bar (default is 100)
        """

        self.clear_progress_window()

        self.progress_window = Toplevel(self)
        self.progress_window.title("Exporting")
        self.progress_window.geometry("300x100")

        Label(self.progress_window,
              text="Exporting images",
              font=("Segoe UI", 16)).pack(fill="x", side="top")

        self.progress_bar = ttk.Progressbar(self.progress_window,
                                            orient="horizontal",
                                            length=280,
                                            mode="determinate")
        self.progress_bar.pack(expand=True, fill="both", side="bottom")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = progress_maximum

        self.progress_window.update()

    def get_settings_status(self):
        """
        Check if our settings are valid (directory exists, width and height are digits etc)

        :return:    The settings status as an enumeration member of the
                    `SettingsStatus` enumeration (e.g. `SettingsStatus.valid_settings`)
        """

        selected_directory = self.selected_directory.get()

        # Check if a directory is selected
        if selected_directory == "No directory selected":
            return SettingsStatus.directory_not_selected

        # Check if the selected directory exists
        if not os.path.isdir(selected_directory):
            return SettingsStatus.directory_does_not_exist

        # Check if width and height are digits
        if (not self.export_properties["width"].get().isdigit()) or \
                (not self.export_properties["height"].get().isdigit()):
            return SettingsStatus.invalid_dimensions

        return SettingsStatus.valid_settings

    def export_button_handler(self):
        """
        The handler of the Export button
        """

        settings_status = self.get_settings_status()

        if settings_status is not SettingsStatus.valid_settings:
            # Invalid settings, display an error message
            error_messages = {
                SettingsStatus.directory_not_selected: [
                    "Invalid directory",
                    "You have to select a directory first"
                ],
                SettingsStatus.directory_does_not_exist: [
                    "Invalid directory",
                    "The directory \"" + self.selected_directory.get() + "\" does not exist"
                ],
                SettingsStatus.invalid_dimensions: [
                    "Invalid dimensions",
                    "Width and height must be integers"
                ],
            }
            messagebox.showerror(*error_messages[settings_status])
        else:
            # Valid settings, confirm settings with the user and export
            if self.confirm_settings():
                num_of_images = imgedit.image_files_in_dir(self.selected_directory.get())
                self.display_progress_window(num_of_images)
                print("Progress window is on screen")

                print("Exporting images")
                result = imgedit.export_all_in_dir(
                    self.selected_directory.get(),
                    int(self.export_properties["width"].get()),
                    int(self.export_properties["height"].get()),
                    self.export_properties["type"].get(),
                    self.overwrite_original.get(),
                    self.increase_progress_bar_value
                )

                self.clear_progress_window()
                print("Progress window is cleared")

                if result:
                    # at this point, we are done with our exports, display a success message
                    messagebox.showinfo("Exports completed",
                                        "All images were exported successfully")
                else:
                    # one or more images failed to export, display a warning
                    messagebox.showwarning("Exports failed",
                                           "One or more images failed to export")

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

    def clear_entry(self, e):
        """
        Clear the entry (gets called when an entry is focused)

        :param e: the event parameter
        :return:
        """
        e.widget.delete(0, "end")

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
        Label(main_container, text="Batch Image Resize", font=font_big).grid(
            row=0, column=0, columnspan=3, pady=8)

        # Browse
        ttk.Entry(main_container, textvariable=self.selected_directory).grid(
            row=1, column=0, columnspan=2, sticky="we", padx=2)

        ttk.Button(main_container, text="Browse", command=self.browse_for_directory).grid(
            row=1, column=2, sticky="we", padx=2)

        # Resize to
        Label(main_container, text="Resize to:", font=font_medium).grid(
            row=2, column=0, sticky="e")

        resize_width_field = ttk.Entry(main_container, textvariable=self.export_properties["width"])
        resize_width_field.grid(row=2, column=1, padx=2)
        resize_width_field.bind("<FocusIn>", self.clear_entry)

        resize_height_field = ttk.Entry(main_container, textvariable=self.export_properties["height"])
        resize_height_field.grid(row=2, column=2, padx=3)
        resize_height_field.bind("<FocusIn>", self.clear_entry)

        # Save as
        Label(main_container, text="Save as:", font=font_medium).grid(
            row=3, column=0, sticky="e")

        self.save_as_dropdown = ttk.OptionMenu(main_container,
                                               self.export_properties["type"],
                                               self.export_properties["type"].get(),
                                               "PNG",
                                               "JPEG")
        self.save_as_dropdown.grid(row=3, column=1, sticky="we", padx=2)

        # Overwrite original
        ttk.Checkbutton(main_container,
                        text="Overwrite original",
                        variable=self.overwrite_original,
                        onvalue=True,
                        offvalue=False,
                        command=self.toggle_save_as_dropdown).grid(
            row=4, column=0, columnspan=2, sticky="w")

        # Export
        ttk.Button(main_container, text="Export", command=self.export_button_handler).grid(
            row=3, column=2, rowspan=2, sticky="nesw", padx=2)

        # Copyright
        Label(main_container, text="Copyright (c) 2016 dn0z | v0.1", font=font_small).grid(
            row=5, column=0, columnspan=3, sticky="we", pady=20)

    def __init__(self, parent=None):
        """
        The constructor of the Application class
        """

        # super class call
        Frame.__init__(self, parent)

        # properties
        self.save_as_dropdown = None
        self.progress_window = None
        self.progress_bar = None

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
