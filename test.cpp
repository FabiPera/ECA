#include <bitset>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include "ECA.h"
using namespace std;

int main(int argc, char **argv){
	ECA eca;
	int size=16;
	int* bin=new int[size];
	bin=eca.intToBin(10, size);
	cout << "Bin" << endl;
	for(int i=0; i<size; i++){
		cout << " " << bin[i] << " " << ends;
	}
	cout << "" << endl;
	int n=eca.binToInt(bin, size);
	cout << "int=" << n << endl;
	double p=static_cast<double>(n)/static_cast<double>(n+5);
	cout << "p=" << p << endl;

	return 0;
}