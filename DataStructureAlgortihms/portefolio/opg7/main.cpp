// Opgave så lang jeg ikke gider indsætte den.

#include <iostream>
#include <cmath>
using namespace std;

pair<int, int> algoritme(int z)
{
    int x = 0;
    int y = 0;
    for (int i = 3; i < cbrt(z); i++) // Giver det højeste tal som i^3 er <= z
    {
        for (int j = 3; j < log(z)/log(3); j++) // 3^y < z => y*log(3) < log(z) => y < log(z)/log(3)
        {
            if(pow(i,j) == z){
                x = i;
                y = j;
            }
        }
        
    }
    return pair<int,int> (x,y);
}

int main()
{
    pair<int,int> res = algoritme(3125);
    cout << "3125 => x: " << res.first << ", y: " << res.second << endl;
    res = algoritme(6561);
    cout << "6561 => x: " << res.first << ", y: " << res.second << endl;
    res = algoritme(3000);
    cout << "3000 => x: " << res.first << ", y: " << res.second << endl;


    return 0;
}
