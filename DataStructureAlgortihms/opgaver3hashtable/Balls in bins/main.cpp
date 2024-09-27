#include <iostream>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <random>

class ballsnbins
{
private:
    int *bins;
    int size;
    std::mt19937 generator; // Tilfældighedsgenerator

public:
    ballsnbins(int s) : size(s), generator(std::random_device{}())
    {
        bins = new int[size](); // Initialize all elements to zero
        for (int i = 0; i < size; ++i)
        {
            bins[i] = 0;
        }
        // std::srand(std::time(nullptr)); // Seed the random number generator
    }

    ~ballsnbins()
    {
        delete[] bins;
    }

    int getSize() const
    {
        return size;
    }

    int &operator[](int index)
    {
        return bins[index];
    }

    const int &operator[](int index) const
    {
        return bins[index];
    }

    void place_balls_rand()
    {
        std::uniform_int_distribution<int> distribution(0, size - 1); // Fortsat tilfældig distribution

        for (int i = 0; i < size; i++)
        {
            bins[distribution(generator)]++;
        }
    }

    void place_balls_two()
    {
        std::uniform_int_distribution<int> distribution(0, size - 1);
        for (int i = 0; i < size; i++)
        {
            int a = distribution(generator);
            int b = distribution(generator);

            if (bins[a] < bins[b])
            {
                bins[a]++;
            }
            else
            {
                bins[b]++;
            }
        }
    }

    void clear_bins()
    {
        for (int i = 0; i < size; ++i)
        {
            bins[i] = 0;
        }
    }

    int get_max()
    {
        int max = *std::max_element(bins, bins + size);
        // std::cout << "Max: " << max << std::endl;
        return max;
    }
};

int main()
{
    std::cout << "Hello, World!" << std::endl;
    ballsnbins bb1(32749);
    //    bb1.place_balls_rand();

    // for (int i = 0; i < 10000; i++)
    // {
    //     std::cout << i << "  |  " << bb1.operator[](i) << std::endl;
    // }

    int sum = 0;
    double avg = 0.0; // or double for higher precision
    int n = 10000;
    int peak = 0;
    for (int i = 0; i < n; ++i)
    {
        bb1.clear_bins();
        bb1.place_balls_two();
        // bb1.place_balls_two();
        int current_max = bb1.get_max();
        sum += current_max;
        if (peak < current_max)
        {
            peak = current_max;
        }
    }
    avg = ((double)sum) / n;

    std::cout << "Avg: " << avg << " | Peak: " << peak << std::endl;

    return 0;
}

/* 10.007 bins n balls:
    n = 100.000
    Avg: 6.67125 | Peak: 12

        log(10007) / (log(log(10007))) = 4.148 364 529
        Jeg kan ikke se hvordan det stemmer overens med noget som helst. Jeg regner nok de forkerte ting ud.

    32.749 bins n balls:
    n = 100.000
    Avg: 7.26052 | Peak: 12


    //// POWER OF TWO CHOICES ///

    10.007 bins n balls:
    n = 100.000
    Avg: 3.0595 | Peak: 4

    32.747 bins n balls:
    n = 100.000
    Avg: 3.18057 | Peak: 4



*/