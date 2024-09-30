/*
Suppose you have an array of N elements containing only two distinct keys, true
and false. Give an O(N) algorithm to rearrange the list so that all false elements
precede the true elements. You may use only constant extra space.
*/

#include <iostream>
#include <vector>
using namespace std;

void rearrange(vector<int> &input){
    int *left = &input[0];
    int *right = &input[input.size()-1];

    while(left != right){
        if(*right == 1){
            right--;
        }
        else if (*left == 0)
        {
            left++;
        }
        else{
            *left = 0;
            *right = 1;
        }
    }

}




int main() {
    std::cout << "Hello, World!" << std::endl;
    vector<int> input1 = {1,0,1,1,0,1,0,0,0,1,1,1,1,0};

    rearrange(input1);

    for (auto &&i : input1)
    {
        cout << i << ",";
    }
    cout << endl;

    return 0;
}