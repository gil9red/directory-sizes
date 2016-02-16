# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [
    Executable(
        'directory_sizes_gui.py',
        base='Win32GUI',
    )
]

setup(name='directory-sizes',
      version='0.1',
      description='directory-sizes',
      executables=executables
      )
