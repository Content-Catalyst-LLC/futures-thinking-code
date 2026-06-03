#include <stdio.h>
double enabling_score(double m,double c,double s,double i,double g,double l,double e){return 0.16*m+0.18*c+0.16*s+0.16*i+0.14*g+0.12*l+0.08*(1-e);} int main(void){printf("Renewable energy acceleration enabling score: %.4f\n", enabling_score(0.78,0.74,0.74,0.68,0.66,0.72,0.48)); return 0;}
