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
		int* frequencies;
		int* damageFreq;
		int steps;
		int denPer;
		int t0Freq;
		int damFreq;
		//double* ps;
		//double h;
		//double hm;

		ECA(){
			t0Freq=0;
		}

		ECA(int r, int s, string str){
			setRule(r);
			setGens(s);
			setT0(str);
			frequencies=new int[steps];
		}

		ECA(int r, int s, int d, int l){
			setRule(r);
			setGens(s);
			setDen(d);
			setRandomT0(l);
			frequencies=new int[steps];
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

		void setT0(string str0){
			t0=BitString(str0.length());
			t0.setStringBits(str0);
			seedConfig=t0;
		}

		void setRandomT0(int l){
			t0=BitString(l);
			seedConfig=BitString(l);
			t0Freq=0;
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
			damageFreq=new int[t0.length]();
			tDam=BitString(t0.length);
			t0=seedConfig;
			tDam=seedConfig;
			int aux=t0.bits[m];
			tDam.bits[m]=(!aux);
		}

		int countDefects(){
			int defects=0;
			for(int i=0; i < t0.length; i++){
				defects+=damageFreq[i];
			}
			return defects;
		}
		
		double getLyapunovExp(int a1, int a2){
			double a=static_cast<double>(a1);
			double b=static_cast<double>(a2);
			double lyapExp=(1.0 / static_cast<double>(steps)) * log(b / a);
			return lyapExp;
		}

		/*void getSpaceEntropy(int size){
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
		}*/

		/*void getSpaceEntropyMetric(int size){
			int pSize=pow(2, size), n, i;
			hm=0.0;
			double p;
			for(i=0; i < pSize; i++){
				p=ps[i] / static_cast<double>(t0.length);
				hm+=(p) * (log2(p));
			}
			hm*=(1.0 / static_cast<double>(size)) * (-1.0);
		}*/
		
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