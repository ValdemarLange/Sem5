#pragma once
#include <iostream>
using namespace std;
class Aktivitet
{
public:
	Aktivitet();
	Aktivitet(int, string, int);
	int getEvent();
	string getTask();
	int getDuration();
private:
	int event;
	string task;
	int duration;
};

