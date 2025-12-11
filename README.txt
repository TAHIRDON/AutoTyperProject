# GhostType 👻✍️
### The Undetectable Assignment Auto-Writer

**GhostType** is a Python-based automation tool designed to simulate human typing behavior. Unlike standard copy-paste scripts, GhostType uses a sophisticated algorithm to vary keystroke delays, introduce "thinking" pauses, and mimic natural fluctuations in typing speed.

![GhostType App]

## 🚀 Features

* **📄 PDF & Text Support:** Directly load content from `.txt` or `.pdf` files.
* **🧠 Human Simulation Algorithm:**
    * **Variable Speed:** Uses Gaussian distribution to randomize typing intervals (no two keystrokes are identical).
    * **Punctuation Pauses:** Naturally pauses longer after periods (`.`), commas (`,`), and newlines.
    * **Fatigue System:** Randomly takes short "thinking" breaks to mimic human behavior.
* **⚡ Speed Control:** Adjustable **WPM (Words Per Minute)** setting to match your desired typing speed.
* **🛡️ Emergency Stop:** Instant kill-switch to stop automation safely.
* **🎨 Modern GUI:** Clean interface built with Tkinter.

## 🛠️ Installation & Usage

### Option 1: Run the Executable (No Python Required)
1.  Download the latest `GhostType.exe` from the [Releases](https://github.com/TAHIRDON/AutoTyperProject/releases) section.
2.  Run the application.
3.  Load your file, set your speed, and click **Start**.

### Option 2: Run from Source
If you want to modify the code, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/TAHIRDON/AutoTyperProject.git](https://github.com/TAHIRDON/AutoTyperProject.git)
    cd AutoTyperProject
    ```

2.  **Install dependencies:**
    ```bash
    pip install pyautogui pdfplumber
    ```
    *(Note: `tkinter` usually comes pre-installed with Python)*

3.  **Run the script:**
    ```bash
    python main.py
    ```

## ⚙️ How It Works
The typing logic is built on top of `pyautogui` but adds a layer of randomization:
* **Keystroke Duration:** Holds keys down for 50ms–90ms (mimicking physical finger press time).
* **Micro-Latencies:** Adds tiny random delays between characters based on a bell curve of your target WPM.

## 📦 Building the EXE
To build your own executable with the icon included:

```bash
pyinstaller --onefile --noconsole --name="GhostType" --icon="GhostType.ico" --add-data 'GhostType.ico;.' assignment_bot.py

⚠️ Disclaimer
This tool is intended for educational purposes and personal automation tasks. Please use responsibly.
Author: TAHIR_MIYA(TAHIRDON)
