#include <iostream>

class Node {
public:
    int data;
    Node* next;

    Node(int value) : data(value), next(nullptr) {}
};

class SinglyLinkedList {
private:
    Node* header;  // Pointer til header-noden

public:
    SinglyLinkedList() {
        header = new Node(0);  // Header node med dummy værdi
    }

    ~SinglyLinkedList() {
        Node* current = header;
        while (current != nullptr) {
            Node* nextNode = current->next;
            delete current;
            current = nextNode;
        }
    }

    // Opgave a: Returner størrelsen af den linked list
    int size() const {
        int count = 0;
        Node* current = header->next;

        while (current != nullptr)
        {
            count++;
            current = current->next;
        }
        
        return count;
    }

    // Opgave b: Udskriv den linked list
    void print() const {
        Node* current = header->next;

        while (current != nullptr)
        {
            std::cout << current->data << " ";
            current = current->next;

        }
        std::cout << std::endl;
    }

    // Opgave c: Test om en værdi x findes i listen
    bool contains(int x) const {
        Node* current = header->next;

        while (current != nullptr){
            if(current->data == x){
                return true;
            }
            current = current->next;
        }
        return false;
    }

    // Opgave d: Tilføj en værdi x, hvis den ikke allerede findes
    void add(int x) {
        if(!contains(x)){
            Node* newNode = new Node(x);
            newNode->next = header->next;
            header->next = newNode;
        }
    }

    // Opgave e: Fjern en værdi x, hvis den findes i listen
    void remove(int x) {
        Node* current = header->next;

        while (current != nullptr)
        {
            if(current->next->data == x){
                Node* nodeToDelete = current->next;
                current->next = current->next->next;
                delete nodeToDelete;
                return;
            }
            current = current->next;
        }
    }
};

int main() {
    SinglyLinkedList list;

    // Her kan du teste metoderne efter du har implementeret dem
    list.add(3);
    list.add(7);
    list.add(5);
    list.print();  // Skal udskrive: 5 7 3

    std::cout << "Size: " << list.size() << std::endl;  // Skal udskrive: 3

    list.remove(7);
    list.print();  // Skal udskrive: 5 3

    std::cout << "Contains 3: " << (list.contains(3) ? "Yes" : "No") << std::endl;  // Skal udskrive: Yes
    std::cout << "Contains 7: " << (list.contains(7) ? "Yes" : "No") << std::endl;  // Skal udskrive: No

    return 0;
}
