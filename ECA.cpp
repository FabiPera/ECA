#include "ECA.h"
#include <bitset>
#include <stdlib.h>
#include <iostream>
#include <sstream>

int readIntegerInput(int number, std::string input){
	while(true){
		getline(std::cin, input);
		std::stringstream myStream(input);
		if(myStream >> number)
	  		break;
		std::cout << "Invalid number, please try again" << std::endl;
	}
	return number;
}

int main(int argc, char const *argv[]){
	
	bool run=true;
	int rule=0;
	int cells=0;
	int gens=0;
	int den=0;
	int option=0;
	std::string input="";

	do{
		std::cout << ".::Choose first generation mode::." << std::endl;
		std::cout << "1.-One cell" << std::endl;
		std::cout << "2.-Random" << std::endl;
		std::cout << "3.-From a string" << std::endl;
		std::cout << "4.-Exit" << std::endl;

		option=readIntegerInput(option, input);

		switch(option){
			case 1:{
				std::cout << "Introduce rule" << std::endl;
				rule=readIntegerInput(rule, input);
				input="";
				std::cout << "How many cells?" << std::endl;
				cells=readIntegerInput(cells, input);
				input="";
				std::cout << "How many generations?" << std::endl;
				gens=readIntegerInput(gens, input);
				input="";
				ECA eca1(rule, cells, gens, 0);
				eca1.startSim(0);
				break;
			}
			case 2:{
				std::cout << "Introduce rule" << std::endl;
				rule=readIntegerInput(rule, input);
				input="";
				std::cout << "How many cells?" << std::endl;
				cells=readIntegerInput(cells, input);
				input="";
				std::cout << "How many generations?" << std::endl;
				gens=readIntegerInput(gens, input);
				input="";
				std::cout << "Introduce the initial density" << std::endl;
				cells=readIntegerInput(den, input);
				input="";
				ECA eca2(rule, cells, gens, den);
				eca2.startSim(1);
				break;
			}
			case 3:{
				std::cout << "Introduce rule" << std::endl;
				rule=readIntegerInput(rule, input);
				input="";
				std::cout << "How many generations?" << std::endl;
				gens=readIntegerInput(gens, input);
				input="";
				std::cout << "Introduce the first generation string" << std::endl;
				getline(std::cin, input);
				ECA eca3(30, static_cast<int>(input.size()), 100, input);
				eca3.startSim(2);
				break;
			}
			case 4:{
				run=false;
				break;
			}
			default:{
				std::cout << "Invalid option, please try again" << std::endl;
				break;
			}
		}
	}
	while(run);
	return 0;
}
