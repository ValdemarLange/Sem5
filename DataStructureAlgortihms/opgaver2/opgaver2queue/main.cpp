#include <iostream>

class queue
{
private:
    int* array;
    int size;
    int head = 0;
    int tail = 0;
    int data_count = 0;
public:
    queue(int size);
    ~queue();
    void enqueue(int input);
    int dequeue();
    std::pair<int, int> get_head_tail() const;
};

queue::queue(int size) : size(size)
{
    array = new int[size];
}

queue::~queue()
{
    delete [] array;
}

void queue::enqueue(int input){
    if (data_count == size){
        throw std::runtime_error("Queue is full. Cannot enqueue.");
    }
    array[tail] = input;
    tail = (tail + 1) % size;
    data_count++;
}

int queue::dequeue(){
    if (data_count == 0) {
        throw std::runtime_error("Queue is empty. Cannot dequeue.");
    }
    int output = array[head];
    head = (head + 1) % size;
    data_count--;
    return output;
}

std::pair<int, int> queue::get_head_tail() const {
    return {head, tail};
}

int main() {
    std::cout << "Hello, World!" << std::endl;

    queue q(10);

    try {
        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);
        std::cout << "Dequeued: " << q.dequeue() << std::endl; // Should print 1
        std::cout << "Dequeued: " << q.dequeue() << std::endl; // Should print 2
        q.enqueue(4);
        q.enqueue(5);
        auto [head, tail] = q.get_head_tail();
        std::cout << "Head: " << head << ", Tail: " << tail << std::endl;
        std::cout << "Dequeued: " << q.dequeue() << std::endl; // Should print 3
        std::cout << "Dequeued: " << q.dequeue() << std::endl; // Should print 4
        std::cout << "Dequeued: " << q.dequeue() << std::endl; // Should print 5

        // Test queue full condition
        for (int i = 0; i < 10; ++i) {
            q.enqueue(i);
        }
        std::cout << "Queue full test passed." << std::endl;

        std::cout << "New Head: " << q.get_head_tail().first << ", New Tail: " << q.get_head_tail().second << std::endl;

        // Test queue empty condition
        for (int i = 0; i < 10; ++i) {
            std::cout << "Dequeued: " << q.dequeue() << std::endl;
        }
        std::cout << "Queue empty test passed." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}