#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include "Configuration.h"
using namespace std;

#ifndef __ECA__
#define __ECA__
	
class ECA{
	
	public:
		Configuration rule;
		Configuration initConfig;
		Configuration t0;
		Configuration tDam;
		int* tFreq;
		int* dFreq;
		double* ps;
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
			this->rule=Configuration(rule, 8);
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
			this->t0=Configuration(t0.length());
			this->t0.setConfiguration(t0);
			this->initConfig=Configuration(t0.length());
			this->initConfig.setConfiguration(t0);
		}

		void setRandomT0(int l){
			this->t0=Configuration(l);
			this->initConfig=Configuration(l);
			this->gFreq=0;
			int dens=static_cast<int>((this->denPer)*(t0.length))/100;
			this->t0.setRandomConfiguration(dens);
			this->initConfig.setRandomConfiguration(dens);
		}

		Configuration evolve(Configuration t0){
			Configuration t1(t0.length);
			int n;
			Configuration neighb(3);
			for(int i=0; i<t0.length; i++){
				neighb.config[2]=t0.getCellValue(i-1);
				neighb.config[1]=t0.getCellValue(i);
				neighb.config[0]=t0.getCellValue(i+1);
				n=0;
				n=neighb.binToInt();
				if(this->rule.config[n]){
					t1.config[i]=1;
				}
				else{
					t1.config[i]=0;
				}
			}
			return t1;
		}

		void setDamage(int m){
			this->dFreq=new int[t0.length];
			this->tDam=Configuration(t0.length);
			for(int i=0; i<t0.length; i++){
				this->dFreq[i]=0;
				t0.config[i]=initConfig.config[i];
				if(i==m){
					this->tDam.config[i]=(!this->t0.config[i]);
				}
				else{
					this->tDam.config[i]=this->t0.config[i];
				}
			}
		}

		void getSpaceEntropy(int size){
			Configuration str(size);
			int pSize=pow(2, size), n, i, j, k;
			this->ps=new double[pSize];
			this->h=0.0;

			for(i=0; i<(t0.length)-size; i++){
				k=i;
				for(j=0; j<size; j++){
					str.config[j]=this->t0.config[k];
					k++;
				}
				n=str.binToInt();
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
				p=this->ps[i]/static_cast<double>(t0.length);
				this->hm+=(p)*(log2(p));
			}
			this->hm*=(1.0/static_cast<double>(size))*(-1.0);
		}

		void phenotipicAnalysis(){
			int m=this->t0.length/2;
			setDamage(m);
		}
		
		/*void printGen(){
			for(int i=0; i<(this->t0.length); i++){
				if(this->t0[i]){
					cout << "1" << ends;
				}
				else{
					cout << "0" << ends;		
				}
			}
			cout << "" << endl;
		}*/

		/*void printDamageFreq(){
			for (int i=0; i<this->t0.length; i++){
				cout << this->dFreq[i] << ends;
			}
			cout << "" << endl;
		}*/
};

#endif