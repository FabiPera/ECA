#include <bitset>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>

#ifndef __ECA__
#define __ECA__
	
class ECA{
	
	public:
		std::bitset<8> rule;
		int* initConfig;
		int* t0;
		int* tDam;
		int* tFreq;
		int nCells;
		int steps;
		int denPer;
		int gFreq;
		int damFreq;

		ECA(){
			this->gFreq=0;
		}

		/* Setters */
		void setRule(int rule){
			std::bitset<8> ruleBS(rule);
			for(int i=0; i<8; i++){
				std::cout << ruleBS[i] << std::ends;
				this->rule[i]=ruleBS[i];
			}
			std::cout << "" << std::endl;
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
			this->tFreq=(int*) malloc(this->steps*sizeof(int));
		}

		void setT0(std::string t0){
			std::string str("1");
			this->t0=(int*) malloc(this->nCells*sizeof(int));
			this->initConfig=(int*) malloc(this->nCells*sizeof(int));
			for(int i=0; i<(t0.size()); i++){
				if((str.compare(t0.substr(i, 1)))==0){
					this->t0[i]=1;
					this->initConfig[i]=1;
					this->gFreq+=1;	
				}
				else{
					this->t0[i]=0;
					this->initConfig[i]=0;
				}	
			}
			printGen();
		}

		int mod(int a){
			if(a<0){
				return (this->nCells)+a;
			}
			else{
				return a%(this->nCells);
			}	
		}

		void getRandomConfiguration(){
			this->t0=(int*) malloc(nCells*sizeof(int));
			this->initConfig=(int*) malloc(nCells*sizeof(int));
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
		}

		void setDamage(int m){
			this->tDam=(int*) malloc(this->nCells*sizeof(int));
			for(int i=0; i<this->nCells; i++){
				t0[i]=initConfig[i];
				if(i==m){
					this->tDam[i]=(!this->t0[i]);
				}
				else{
					this->tDam[i]=this->t0[i];
				}
				std::cout << tDam[i] << std::ends;
			}
			std::cout << "" << std::endl;
		}

		void phenotipicAnalysis(){
			int m=this->nCells/2;
			std::cout << m << std::endl;
			setDamage(m);
		}

		int* evolve(int* t0){
			int* t1=(int*) malloc(this->nCells*sizeof(int));
			int n;
			std::bitset<3> neighb;

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
		
		void getNextGen(){
			int* t1=(int*) malloc(nCells*sizeof(int));
			this->gFreq=0;
			int n;
			std::bitset<3> next;

			for(int i=0; i<(this->nCells); i++){
				next[0]=(this->t0[mod(i-1)]);
				next[1]=(this->t0[i]);
				next[2]=(this->t0[mod(i+1)]);
				n=0;
				if(next.test(0)){
					n+=4;
				}
				if(next.test(1)){
					n+=2;
				}
				if(next.test(2)){
					n+=1;
				}
				if(this->rule.test(n)){
					gFreq+=1;
					t1[i]=1;
				}
				else{
					t1[i]=0;
				}
			}
			this->t0=t1;
		}

		void printGen(){
			for(int i=0; i<(this->nCells); i++){
				if(this->t0[i]){
					std::cout << "1" << std::ends;
				}
				else{
					std::cout << "0" << std::ends;		
				}
				
			}
			std::cout << "" << std::endl;
		}
};

#endif