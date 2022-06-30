let clockFont;


function setup() {
	createCanvas(windowWidth, windowHeight);
	clockFont = loadFont("./digital-7/digital-7.ttf");
	//clockFont = loadFont("./Orbitron/static/Orbitron-Regular.ttf");
	//textSize(10);
}


function draw() {
	background("Black");
	clock();
}

function clock() {
	fill("White");
	textFont(clockFont);
	textAlign(CENTER, CENTER);
	textSize(width/4.25);
	let Hour = hour();
	let min = minute();
	let secs = second();
	secs = secs.toString();
	let noon = Hour >= 12 ? " PM" : " AM"
	if (min < 10) {
		min = "0" + min;
	}
	Hour %= 12
	if (secs.length === 1) {
		secs = "0"+secs;
	}
	text(Hour+":"+min+":"+secs, width/2, height/2); 

	textSize(80);
	text(noon, width/2, (height/2)+210);
}