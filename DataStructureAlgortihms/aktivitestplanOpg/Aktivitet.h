#pragma once

class Aktivitet
{
private:
    int event;
    std::string task;
    int duration;
public:
    Aktivitet(int event, std::string task, int duration);
    ~Aktivitet();
    int getEvent();
    std::string getTask();
    int getDuration();
};

Aktivitet::Aktivitet(int event, std::string task, int duration) : event(event), task(task), duration(duration)
{
}

Aktivitet::~Aktivitet()
{
}

int Aktivitet::getEvent(){
    return event;
}

std::string Aktivitet::getTask(){
    return task;
}

int Aktivitet::getDuration(){
    return duration;
}