/*
Skriv en rekursiv metode med følgende signatur:
    int logTo(int N)
Algoritmen returner totals-logaritmen af N, og det er en forudsætning,
at N er et naturligt tal og en potens af 2.
Kaldt med N = 32 returneres 5, og med N = 4096 returneres   12
*/

#include <iostream>

int logTo(int N)
{
    if(N == 2){     // Givet at N altid er potens af 2 => aldrig mindre end 2 :)
        return 1;
    }
    return 1 + logTo(N/2);
}

int main()
{
    std::cout << logTo(4096) << std::endl;
    std::cout << logTo(32) << std::endl;

    return 0;
}