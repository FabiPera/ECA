#include <iostream>
#include <string>
#include <random>
#include <math.h>
using namespace std;

#ifndef __BitString__
#define __BitString__

class BitString{
	
	public:
		int* bits;
		int length;

		BitString(){
			length=8;
			bits=new int[length]();
		}

		BitString(int l){
			length=l;
			bits=new int[length]();
		}

		BitString(int n, int l){
			length=l;
			bits=intToBin(n, length);
		}

		void operator=(const BitString& b){
			bits=new int[b.length]();
			length=b.length;
			memcpy(bits, b.bits, sizeof(int) * b.length);
		}

		int getCellValue(int i){
			i=mod(i);
			return bits[i];
		}

		void setStringBits(string t0){
			string str("1");
			for(int i=0; i < t0.length(); i++){
				if((str.compare(t0.substr(i, 1))) == 0){
					bits[i]=1;
				}
				else{
					bits[i]=0;
				}	
			}
		}

		void setRandomBits(int dens){
			int n, t0Freq=0;
			srand((unsigned) time(0));
			random_device rd;
			mt19937 engine(rd());
			uniform_int_distribution<> dist(0, length - 1);
			while(t0Freq < dens){
				n=dist(engine);
				if(bits[n] != 1){
					bits[n]=1;
					t0Freq+=1;
				}
			}
		}

		int* intToBin(int n, int size){
			int* a=new int[size];
			int* bin=new int[size];
			int i=0, j=0;
			while(n){
				a[i]=n % 2;
				n/=2;
				i++;
			}
			i--;

			while(j < size){
				if(i >= 0){
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
			for(int i=0; i < length; ++i){
				if(bits[i]){
					n+=pow(2.0, i);
				}
			}
			return n;
		}

		string bitsToString(){
			string str="";
			for(int i=0; i < length; i++){
				str.append(to_string(bits[i]));
			}
			return str;
		}

		int mod(int a){
			if(a < 0){
				return (length) + a;
			}
			else{
				return a % (length);
			}	
		}
		
};

#endif