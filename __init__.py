import os

COLOR_RED = "\033[31m"
END = "\033[m"

CPP_SUFFIXES = (".cpp", ".cxx", ".cc", ".ipp", ".ixx")
C_SUFFIXES = (".c",)
SOURCE_SUFFIXES = CPP_SUFFIXES + C_SUFFIXES

def _try_run(args: list[str]):
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

class _cmd():
    def __init__(self, compiler: str):
        self.compiler = compiler
        self.source_files = []
        self.executable_name = ""
        self.flags = []
        self.includes = []

class Builder():
    def __init__(self, compiler=""):
        self.__cmd = _cmd(compiler)

    def compiler(self):
        return self.__cmd.compiler

    def set_compiler(self, name: str):
        self.__cmd.compiler = name

    def executable_name(self):
        return self.__cmd.executable_name

    def set_executable_name(self, name: str):
        self.__cmd.executable_name = name

    def source_files(self):
        return self.__cmd.source_files

    def include(self, path="."):
        if not is_empty(path):
            p = f"-I{path}"
            self.__cmd.includes.append(p)
        else:
            _search_dir("include")

    def includes(self):
        return self.__cmd.includes

    def get_sources(self, path: str):
        """
        Enter the path and search for valid source code files, and
        returns a list of source code paths.
        """
        with os.scandir(path) as entries:
            for item in entries:
                if item.is_file() and item.name.endswith(SOURCE_SUFFIXES):
                    self.__cmd.source_files.append(item.path)
                elif item.is_dir():
                    self.get_sources(item.path)

        return self.__cmd.source_files

    def flags(self):
        return self.__cmd.flags

    def set_flags(self, *args):
        """
        Set flags for the compiler
        """
        self.__cmd.flags = list(args)

    def build_executable(self, builddir=".", executablename=""):
        """
        Build an executable to a given build path
        """
        if is_empty(self.__cmd.compiler):
            print(f"{COLOR_RED}Cannot detect compiler... Compilation failed!{END}")
            return

        if not executablename:
            executablename = self.__cmd.executable_name

        if builddir != "." and not _search_dir(builddir):
            os.makedirs(builddir, exist_ok=True)

        cmd = [self.__cmd.compiler, *self.__cmd.flags, *self.__cmd.includes, *self.__cmd.source_files]
        if executablename:
            cmd += ["-o", f"{builddir}/{executablename}"]
            _try_run(cmd)
        else:
            print(f"{COLOR_RED}Executable name was not specified...{END}")