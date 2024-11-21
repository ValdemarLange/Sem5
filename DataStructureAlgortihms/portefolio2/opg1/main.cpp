#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

std::string mostOccurences(std::string s)
{
    std::unordered_map<std::string, int> occurrences;
    std::string current_word;
    bool lastSymbol = true;

    for(int i = 0; i < s.size(); i++){
        if( s[i] == ' ' || s[i] == ',' || s[i] == '.'){
            if( lastSymbol ){
                ;
            }
            else {
                occurrences[current_word]++;
                lastSymbol = true;
                
                current_word.clear();
            }
        }
        else{
            lastSymbol = false;
            current_word += s[i];
        }
    }

    std::string most_occuring;
    int highest_count = 0;
    

    for (auto word : occurrences) {
        if (word.second > highest_count) {
            highest_count = word.second;
            most_occuring = word.first;
        }
    }
    // std::cout << highest_count << std::endl;
    return most_occuring;

}

int main()
{
    std::string my_string = "The cattle were running back and forth, but there was no wolf to be seen, heard, or smelled, so the shepherd decided to take a little nap in a bed of grass and early summer flowers. Soon he was awakened by a sound he had never heard before.";

    std::cout << mostOccurences(my_string) << std::endl;

    return 0;
}