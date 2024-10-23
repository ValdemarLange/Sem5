/*
Tabellen nedenfor repræsenterer de afgivne stemmer ved et valg.
    {7,4,3,5,3,1,6,4,5,1,7,5}
I  dette eksempel er der 7 kandidater (1-7), og der er afgivet 12 stemmer.
Kandidat 6 fik 1 stemme, kandidaterne 1, 3, 4 og 7 fik hver 2 stemmer,
kandidat 5 fik 3 stemmer,  and kandidat 2 fik 0 stemmer.
Opgaven går ud på at skrive en algoritme, som kaldt med tabellen og eventuelt tabellens længde,
kan afgøre om en kandidat fik mere end 50 % af stemmerne. I så fald returneres kandidatens nummer.
Hvis ingen kandidat fik over 50 % af stemmerne, returneres -1.
I  eksemplet opnåede ingen af kandidaterne flertal, og der returneres -1.
Hvad er din algoritmes tidskompleksitet?
*/

#include <iostream>
#include <vector>
using namespace std;

int findWinner(vector<int> votes)
{
    int N = votes.size();

    for (int i = 0; i < N; i++)
    {
        int count = 1;
        int j = i;
        while (j < N)
        {
            j++;
            if (votes[i] == votes[j])
            {
                count++;
                if (count > N / 2)
                {
                    return votes[i];
                }
            }
        }
    }
    return -1;
}
// O(N²) Selvom anden løkker bliver mindre og mindre. dårlig løsning makker!

int findWinner2(vector<int> votes)
{
    int N = votes.size();
    int max_cand = 0;
    for (int i = 0; i < N; i++) // Find højeste kandidat nr.
    {
        if(votes[i] > max_cand){
            max_cand = votes[i];
        }
    }
    
    vector<int> counts(max_cand,0); 
    for (int i = 0; i < N; i++)     // Tæl stemmer
    {
        counts[votes[i]]++;
    }
    


    for (int i = 0; i <= max_cand; i++) // Tjek om der en vinder
    {
        if(counts[i] > N/2){
            return i;
        }
    }
    
    return -1;
}
// Alle 3 løkker er O(N) dermed samlet => O(N)

int main()
{
    vector<int> a = {7, 5, 7, 5, 7, 3, 6, 7, 7, 7, 7, 4};

    std::cout << findWinner(a) << std::endl;
    std::cout << findWinner2(a) << std::endl;

    return 0;
}