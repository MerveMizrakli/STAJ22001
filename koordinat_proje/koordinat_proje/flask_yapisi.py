from flask import Flask, render_template, request, send_file
import os
from koor_bul import koordinat_bul
from koor_dogrulu import koordinat_dogrulugu_kontrol

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("koor.html")

# 1. Koordinat Bul
@app.route('/bul', methods=['POST'])
def koordinat_bul_route():
    dosya = request.files['dosyam']
    if dosya and dosya.filename.endswith(".xlsx"):
        input_path = os.path.join(UPLOAD_FOLDER, dosya.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "koordinatli_" + dosya.filename)
        dosya.save(input_path)
        koordinat_bul(input_path, output_path)
        return send_file(output_path, as_attachment=True)
    return "Geçerli bir .xlsx dosyası yükleyin."

# 2. Doğruluk Kontrol
@app.route('/dogruluk', methods=['POST'])
def koordinat_dogruluk_route():
    dosya = request.files['dosyam']
    if dosya and dosya.filename.endswith(".xlsx"):
        input_path = os.path.join(UPLOAD_FOLDER, dosya.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "dogruluk_" + dosya.filename)
        dosya.save(input_path)
        koordinat_dogrulugu_kontrol(input_path, output_path)
        return send_file(output_path, as_attachment=True)
    return "Geçerli bir .xlsx dosyası yükleyin."

if __name__ == '__main__':
    app.run(debug=True)
