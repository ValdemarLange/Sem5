#include <iostream>
#include <vector>
using namespace std;

bool quad(vector<int> a, int X){
    int n = a.size();
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (a[i] + a[j] == X && i != j){
                return true;
            }
        }
           
    }
    return false;
}

bool lin(vector<int> a, int X){
    int pa = 0;
    int pb = a.size()-1;

    while(pa != pb){
        if(a[pa] + a[pb] == X){
            return true;
        }
        if(a[pa] + a[pb] < X){
            pa++;
        }
        if(a[pa] + a[pb] > X){
            pb--;
        }
    }
    return false;
}

int main() {
    vector<int> testVector = {1, 2, 3, 4, 5, 6};
    int targetSum = 2;

    if (quad(testVector, targetSum)) {
        cout << "Found a pair with the given sum." << endl;
    } else {
        cout << "No pair with the given sum found." << endl;
    }

    if (lin(testVector, targetSum)) {
        cout << "Found a pair with the given sum." << endl;
    } else {
        cout << "No pair with the given sum found." << endl;
    }

    return 0;
}