#include <iostream>
#include <vector>

class HashTable
{
private:
    int table_size;
    std::vector<char> table;
public:
    HashTable(int size): table_size(size), table(size, '\0'){};
    void hashFuncLin(char k);
    void hashFuncQuad(char k);
    void disp();
};

void HashTable::hashFuncLin(char k){
    int index = (11*(k-64)) % table_size;
    bool collision = true;
    int i = 0;
    while(collision){
        if (table[(index + i) % table_size] == '\0'){
            table[(index + i) % table_size] = k;
            collision = false;
        } else{
            i++;
        }
    }
};

void HashTable::hashFuncQuad(char k){
    int index = (11*(k-64)) % table_size;
    bool collision = true;
    int i = 0;
    while(collision){
        if (table[(index + i*i) % table_size] == '\0'){
            table[(index + i*i) % table_size] = k;
            collision = false;
        } else{
            i++;
        }
    }
};

void HashTable::disp(){
    std::cout << "----------------" << std::endl;
    for (int i = 0; i < table_size; i++)
    {
        std::cout << i << " | " << table[i] << std::endl;
    }
};


int main() {
    HashTable ht1(16);
    ht1.hashFuncLin('D');
    ht1.hashFuncLin('E');
    ht1.hashFuncLin('M');
    ht1.hashFuncLin('O');
    ht1.hashFuncLin('C');
    ht1.hashFuncLin('R');
    ht1.hashFuncLin('A');
    ht1.hashFuncLin('T');
    ht1.disp();

    HashTable ht2(16);
    ht2.hashFuncQuad('R');
    ht2.hashFuncQuad('E');
    ht2.hashFuncQuad('P');
    ht2.hashFuncQuad('U');
    ht2.hashFuncQuad('B');
    ht2.hashFuncQuad('L');
    ht2.hashFuncQuad('I');
    ht2.hashFuncQuad('C');
    ht2.hashFuncQuad('A');
    ht2.hashFuncQuad('N');

    ht2.disp();

    return 0;
}