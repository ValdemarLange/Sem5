/*
Skriv metoder til pre-order, in-order, post-order
og level order traversering af binære (søge)
træer
*/

#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryHeap.h"
#include "dsexceptions.h"

int main() {
    BinarySearchTree træ;

    træ.insert(5);    
    træ.insert(3);
    træ.insert(7);
    træ.insert(2);
    træ.insert(8);
    træ.insert(4);
    træ.insert(6);

//    træ.printTree();
    std::cout << "-----------------preorder-------" << std::endl;
    træ.preorder();
    std::cout << "-----------------inorder-------" << std::endl;
    træ.inorder();
    std::cout << "-----------------postorder-------" << std::endl;
    træ.postorder();
    std::cout << "-----------------levelorder-------" << std::endl;

    træ.levelorder();

    return 0;
}