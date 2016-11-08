#! /usr/bin/env python

# Batch Image Resize
# Copyright (c) 2016 dn0z
# https://github.com/dn0z/Batch-Image-Resize

from tkinter import *
from tkinter import ttk


class Application(Frame):
    def create_widgets(self, parent):
        """
        Create the UI widgets
        """

        # Fonts
        font_big = ("Segoe UI", 24)
        font_medium = ("Segoe UI", 10)
        font_small = ("Segoe UI", 8)

        main_container = Frame(self)
        main_container.grid(row=0, column=0, padx=20)

        # Header/title
        label = Label(main_container, text="Batch Image Resize", font=font_big)
        label.grid(row=0, column=0, columnspan=3, pady=10)

        # Browse
        browse_field = ttk.Entry(main_container)
        browse_field.insert(0, "No directory selected")
        browse_field.grid(row=1, column=0, columnspan=2, sticky="we")

        browse_btn = ttk.Button(main_container)
        browse_btn["text"] = "Browse"
        browse_btn.grid(row=1, column=2, sticky="we", padx=2)

        # Resize to
        resize_to_label = Label(main_container, text="Resize to:", font=font_medium)
        resize_to_label.grid(row=2, column=0, sticky="e")

        resize_width_field = ttk.Entry(main_container)
        resize_width_field.grid(row=2, column=1, padx=2)

        resize_height_field = ttk.Entry(main_container)
        resize_height_field.grid(row=2, column=2, padx=2)

        # Save as
        save_as_label = Label(main_container, text="Save as:", font=font_medium)
        save_as_label.grid(row=3, column=0, sticky="e")

        save_as_dropdown = ttk.OptionMenu(main_container, self.export_type, self.export_type.get(), "PNG", "JPEG")
        save_as_dropdown.grid(row=3, column=1, sticky="we")

        # Overwrite original
        overwrite_checkbox = ttk.Checkbutton(main_container,
                                             text="Overwrite original",
                                             variable=self.overwrite_original,
                                             onvalue=1,
                                             offvalue=0)
        overwrite_checkbox.grid(row=4, column=0, columnspan=2, sticky="w")

        # Export
        export_btn = ttk.Button(main_container)
        export_btn["text"] = "Export"
        export_btn.grid(row=3, column=2, rowspan=2, sticky="nesw")

        # Copyright
        copyright_label = Label(main_container, text="Copyright (c) 2016 dn0z | v0.1", font=font_small)
        copyright_label.grid(row=5, column=0, columnspan=3, pady=20)

    def __init__(self, master=None):
        """
        The constructor of the Application class
        """

        Frame.__init__(self, master)
        self.export_type = StringVar(self)
        self.export_type.set("PNG")             # default export type
        self.overwrite_original = IntVar(self)
        self.overwrite_original.set(0)          # default is disabled

        self.grid()
        self.create_widgets(master)


def main():
    root = Tk()

    root.title("Hello world")
    root.geometry("360x210")

    style = ttk.Style()
    style.theme_use("vista")

    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
