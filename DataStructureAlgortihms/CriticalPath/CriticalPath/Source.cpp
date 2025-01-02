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
	
	return 0;
}