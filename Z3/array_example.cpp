#include <iostream>
#include "z3++.h"

using namespace z3;

int main(){

  context c;

  // create an array
  std::cout << "create array" << std::endl;
  sort A = c.int_sort();
  sort IntSort = c.int_sort();
  sort array = c.array_sort(IntSort,IntSort);
  expr arr =c.constant("arr",array); 

  // variables
  std::cout << "create variables" << std::endl;
  expr a = c.int_const("val_a");
  expr b = c.int_const("val_b");

  int index = 0;
  // store a at pos index
  std::cout << "store at index" << std::endl;
  // store returns modified array
  expr new_arr = store(arr, index, a);
  
  // check val at index
  std::cout << "select at index" << std::endl;
  expr cond = select(new_arr, index) != a;
  
  // print Z3 constraint
  std::cout << "cond:" << cond << std::endl;

  // check if we correctly set the array entry
  std::cout << "start solving..." << std::endl;
  solver s(c);
  s.add(cond);
  if( s.check() == sat )
    std::cout << "SATISFIABLE" << std::endl;
  else 
    std::cout << "UNSAT" << std::endl;
  
  return 0;
}

