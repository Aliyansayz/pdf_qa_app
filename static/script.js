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




$(document).ready(function() {
    $("#message-input").autocomplete({
        source: function(request, response) {
            // Use the jQuery ajax method to request the suggestions from the Flask app
            $.ajax({
                url: "/suggestions",
                data: {
                    term: request.term
                },
                dataType: "json",
                success: function(data) {
                    response(data);
                }
            });
        }
    });
 
}

, function loadQuestions() {
    const location = document.getElementById("location").value;
    // Define an object with arrays of questions for each food
    const questions = {
      Makkah: [
        "What are the other must-visit places in Makkah ?",
        "Where can I perform Tawaf around the Kaaba ?",
        "What is the significance of the Kaaba"
      ],
      Mina: [
        "How can I travel back to Makkah from Mina ?",
        "What is the purpose of staying in Mina during Hajj ?",
        "What facilities are available in Mina ?",
        "How can I travel back to Makkah from Mina ?"
      ],
      Arfat: [
        "Where can I stay in Arafat during Hajj ?",
        "What happens on the Day of Arafat, the most important day of Hajj ?"
      
      ],
    }
  
    // Get the questions array for the selected food
    const locationQuestions = questions[location];
    // Create an empty string to store the HTML list
    let list = "";
    // Iterate over the questions array and append each question as a list item
    locationQuestions.forEach((question) => {
      list += `<li onclick="copyText('${question}')">${question}</li>`;
    });
    // Wrap the list items in an unordered list element
    list = `<ul>${list}</ul>`;
    // Set the innerHTML of the questions element to the list
    document.getElementById("questions").innerHTML = list;
  
},
  function copyText(text) {
    document.getElementById("message-input").value = text;
  
  }

  
,  function loadfoodQuestions() {

    const food = document.getElementById("food").value;
    // Define an object with arrays of questions for each food
    const questions = {
      NonGluten: [
        "Enlist some egg non Gluten breakfast and deserts in Saudi Arabia ?"
      ],
      EggFree: [
          "Enlist some egg free top dishes  in Saudi Arabia ?"
      ],
      NonDairy: [
        "What are top  non dairy products in Saudi Arabia ?"
      ],
    };
    // Get the questions array for the selected food
    const foodQuestions = questions[food];
    // Create an empty string to store the HTML list
    let list = "";
    // Iterate over the questions array and append each question as a list item
    foodQuestions.forEach((question) => {
      list += `<li onclick="copyfText('${question}')">${question}</li>`;
    });
    // Wrap the list items in an unordered list element
    list = `<ul>${list}</ul>`;
    // Set the innerHTML of the questions element to the list
    document.getElementById("foodquestions").innerHTML = list;
}
,function copyfText(text) {
        document.getElementById("message-input").value = text;
    
}
    
  


