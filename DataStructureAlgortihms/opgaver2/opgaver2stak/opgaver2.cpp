#include <iostream>
#include <vector>
#include <string>
using namespace std;

vector<char> my_stack;

void push(char in){
    my_stack.push_back(in);
}

bool empty(){
    return my_stack.empty();
}

char pop(){
    if (empty()) {
        throw runtime_error("Stack is empty. Cannot pop.");
    }
    char value = my_stack.back();
    my_stack.pop_back();
    return value;
}

char top(){
    if (empty()) {
        throw runtime_error("Stack is empty. Cannot access top element.");
    }
    return my_stack.back();
}

void clear(){
    my_stack.clear();
}

bool balPar(string text){
    clear();
    for (char c : text)
    {
        if(c == '('){
            if (!empty() && top() == ')'){
                pop();
            }
            else{
                push(c);
            }
        }
        if(c == ')'){
            if (!empty() && top() == '('){
                pop();
            }
            else{
                push(c);
            }
        }
    }
    return empty();
}

int main() {
    push('A');
    push('B');
    push('C');

    cout << "Top: " << top() << endl; // Should print 30

    cout << "Popped: " << pop() << endl; // Should print 30
    cout << "Popped: " << pop() << endl; // Should print 20
    cout << "Popped: " << pop() << endl; // Should print 10

    string test1 = "(())";
    string test2 = "(()";
    string test3 = "())";
    string test4 = "wall(hi)min br(o)r";

    cout << "Test 1: " << (balPar(test1) ? "Balanced" : "Not Balanced") << endl;
    cout << "Test 2: " << (balPar(test2) ? "Balanced" : "Not Balanced") << endl;
    cout << "Test 3: " << (balPar(test3) ? "Balanced" : "Not Balanced") << endl;
    cout << "Test 4: " << (balPar(test4) ? "Balanced" : "Not Balanced") << endl;

    return 0;
}