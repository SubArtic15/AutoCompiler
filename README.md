# AutoCompiler
A helpful script used to automatically generate C++ compatible Makefiles. This script operates by passing the mainfile associated with a given project. It then recursivly parses the file for local libraries to be compiled and linked.

### Features 
* Custom Makefile naming schema
* Scalability
* Dynamic linking

### Installation
```bash
git clone https://github.com/SubArtic15/AutoCompiler.git
cd AutoCompiler
./setup.sh
```


### Usage

```bash
python3 AutoMaker.py [MAIN_FILE]

or

auto_maker [MAIN_FILE]
```


### Example

```bash
$ auto_maker test/reference-sheet.cpp

[+] Compiling: ./test/reference-sheet.cpp
[+] Headers found: 1
[+] 'reference-sheet.hpp' detected in local directory
[+] 'Library.hpp' detected in local directory
[+] Local headers found: 2
[+] Generated a Makefile with external dependencies

Run using: ~$ make -f reference-sheet

```


