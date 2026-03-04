import os
import pandas as pd
from flask import Flask, request, render_template, send_file, send_from_directory
from fpdf import FPDF
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "CSV Data Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def generate(self, df, stats):
        self.add_page()

        # Summary Stats
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Summary Statistics:", ln=True)
        self.ln(2)

        self.set_font("Arial", "", 11)
        for col, val in stats.items():
            self.cell(90, 8, str(col), ln=False)
            self.cell(0, 8, str(val), ln=True)
        self.ln(8)

        # Table Section
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Full Dataset:", ln=True)
        self.ln(4)

        # Header row
        self.set_font("Arial", "B", 8)
        col_widths = self.get_column_widths(df)

        for i, col in enumerate(df.columns):
            self.cell(col_widths[i], 6, str(col)[:20], border=1)
        self.ln()

        # Data rows
        self.set_font("Arial", "", 7)
        for _, row in df.iterrows():
            for i, col in enumerate(df.columns):
                val = str(row[col])[:18]  # Shortened content
                self.cell(col_widths[i], 6, val, border=1)
            self.ln()

            if self.get_y() > 190:  # add page if needed (landscape height = ~200)
                self.add_page()
                self.set_font("Arial", "B", 8)
                for i, col in enumerate(df.columns):
                    self.cell(col_widths[i], 6, str(col)[:20], border=1)
                self.ln()
                self.set_font("Arial", "", 7)

    def get_column_widths(self, df):
        max_width = 275  # full width of landscape A4
        num_cols = len(df.columns)
        base_width = max_width / num_cols
        widths = []

        for col in df.columns:
            avg_len = df[col].astype(str).str.len().mean()
            if avg_len > 20:
                widths.append(base_width + 10)
            elif avg_len < 5:
                widths.append(base_width - 5)
            else:
                widths.append(base_width)
        
        # Normalize if needed
        scale = max_width / sum(widths)
        return [w * scale for w in widths]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            df = pd.read_csv(filepath)
            numeric_cols = df.select_dtypes(include='number').columns.tolist()

            stats = {
                f"{col} - Total": round(df[col].sum(), 2)
                for col in numeric_cols
            }
            stats.update({
                f"{col} - Average": round(df[col].mean(), 2)
                for col in numeric_cols
            })

            # Generate PDF report
            pdf = PDFReport(orientation='L', unit='mm', format='A4')
            pdf.generate(df, stats)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'report.pdf')
            pdf.output(pdf_path)

            preview = df.head(10).to_html(classes='table table-dark table-striped', index=False)

            return render_template('result.html', stats=stats, preview=preview, pdf_url='/download')

    return render_template('index.html')


@app.route('/download')
def download_pdf():
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'report.pdf')
    return send_file(pdf_path, as_attachment=True)


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
