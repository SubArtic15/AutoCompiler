#ifndef LIBRARY_H
#define LIBRARY_H

#include <iostream> // print functions
#include <fstream>  // file functions
#include <list>     // list class
#include <omp.h>    // openMP

using namespace std;

extern const int SIZE;



list <string> readFile( string fileName );
void printOpenMP();

#endif
