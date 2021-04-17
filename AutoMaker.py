"""

"""
import re
from sys import argv
from os import listdir, getcwd, path


def read_and_clean_file(fname):
    with open(fname, 'r') as fn:
        return list(map(lambda l: l.strip(), fn.readlines()))


def find_local_file(fname, local_files):
    for l_file in local_files:
        l_path, l_fname = path.split(l_file)

        if l_fname == fname:
            return l_file

    return None



def get_headers(file_contents):
    """get all header files"""
    header_files = []
    include_regex = re.compile(r"#include [<\"][A-Za-z\-]{1,20}[\.|>]?[a-z]{1,5}[>\"]")

    for file_line in file_contents:

        regex_result = include_regex.search(file_line)

        if regex_result is not None:
            regex_result = regex_result[0]
            regex_result = regex_result.replace("#include ", "")
            regex_result = regex_result[1:-1]

            header_files.append(regex_result)

    return header_files


def recursve_depdendency_tracker(main_header_files, local_header_files):
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
    BASE_MAKE = ["CC = g++",
                 "CFLAGS = -Wall -std=c++11 -pedantic -c $(DEBUG)",
                 "LFLAGS = -Wall -std=c++11 -pedantic $(DEBUG)",
                 "HFLAGS = -fopenmp -pthread"]



    if len(argv) != 2:
        raise ValueError("This program requires ONLY two command line arguments.")

    cpp_file = path.join(getcwd(), argv[1])
    cpp_path, cpp_fname = path.split(cpp_file)
    cpp_basename, cpp_ext = path.splitext(cpp_fname)

    if ".cpp" not in cpp_file:
        raise ValueError("A .cpp was not provided.")

    print(f"[+] Compiling: {cpp_file}")

    fcontents = read_and_clean_file(cpp_file)
    main_header_files = get_headers(fcontents)

    print(f"[+] Headers found: {len(main_header_files)}")

    local_files = [path.join(cpp_path, file) for file in listdir(cpp_path) if ".hpp" in file]
    all_depdendencies = recursve_depdendency_tracker(main_header_files, local_files)

    print(f"[+] Local headers found: {len(all_depdendencies)}")

    all_base_files = []
    for dependency in all_depdendencies:
        dependency_path, dependency_fname = path.split(dependency)
        dependency_basename, dependency_ext = path.splitext(dependency_fname)
        all_base_files.append(dependency_basename)

    all_object_files = [f"{base_file}.o" for base_file in all_base_files]

    with open(f"{cpp_path}/{cpp_basename}-Makefile", "w") as m_writer:
        m_writer.write('\n'.join(BASE_MAKE) + '\n\n')

        if len(all_depdendencies) == 0:
            m_writer.write(f"{cpp_basename} : {cpp_basename}.cpp\n")
            m_writer.write(f"\t$(CC) $(LFLAGS) $(HFLAGS) {cpp_basename}.cpp -o {cpp_basename}\n\n")
            m_writer.write("clean:\n")
            m_writer.write(f"\t\\rm {cpp_basename}\n")

            print("[+] Generated a Makefile with no external dependencies")

        else:
            m_writer.write(f"{cpp_basename} : {' '.join(all_object_files)}\n")
            m_writer.write(f"\t$(CC) $(LFLAGS) $(HFLAGS) {' '.join(all_object_files)} -o {cpp_basename}\n\n")

            for base_name in all_base_files:
                m_writer.write(f"{base_name}.o : {base_name}.cpp {base_name}.hpp\n")
                m_writer.write(f"\t$(CC) $(CFLAGS) $(HFLAGS) {base_name}.cpp\n\n\n")

            m_writer.write("clean:\n")
            m_writer.write(f"\t\\rm *.o {cpp_basename}\n")

            print("[+] Generated a Makefile with external dependencies")

    print(f"\nRun using: ~$ make -f {cpp_basename}")
