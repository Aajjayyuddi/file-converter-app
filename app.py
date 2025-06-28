from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from docx import Document
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        option = request.form['convert_to']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if option == 'pdf' and filename.endswith('.docx'):
            doc = Document(filepath)
            pdf_path = filepath.replace('.docx', '.pdf')
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for para in doc.paragraphs:
                pdf.multi_cell(0, 10, para.text)
            pdf.output(pdf_path)
            return send_file(pdf_path, as_attachment=True)

        elif option == 'docx' and filename.endswith('.pdf'):
            return "PDF to DOCX conversion not supported in this version."

        return "Unsupported file or conversion type."

    return render_template('index.html')
