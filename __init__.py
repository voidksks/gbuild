import os
from sys import platform
from _command import _cmd

COLOR_RED = "\033[31m"
END = "\033[m"

CPP_SUFFIXES = (".cpp", ".cxx", ".cc", ".ipp", ".ixx")
C_SUFFIXES = (".c",)
SOURCE_SUFFIXES = CPP_SUFFIXES + C_SUFFIXES

def _try_compile(args: list[str]):
    import subprocess
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        print(f"{COLOR_RED}Compilation error...{END}")
    except OSError:
        print(f"{COLOR_RED}Cannot run the command...{END}")

def _search_dir(target: str, path="."):
    with os.scandir(path) as entries:
        return any(e.name == target and e.is_dir() for e in entries)

def _search_file(target: str, path="."):
    with os.scandir(path) as entries:
        return any(e.name == target and e.is_file() for e in entries)

def is_empty(string: str):
    return string == ""

class Builder():
    def __init__(self, compiler=""):
        self._cmd = _cmd(compiler)

    def compiler(self):
        return self._cmd.compiler

    def set_compiler(self, name: str):
        if self._cmd.compiler is None:
            self._cmd.compiler = name

    def executable_name(self):
        return self._cmd.out

    def set_executable_name(self, name: str):
        if is_empty(self._cmd.out):
            if platform == "win32" and ".exe" not in name:
                self._cmd.out = f"{name}.exe"
            else:
                self._cmd.out = f"{name}"
        
    def source_files(self):
        return self._cmd.source_files

    def include(self, path="."):
        if not is_empty(path):
            p = f"-I{path}"
            self._cmd.includes.append(p)
        else:
            _search_dir("include")

    def includes(self):
        return self._cmd.includes

    def get_sources(self, path: str):
        """
        Enter the path and search for valid source code files, and
        returns a list of source code paths.
        """
        sources = self._cmd.source_files
        with os.scandir(path) as entries:
            for item in entries:
                if item.is_file() and item.name.endswith(SOURCE_SUFFIXES):
                    sources.append(item.path)
                elif item.is_dir():
                    self.get_sources(item.path)

        return sources

    def flags(self):
        return self._cmd.flags

    def set_flags(self, *args):
        """
        Set flags for the compiler
        """
        self._cmd.flags = list(args)

    def build_executable(self, executablename="", builddir="."):
        """
        Build an executable to a given build path
        """
        if is_empty(self._cmd.compiler):
            print(f"{COLOR_RED}Cannot detect compiler... Compilation failed!{END}")
            return

        if is_empty(executablename) and self._cmd.out is not None:
            executablename = self._cmd.out

        if builddir != "." and not _search_dir(builddir):
            os.makedirs(builddir, exist_ok=True)

        cmd = [self._cmd.compiler, *self._cmd.flags, *self._cmd.includes, *self._cmd.source_files]
        if executablename:
            if "/" not in builddir:
                builddir += "/"
            cmd += ["-o" ,f"{builddir}{self._cmd.out}"]
            _try_compile(cmd)
            pass
        else:
            print(f"{COLOR_RED}Executable name was not specified...{END}")
