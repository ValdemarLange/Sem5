/*
Skriv en rekursiv metode/algoritme med følgende signatur: 
    int sumDeleligMedTreOgOtte(int N) 
Metoden returnerer summen af de tal, som er mindre end eller lig med N og er delelige med 3 eller 8. 
Er et tal deleligt med både tre og otte, tælles det kun med én gang. 
Kaldt med parameteren 26   returneres 132 (3+6+8+9+12+15+16+18+21+24

*/

#include <iostream>

int sumDeleligMedTreOgOtte(int N){
    if ( N < 3){   // Base case
        return 0;
    }

    if ( N % 3 == 0 || N % 8 == 0 ) {
        return N + sumDeleligMedTreOgOtte(N-1);
    }

    return sumDeleligMedTreOgOtte(N-1);

}


int main(int argc, char const *argv[])
{
    std::cout << sumDeleligMedTreOgOtte(26) << std::endl;
    return 0;
}
