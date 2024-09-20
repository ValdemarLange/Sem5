#include <iostream>
#include <string>
#include <vector>
using namespace std;



int sum(int n) {
    if(n == 0){
        return 0; // Basis
    }
    else {
        return n + sum(n-1);
    }
}

int evenSquares(int n) {
    if (n == 0){
        return 0;
    }
    else {
        return (2*n) * (2*n) + evenSquares(n-1);
    }
}

int fib(int n) {
    if (n == 0){
        return 0;
    }
    if (n == 1){
        return 1;
    }
    else {
        return fib(n-1) + fib(n-2);
    }
}

bool linear(string s, char c, int l) {
    if (l == 0){
        return 0;
    }
    else if (s[0] == c){
        return 1;
    }
    else{
        return linear(s.substr(1), c, l-1);
    }
}

bool binarySearch(vector<int> arr, int begin, int end, int value) {     
    int mid = 0;

    if (begin > end){
        return false;
    }
    else {
        mid = (begin + end) / 2;
        if( arr[mid] == value){
            return true;
        }
        else if(arr[mid] < value){
            return binarySearch(arr, mid + 1, end, value);
        }
        else{
            return binarySearch(arr, begin, mid - 1, value);
        }
    }
}


int main() {
    std::cout << "Hello, World!" << std::endl;
 
    std::cout << "Sum: " << sum(15) << std::endl;

    std::cout << "Even Squares: " << evenSquares(13) << std::endl;

    std::cout << "Fibonacci: " << fib(17) << std::endl;

    std::cout << "Linear: " << linear("Hello, World!", 'd', 13) << std::endl;

    std::vector<int> arr = {1, 2, 3, 4, 5};
    int value = 2;

    std::cout << "Binary Search: " << binarySearch(arr, 0, arr.size()-1,value) << std::endl;
 
    return 0;
}