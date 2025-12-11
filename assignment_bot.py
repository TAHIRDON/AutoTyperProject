import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyautogui
import pdfplumber
import time
import threading
import random
import os
import sys  # Needed for the resource_path fix
import ctypes

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class UniversalAutoTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("GhostType")
        self.root.geometry("650x700")
        self.root.configure(bg="#f0f2f5")

        # --- FIX: Use resource_path to find the icon inside the EXE ---
        try:
            icon_file = resource_path("GhostType.ico")
            self.root.iconbitmap(icon_file)
        except Exception as e:
            print(f"Icon error: {e}")
        # -------------------------------------------------------------

        # State variables
        self.is_running = False
        self.is_paused = False

        # --- STYLE ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 10))
        
        # --- HEADER ---
        header_frame = tk.Frame(root, bg="#2c3e50", pady=20)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Assignment Auto-Writer", font=("Segoe UI", 20, "bold"), bg="#2c3e50", fg="white").pack()
        tk.Label(header_frame, text="Undetectable Human Simulation Algorithm", font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7").pack()

        # --- MAIN BODY ---
        main_frame = tk.Frame(root, bg="#f0f2f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. File Loader
        file_frame = tk.LabelFrame(main_frame, text="Source Content", bg="#f0f2f5", font=("Segoe UI", 11, "bold"))
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_upload = tk.Button(file_frame, text="📂 Load PDF / Text File", command=self.upload_file, bg="#ecf0f1", relief=tk.FLAT)
        btn_upload.pack(fill=tk.X, padx=10, pady=10)

        # 2. Text Preview
        self.text_area = tk.Text(main_frame, height=10, font=("Consolas", 10), bd=2, relief=tk.FLAT)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 3. Tuning
        tune_frame = tk.LabelFrame(main_frame, text="Human Behavior Tuning", bg="#f0f2f5", font=("Segoe UI", 11, "bold"))
        tune_frame.pack(fill=tk.X, pady=10)

        tk.Label(tune_frame, text="WPM (Words Per Minute):").pack(side=tk.LEFT, padx=10)
        self.wpm_entry = tk.Entry(tune_frame, width=5)
        self.wpm_entry.insert(0, "70") 
        self.wpm_entry.pack(side=tk.LEFT)

        # 4. Controls
        ctrl_frame = tk.Frame(main_frame, bg="#f0f2f5")
        ctrl_frame.pack(fill=tk.X, pady=15)

        self.btn_start = tk.Button(ctrl_frame, text="▶ START WRITING", command=self.start_thread, bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), width=20, relief=tk.FLAT)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(ctrl_frame, text="⏹ EMERGENCY STOP", command=self.stop_typing, bg="#c0392b", fg="white", font=("Segoe UI", 11, "bold"), width=20, relief=tk.FLAT, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.RIGHT, padx=5)

        # 5. Status Bar
        self.status_var = tk.StringVar(value="Ready. Load text to begin.")
        self.lbl_status = tk.Label(root, textvariable=self.status_var, bg="#34495e", fg="white", pady=8, font=("Consolas", 10))
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.txt")])
        if not file_path: return
        
        try:
            text = ""
            if file_path.endswith(".pdf"):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted: text += extracted + "\n"
            else: 
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, text)
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

    def start_thread(self):
        self.is_running = True
        self.btn_start.config(state=tk.DISABLED, bg="#95a5a6")
        self.btn_stop.config(state=tk.NORMAL, bg="#c0392b")
        t = threading.Thread(target=self.human_typing_logic, daemon=True)
        t.start()

    def stop_typing(self):
        self.is_running = False
        self.status_var.set("❌ Process Stopped by User.")

    def human_typing_logic(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            self.reset_ui()
            return

        try:
            wpm = float(self.wpm_entry.get())
            cps = (wpm * 5) / 60
            base_delay = 1 / cps
        except:
            base_delay = 0.1

        for i in range(5, 0, -1):
            if not self.is_running: return
            self.status_var.set(f"⏳ Click target window! Starting in {i}...")
            time.sleep(1)

        self.status_var.set("✍ Typing in progress... Do not touch mouse/keyboard.")
        
        try:
            for i, char in enumerate(content):
                if not self.is_running: break
                pyautogui.keyDown(char)
                time.sleep(random.uniform(0.05, 0.09))
                pyautogui.keyUp(char)
                actual_delay = random.gauss(base_delay, 0.03) 
                if actual_delay < 0.02: actual_delay = 0.02
                time.sleep(actual_delay)
                if char in ['.', '?', '!', '\n']:
                    time.sleep(random.uniform(0.3, 0.6))
                elif char in [',', ';']:
                    time.sleep(random.uniform(0.15, 0.25))
                if i % 150 == 0 and random.random() < 0.1:
                    time.sleep(random.uniform(0.5, 1.2))
            if self.is_running:
                self.status_var.set("✅ Typing Completed Successfully.")
                messagebox.showinfo("Success", "Assignment Typing Complete!")
        except Exception as e:
            self.status_var.set(f"⚠️ Error: {e}")
            print(e)
        self.reset_ui()

    def reset_ui(self):
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL, bg="#27ae60")
        self.btn_stop.config(state=tk.DISABLED, bg="#95a5a6")

if __name__ == "__main__":
    try:
        # TASKBAR FIX: Ensure unique App ID
        myappid = 'tahirdon.ghosttype.autowriter.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    root = tk.Tk()
    app = UniversalAutoTyper(root)
    root.mainloop()