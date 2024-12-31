/*
Skriv en rekursiv metode/algoritme med følgende signatur: 
    int antalVokaler(String str,int l) 
Parameteren str indeholder små bogstaver i det  engelske alfabet: 
    {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}.
Og metoden skal returnere antallet af vokaler i strengen str, og vi antager, at vokalerne er:
    {a,e,i,o,u,y}
Kaldt med strengen ”stationsbygninger”   returneres 6, eftersom vokalerne i strengen er ”a,i,o,y,i,e”. 
Den anden parameter i metoden angiver længden af strengen minus 1, idet det antages, at strengen 
opfattes som et array af karakterer (chars). 
Det kan anbefales at skrive en hjælpemetode med returværdi true ellers false, som kan afgøre om 
den enlige parameter af datatypen char, er en vokal eller en konsonant
*/

#include <iostream>
#include <string>

bool erVokal(char c){
    return (c == 'a' || c == 'e' ||c == 'i' ||c == 'o' ||c == 'u' || c == 'y');
}

int antalVokaler(std::string str, int l){
    if (l < 0){
        return 0;
    }

    if ( erVokal(str.at(l)) ){
        return 1 + antalVokaler(str, l-1);
    }

    return antalVokaler(str, l-1);

}


int main(int argc, char const *argv[])
{
    std::string s = "stationsbygninger";

    std::cout << antalVokaler(s, s.size() -1) << std::endl;

    return 0;
}
