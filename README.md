# GBuild
A **simple and easy to use** Python package for building C/C++ executables.

## Getting Started
To use **GBuild**, you need to clone the repository into your project folder. <br>
```
git clone https://github.com/voidksks/gbuild.git
```
Or download the source code manually. <br>
<br>
An example script for building a simple executable in a file called `build.py` :
```py
from gbuild import Builder

build = Builder("g++")
build.search_sources("src")
build.build_executable("build/release", "build.exe")
```
This script search for C/C++ files and build an executable called `build.exe` at path  `build/release`
<br>
### Adding flags.
The `Builder` class, has a method called `set_flags()`, that you can pass valid flags based on our compiler. <br>
Example:
```py
from gbuild import Builder

build = Builder("g++")
build.set_flags("-Wall", "-Wextra", "-std=c++20")
build.search_sources("src")
build.build_executable("build/release", "build.exe")
```

### Including Headers
The class `Builder` has a method called `include`. This method can include headers from a specified path.
```py
from gbuild import Builder

build = Builder("g++")
build.include("include")
build.search_sources("src")
build.build_executable("build/release", "build.exe")
```

### Linking
**GBuild** still do not have native support to link libs *(yet)*, but you can use `set_flags()` for linking.

> [!NOTE]
> **GBuild** still under development, maybe you miss some functionalities.
