/*
Opgaven går ud på at skrive en metode, der kan sortere et array, som altid 
består af 100 positive heltal, hvorom det gælder, at alle tal i tabellen 
er større end eller lig med en (1) og mindre end eller lig med 200. 
Metoden har ingen returværdi, men skal blot udskrive tallene fra tabellen i stigende rækkefølge, 
og det er ikke tilladt at benytte sorteringsmetoder fra standardbibliotekerne.
For at få fuldt points skal din metode have lineær - O(N) -  tidskompleksitet.
Metoden kunne have følgende signatur: 
    void minSortering(int[] arr);
*/

#include <iostream>
#include <vector>
#include <random>

void minSortering(std::vector<int> arr){
    std::vector<int> counts(200,0); // 200 elementer med værdi = 0
    for (int i = 0; i < 100; i++)
    {
        counts[arr[i]]++;
    }

    for( int i = 0; i < 200; i++){
        while( counts[i] > 0){
            std::cout << i << ", ";
            counts[i]--;
        }

    }
    std::cout << std::endl;

}


int main(int argc, char const *argv[])
{
    std::random_device rd;  // Entropikilde
    std::mt19937 gen(rd()); // Mersenne Twister-generator
    std::uniform_int_distribution<> dist(1, 200); // Intervallet [1, 200]

    std::vector<int> arr;

    // Generer 100 tilfældige tal
    for (int i = 0; i < 100; ++i) {
        int randomNumber = dist(gen); // Generer tilfældigt tal
        arr.push_back(randomNumber);
    }

    minSortering(arr);
    return 0;
}
