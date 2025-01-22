#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryHeap.h"
#include "dsexceptions.h"

int main()
{
    BinarySearchTree abe;
    abe.insert(45);
    abe.insert(15);
    abe.insert(20);
    abe.insert(10);
    abe.insert(22);
    abe.insert(30);
    abe.insert(40);
    abe.insert(5);
    abe.insert(12);
    abe.insert(28);
    abe.insert(38);
    abe.insert(48);
    abe.insert(1);
    abe.insert(8);
    abe.insert(15);
    abe.insert(45);
    abe.insert(50);

    abe.printTree();
    std::cout << abe.findMin() << " MIN " << std::endl;
    abe.remove(abe.findMin());
    // abe.printTree();
    std::cout << abe.findMax() << " MAX " << std::endl;
    abe.printTree();

    

    return 0;
}