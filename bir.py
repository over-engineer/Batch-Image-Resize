#! /usr/bin/env python

# Batch Image Resize
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

import imgedit

import os
import queue
import threading

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

    def exporting_interval(self, q):
        """
        Run @ a 100 ms interval using tkinter's `.after()` while the exporting thread is running

        In order to keep tkinter's event loop running, our image editing code runs
        on a different thread. We look at `num_of_exported_images`, `images_to_export`
        and the result of our `q` queue (which represents if our code failed to
        open, resize and/or save any images) to check the status of the thread

        Once everything is done, we will get the operation's result using `q.get()`
        and we will call the `self.exported()` (passing the result) to handle the rest

        :param q: our `Queue` instance
        """

        run_the_interval = True

        if self.img_edit.num_of_images_to_export is not None:
            exported_images = self.img_edit.num_of_exported_images
            images_to_export = self.img_edit.num_of_images_to_export

            # update progress bar
            self.progress_bar["value"] = exported_images
            self.progress_bar["maximum"] = images_to_export

            # check if we are done
            if exported_images >= images_to_export:
                run_the_interval = False
                self.exported(q.get())

        if run_the_interval:
            self.after(100, self.exporting_interval, q)

    def exported(self, result):
        """
        Display a success or an error message depending on the operation's result

        Close the progress window first, then display the message box

        :param result:  the result of the exports (`True` if everything is okay,
                        or `False` if there was an error)
        """

        self.clear_progress_window()

        if result:
            messagebox.showinfo("Exports completed",
                                "All images were exported successfully")
        else:
            messagebox.showwarning("Exports failed",
                                   "One or more images failed to export")

    def clear_progress_window(self):
        """
        Clear the progress window
        """

        if self.progress_window is not None:
            self.progress_window.destroy()

    def display_progress_window(self):
        """
        Display the progress window
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

    def display_about(self):
        """
        Display the about window (with a scrollbar)
        """

        if self.about_window is not None:
            self.about_window.destroy()

        # Set the window
        self.about_window = Toplevel(self)
        self.about_window.title("About")
        self.about_window.geometry("400x300")

        # Header
        header_imagetk = imgedit.HelpingMethods.get_imagetk("about_header.png")

        header_label = Label(self.about_window, width=400, height=150)
        header_label.pack(side="top", fill="both")
        header_label.configure(image=header_imagetk)
        header_label.image = header_imagetk

        # Text with scrollbar
        t = Text(self.about_window, width=300, height=200, font=("Courier New", 11))

        scrollbar = ttk.Scrollbar(self.about_window)
        scrollbar.pack(side="right", fill="y")
        t.pack(side="left", fill="y")
        scrollbar.config(command=t.yview)
        t.config(yscrollcommand=scrollbar.set)

        t.insert(END,
                 "Batch Image Resize (v0.1)"
                 "\n"
                 "\nDeveloped by dn0z"
                 "\nhttps://github.com/dn0z/Batch-Image-Resize"
                 "\n"
                 "\nThe icon is designed by Vecteezy "
                 "(https://iconfinder.com/icons/532771) "
                 "and it is licensed under Creative Commons "
                 "(Attribution-Share Alike 3.0 Unported)"
                 "\n\n"
                 "The MIT License (MIT)"
                 "\n\n"
                 "Copyright (c) 2016 dn0z"
                 "\n\n"
                 "Permission is hereby granted, free of charge, to any person obtaining a copy"
                 "of this software and associated documentation files (the \"Software\"), to deal"
                 "in the Software without restriction, including without limitation the rights"
                 "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell"
                 "copies of the Software, and to permit persons to whom the Software is"
                 "furnished to do so, subject to the following conditions:"
                 "\n\n"
                 "The above copyright notice and this permission notice shall be included in all"
                 "copies or substantial portions of the Software."
                 "\n\n"
                 "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR"
                 "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,"
                 "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE"
                 "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
                 "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,"
                 "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE"
                 "SOFTWARE.")

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
                self.display_progress_window()

                # call `ImgEdit.export_all_in_dir` as the target of a new thread
                # and put the final result in a `Queue`
                q = queue.Queue()
                my_thread = threading.Thread(target=self.img_edit.export_all_in_dir,
                                             args=(self.selected_directory.get(),
                                                   int(self.export_properties["width"].get()),
                                                   int(self.export_properties["height"].get()),
                                                   self.export_properties["type"].get(),
                                                   self.overwrite_original.get(),
                                                   q)
                                             )
                my_thread.start()
                self.exporting_interval(q)

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

        # About
        ttk.Button(main_container, text="About", command=self.display_about).grid(
            row=5, column=2, sticky="we")

        # Copyright
        Label(main_container, text="Copyright (c) 2016 dn0z | v0.1", font=font_small).grid(
            row=5, column=0, columnspan=2, sticky="we", pady=20)

    def __init__(self, parent=None):
        """
        The constructor of the Application class
        """

        # super class call
        Frame.__init__(self, parent)

        # properties
        self.about_window = None
        self.save_as_dropdown = None
        self.progress_window = None
        self.progress_bar = None

        self.img_edit = imgedit.ImgEdit()

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
