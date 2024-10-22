#include <iostream>

int test = 0;

int myMethod(int n){
    test++;
    if (n <= 1){
        return 1;
    }
    else{
        return myMethod(n-1) + myMethod(n-2);
    }
}

int main()
{
    std::cout << myMethod(12) << std::endl;
    std::cout << test << std::endl;
    return 0;
}
