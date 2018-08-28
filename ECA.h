#include <bitset>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
using namespace std;

#ifndef __ECA__
#define __ECA__
	
class ECA{
	
	public:
		bitset<8> rule;
		int* initConfig;
		int* t0;
		int* tDam;
		int* tFreq;
		int* dFreq;
		int* depFreqFR;
		int* depFreqFL;
		double* ps;
		int nCells;
		int steps;
		int denPer;
		int gFreq;
		int damFreq;
		double h;
		double hm;

		ECA(){
			this->gFreq=0;
		}

		/* Setters */
		void setRule(int rule){
			bitset<8> ruleBS(rule);
			for(int i=0; i<8; i++){
				this->rule[i]=ruleBS[i];
			}
		}

		void setCells(int cells){
			this->nCells=cells;
		}

		void setGens(int gens){
			this->steps=gens;
		}

		void setDen(int den){
			this->denPer=den;
		}

		void setTFreq(){
			this->tFreq=new int[this->steps];
		}

		void setT0(string t0){
			string str("1");
			this->t0=new int[this->nCells];
			this->initConfig=new int[this->nCells];
			for(int i=0; i<nCells; i++){
				if((str.compare(t0.substr(i, 1)))==0){
					this->t0[i]=1;
					this->initConfig[i]=1;	
				}
				else{
					this->t0[i]=0;
					this->initConfig[i]=0;
				}	
			}
		}

		int mod(int a){
			if(a<0){
				return (this->nCells)+a;
			}
			else{
				return a%(this->nCells);
			}	
		}

		int* intToBin(int n, int size){
			int* a=new int[size];
			int* bin=new int[size];
			int i=0, j=0;
			while(n){
				a[i]=n%2;
				cout << a[i] << endl;
				n/=2;
				i++;
			}
			i--;

			while(j<size){
				if(i>=0){
					bin[i]=a[i];
					i--;
				}
				else{
					bin[j]=0;
				}
				j++;
			}
			return bin;
		}

		int binToInt(int* bin, int size){
			int n=0;
			for(int i=0; i<size; ++i){
				if(bin[i]){
					n+=pow(2.0, i);
				}
			}
			return n;
		}

		void getRandomConfiguration(){
			this->t0=new int[nCells];
			this->initConfig=new int[nCells];
			int dens=((this->denPer)*(this->nCells))/100;
			int n, x, d=0;
			for(int i=0; i<(this->nCells); i++){
				n=3214847 + (rand()%static_cast<int>(52178912397 - 3214847 + 1));
				x=n%2;
				if(x){
					this->t0[i]=1;
					this->initConfig[i]=1;
					this->gFreq+=1;
					d+=1;
				}
			}

			while(this->gFreq>dens){
				n=0+(rand()%static_cast<int>(((this->nCells)-0)+1));
				if(t0[n]){
					t0[n]=0;
					initConfig[n]=0;
					this->gFreq-=1;
				}
			}

			while(this->gFreq<dens){
				n=0+(rand()%static_cast<int>(((this->nCells)-0)+1));
				if(!(t0[n])){
					t0[n]=1;
					initConfig[n]=1;
					this->gFreq+=1;
				}	
			}
		}

		int* evolve(int* t0){
			int* t1=new int[this->nCells];
			int n;
			bitset<3> neighb;

			for(int i=0; i<(this->nCells); i++){
				neighb[0]=(t0[mod(i-1)]);
				neighb[1]=(t0[i]);
				neighb[2]=(t0[mod(i+1)]);
				n=0;
				if(neighb.test(0)){
					n+=4;
				}
				if(neighb.test(1)){
					n+=2;
				}
				if(neighb.test(2)){
					n+=1;
				}
				if(this->rule.test(n)){
					t1[i]=1;
				}
				else{
					t1[i]=0;
				}
			}
			return t1;
		}

		void setDamage(int m){
			this->dFreq=new int[nCells];
			this->tDam=new int[nCells];
			for(int i=0; i<this->nCells; i++){
				this->dFreq[i]=0;
				t0[i]=initConfig[i];
				if(i==m){
					this->tDam[i]=(!this->t0[i]);
				}
				else{
					this->tDam[i]=this->t0[i];
				}
			}
		}

		void printDamageFreq(){
			for (int i=0; i<this->nCells; i++){
				cout << this->dFreq[i] << ends;
			}
			cout << "" << endl;
		}

		void getSpaceEntropy(int size){
			int* str=new int[size];
			int pSize=pow(2, size), n, i, j, k;
			this->ps=new double[pSize];
			this->h=0.0;

			for(i=0; i<(this->nCells)-size; i++){
				k=i;
				for(j=0; j<size; j++){
					str[j]=this->t0[k];
					k++;
				}
				n=binToInt(str, size);
				this->ps[n]+=1.0;
			}

			for(i=0; i<pSize; i++){
				if(this->ps[i]){
					this->h+=1.0;
				}
			}
			this->h=(1.0/static_cast<double>(size))*log2(h);
		}

		void getSpaceEntropyMetric(int size){
			int pSize=pow(2, size), n, i;
			this->hm=0.0;
			double p;
			for(i=0; i<pSize; i++){
				p=this->ps[i]/static_cast<double>(nCells);
				this->hm+=(p)*(log2(p));
			}
			this->hm*=(1.0/static_cast<double>(size))*(-1.0);
		}

		void phenotipicAnalysis(){
			int m=this->nCells/2;
			setDamage(m);
		}
		
		void printGen(){
			for(int i=0; i<(this->nCells); i++){
				if(this->t0[i]){
					cout << "1" << ends;
				}
				else{
					cout << "0" << ends;		
				}
			}
			cout << "" << endl;
		}
};

#endif