#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryHeap.h"
#include "dsexceptions.h"

int main()
{
       // Opret en tom BinaryHeap til heltal
    BinaryHeap<int> heap;

    // Indsæt elementer i heapen
    heap.insert(10);
    heap.insert(20);
    heap.insert(5);
    heap.insert(30);

    // Find og udskriv det mindste element
    std::cout << "Minimum element: " << heap.findMin() << std::endl;

    // Fjern det mindste element
    heap.deleteMin();
    std::cout << "Minimum element efter deleteMin: " << heap.findMin() << std::endl;

    // Opret en BinaryHeap fra en eksisterende liste
    std::vector<int> items = {15, 25, 7, 40};
    BinaryHeap<int> heapFromList(items);

    // Find det mindste element i den nye heap
    std::cout << "Minimum element i heapFromList: " << heapFromList.findMin() << std::endl;


    // std::cout << "---|||||||||||--" << std::endl;

    // BinarySearchTree abe;
    // abe.insert(25);
    // abe.insert(20);
    // abe.insert(36);
    // abe.insert(10);
    // abe.insert(22);
    // abe.insert(30);
    // abe.insert(40);
    // abe.insert(5);
    // abe.insert(12);
    // abe.insert(28);
    // abe.insert(38);
    // abe.insert(48);
    // abe.insert(1);
    // abe.insert(8);
    // abe.insert(15);
    // abe.insert(45);
    // abe.insert(50);

    // abe.printTree();
    // std::cout << abe.findMin() << " MIN " << std::endl;
    // abe.remove(abe.findMin());
    // // abe.printTree();
    // std::cout << abe.findMax() << " MAX " << std::endl;
    // abe.printTree();

    

    return 0;
}