// CheatOnMe.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Windows.h""

volatile int changeme = 200;

int main()
{
    std::cout << "Hello World!\n";

    while (true) {
        std::cout << "current value: " << changeme << std::endl;
        Sleep(100);
    }

    return 0;
}
