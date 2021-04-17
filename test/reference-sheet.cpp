/*
* :summary a reference file full of helpful cpp snippets
*/
#include "reference-sheet.hpp"

using namespace std;

const int SIZE = 5;


///////////////////////////////////////////////////////////////////////////////
//////////////////////////////   CLASS BASICS    //////////////////////////////
///////////////////////////////////////////////////////////////////////////////
class MyClass
{
  int variableName;

public:
  // initializer method
  MyClass( int initVariableName )
  {
    variableName = initVariableName;
  }

  // get method
  int getVariable()
  {
    return variableName;
  }
};




int main()
{
  // class main
  // MyClass * obj = (MyClass *) calloc(SIZE, sizeof( MyClass ) );
  // for( int i = 0; i < SIZE; i++ )
  // {
  //   obj[i] = MyClass( pow(2, i) );
  //   cout << "itemID: " << i << endl;
  //   cout << "classValue: " << obj[i].getVariable() << "\n" << endl;
  // }

  // file reading main
  // list <string> fileContents = readFile( "file.txt" );
  // for( string line : fileContents )
  // {
  //   cout << line << endl;
  // }

  // OpenMP basics
  printOpenMP();

  return 0;
}
