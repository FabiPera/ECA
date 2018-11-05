#include <bitset>
#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include "ECA.h"
using namespace std;

int main(int argc, char **argv){
	int lyap0=0, lyapN=0;
	ofstream lyapExpFile;
	lyapExpFile.open("lyapExp.txt");
	double lyapExp;
	string str("0101101110010010001");
	ECA eca(50, 30, str);
	eca.dmgPos=9;
	eca.setDamage();
	for(int i=0; i < eca.steps; i++){
		for(int j=0; j < eca.t0.length; j++){
			if(eca.t0.bits[j] ^ eca.tDam.bits[j]){
				eca.damageFreq[j]+=1;
			}
		}
		if(i > 0){
			lyapN=eca.countDefects();
			lyapExp=eca.getLyapunovExp(1, lyapN);
			cout << lyapExp << endl;
			lyapExpFile << i << " ";
			lyapExpFile << lyapExp << "\n";
		}
		eca.t0=eca.evolve(eca.t0);
		eca.tDam=eca.evolve(eca.tDam);
	}
	lyapExpFile.close();
	//cout << lyap0 << endl;
	//lyapN=eca.countDefects();
	//cout << lyapN << endl;
	//double lyapExp=eca.getLyapunovExp(1, lyapN);
	

	return 0;
}