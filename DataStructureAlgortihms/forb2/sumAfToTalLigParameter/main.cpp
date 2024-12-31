/*
Skriv en metode/algoritme med følgende signatur: 
    bool sumAfToTalLigParameter(int[] arr, int l, int X) 
Den første parameter er et array af positive, sorterede heltal uden dubletter; anden parameter er længden 
af arrayet;  og tredje parameter er den værdi, der ledes efter. 
Metoden skal finde af om der findes to tal i arrayet, hvis sum er lig med parameteren X. 
Hvis svaret er ja, returneres true. Hvis svaret er nej, returneres false. 
Det samme tal må ikke bruges to gange.

Opgaven skal løses i to versioner således at:
    •Version 1 har kvadratisk tidskompleksitet –   O(N2). 
    •Version 2 har lineær tidskompleksitet O(N), det vil sige, at hvert element i tabellen kun må læses én gang.
De to løsninger tæller lige meget, altså 6 %
*/

#include <iostream>
#include <vector>

int sumAfToTalLigParameterV1(std::vector<int> arr, int l, int X){
    for (int i = 0; i < l; i++)
    {
        for (int j = 0; j < l; j++)
        {
            if (i == j){
                ; // Same number => Do nothing
            }
            else if( arr[i] + arr[j] == X){
                return true;
            }
        }
        
    }
    return false;  
}

int sumAfToTalLigParameterV2(std::vector<int> arr, int l, int X){
    int left = 0;
    int right = l-1;

    while(left < right){
        if ( arr.at(left) + arr.at(right) == X){
            return true;
        }
        else if ( arr.at(left) + arr.at(right) < X){
            left++;
        }
        else {
            right--;
        }
    }

    return false;
}


int main(int argc, char const *argv[])
{
    std::vector<int> a = {1, 2, 3, 4, 5, 6};
    std::cout << sumAfToTalLigParameterV1(a, a.size(), 10) << std::endl;
    std::cout << sumAfToTalLigParameterV2(a, a.size(), 11) << std::endl;

    return 0;
}
