/*
Simpel prioritetskø implementation. Arrayet bruger ikke plads 0. Derefter er det {rod, barn1, barn2, barntil1, barntil1, barntil2, osv}

Insert: O(log⁡n)O(logn), da vi kun bobler op én gang pr. niveau, og højden af træet er log⁡nlogn.
deleteMin: O(log⁡n)O(logn), da vi potentielt skal "boble ned" hele træhøjden.

Pladsforbrug: O(n)O(n), da vi bruger en array/vektor til at gemme alle elementer.

*/


#include <iostream>
#include <vector>

class PriorityQueue {
private:
    std::vector<int> heap; // Bruges til at gemme heap'en

public:
    PriorityQueue() {
        heap.push_back(-1); // Reserverer indeks 0 (ikke brugt)
    }

    void insert(int value) {
        heap.push_back(value);           // Tilføj elementet i bunden
        int current = heap.size() - 1;   // Start ved det nye elements indeks

        // Bobl op, mens heap-egenskaben ikke er opfyldt
        while (current > 1 && heap[current] < heap[current / 2]) {
            std::swap(heap[current], heap[current / 2]); // Byt med forælder
            current = current / 2;                       // Gå op til forælderen
        }
    }

    int deleteMin() {
        if (heap.size() <= 1) {
            throw std::underflow_error("PriorityQueue is empty");
        }

        int minValue = heap[1];                   // Mindste element er i roden
        heap[1] = heap.back();                   // Flyt det sidste element til roden
        heap.pop_back();                         // Fjern det sidste element

        int current = 1;

        // Bobl ned for at opretholde heap-egenskaben
        while (true) {
            int leftChild = 2 * current;
            int rightChild = 2 * current + 1;
            int smallest = current;

            // Tjek venstre barn
            if (leftChild < heap.size() && heap[leftChild] < heap[smallest]) {
                smallest = leftChild;
            }

            // Tjek højre barn
            if (rightChild < heap.size() && heap[rightChild] < heap[smallest]) {
                smallest = rightChild;
            }

            // Hvis det mindste er ændret, byt og fortsæt
            if (smallest != current) {
                std::swap(heap[current], heap[smallest]);
                current = smallest; // Fortsæt ned til det mindste barn
            } else {
                break; // Heap-egenskaben er opfyldt
            }
        }

        return minValue; // Returnér den oprindelige rod
    }

    void display() {
        for (int i = 1; i < heap.size(); i++) {
            std::cout << heap[i] << " ";
        }
        std::cout << std::endl;
    }
};

int main() {
    PriorityQueue pq;
    pq.insert(10);
    pq.insert(5);
    pq.insert(20);
    pq.insert(3);

    std::cout << "Heap: ";
    pq.display(); // Output: 3 5 20 10

    std::cout << "deleteMin: " << pq.deleteMin() << std::endl; // Output: 3
    std::cout << "Heap after deleteMin: ";
    pq.display(); // Output: 5 10 20

    std::cout << "deleteMin: " << pq.deleteMin() << std::endl; // Output: 5
    std::cout << "Heap after deleteMin: ";
    pq.display(); // Output: 10 20

    return 0;
}
