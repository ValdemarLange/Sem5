/*Skriv en rekursiv algoritme, som har et naturligt tal som parameter og returnerer summen af de ulige tals kvadrater fra 1 til N.  
Eksempel: kaldt med parameteren 8 returneres 84 (1^2 +3^2 + 5^2 + 7^2).   
Det er vigtigt at optimere algoritmen, så overflødige rekursive kald undgås.*/

#include <iostream>

int sumOfOddSquares(int n){
    if (n == 1){
        return 1;
    }
    else if(n % 2 == 0){
        return sumOfOddSquares(n-1);
    }
    else {
        return sumOfOddSquares(n-2) + n*n;
    }
}


int main()
{
    std::cout << sumOfOddSquares(8) << std::endl;
    return 0;
}
