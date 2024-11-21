#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryHeap.h"
#include "dsexceptions.h"

int main()
{
    BinarySearchTree tree;
    tree.insert(7);
    tree.insert(4);
    tree.insert(3);
    tree.insert(2);
    tree.insert(1);
    tree.insert(28);
    tree.insert(55);
    tree.insert(51);
    tree.insert(60);
    tree.insert(48);
    tree.insert(58);
    tree.insert(69);
    tree.insert(40);
    tree.insert(57);
    tree.insert(35);

    tree.levelorder();
    std::cout << "-----" << std::endl;

    std::cout << tree.numberOfBranches() << std::endl;;

    std::cout << "---|||||||||||--" << std::endl;

    BinarySearchTree abe;
    abe.insert(25);
    abe.insert(20);
    abe.insert(36);
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


    abe.postorder();
    std::cout << "-----" << std::endl;
    abe.preorder();
    std::cout << "-----" << std::endl;

    std::cout << abe.internalPathLength();
    return 0;
}