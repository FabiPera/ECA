#include "ECA.h"
#include <bitset>
#include <stdlib.h>
#include <iostream>

int main(int argc, char const *argv[]){

	std::string s0="0000010101000101010101011110111011011011101010101010101110001101";
	
	std::cout << static_cast<int>(s0.size()) << std::endl;
	//ECA eca(30, static_cast<int>(s0.size()), 100, s0);
	ECA eca(30, 64, 100, 50);

	int i;

	//std::cout << eca.t0[10] << std::endl;
	//eca.setOneCellFirstGen();
	/*for(i=0; i<8 ; ++i){
		if(eca.rule.test(i)){
			std::cout << "*" << std::ends;
		}
		else{
			std::cout << "_" << std::ends;		
		}
		
	}
	std::cout << "" << std::endl;
	*/
	eca.setRandomFirstGen();

	for(i=0; i<eca.gens; i++){
		eca.printGen();
		eca.getNextGen();	
	}
	return 0;
}
