#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include "Aktivitet.h"
using namespace std;

string kritiskVej("");

Aktivitet genererAkt(string linje)
{
	
	int pos = 0;
	string temp("");
	for (; linje.at(pos) != '\n' && linje.at(pos) != ';'; pos++)
		temp.push_back(linje.at(pos));
	int e = stoi(temp);
	
	temp = ""; pos++;
	for (; linje.at(pos) != '\n' && linje.at(pos) != ';'; pos++)
		temp.push_back(linje.at(pos));
	string t = temp;
	
	temp = ""; pos++;
	for (; pos < linje.size(); pos++)
		temp.push_back(linje.at(pos));
	int d = stoi(temp);
	
	return Aktivitet(e, t, d);
}

vector<Aktivitet> createTable()
{
	ifstream data;
	data.open("data.txt");
	vector<Aktivitet> tabel;

	while (!data.eof())
	{
		string sa;
		getline(data, sa);
		tabel.push_back(genererAkt(sa));

	}
	return tabel;
}


int main()
{
	vector<Aktivitet> tabel = createTable();

	int totalDuration = 0;

	for (int i = 0; i < tabel.size(); i++)
		totalDuration += tabel[i].getDuration();

	std::cout << "Antal aktiviteter:      " << tabel.size() << endl;
	std::cout << "Gennemsnitlig varighed: " << (float) totalDuration / tabel.size() << endl;

	int laengdeKritiskVej = 0;
	int noOfEvents = tabel[tabel.size()-1].getEvent();
	int aktuelEvent = 1;
	int indeks = 0;
	int maxVarighedAktuelEvent = 0;
	string maxTask = "";
	string minTask = "";				// ny
	string finalMinTask = "";			// ny

	while (true)
	{
		while (indeks < tabel.size() && tabel[indeks].getEvent() == aktuelEvent)
		{
			if (maxVarighedAktuelEvent < tabel[indeks].getDuration())
			{
				maxVarighedAktuelEvent = tabel[indeks].getDuration();
				maxTask = tabel[indeks].getTask();
			}
					
			indeks++;
			
		}
		
		laengdeKritiskVej += maxVarighedAktuelEvent;
		kritiskVej += maxTask;
		maxVarighedAktuelEvent = 0;
		maxTask = "";
		 
		if (indeks == tabel.size())
			break;
		aktuelEvent = tabel[indeks].getEvent();
		
	}

	std::cout << "L�ngde af kritisk vej:  " << laengdeKritiskVej << endl;
	std::cout << "Kritisk vej:            " << kritiskVej << endl;

	// Find aktivitet med mest slæk ( I med 6 tidsenhder )
	
	int maxEvent = tabel.back().getEvent();
    
	// Først findes de højeste durations for hver event.
	std::vector<int> critDurations(maxEvent + 1); // +1 for at negligere 0 index. Vector med antal events elementer, som skal holde en duration for hvert event.
    std::vector<std::string> critEvents(maxEvent + 1); // Vector med strings som gemmer hvilken task, der havde den længste duration til en given event.

    for (Aktivitet i : tabel)
    {
        if( i.getDuration() > critDurations[i.getEvent()]){ //Hvis nuværende task har højere duration end andre task med samme event nr.
            critDurations[i.getEvent()] = i.getDuration();
            critEvents[i.getEvent()] = i.getTask();
        }
    }
	
	// Dernæst sammenlignes vær tasks duration med den længste/kritiske duration for samme event.
	std::vector<int> slackDurations(maxEvent + 1); // +1 for at negligere 0 index
	std::vector<std::string> slackEvents(maxEvent + 1);

	for (Aktivitet i : tabel)
	{
		if ( i.getDuration() < critDurations[i.getEvent()]){
			if ( slackDurations[i.getEvent()] < critDurations[i.getEvent()] - i.getDuration()){ // Hvis kritiske duration - nuværende duration er større end tidligere fundet slack
				slackDurations[i.getEvent()] = critDurations[i.getEvent()] - i.getDuration(); // Opdater den nye højeste slack
				slackEvents[i.getEvent()] = i.getTask(); // angiv hvilken task har højst slack
			}
		}
	}

	// Nu gemmes hver events højeste slæk i slackDurations, med deres tilhørende task i SlackEvents.
	// Så det bare at finde den højeste og printe den.

	int highestSlack = 0;
	std::string highestSlackTask = "";

	for (int i = 1; i < slackDurations.size(); i++)
	{
		if (slackDurations[i] > highestSlack){
			highestSlack = slackDurations[i];
			highestSlackTask = slackEvents[i];
		}
	}
	
	std::cout << "highest slack = " << highestSlack << " on task " << highestSlackTask << std::endl;

	
	
	return 0;
}