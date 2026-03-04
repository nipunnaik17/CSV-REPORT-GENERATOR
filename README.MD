

---

# 📊 CSV Data Report Generator (Flask)

A Flask-based web application that allows users to upload a CSV file, automatically generate summary statistics, preview the dataset, and download a structured PDF report.

---

## 🚀 Features

* Upload CSV files
* Automatic summary statistics (Total & Average for numeric columns)
* Dataset preview (Top 10 rows)
* Auto-generated downloadable PDF report
* Clean web interface using Flask templates

---

## 🛠️ Tech Stack

* Python
* Flask
* Pandas
* FPDF
* HTML/CSS

---

## 📂 Folder Structure

```text
TASK-2/
│
├── data.csv
├── report.pdf
│
├── uploads/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── task2.py
│
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

```bash
pip install flask pandas fpdf
```

### 2️⃣ Run the Application

```bash
python task2.py
```

### 3️⃣ Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📌 How It Works

1. User uploads a CSV file.
2. Pandas reads and processes the dataset.
3. Numeric columns are analyzed (Total & Average).
4. A structured PDF report is generated using FPDF.
5. User can preview data and download the report.

---

👨‍💻 Developed by Nipun Naik
Internship Project | Flask & Data Processing

---


