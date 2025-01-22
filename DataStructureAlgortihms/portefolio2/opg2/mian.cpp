#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryHeap.h"
#include "dsexceptions.h"
#include <string>
#include <sstream>

int main()
{
    BinarySearchTree tree;
    tree.insert(45);
    tree.insert(15);
    tree.insert(79);
    tree.insert(10);
    tree.insert(20);
    tree.insert(55);
    tree.insert(90);
    tree.insert(12);
    tree.insert(50);

    tree.levelorder();
    std::cout << "-----" << std::endl;
    std::cout << tree.findRoute(50) << std::endl;

    std::cout << tree.findRoute(16) << std::endl;


    return 0;
}