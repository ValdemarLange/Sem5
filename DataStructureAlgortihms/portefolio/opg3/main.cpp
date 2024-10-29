/*
Skriv en rekursiv algoritme med følgende signatur:
bool additive(String s) 
Parameteren indeholder en streng bestående af cifre, fx. “82842605”.
Algoritmen returnerer true, hvis parameteren indeholder en substring af tre på hinanden efterfølgende tal, 
hvor det  tredje ciffer er lig med summen af de to forrige.I ovenstående eksempel returneres true, 
fordi indeks 5 (6) er summen af indeks 3 og 4 (4 plus 2).

Tip: ASCII-værdien af karakteren ‘7’ er 55.
*/
#include <iostream>
#include <string>

bool additive(std::string s){
    if (s.length() == 2){
        return false;
    }
    if (s[0]-'0' + s[1]-'0' == s[2]-'0' ){
        return true;
    }
    else{
        return additive(s.substr(1));
    }
}


int main() {
    std::cout << additive("82842605") << std::endl;
    return 0;
}