/*
Skriv en algoritme, der har et array af usorterede, entydige naturlige tal som input og find de tre tal i arrayet,
hvis sum er tættest på en potens af 2. Det samme tal kan må bruges én gang.
Algoritmens returværdi skal være et heltalsarray, som først indeholder de tre tal og
dernæst den tilhørende potens af to (fx 512).Kaldt med arrayet {23,56,22,11,65,89,3,44,87,910,45,35,98},
returneres de tre tal 89, 3, 35 og potensen af 2: 128.Hvad er Store-O tidskompleksiteten af din algoritme?
Begrund dit svar og diskuter mulighederne for at optimere din løsning yderligere
*/
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

vector<int> nearestSum(vector<int> vec)
{
    int size = vec.size();
    int shortest_dist = 1000000000;
    vector<int> best;
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            for (int k = 0; k < size; k++)
            {
                if (i == j || i == k || j == k)
                {
                    ; // Do nothing; duplicates
                }
                else
                {
                    int sum = vec[i] + vec[j] + vec[k];
                    int pot = log2(sum);
                    int lower_dist = sum-pow(2,pot);
                    int upper_dist = pow(2,pot+1)-sum;
                    int dist = 0;

                    if(lower_dist <= upper_dist){
                        dist = lower_dist;
                    }
                    else{
                        dist = upper_dist;
                        pot++;
                    }

                    if(dist < shortest_dist){
                        best.clear();
                        best.push_back(vec[i]);
                        best.push_back(vec[j]);
                        best.push_back(vec[k]);
                        best.push_back(pow(2,pot));
                        shortest_dist = dist;

                    }
                }
            }
        }
    }
    return best;
}

int main()
{
    vector<int> vec = {23, 56, 22, 11, 65, 89, 3, 44, 87, 910, 45, 35, 98};
    vector<int> result = nearestSum(vec);

    for (int num : result) {
        cout << num << " ";
    }
    cout << endl;


    return 0;
}