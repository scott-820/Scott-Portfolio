// include the LED Matrix library from the Uno R4 core:
#include "Arduino_LED_Matrix.h"
// make an instance of the library:
ArduinoLEDMatrix matrix;

byte frame[8][12] = {
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0}
};

byte blocks[3][12] = {
  {1,1,1,1,1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1,1,1,1,1}
};

byte W[8][12] = {
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,1,0,0,0,0,0,0,0,0,1,0},
  {0,1,0,0,0,1,1,0,0,0,1,0},
  {0,0,1,0,0,1,1,0,0,1,0,0},
  {0,0,1,0,1,0,0,1,0,1,0,0},
  {0,0,0,1,0,0,0,0,1,0,0,0},
  {0,0,0,1,0,0,0,0,1,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0}
};

byte L[8][12] = {
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,1,0,0,0,0,0,0,0},
  {0,0,0,0,1,0,0,0,0,0,0,0},
  {0,0,0,0,1,0,0,0,0,0,0,0},
  {0,0,0,0,1,0,0,0,0,0,0,0},
  {0,0,0,0,1,0,0,0,0,0,0,0},
  {0,0,0,0,1,1,1,1,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0}
};

int upPin = 1;  // left
int dnPin = 0;  // right
int upNew, dnNew;
int dt = 100;
int i, j, k, l, p, q;
int xinc = 1;
int yinc = 1;
int paddle, paddleRow, paddleWid, hits;
int subLoopCnt = 2; //move the ball every 2 times through the loop, but move the paddles every time through
int subLoop;
int ballCount = 5;
bool win;
int iStart = 3;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  matrix.begin();
  pinMode(upPin,INPUT_PULLUP);
  pinMode(dnPin,INPUT_PULLUP);

} // end setup

void loop() {
  // This code executes once per ball
  bool running = 1;
  iStart = iStart+1;    // Need both odd and even start positions to clear blocks
  i = iStart;
  j = 5;
  yinc = -1;
  paddle = 5;           // Initial paddle coordinates
  paddleRow = 6;
  paddleWid = 3;
  hits = 0;
  upNew = 1;
  dnNew = 1;
  subLoop = 0;

  while (running & ballCount > 0){
    subLoop = subLoop+1;
    // clear the LED matrix
    for(k=0;k<=11;k=k+1){
      for(l=0;l<=7;l=l+1){
        frame[l][k] = 0;
      }
    }
    // draw the blocks
    for (k=0;k<=11;k=k+1){
      for (l=0;l<=2;l=l+1){
        frame[l][k] = blocks[l][k];
      }
    }
    // draw the ball in the new spot
    frame[j][i] = 1;
    // draw the paddle in the new spot  
    for (p=0;p<paddleWid;p=p+1){
      frame[paddleRow][paddle+p] = 1;
    }
    // draw the ball counter
    for (q=0;q<ballCount-1;q=q+1){
      frame[7][q] = 1;
    }
  
    // update the matrix with new ball and paddle, then delay
    matrix.renderBitmap(frame,8,12);
    delay(dt);

    // Update paddle position every time through the while loop
    upNew = digitalRead(upPin);
    dnNew = digitalRead(dnPin);
    if (upNew == 0){
      paddle = paddle - 1;
      if (paddle < 0){
        paddle = 0;
      }
    }
    if (dnNew==0){  
      paddle = paddle + 1;
      if (paddle > 12-paddleWid){
        paddle = 12-paddleWid;
      }
    }

    // Update ball position every subLoopCnt times through the while loop
    if (subLoop==subLoopCnt){
      subLoop = 0;
      // Test current ball position and flip directions when contact detected (i is col, j is row)

      // Test for contact with blocks
      if (j==0 & blocks[j][i]==0){
        yinc = yinc * -1;
      }
      if (j<=2 & blocks[j][i]==1){
        blocks[j][i] = 0;
        yinc = yinc * -1;
      }

      if(i>=11 || i<=0){
        xinc = xinc * -1;
      }
      // Detect paddle hit or miss after ball and paddle positions updated
      if(j==paddleRow & (i>=paddle & i<paddle+paddleWid)){
        hits = hits + 1;
        Serial.print("Paddle Hits = ");
        Serial.println(hits);
        yinc = yinc * -1;
      }
      // Detect paddle miss; decrement ball count. Print L and end game if none left.
      if (j==7){
        Serial.println("Missed the Ball!");
        ballCount = ballCount - 1;
        if (ballCount == 0){
          Serial.println("Game Over!");
          for(k=0;k<=11;k=k+1){
            for(l=0;l<=7;l=l+1){
              frame[l][k] = L[l][k];
            }
          }
          matrix.renderBitmap(frame,8,12);  //render empty frame on loss. Call banner function here.
        }
        running = 0;
        yinc = yinc * -1;
        delay(1000);        
      }
      // Check for Win. Print W and end game.
      win = true;
      for(k=0;k<=11;k=k+1){
        for(l=0;l<=2;l=l+1){
          if (blocks[l][k] == 1){
            win = false;
          }
        }
      }
      if (win){
        Serial.println("You Win!");
        for(k=0;k<=11;k=k+1){
          for(l=0;l<=7;l=l+1){
            frame[l][k] = W[l][k];
          }
        }
        matrix.renderBitmap(frame,8,12);  //render full frame on win. Call banner function here.
        ballCount = 0;
        running = 0;
      }     

      i = i + xinc;
      j = j + yinc;

    }  // end if subLoop
  } // end while running
} // end loop