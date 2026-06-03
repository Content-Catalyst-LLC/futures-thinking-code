#include <iostream>
double data_quality(double c,double v,double f,double t){return 0.25*c+0.25*v+0.25*f+0.25*t;}
int main(){std::cout<<"Public trust driver data quality="<<data_quality(1.0,0.95,0.78,0.70)<<"\n";return 0;}
