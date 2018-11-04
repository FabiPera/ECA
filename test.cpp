#include <bitset>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include "ECA.h"
using namespace std;

int main(int argc, char **argv){
	int lyap0=0, lyapN=0;
	double lyapExp;
	string str("0101101110010010001");
	ECA eca(30, 30, str);
	eca.setDamage(9);
	for(int i=0; i < eca.steps; i++){
		for(int j=0; j < eca.t0.length; j++){
			if(eca.t0.bits[j] ^ eca.tDam.bits[j]){
				eca.damageFreq[j]+=1;
			}
		}
		if(i > 1){
			lyapN=eca.countDefects();
			lyapExp=eca.getLyapunovExp(1, lyapN);
			cout << lyapExp << endl;
		}
		eca.t0=eca.evolve(eca.t0);
		eca.tDam=eca.evolve(eca.tDam);
	}
	//cout << lyap0 << endl;
	//lyapN=eca.countDefects();
	//cout << lyapN << endl;
	//double lyapExp=eca.getLyapunovExp(1, lyapN);
	

	return 0;
}