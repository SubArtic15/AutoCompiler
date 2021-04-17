"""
:summary parses a provided main file for all local dependencies then
         generates a similiarly named Makefile

:project AutoCompiler

:changelog
    V0.1 Works with CPP files only

:future-work
    + compatiability with C files
    + dynamically check for specialized libraries
        ex. pthread : -lpthread or -pthread
"""
import re
from sys import argv
from os import listdir, getcwd, path





def read_and_clean_file(fname):
    """read in a provided file, then remove all newline characters"""
    with open(fname, 'r') as fn:
        return list(map(lambda l: l.strip(), fn.readlines()))


def find_local_file(fname, local_files):
    """search for a provided file/library name in an array of (local) files"""
    for l_file in local_files:
        l_fname = path.split(l_file)[1]
        if l_fname == fname:
            return l_file
    return None



def get_headers(file_contents):
    """extract all possible library files from a given file"""
    found_headers = []
    include_regex = re.compile(r"#include [<\"][A-Za-z\-]{1,20}[\.|>]?[a-z]{1,5}[>\"]")

    for file_line in file_contents:
        regex_result = include_regex.search(file_line)

        # if a statement was found, then clean, and append it
        if regex_result is not None:
            regex_result = regex_result[0]
            regex_result = regex_result.replace("#include ", "")
            regex_result = regex_result[1:-1]
            found_headers.append(regex_result)

    return found_headers


def recursve_depdendency_tracker(main_header_files, local_header_files):
    """recursively solve dependency tree"""
    dependencies = []

    for header_file in main_header_files:
        local_file = find_local_file(header_file, local_header_files)

        if local_file is not None:
            dependencies.append(local_file)
            print(f"[+] '{header_file}' detected in local directory")

            l_contents = read_and_clean_file(local_file)
            l_headers = get_headers(l_contents)

            for l_dep in recursve_depdendency_tracker(l_headers, local_header_files):
                dependencies.append(l_dep)

    return dependencies




if __name__ == '__main__':
    # constants used in make file, will be written first in Makefile
    BASE_MAKE = ["CC = g++",
                 "CFLAGS = -Wall -std=c++11 -pedantic -c $(DEBUG)",
                 "LFLAGS = -Wall -std=c++11 -pedantic $(DEBUG)",
                 "HFLAGS = -fopenmp -pthread"]

    # used to check for extension type
    VALID_EXT = [".cpp"]

    # validity check: ensure proper number of arguments are provided,
    # if not, then return error.
    if len(argv) != 2:
        raise ValueError("This program requires ONLY two command line arguments.")

    # generate the full path, path, filename, and extension of the provided file
    cpp_file = argv[1]
    cpp_file = path.join(getcwd(), cpp_file)
    cpp_path, cpp_fname = path.split(cpp_file)
    cpp_basename, cpp_ext = path.splitext(cpp_fname)

    # validity check: ensure proper file type
    if cpp_ext not in VALID_EXT:
        raise ValueError("An invalid file-type was given.")

    print(f"[+] Compiling: '{cpp_fname}' as main file")

    # get file contents of main file then extract all headers
    fcontents = read_and_clean_file(cpp_file)
    main_header_files = get_headers(fcontents)

    print(f"[+] Headers found: {len(main_header_files)}")

    # find all files in local directory, then find all project dependencies
    # with relation to local files
    local_files = [path.join(cpp_path, file) for file in listdir(cpp_path) if ".hpp" in file]
    all_depdendencies = recursve_depdendency_tracker(main_header_files, local_files)

    print(f"[+] Local headers found: {len(all_depdendencies)}")

    # generate an array of all basename dependencies
    all_base_files = []
    all_object_files = []
    for dependency in all_depdendencies:
        dependency_path, dependency_fname = path.split(dependency)
        dependency_basename, dependency_ext = path.splitext(dependency_fname)
        all_base_files.append(dependency_basename)
        all_object_files.append(f"{dependency_basename}.o")

    # generate Makefile
    with open(f"{cpp_path}/{cpp_basename}-Makefile", "w") as m_writer:
        # 1. write Makefile variables to file
        m_writer.write('\n'.join(BASE_MAKE) + '\n\n')

        # 2A. if there were no local dependencies found, then write a simple
        #     one liner to compile a given project
        if len(all_depdendencies) == 0:
            m_writer.write(f"{cpp_basename} : {cpp_basename}.cpp\n")
            m_writer.write(f"\t$(CC) $(LFLAGS) $(HFLAGS) {cpp_basename}.cpp -o {cpp_basename}\n\n")
            m_writer.write("clean:\n")
            m_writer.write(f"\t\\rm {cpp_basename}\n")

            print("[+] Generated a Makefile with no external dependencies")

        # 2B. if there are local dependencies then write a more complex make file
        #     that generates object files for all local dependencies then links
        #     them together to create the final binary
        else:
            all_object_files_str = ' '.join(all_object_files)

            m_writer.write(f"{cpp_basename} : {all_object_files_str}\n")
            m_writer.write(f"\t$(CC) $(LFLAGS) $(HFLAGS) {all_object_files_str} -o {cpp_basename}\n\n")

            for base_name in all_base_files:
                m_writer.write(f"{base_name}.o : {base_name}.cpp {base_name}.hpp\n")
                m_writer.write(f"\t$(CC) $(CFLAGS) $(HFLAGS) {base_name}.cpp\n\n\n")

            m_writer.write("clean:\n")
            m_writer.write(f"\t\\rm *.o {cpp_basename}\n")

            print("[+] Generated a Makefile with external dependencies")

    print(f"\nRun using: ~$ make -f {cpp_basename}")
