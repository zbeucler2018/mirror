

// configs
const workTime = 25 * 60;
const restTime = 5 * 60;
const SQUARE_SIZE = 500;


//
let currentTime = 0;
let WORKING = true;
let RESTING = false;
let fillCounter = 0;
let timeText = "00:00";
let startTime, fillAmount;
//let cycleNumber = 0;



function convertSeconds(s) {
  var min = floor(s / 60);
  var sec = s % 60;
  return nf(min, 2) + ':' + nf(sec, 2);
}


function setup() {
  createCanvas(windowWidth, windowHeight);
  background("Black");
  textAlign(CENTER);
  rectMode(CENTER);
  textSize(120);
  startTime = millis();
}


function draw() {
  
  if (WORKING) {
    // give inital value 25:00
    timeText = convertSeconds(workTime - currentTime); 
    
    // update the time every second with the new time
    if (frameCount % 60 == 0) { 
      currentTime = floor((millis() - startTime) / 1000);
      timeText = convertSeconds(workTime - currentTime);
      
      // update the filler rectangle
      fillCounter = fillCounter+1;
      fillAmount = fillCounter * (SQUARE_SIZE / workTime);

      // move to next stage if time is finished
      if (currentTime == workTime) {
        RESTING = true;
        WORKING = false;
        fillCounter = 0;
      }
    }
  }

  if (RESTING) {
    // give inital value 5:00
    timeText = convertSeconds(restTime - currentTime); 
    
    // update the time every second with the new time
    if (frameCount % 60 == 0) { 
      currentTime = floor((millis() - startTime) / 1000);
      timeText = convertSeconds(restTime - currentTime);
      
      // update the filler rectangle
      fillCounter = fillCounter+1;
      fillAmount = fillCounter * (SQUARE_SIZE / restTime);

      // move to next stage if time is finished
      if (currentTime == restTime) {
        RESTING = false;
        WORKING = true;
        fillCounter = 0;
      }
    }
  }
  
  //the main rectangle
  stroke("White");
  strokeWeight(4);
  fill("Black");
  rect(width/2, height/2, SQUARE_SIZE, SQUARE_SIZE);

  // fill rectangle
  fill("White");
  rect(width/2, height/2, SQUARE_SIZE, fillAmount);
  
  //The timer text
  fill("Black")
  text(timeText, width/2, (height/2)+30);
}
