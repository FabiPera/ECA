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
		int* t0;
		int* t1;
		int* tFreq;
		int nCells;
		int steps;
		int denPer;
		int gFreq;

		ECA(){
			this->gFreq=0;
		}

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
			for(int i=0; i<(t0.size()); i++){
				if((str.compare(t0.substr(i, 1)))==0){
					this->t0[i]=1;
					this->gFreq+=1;	
				}
				else{
					this->t0[i]=0;		
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
			int dens=((this->denPer)*(this->nCells))/100;
			int n, x, d=0;
			for(int i=0; i<(this->nCells); i++){
				n=3214847 + (rand()%static_cast<int>(52178912397 - 3214847 + 1));
				x=n%2;
				if(x){
					this->t0[i]=1;
					this->gFreq+=1;
					d+=1;
				}
			}

			while(this->gFreq>dens){
				n=0+(rand()%static_cast<int>(((this->nCells)-0)+1));
				if(t0[n]){
					t0[n]=0;
					this->gFreq-=1;
				}
			}
		}
		
		void getNextGen(){
			this->t1=(int*) malloc(nCells*sizeof(int));
			this->gFreq=0;
			int n;
			std::bitset<3> next;

			for(int i=0; i<(this->nCells); i++){
				next[0]=(this->t0[mod(i-1)]);
				next[1]=(this->t0[i]);
				next[2]=(this->t0[mod(i+1)]);
				for(int j=0; j<3; j++){
					
				}
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
					this->t1[i]=1;
				}
				else{
					this->t1[i]=0;
				}
			}
			this->t0=this->t1;
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