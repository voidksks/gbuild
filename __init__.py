import os
import subprocess

CPP_SUFFIXES = (".cpp", ".cxx", ".cc", ".ipp", ".ixx")
C_SUFFIXES = (".c",)
SOURCE_SUFFIXES = CPP_SUFFIXES + C_SUFFIXES


def _try_run(args: list[str]):
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        print("\033[31mCompilation error...\033[m")
    except OSError:
        print("\033[31mCannot run the command...\033[m")


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
        self.__compiler = compiler
        self.__source_files = []
        self.__executable_name = ""
        self.__flags = []

    def compiler(self):
        return self.__compiler

    def set_compiler(self, name: str):
        self.__compiler = name

    def executable_name(self):
        return self.__executable_name

    def set_executable_name(self, name: str):
        self.__executable_name = name

    def source_files(self):
        return self.__source_files

    def get_sources(self, path: str):
        """
        Enter the path and search for valid source code files, and
        returns a list of source code paths.
        """
        with os.scandir(path) as entries:
            for item in entries:
                if item.is_file() and item.name.endswith(SOURCE_SUFFIXES):
                    self.__source_files.append(item.path)
                elif item.is_dir():
                    self.get_sources(item.path)
        return self.__source_files

    def flags(self):
        return self.__flags

    def set_flags(self, *args):
        """
        Set flags for the compiler
        """
        self.__flags = list(args)

    def build_executable(self, builddir=".", executablename=""):
        """
        Build an executable to a given build path
        """
        if is_empty(self.__compiler):
            print("\033[31mCannot detect compiler... Compilation failed!\033[m")
            return

        if not executablename:
            executablename = self.__executable_name

        if builddir != "." and not _search_dir(builddir):
            os.makedirs(builddir)

        cmd = [self.__compiler, *self.__flags, *self.__source_files]
        if executablename:
            cmd += ["-o", f"{builddir}/{executablename}"]

        _try_run(cmd)
