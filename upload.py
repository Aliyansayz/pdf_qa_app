app.config['UPLOAD_FOLDER'] = '/documents'

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded = True
        files = request.files.getlist('files')
        filenames = []
        for file in files:
            print(file.filename)
            # final_docs_list.append(file)
            # Save the file to the documents directory
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
        return redirect(url_for('home', messages=messages, uploaded=uploaded, filenames=filenames))
