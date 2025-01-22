/*
Skriv en rekursiv algoritme som kan tælle antallet af forekomster af et bestemt bogstav i en String.
Eksempel: kaldt med ”banana” og ’a’ returneres værdien 3.
Mulig signatur: 
    int countLettersInWord(String word, char letter, int index);
*/

#include <iostream>
#include <string>

int countLettersInWord(std::string word, char letter, int index){
    if (index > word.size() - 1){   // Base case
        return 0;
    }

    if ( word.at(index) == letter){
        return 1 + countLettersInWord(word, letter, index+1);
    }
    return countLettersInWord(word, letter, index +1);


}


int main(int argc, char const *argv[])
{
    std::string word = "banana";
    std::cout << countLettersInWord(word, 'a', 0) << std::endl;
    return 0;
}
