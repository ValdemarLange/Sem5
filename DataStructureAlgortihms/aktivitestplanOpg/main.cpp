#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

#include "Aktivitet.h"

std::pair<int, std::string> getCriticalPath(std::vector<Aktivitet> tabel)
{
    int maxEvent = tabel.back().getEvent();
    std::vector<int> critDurations(maxEvent + 1); // +1 for at negligere 0 index
    std::vector<std::string> critEvents(maxEvent + 1);

    for (Aktivitet i : tabel)
    {
        if( i.getDuration() > critDurations[i.getEvent()]){
            critDurations[i.getEvent()] = i.getDuration();
            critEvents[i.getEvent()] = i.getTask();
        }
    }
    int durationSum = 0;
    std::string order = "(";
    for (int i = 1; i < maxEvent +1; i++)
    {
        if(critDurations[i] != 0){
            durationSum += critDurations[i];
            order.append(critEvents[i]);
            order.append(", ");
        }
    }
    order.pop_back();
    order.pop_back();
    order.append(")");
    
    return std::pair<int, std::string> (durationSum,order);
}

int main()
{
    std::ifstream file("data1.txt");
    if (!file.is_open())
    {
        std::cerr << "Failed to open file" << std::endl;
        return 1;
    }
    std::cout << std::endl;
    std::vector<Aktivitet> tabel;

    std::string line;
    while (std::getline(file, line))
    {
        std::istringstream iss(line);
        std::string token;
        int event, duration;
        std::string task;

        std::getline(iss, token, ';');
        event = std::stoi(token);

        std::getline(iss, task, ';');

        std::getline(iss, token, ';');
        duration = std::stoi(token);

        tabel.push_back(Aktivitet(event, task, duration));
    }

//    std::cout << tabel[1].getEvent() << tabel[1].getTask() << tabel[1].getDuration() << std::endl;

    int count = tabel.size();
    float avg = 0;
    for (Aktivitet i : tabel)
    {
        avg += i.getDuration();
    }
    avg = avg / count;

    std::cout << "Antal aktiviteter: " << count << ", gennesnitlig varighed: " << avg << std::endl;

    std::pair<int, std::string> criticalPath = getCriticalPath(tabel);
    int critDuration = criticalPath.first;
    std::string critOrder = criticalPath.second;


    std::cout << "Kritiske vej:" << std::endl;
    std::cout << "  varighed: " << critDuration << ", rækkefølge: " << critOrder << std::endl;

    file.close();
    std::cout << std::endl;
    return 0;
}