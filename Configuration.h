#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
using namespace std;

#ifndef __Configuration__
#define __Configuration__

class Configuration{
	
	public:
		int* config;
		int length;

		Configuration(){
			length=8;
		}

		Configuration(int l){
			length=l;
			config=new int[length]();
		}

		Configuration(int n, int l){
			length=l;
			config=intToBin(n, length);
		}

		int getCellValue(int i){
			i=mod(i);
			return config[i];
		}

		void setConfiguration(string t0){
			string str("1");
			for(int i=0; i<t0.length(); i++){
				if((str.compare(t0.substr(i, 1)))==0){
					this->config[i]=1;
				}
				else{
					this->config[i]=0;
				}	
			}
		}

		void setRandomConfiguration(int dens){
			int n, gFreq=0;
			srand((unsigned) time(0));
			while(gFreq<dens){
				n=0+(rand()%static_cast<int>(((this->length-1)-0)+1));
				if(this->config[n]!=1){
					this->config[n]=1;
					gFreq+=1;
				}
			}
		}

		int* intToBin(int n, int size){
			int* a=new int[size];
			int* bin=new int[size];
			int i=0, j=0;
			while(n){
				a[i]=n%2;
				//cout << a[i] << endl;
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

		int binToInt(){
			int n=0;
			for(int i=0; i<length; ++i){
				if(config[i]){
					n+=pow(2.0, i);
				}
			}
			return n;
		}

		int mod(int a){
			if(a<0){
				return (length)+a;
			}
			else{
				return a%(length);
			}	
		}
};

#endif