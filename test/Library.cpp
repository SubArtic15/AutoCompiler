#include "Library.hpp"

using namespace std;

list <string> readFile( string fileName )
{
  list <string> fileContents;
  string lineBuffer;
  ifstream inputFile;

  inputFile.open( fileName );

  while( getline(inputFile, lineBuffer) )
  {
    fileContents.push_back(lineBuffer);
  }

  return fileContents;
}


void printOpenMP()
{
  #pragma omp parallel for
  for( int i = 0; i < SIZE; i++ )
  {

    #pragma omp critical
    {
      int tid = omp_get_thread_num();
      cout << "PID: " << tid << "\tValue: " << i << endl;
    }

  }

}
