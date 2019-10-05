#include<vector>
#include"z3++.h"
using namespace z3;


void faculty() {
    std::cout << "visit example\n";
    context c;
    solver s(c);

    expr x = c.int_const("x");
    expr f = x! == (x-1)!*x;

    s.add(f);
    s.check();
}

int main() {
    try {
        faculty(); std::cout << "\n";
        std::cout << "done\n";
    }
    catch (exception & ex) {
        std::cout << "unexpected error: " << ex << "\n";
    }
    return 0;
}
