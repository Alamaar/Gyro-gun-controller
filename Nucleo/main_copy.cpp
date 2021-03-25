#include "mbed.h"
#include "L3G4200D.h"
#include <cstdio>


Timer timer;

L3G4200D gyro(D14, D15);            // Gyron kytkentänavat suluissa


AnalogIn X(A0);  //AD-muuntimella saatavat kiihtyvyystiedot. 0 = 0V ja 1.0 = 3.3V (maksimi)
AnalogIn Y(A1);
AnalogIn Z(A2);


int rawGyro[3] = {0, 0, 0};                 // Gyro-raakadata x, y, z
double rawAcc[3] = {0.0, 0.0, 0.0};

double kerroin = 0.07;  //gyron kerroin 


long long aika= 0;

long long printrate = 0;

double angleGyro[3] = {0, 0, 0};
double angleAccX = 0.0;         //roll
double angleAccY = 0.0;         //pitch

double roll = 0;
double pitch = 0;
double yawn = 0;

double roll2 = 0;
double pitch2 = 0;





int main() 
{
    timer.start();
    timer.reset();
	while(true)
	{
		
        aika = chrono::duration_cast<chrono::microseconds>(timer.elapsed_time()).count(); // Kierrokseen kulunut aika (mikrosekunnit)

        if(aika > 10000)    //näyteväli 10ms
        {   
            timer.reset(); //nollataan laskuri
            gyro.read(rawGyro);
            
            rawGyro[0] = rawGyro[0] - 0.3; // Raakadatan nollakorjaus x, y, z
            rawGyro[1] = rawGyro[1] + 14.8;
            rawGyro[2] = rawGyro[2] - 5.3;

            rawAcc[0] = 97.1 * X - 48.259;
            rawAcc[1] = 96.6 * Y - 47.616; 
            rawAcc[2] = 96.6 * Z - 52.535;   

            
            for(int i=0; i<3; i++)
            {
                angleGyro[i] = (angleGyro[i] +(rawGyro[i]*kerroin*aika*0.000001));   
            }

            angleAccX =  -atan2(-rawAcc[1],rawAcc[2])*57.2957795;
            angleAccY =  (atan2(-rawAcc[0] , sqrt(rawAcc[1] * rawAcc[1] + rawAcc[2] * rawAcc[2])) * 180.0) / 3.14 ;

        

        
            angleGyro[0] = 0.96 * angleGyro[0] + 0.04 * angleAccX;
            angleGyro[1] = 0.96 * angleGyro[1] + 0.04 * angleAccY;


            roll = angleGyro[0];
            pitch = angleGyro[1];
            yawn = angleGyro[2] ;
  
        

            for(int i=0; i<3; i++){                       
                // printf("%i, ",(int)rawGyro[i]);             
                }

            printrate += aika;

            if (printrate > 100000) // 200 ms
            {
                printrate = 0;
                printf("roll %i ", (int)roll);
                printf("pitch %i ", (int)pitch);
                printf("yawn %i ", (int)yawn);
                printf("\r\n"); //Rivinvaihto

            }

        }

	}//end while 
}//end main	