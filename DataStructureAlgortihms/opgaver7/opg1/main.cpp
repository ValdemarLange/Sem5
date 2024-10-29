/*
Skriv metoder til pre-order, in-order, post-order
og level order traversering af binære (søge)
træer
*/

/* 4.31

Write efﬁcient functions that take only a pointer to the root of a binary tree, T, and
compute
a. the number of nodes in T
b. the number of leaves in T
c. the number of full nodes in T
What is the running time of your routines?
*/

/*
Skriv en metode, som kan beregne internal path length af et binært træ
*/

/*
Skriv en metode, som kan skabe et perfekt
binært træ med højden h (>0)
*/

#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryHeap.h"
#include "dsexceptions.h"
#include <vector>

int main() {
    BinarySearchTree træ;

    træ.insert(5);    
    træ.insert(3);
    træ.insert(7);
    træ.insert(2);
    træ.insert(8);
    træ.insert(4);
    træ.insert(6);
    // træ.insert(10);
    // træ.insert(16);
    // træ.insert(11);
    // træ.insert(12);
    // træ.insert(17);





//    træ.printTree();
    std::cout << "-----------------preorder-------" << std::endl;
    træ.preorder();
    std::cout << "-----------------inorder-------" << std::endl;
    træ.inorder();
    std::cout << "-----------------postorder-------" << std::endl;
    træ.postorder();
    std::cout << "-----------------levelorder-------" << std::endl;
    træ.levelorder();

    std::cout << "-----------------Number of Nodes-------" << std::endl;
    std::cout << træ.numberOfNodes() << std::endl;

    std::cout << "-----------------Number of Leaves-------" << std::endl;
    std::cout << træ.numberOfLeaves() << std::endl;

    std::cout << "-----------------Number of Full Nodes-------" << std::endl;
    std::cout << træ.numberOfFull() << std::endl;

    std::cout << "-----------------Internal Path Length-------" << std::endl;
    std::cout << træ.internalPathLength() << std::endl;

    std::cout << "-----------------Create Perfect Tree--------" << std::endl;

    BinarySearchTree aaaaaaa;
    vector<int> b = {2,45,4,5,10,7,8};


// VIRKER IKKE
    aaaaaaa.createPerfect(b, 2);
    aaaaaaa.levelorder();

    return 0;
}