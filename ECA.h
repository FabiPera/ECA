#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include "BitString.h"
using namespace std;

#ifndef __ECA__
#define __ECA__
	
class ECA{
	
	public:
		BitString rule;
		BitString seedConfig;
		BitString t0;
		BitString tDam;
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
			gFreq=0;
		}

		/* Setters */
		void setRule(int r){
			rule=BitString(r, 8);
		}

		void setGens(int gens){
			steps=gens;
		}

		void setDen(int den){
			denPer=den;
		}

		void setTFreq(){
			tFreq=new int[steps];
		}

		void setT0(string str0){
			string str("1");
			t0=BitString(str0.length());
			t0.setStringBits(str0);
			seedConfig=t0;
			/*this->t0=Configuration(t0.length());
			this->t0.setConfiguration(t0);
			this->initConfig=Configuration(t0.length());
			this->initConfig.setConfiguration(t0);*/
		}

		void setRandomT0(int l){
			t0=BitString(l);
			seedConfig=BitString(l);
			gFreq=0;
			int dens=static_cast<int>((denPer) * (t0.length) / 100);
			t0.setRandomBits(dens);
			seedConfig=t0;
		}

		BitString evolve(BitString t0){
			BitString t1(t0.length);
			int n=0;
			BitString neighb(3);
			for(int i=0; i < t0.length; i++){
				neighb.bits[2]=t0.getCellValue(i-1);
				neighb.bits[1]=t0.getCellValue(i);
				neighb.bits[0]=t0.getCellValue(i+1);
				n=neighb.binToInt();
				if(rule.bits[n]){
					t1.bits[i]=1;
				}
				else{
					t1.bits[i]=0;
				}
			}
			return t1;
		}

		void setDamage(int m){
			dFreq=new int[t0.length]();
			tDam=BitString(t0.length);
			t0=seedConfig;
			tDam=seedConfig;
			tDam.bits[m]=!(t0.bits[m]);
			/*for(int i=0; i < t0.length; i++){
				dFreq[i]=0;
				t0.config[i]=initConfig.config[i];
				if(i==m){
					this->tDam.config[i]=(!this->t0.config[i]);
				}
				else{
					this->tDam.config[i]=this->t0.config[i];
				}
			}*/
		}

		void getSpaceEntropy(int size){
			BitString str(size);
			int pSize=pow(2, size), n, i, j, k;
			ps=new double[pSize];
			h=0.0;

			for(i=0; i < (t0.length - size); i++){
				k=i;
				for(j=0; j < size; j++){
					str.bits[j]=t0.bits[k];
					k++;
				}
				n=str.binToInt();
				ps[n]+=1.0;
			}

			for(i=0; i < pSize; i++){
				if(ps[i]){
					h+=1.0;
				}
			}
			h=(1.0 / static_cast<double>(size)) * log2(h);
		}

		void getSpaceEntropyMetric(int size){
			int pSize=pow(2, size), n, i;
			hm=0.0;
			double p;
			for(i=0; i < pSize; i++){
				p=ps[i] / static_cast<double>(t0.length);
				hm+=(p) * (log2(p));
			}
			hm*=(1.0 / static_cast<double>(size)) * (-1.0);
		}

		void phenotipicAnalysis(){
			int m=t0.length / 2;
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