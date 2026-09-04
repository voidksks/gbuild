# GBuild
A **simple and easy to use** Python package for building C/C++ executables.

## Getting Started
To use **GBuild**, you need to clone the repository into your project folder. <br>
```
git clone https://github.com/voidksks/gbuild.git
```
Or download the source code manually. <br>
<br>
After that, you can create an python script for using the package. <br>
An example script for building a simple executable in a file called `build.py` :
```
from gbuild import Builder

build = Builder("g++")
build.get_sources("src")
build.build_executable("build/release", "build.exe")
```
### Let's breakdown the script...
The first line ```from gbuild import Builder``` includes the `Builder` class that manage our compilation. <br>
After that the script creates an object from our `Builder` class ```build = Builder("g++")``` passing the `g++` compiler. <br>
The ```build.get_sources("src")``` line, passes where our source code is located. The `get_sources()` method will search recursively search new source files if the method found a new folder. <br>
And finally the `build.build_executable("build/release", "build.exe")` line, that line will generate an executable called `build.exe` in the path `build/release`. <br>
<br>
If no error occurred and everything was in place, in your project will apear the executable `build.exe` in the given path that was specified in the `build_executable()` method.
<br>

### Adding flags.
The `Builder` class, has a method called `set_flags()`, that you can pass valid flags based on our compiler. <br>
Example:
```
from gbuild import Builder

build = Builder("g++")
build.set_flags("-Wall", "-Wextra", "-std=c++20")
build.get_sources("src")
build.build_executable("build/release", "build.exe")
```

### Linking
**GBuild** still do not have native support to link libs *(yet)*, but you can use `set_flags()` for linking.

> [!NOTE]
> **GBuild** still under development, maybe you miss some functionalities.