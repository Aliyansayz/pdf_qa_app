// suggestions.js

// Wait for the document to be ready
$(document).ready(function() {
    // Select the text input with the id of "query"
    $("#message-input").autocomplete({
        // Specify a function for the source option
        source: function(request, response) {
            // Use the jQuery ajax method to request the suggestions from the Flask app
            $.ajax({
                url: "/suggestions",
                data: {
                    // Pass the term parameter with the value of the request
                    term: request.term
                },
                dataType: "json",
                success: function(data) {
                    // Pass the data to the response callback
                    response(data);
                }
            });
        }
    });
});
