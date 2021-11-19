
URL = window.URL || window.webkitURL;

var userStream; 					//stream from getUserMedia()
var recorder; 						//WebAudioRecorder object
var input; 							//MediaStreamAudioSourceNode  we'll be recording
var encodingType; 					//holds selected encoding for resulting audio (file)
var encodeAfterRecord = true;       // when to encode
var clicked = false;
var starTime;

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record
var analyserNode;

var nextButton = document.getElementById("nextButton");
var record = document.getElementById("record");
var volumeMeterEl = document.getElementById("volumeMeter");

//add events to those 2 buttons
record.addEventListener("click", startRecording);
//recordButton.addEventListener("click", startRecording);
//stopButton.addEventListener("click", stopRecording);
var queue = new Queue();
var recordingTime = 0;


function timer() {
	var endTime = new Date();
	var timeDiff = endTime - startTime;
	// strip the miliseconds
	timeDiff /= 1000;
	// get seconds
	var seconds = Math.round(timeDiff % 60);
	setTimeout(timer, 1000);
	console.log(seconds);

	if (seconds > 20) {
		document.getElementById("pressrecord").style.display = "block";
		document.getElementById("pressrecord").innerHTML = "Press the stop button"
		
	}
	
}

function startRecording() {
	if (!clicked) {
		queue.size = 100;
		console.log("startRecording() called");
		document.getElementById("pressrecord").style.display = "none";
		startTime = new Date();
		timer();

		var constraints = {
			audio: {
				echoCancellation: false,
				noiseSuppression: true,
				autoGainControl: false,
			},
			video: false

		}

		navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
			__log("getUserMedia() success, stream created, initializing WebAudioRecorder...");

			audioContext = new AudioContext();
			userStream = stream;

			input = audioContext.createMediaStreamSource(stream);
			encodingType = "mp3";

			analyserNode = audioContext.createAnalyser();
			input.connect(analyserNode);

			const pcmData = new Float32Array(analyserNode.fftSize);

			const onFrame = () => {
				analyserNode.getFloatTimeDomainData(pcmData);
				let sumSquares = 0.0;
				for (const amplitude of pcmData) { sumSquares += amplitude * amplitude; }
				volumeMeterEl.value = Math.sqrt(sumSquares / pcmData.length);

				/* 
					var volumeNormalized = volumeMeterEl.value * 1000;
					setTimeout(function () {
					queue.enqueue(volumeNormalized);
				}, 4000);
				if (queue.data.length == 100) {
					queue.dequeue(queue.getFront());
				}
				var averageValue = calculateAverage(queue.data);
				if (averageValue < 3) {
					speak.play();
				} */

				window.requestAnimationFrame(onFrame);
			}
			window.requestAnimationFrame(onFrame);

			recorder = new WebAudioRecorder(input, {
				workerDir: "static/",
				encoding: encodingType,
				numChannels: 2,
				onEncoderLoading: function (recorder, encoding) {
					// show "loading encoder..." display
					__log("Loading " + encoding + " encoder...");
				},
				onEncoderLoaded: function (recorder, encoding) {
					// hide "loading encoder..." display
					__log(encoding + " encoder loaded");
				}
			});


			recorder.onComplete = function (recorder, blob) {
				__log("Encoding complete");
				createDownloadLink(blob);
			}

			recorder.setOptions({
				timeLimit: 30,
				encodeAfterRecord: encodeAfterRecord,
				mp3: {
					bitRate: 192
				}
			});

			//start the recording process
			recorder.startRecording();

			__log("Recording started");	

		}).catch(function (err) {
			//enable the record button if getUSerMedia() fails
			//recordButton.disabled = false;
			//stopButton.disabled = true;

		});

		//disable the record button
		//recordButton.disabled = true;
		//stopButton.disabled = false;
	}
	clicked = true;
	nextButton.style.display = "none";
	record.removeEventListener("click", startRecording);
	record.addEventListener("click", stopRecording);
}

function stopRecording() {
	recordingTime = recorder.recordingTime();

	if (clicked) {
		if (recordingTime < 7) {
			alert("Please record at least 7 seconds!");
			record.removeEventListener("click", stopRecording);
			record.addEventListener("click", startRecording);
			document.getElementById("pressrecord").style.display = "block";
			document.getElementById("pressrecord").innerHTML = "Press the record button again"
		} else {
			startTime = new Date();
		
			queue.clear();
			queue.size = 0;
			console.log("stopRecording() called");

			//stop microphone access
			userStream.getAudioTracks()[0].stop();
			record.disabled = true;

			//tell the recorder to finish the recording (stop recording + encode the recorded audio)
			recorder.finishRecording();

			__log('Recording stopped');

			nextButton.style.display = "flex";
			
		}
		
	}
	clicked = false;
	record.removeEventListener("click", stopRecording);
	record.addEventListener("click", startRecording);
	
}


function createDownloadLink(blob) {
	fetch('/saveAudio', { method: "POST", body: blob }).then(response => response.text().then(text => {
		document.getElementById("formats").innerHTML = 'downloaded';
	}));
}


function __log(e, data) {
	log.innerHTML += "\n" + e + " " + (data || '');
}

function calculateAverage(elmt) {
	var sum = 0;
	for (var i = 0; i < elmt.length; i++) {
		sum += parseInt(elmt[i], 10);
	}

	var avg = sum / elmt.length;

	return avg;
}
