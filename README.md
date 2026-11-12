# 🚀 ML Tracker

**A lightweight Data Version Control tool for Machine Learning datasets.**

ML Tracker is a Python-based command-line tool that helps you track different versions of CSV datasets using SHA-256 hashing.

It creates snapshots of your datasets and maintains a local history of changes, making dataset version tracking simple and easy.

---

## ✨ Features

- Initialize a local tracking repository
- Track CSV files using SHA-256 hashing
- Automatically calculate rows and columns
- Store exact snapshots of datasets
- Maintain version history using JSON
- View previous dataset versions
- Check whether a dataset has changed
- Detect consecutive duplicate commits
- Support optional commit messages

---

## 🛠️ Built With

- **Python** – Core programming language
- **Hashlib** – SHA-256 fingerprinting
- **Pathlib** – File and directory handling
- **JSON** – Version history storage
- **CSV** – Dataset processing

No external dependencies required.

---

## 📋 Requirements

- Python 3.7 or higher
- A CSV dataset to track

---

## ⚡ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/krishnaish-cipher/mltracker.git
```

### 2. Navigate to the project folder

```bash
cd mltracker
```

### 3. Initialize ML Tracker

```bash
python main.py init
```

### 4. Commit a dataset

```bash
python main.py commit data.csv -m "initial version"
```

### 5. View commit history

```bash
python main.py log
```

### 6. Check dataset status

```bash
python main.py status data.csv
```

---

## 📖 Available Commands

| Command | Description |
|---|---|
| `python main.py init` | Initialize ML Tracker |
| `python main.py commit data.csv` | Save a dataset snapshot |
| `python main.py commit data.csv -m "message"` | Save a snapshot with a message |
| `python main.py log` | Display version history |
| `python main.py status data.csv` | Check dataset status |

**Note:** Commit messages are currently displayed during execution but are not yet saved in the history file.

---

## 🔄 Example Workflow

```bash
# Initialize the repository
python main.py init

# Track the original dataset
python main.py commit products.csv -m "initial dataset"

# Make changes to your CSV file

# Check whether changes were made
python main.py status products.csv

# Save the updated dataset
python main.py commit products.csv -m "updated product data"

# View version history
python main.py log
```

---

## 📁 Project Structure

```text
mltracker/
│
├── main.py
│
├── README.md
│
└── .mltracker/
    │
    ├── snapshots/
    │   └── Stored dataset versions
    │
    └── history.json
```

The `.mltracker/` directory is generated when you initialize the tool.

---

## ⚙️ How It Works

1. **Hash Generation:** ML Tracker calculates a SHA-256 hash of the CSV file.
2. **Dataset Analysis:** It calculates the number of rows and columns.
3. **Snapshot Storage:** A copy of the dataset is stored using its hash as the filename.
4. **History Tracking:** Dataset metadata is stored in a JSON file.
5. **Duplicate Detection:** If the latest recorded hash matches the current file hash, a duplicate commit is prevented.

---

## 🎯 Project Goal

The goal of ML Tracker is to make dataset version management easier for Machine Learning projects without requiring complicated version control workflows.

---

## 👨‍💻 Author

**Krishna**

GitHub: [@krishnaish-cipher](https://github.com/krishnaish-cipher)

---

⭐ If you find this project interesting, consider giving it a star!
