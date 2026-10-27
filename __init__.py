import os
import log
from command import cmd

CPP_SUFFIXES = (".cpp", ".cxx", ".cc", ".ipp", ".ixx")
C_SUFFIXES = (".c",)
SOURCE_SUFFIXES = CPP_SUFFIXES + C_SUFFIXES

def _try_compile(args: list[str]):
    import subprocess
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        log.log_error("Compile error...")
    except OSError:
        log.log_warning("Cannot run the command...")

def _search_dir(target: str, path=".", recursive=False):
    with os.scandir(path) as entries:
        for item in entries:
            if item.is_dir() and item.name == target:
                return True
            if recursive and item.is_dir():
                _search_dir(target, item.path)
    return False

def _search_file(target: str, path=".", recursive=False):
    with os.scandir(path) as entries:
        for item in entries:
            if item.is_file() and item.name == target:
                return True
            if recursive and item.is_file():
                _search_file(target, item.path)
    return False

def is_empty(iterable):
    return len(iterable) == 0

class Builder():
    def __init__(self, compiler=""):
        self._cmd = cmd(compiler)

    def compiler(self):
        return self._cmd.compiler

    def set_compiler(self, name: str):
        if self._cmd.compiler is None:
            self._cmd.compiler = name

    def executable_name(self):
        return self._cmd.out

    def set_executable_name(self, name: str):
        from sys import platform
        if is_empty(self._cmd.out):
            if platform == "win32" and ".exe" not in name:
                self._cmd.out = name + ".exe"
            else:
                self._cmd.out = name
        
    def source_files(self):
        return self._cmd.source_files

    def include(self, path: str):
        if not is_empty(path):
            p = f"-I{path}"
            self._cmd.includes.append(p)

    def includes(self):
        return self._cmd.includes

    def search_sources(self, path: str, recursive=False):
        """
        Enter the path and search for valid source code files, and
        returns a list of source code paths.
        """
        sources = self._cmd.source_files
        with os.scandir(path) as entries:
            for item in entries:
                if item.is_file() and item.name.endswith(SOURCE_SUFFIXES):
                    sources.append(item.path)
                if item.is_dir() and recursive:
                    self.search_sources(item.path)

    def flags(self):
        return self._cmd.flags

    def set_flags(self, *args):
        """
        Set flags for the compiler
        """
        self._cmd.flags += list(args)

    def build_executable(self, executablename="", builddir="."):
        """
        Build an executable to a given build path
        """
        if is_empty(self._cmd.compiler):
            log.log_error("Cannot detect compiler... Compilation failed!")
            return

        if is_empty(executablename) and self._cmd.out is not None:
            executablename = self._cmd.out

        if builddir != "." and not _search_dir(builddir):
            os.makedirs(builddir, exist_ok=True)

        if is_empty(self._cmd.source_files):
            log.log_error("No source files was specified...")
            return

        cmd = [self._cmd.compiler, *self._cmd.flags, *self._cmd.includes, *self._cmd.source_files]
        if executablename:
            if "/" not in builddir:
                builddir += "/"
            cmd += ["-o" ,f"{builddir}{executablename}"]
            _try_compile(cmd)
        else:
            log.log_error("Executable name was not defined...")
