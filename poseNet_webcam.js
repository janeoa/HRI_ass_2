// Copyright (c) 2018 ml5
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/*
 Human pose detection using machine learning.
 This code uses: 
    ML5.js: giving us easy to use poseNet ML model.
    P5.js: for drawing and creating video output in the browser.
*/

// the output of our webcam
let webcam_output;
// to store the ML model
let poseNet;
// output of our ML model is stores in this
let poses = [];

let framesPerSec = 5;

var poseRec = {
	neutral : {
		frames : 0,
		time : 0
	},
	happy : {
		frames : 0,
		time : 0
	},
	upset : {
		frames : 0,
		time : 0
	},
	angry : {
		frames : 0,
		time : 0
	}
}

/* function setup() is by P5.js:
      it is the first function that is executed and runs only once.
      We will do our initial setup here.
*/

function centerCanvas() {
  var x = (windowWidth) / 2;
  var y = x*3/4;
  resizeCanvas(x, y);
}

function changeFPS(){
	var gotFps = constrain($("#fpsPIcker").val(), 1, 15);
	$("#fpsPIcker").val(gotFps);
	frameRate(gotFps);
	framesPerSec = gotFps;
}

function setup() {
	frameRate(5);
  /* create a box in browser to show our output. Canvas having:
         width: 640 pixels and
         height: 480 pixels
  */
  var x = (windowWidth) / 2;
  var y = x*3/4;
  var atConva = createCanvas(x, y);
  atConva.parent('sketch-holder');
  background(255, 0, 200);

  // get webcam input
  webcam_output = createCapture(VIDEO);
  // set webcam video to the same height and width of our canvas
  webcam_output.size(width, height);

  /* Create a new poseNet model. Input:
      1) give our present webcam output
      2) a function "modelReady" when the model is loaded and ready to use
  */
  poseNet = ml5.poseNet(webcam_output, modelReady);

  /*
    An event or trigger.
    Whenever webcam gives a new image, it is given to the poseNet model.
    The moment pose is detected and output is ready it calls:
    function(result): where result is the models output.
    store this in poses variable for furthur use.
  */
  poseNet.on('pose', function(results) {
    poses = results;
  });

  /* Hide the webcam output for now.
     We will modify the images and show with points and lines of the 
     poses detected later on.
  */
  webcam_output.hide();
}

/* function called when the model is ready to use.
   set the #status field to Model Loaded for the
  user to know we are ready to rock!
 */
function modelReady() {
  select('#status').html('Model Loaded');
  centerCanvas();
}

function windowResized() {
  centerCanvas();
}


/* function draw() is by P5.js:
      This function is called on repeat forever (unless you plan on closing the browser
      and/or pressing the power button)
*/
function draw() {

	// show the image we currently have of the webcam output.
	image(webcam_output, 0, 0, width, height);
	
	// draw the points we have got from the poseNet model
	drawKeypoints();
	// draw the lines too.
// 	drawSkeleton();
}


// A function to draw detected points on the image.
function drawKeypoints(){
	/*
	Remember we saved all the result from the poseNet output in "poses" array.
	Loop through every pose and draw keypoints
	*/
	var numOfpoints = 0;
	
	for (let i = 0; i < poses.length; i++) {
		// For each pose detected, loop through all the keypoints
		let pose = poses[i].pose;
		//       console.log(pose);
		
		$("#nkey").html("");
		$("#akey").html("<tr><th>bone</th><th>score</th><th>x</th><th>y</th></tr>");
		
		
// 		console.log(pose);
		var thereWasHand1 = false;
		var thereWasHand2 = false;
		var twoHands = false;
		
		var elbowPos = {x:0, y:0};
		var wristPos = {x:0, y:0};
		var Shoulder = {x:0, y:0};
		
		var secondLoop = false;
	
		for (let j = 0; j < pose.keypoints.length; j++) {
			          
			// A keypoint is an object describing a body part (like rightArm or leftShoulder)
			let keypoint = pose.keypoints[j];
			// Only draw an ellipse if the pose probability is bigger than 0.2
			
			if(!(keypoint.part=="leftElbow" || keypoint.part=="leftWrist" || keypoint.part=="leftShoulder")){
				continue;
			}
			
			if (keypoint.score > 0.8) {
				  	numOfpoints++;
				$("#akey").append(
					"<tr><td>"+keypoint.part+"</td>score<td>"+
					String(keypoint.score).slice(0,4)+"</td>x<td>"+
					String(keypoint.position.x).slice(0,3)+"</td>y<td>"+
					String(keypoint.position.x).slice(0,3)+"</td></tr>");
				
				$("#nkey").html(numOfpoints);
				
				//STRAT
				
				
				
				//STOP
				
				// choosing colour. RGB where each colour ranges from 0 255
				fill(0, 0, 255);
				// disable drawing outline
				noStroke();
				/* draw a small ellipse. Which being so small looks like a dot. Purpose complete.
				    input: X position of the point in the 2D image
				           Y position as well
				           width in px of the ellipse. 10 given
				           height in px of the ellipse. 10 given
				*/
				if(keypoint.part=="leftElbow"){
					twoHands = thereWasHand1;
					fill(255, 0, 0);
					ellipse(keypoint.position.x, keypoint.position.y, 50, 50);
					thereWasHand1 = true;
					if(Math.abs(elbowPos.x-keypoint.position.x)>30 && secondLoop){
						continue;
					}
					elbowPos.x=keypoint.position.x;
					elbowPos.y=keypoint.position.y;
				}else if(keypoint.part=="leftWrist"){
					twoHands = twoHands || thereWasHand2;
					if(Math.abs(wristPos.x-keypoint.position.x)>30 && secondLoop){
						continue;
					}
					fill(255, 255, 0);
					ellipse(keypoint.position.x, keypoint.position.y, 30, 30);
					thereWasHand2 = true;
					wristPos.x=keypoint.position.x;
					wristPos.y=keypoint.position.y;
				}else if(keypoint.part=="leftShoulder"){
					if(Math.abs(Shoulder.x-keypoint.position.x)>30 && secondLoop){
						continue;
					}
					fill(255, 255, 255);
					ellipse(keypoint.position.x, keypoint.position.y, 20, 20);
					Shoulder.x=keypoint.position.x;
					Shoulder.y=keypoint.position.y;
				}
			}
// 			secondLoop = true;
		}
		
		if(thereWasHand1 && thereWasHand2){
			$("#status").html('<span class="w3-text-green">Hand is visible</span>');
		}else{
			$("#status").html('<span class="w3-text-red">Couldn\'t find hand</span>');
			continue;
		}
		if(twoHands){
			$("#status").html('<span class="w3-text-red">There are two hands!</span>');
		}
		$("#elbow").html('elbow: {'+round(elbowPos.x)+' '+round(elbowPos.y)+'}');
		$("#wrist").html('wrist: {'+round(wristPos.x)+' '+round(wristPos.y)+'}');
		$("#Shoul").html('wrist: {'+round(Shoulder.x)+' '+round(Shoulder.y)+'}');
		
		var dist_se = Math.sqrt(Math.pow(elbowPos.x-Shoulder.x,2) + Math.pow(elbowPos.y-Shoulder.y,2));
		var dist_at = Math.sqrt(Math.pow(elbowPos.x-wristPos.x,2) + Math.pow(elbowPos.y-wristPos.y,2));
		$("#distance").html('distance: {'+ round(dist_at) +'}');
		
		var angle = 90-Math.acos((elbowPos.x- wristPos.x)/dist_at)*180/Math.PI;
		$("#angle").html('angle: {'+ round(angle) +'}');
		
		var speed_t = dist_se/dist_at;
		$("#speed").html('speed: {'+ round((speed_t-1)*100)/100 +'}');
		
		var rotation = angle+15;
		$("#rotation").html('rotation: {'+ round(speed_t) +'}');
		
		$.get("https://10.211.55.11:8001",{"speed": speed_t, "rot" : rotation});
	}	
}



// A function to draw the skeletons
function drawSkeleton() {
    /*
    Remember we saved all the result from the poseNet output in "poses" array.
    Loop through every pose and draw skeleton lines.
   */
  // Loop through all the skeletons detected
  for (let i = 0; i < poses.length; i++) {
    let skeleton = poses[i].skeleton;
    // For every skeleton, loop through all body connections
    for (let j = 0; j < skeleton.length; j++) {
      // line start point
      let startPoint = skeleton[j][0];
      // line end point
      let endPoint = skeleton[j][1];
      // Sets the color used to draw lines and borders around shapes
      stroke(0, 255, 0);
      /* draw a line:
            input: X position of start point of line in this 2D image
                   Y position as well
                   X position of end point of line in this 2D image
                   Y position as well
          */
      line(startPoint.position.x, startPoint.position.y, endPoint.position.x, endPoint.position.y);
    }
  }
}
