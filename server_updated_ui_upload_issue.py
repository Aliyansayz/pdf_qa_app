import os 
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from response import * 

load_dotenv()
app = Flask(__name__)
global  final_docs_list, uploaded

app.config['UPLOAD_FOLDER'] = "static/documents" 

uploaded = False

pinecone_environment = "gcp-starter"
pinecone_index_name  = "arabic-bot"
pinecoy_api_key = "83ffe0ca-4d89-4d5e-9a46-75bf76d6106f"

embeddings = OpenAIEmbeddings(model_name="ada")
unique_id  =             "aaa365fe031e4b5ab90aba54eaf6012e"

keywords = {

"safety contact emergency services lost items" : [ "What are the safety precautions I should take during Hajj?",
"Who should I contact in case of emergencies?",
"What emergency response services are available in Mecca and Medina?",
"What are the procedures for lost and found items and missing pilgrims?" ] ,

"hotel room service book hajj" : [ "What types of accommodation are available during Hajj?" , 
"How can I book a hotel or other suitable lodging?", 
"What amenities and services are typically provided by hotels during Hajj?" , 
"What are the regulations and protocols for hotel check-in and check-out during Hajj?"
 ] ,

"waste trash clean" : [ "How can I contribute to a clean and sanitary environment during Hajj?",
"Where can I dispose of waste properly?",
"What are the environmental regulations for pilgrims?", 
"Are there initiatives to promote sustainable practices during Hajj?" ] , 

"health medical vaccine " : 
[ "What common health risks are associated with Hajj?" ,
"What vaccinations are required or recommended for pilgrims?",
"Where can I find medical assistance in Mecca and Medina?",
"Will my medicare cover any medical expenses incurred during Hajj?" ] , 

"transportation makkah medina madinah mecca medinah" : [ "How can I get around Mecca and Medina during Hajj?" ,
"Is public transportation available?",
"Are there private transportation options?",
"What are the regulations for car rentals and hiring taxis?" ],

    "food water diet" : [ "What kind of food will be available?",
"Do I need to bring my own food and water?", 
"Are there dietary restrictions in Mecca and Medina?", 
"Where can I find safe and hygienic drinking water?" ] , 

    "cars": ["What is the best car to buy?", "How to maintain your car?", "How to sell your car?"],
    "animals": ["What are some endangered animals?", "How to adopt a pet?", "How to train your dog?"],
    "sports": ["Who won the last Olympics?", "How to play soccer?", "How to improve your fitness?"]
}


@app.route("/suggestions")
def suggestions():
    # Get the term from the query string
    term = request.args.get("term")
    # Initialize an empty list for the suggestions
    suggestions = []
    # Loop through the keywords and phrases
    for keyword, phrases in keywords.items():
        # Check if the term matches or is a substring of the keyword
        if term == keyword or term in keyword:
            # Add the phrases to the suggestions list
            suggestions.extend(phrases)
    # Return the suggestions as JSON data
    return jsonify(suggestions)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded = True
        files = request.files.getlist('files')
        filenames = []
        for file in files:
            print(file.filename)
            
            file.save(os.path.join( app.config['UPLOAD_FOLDER'], file.filename ))
        docs = create_docs(app.config['UPLOAD_FOLDER'] , unique_id)
        docs_chunk = split_docs(documents, chunk_size=1000, chunk_overlap=0)
        push_to_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,docs)
        print("uploaded to vector database")
        for file in os.listdir( app.config['UPLOAD_FOLDER'] ):
            print(file)
        return redirect(url_for('home', messages=messages, uploaded=uploaded))


# Use a global list for simplicity. In a real application, you'd use a database.

global messages
messages = []



@app.route('/', methods=['GET', 'POST'])
def home():
    global messages
    if request.method == 'POST':
        if 'files' not in request.files.getlist('files'):
            final_docs_list = None
            print("No files found")
        else: 
            files = request.files.getlist('file')
            # final_docs_list = create_docs(files , unique_id )
            # print(files)
            for file in files:
                filename = file.filename
        
                file.save(os.path.join( app.config['UPLOAD_FOLDER'], filename ))

        if 'send'   in  request.form:
            unique_id = "aaa365fe031e4b5ab90aba54eaf6012e"
            query = request.form.get('message')
            # if files : 
            #     docs = create_docs(app.config['UPLOAD_FOLDER'] , unique_id)
            #     docs_chunk = split_docs(documents, chunk_size=1000, chunk_overlap=0)
            #     final_doc_list = docs_chunk
            if len(messages) == 0 : 
                relevant_docs = get_relevant_docs(query, embeddings, unique_id )
                qa_chain = define_qa()
            else :
                relevant_docs = get_relevant_docs(query, embeddings, unique_id)
            
            answer = get_answer(query, qa_chain, relevant_docs)
            # messages.append({'text': message, 'sender': 'user'}) 
            messages.append({'text': f'Possible answer document: {answer}' , 'sender': f"{query}" } )
        
        elif 'reset' in request.form:
            messages = []
    return render_template_string("""
    <html>
        <head>
            <!-- Add Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
            <!-- Add FontAwesome -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.13.0/jquery-ui.min.js"></script>
            <script src="./static/script.js"></script>
            <style>

                body {
                    font-family: 'Roboto', sans-serif;
                }

                .container {
                    width: 100%;
                }

                .row {
                    margin: 0;
                }

                .display-4 {
                    font-weight: 700; /* Bold */
                }

                .lead {
                    font-weight: 400; /* Regular */
                }


                .container {
                    width: 100%;
                }

                .row {
                    margin: 0;
                }

                .chat-element {
                    height: 200px;
                    overflow-y: auto;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                }

                .message-box {
                    border-radius: 10px;
                    margin-bottom: 10px;
                    padding: 10px;
                    color: white;
                    word-wrap: break-word; /* This will prevent long text from overflowing */
                    display: inline-block; /* This will make the width of the box adjust to the text */
                }

                .sender {
                    background-color: #008000; /* Emerald Green */
                    align-self: flex-end; /* This will align the sender's messages to the right */
                }

                .bot {
                    background-color: #808080; /* Gray */
                    align-self: flex-start; /* This will align the bot's responses to the left */
                }

                
                .message {
                    margin: 10px;
                    padding: 10px;
                }


                .user {
                    background-color: #d0f0d0;
                }
                .guide {
                    background-color: #d0d0f0;
                }
                .scrollable {
                    height: 300px;
                    overflow-y: auto;
                 #send-button, #speak-button {
                        border: 5px;
                        font: inherit;
                        background-color: transparent;
                        margin: 2px;
                        appearance: none;
                        padding: 10px 12px 3px 3px ;
                        cursor: pointer;
                        font-size: 24px;
                        display: flex;
                        } 

                    #upload-button {
                    color: white;
                    background-color: #007bff;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 14px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                    margin-top: 12px;
                    }

                    #message-input {
                    bottom: 0;
                    width: 100%;
                    flex-grow: 1;
                    font-size: 16px;
                    box-sizing: border-box;
                    border: none;
                    padding: 10px 0 10px 12px;
                    border-radius: 40px 0 0 40px;
                    background-color: transparent;
                    height: auto;
                    }

                    .input-group {
                    position: relative;
                    display: flex;
                    flex-wrap: nowrap;
                    align-items: stretch;
                    width: 100%;
                    border-radius: 40px;
                    border: 1px solid #2d2d2d;
                    }

                        #reset-button {
                        border: none;
                        font: inherit;
                        background-color: transparent;
                        margin: 0;
                        appearance: none;
                        padding: 10px 12px;
                        cursor: pointer;
                        font-size: 24px;
                        display: flex;
                        }
  
                }
            </style>
          
    
        </head>
        <body>

         


            <div class="container-main">
                <div class="row">
                <!-- Heading -->
                <div class="col-12">
                    <h1 class="display-4">Smart Tourist</h1>
                </div>

                <!-- Description -->
                <div class="col-12">
                    <p class="lead">Hello there! I'm your Smart Tourist guide. I can answer anything, with up-to-date information.</p>
                </div>
                </div>
            </div>
                

            <div class="container">
    <div class="row">
        <div>
            {% if not uploaded %}
                <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="files" accept=".pdf" multiple />
                <input type="submit" id="upload-button" class="btn btn-primary btn-sm" value="Upload">
                </form>

            {% elif uploaded %}
                <p>Successfully Uploaded</p>
            {% endif %}
            
            
        </div>
        <!-- Chat Element -->
        <div class="col-12">
            <div class="chat-element" style="height: 500px; overflow-y: auto;">
                {% for message in messages %}
                    <div class="message-box sender" style="text-align: right;">
                        <div class="me">{{ message.sender }}</div>
                    </div>
                    <div class="message-box bot" style="text-align: left;">
                        <div class="message-line">{{ message.text }}</div>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>


                    
                </div>
    

                <form method="post" class="form-inline justify-content-center"  >
                    <input type="text" id="message-input" name="message"  class="form-control mb-2 mr-sm-2" style="width: 80%;" placeholder="Type your message here...">
                    
                    <button  name="send" id="send-button" class="btn btn-primary send">
                            <i class='fa fa-paper-plane'></i>
                        </button>
                    <button type="button" onclick="record()" id="speak-button"  class="btn btn-primary send"><i class="fa fa-microphone"></i></button>
                    <button name="reset" id="reset-button" class="btn btn-primary reset">
                            <i class="fas fa-sync"></i>
                        </button>
                        </div>
                
                </form>
                <div>
                    <select id="language" name="language">
                    <option value="English">English</option>
                    <option value="Urdu">Urdu</option>
                    <option value="Arabic">Arabic</option>
                    <option value="French">French</option>
                    <option value="Spanish">Spanish</option>
                    </select>
                </div>
            </div>

        </body>
    </html>
    """, messages=messages, uploaded=uploaded)

if __name__ == '__main__':
    app.run(debug=True)
