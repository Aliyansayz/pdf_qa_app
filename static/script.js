var recorder;

// A function to start and stop recording
function record() {
  // Get the record button element
  var recordButton = document.getElementById("speak-button");

  // Check if the recorder is already created
  if (recorder) {
    // Stop the recording
    recorder.stop();

    // Change the record button text
     recordButton.innerHTML = "<i class=\"fa fa-microphone\"></i>" ;
    // Reset the recorder
    recorder = null;
  } else {
    // Create a new recorder object
    recorder = new webkitSpeechRecognition();

    // Get the selected language from the dropdown menu
    var language = document.getElementById("language").value;

    // Set the recorder language
    recorder.lang = language;

    // Set the recorder to continuous mode
    recorder.continuous = true;

    // Set the recorder to return interim results
    recorder.interimResults = true;

    // Get the message box element
    var messageBox = document.getElementById("message-input");

    // Clear the message box
    messageBox.value = "";

    // Add an event listener for the result event
    recorder.onresult = function(event) {
      // Loop through the results
      for (var i = event.resultIndex; i < event.results.length; i++) {
        // Check if the result is final
        if (event.results[i].isFinal) {
          // Append the final result to the message box
          messageBox.value += event.results[i][0].transcript;
        }
      }
    };

    // Start the recording
    recorder.start();

    // Change the record button text
    recordButton.innerHTML = "Stop";
  }
}
