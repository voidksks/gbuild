"""
GBUILD

A python package for compiling C/C++ to executables

This package still undone, so some functionalities need to be finished.
"""

import _log
from _command import _cmd
import os
import sys
from typing import Iterable

CPP_SUFFIXES = (".cpp", ".cxx", ".cc", ".ipp", ".ixx")
C_SUFFIXES = (".c",)
SOURCE_SUFFIXES = CPP_SUFFIXES + C_SUFFIXES

_command = _cmd()

def _try_compile(args: list[str]):
    import subprocess
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        _log.log_error("Compilation error...")
    except OSError:
        _log.log_error("Cannot run the compilation command...")

def search_dir(target: str, path=".", recursive=False):
    """
    Search a target directory and return True if found otherwise False
    """
    with os.scandir(path) as entries:
        for item in entries:
            if item.is_dir() and item.name == target:
                return True
            if recursive and item.is_dir():
                search_dir(target, item.path)
    return False

def search_file(target: str, path=".", recursive=False):
    """
    Search a target file and return True if found other wise False
    """
    with os.scandir(path) as entries:
        for item in entries:
            if item.is_file() and item.name == target:
                return True
            if recursive and item.is_dir():
                search_dir(target, item.path)
        return False

def is_empty(iterable: Iterable):
    return len(iterable) == 0

def get_sources(path=".", recursive=False):
    """
    Search for valid C/C++ source code and return a list of path to the files
    """
    sources = []
    with os.scandir(path) as entries:
        for item in entries:
            if item.is_file() and item.name.endswith(SOURCE_SUFFIXES):
                sources.append(item.path)
            if recursive and item.is_dir():
                get_sources(item.path)
    _command.source_files = sources
    return sources

def set_compiler(compiler: str):
    if not is_empty(compiler):
        _command.compiler = compiler

def set_flags(*flags):
    _command.flags = list(flags)

def set_executable_name(name: str):
    if sys.platform == "win32":
        name += ".exe"
    _command.out = name

def build_exacutable(target: str, buildpath="."):
    """
    Build an executable to an given build path if specified
    """
    if is_empty(_command.compiler):
        _log.log_error("Compiler was not specified...")
        return
    if buildpath != "." and search_dir(buildpath):
        os.makedirs(buildpath, exist_ok=True)
    cmd = [_command.compiler, *_command.flags, *_command.source_files, *_command.includes]
    if _command.out or target:
        cmd += ["-o", f"{buildpath}/{target}"]
        _try_compile(cmd)
    else:
        _log.log_error("Executable name was not defined")
