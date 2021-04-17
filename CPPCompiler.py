"""

"""
import re
from sys import argv
from os import listdir, getcwd, path




def get_header(file_contents):
    """get all header files"""
    header_files = []
    include_regex = re.compile(r"#include [<\"][A-Za-z]{1,20}[\.|>]?[a-z]{1,5}[>\"]")

    for file_line in file_contents:
        regex_result = include_regex.search(file_line)

        if regex_result is not None:
            regex_result = regex_result[0]
            regex_result = regex_result.replace("#include ", "")
            regex_result = regex_result[1:-1]

            header_files.append(regex_result)

    return header_files




if __name__ == '__main__':
    SPECIAL_LIBRARIES = {"omp.h": "-fopenmp",
                         "pthread.h": "-pthread"}

    if len(argv) != 2:
        raise ValueError("This program requires ONLY two command line arguments.")

    cpp_file = path.join(getcwd(), argv[1])

    if ".cpp" not in cpp_file:
        raise ValueError("A .cpp was not provided.")

    print(f"[+] Compiling: {cpp_file}")

    with open(cpp_file, 'r') as f:
        fcontents = list(map(lambda l: l.strip(), f.readlines()))

    header_files = get_header(fcontents)

    print(f"[+] Headers found: {len(header_files)}")

    local_files = [file for file in listdir(getcwd()) if ".hpp" in file]
    print(local_files)
