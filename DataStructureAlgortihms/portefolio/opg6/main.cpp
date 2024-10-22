/*
Skriv en rekursiv algoritme med følgende signatur:
    int sumDivisibleBy3(int N)

Algoritmen returnerer summen af heltal større end 0 og mindre end eller lig med N,
som er dividérbare med 3. Kaldt med N = 12 er den korrekte returværdi 30 (3+6+9+12).
Kaldt med N = 14 er den korrekte returværdi også 30.
Din algoritme skal optimeres således, at overflødige rekursive kald undgås
*/
#include <iostream>

int sumDivisbleBy3(int N)
{
    if (N < 6){
        return 3;   // Man får 3 som base case så man ikke når at kalde sumDivisibleBy3(3-3);
    }
    if (N % 3 != 0){
        N = N - (N % 3);
    }
    return N + sumDivisbleBy3(N-3);
    
}

int main()
{
    std::cout << sumDivisbleBy3(14) << std::endl;
    return 0;
}