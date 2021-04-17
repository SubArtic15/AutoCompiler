CC= g++
DEBUG = -g
CFLAGS = -Wall -std=c++11 -pedantic -c $(DEBUG)
LFLAGS = -Wall -std=c++11 -pedantic $(DEBUG)
HFLAGS = -fopenmp -pthread

# generate binary 'reference-binary' using *.o
reference-binary : reference-sheet.o Library.o
	$(CC) $(LFLAGS) $(HFLAGS) reference-sheet.o Library.o -o reference-binary

Library.o : Library.cpp Library.hpp
	$(CC) $(CFLAGS) $(HFLAGS) Library.cpp

reference-sheet.o : reference-sheet.cpp reference-sheet.hpp
	$(CC) $(CFLAGS) $(HFLAGS) reference-sheet.cpp


clean:
	\rm *.o reference-binary
