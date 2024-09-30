#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool isAnagram(string a, string b){
    bool error = true;
    
    if(int(a.length()) != int(b.length())){
        return false;
    }

    for (int i = 0; i < int(a.length()); i++){
        error = true;
        for(int j = 0; j < int(b.length()); j++){
            
            if( a[i] == b[j]){
                b.erase(j,1);
                error = false;
                break;
            }
        }
    }
    if (!error){
        return true;
    }
    return false;
}

int main() {
    std::cout << "Hello, World!" << std::endl;

    string str1 = "listen";
    string str2 = "silentp";

    if (isAnagram(str1, str2)) {
        cout << str1 << " and " << str2 << " are anagrams." << endl;
    } else {
        cout << str1 << " and " << str2 << " are not anagrams." << endl;
    }
    return 0;
}