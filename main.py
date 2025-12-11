import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import pdfplumber
import time
import threading
import random
import os

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Undetectable Auto-Typer")
        self.root.geometry("600x650")
        
        self.is_running = False

        # --- HEADER ---
        header = tk.Frame(root, bg="#222")
        header.pack(fill=tk.X)
        tk.Label(header, text="Ghost Writer (Human Mode)", font=("Segoe UI", 16, "bold"), bg="#222", fg="#00ff00", pady=15).pack()

        # --- BODY ---
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Upload
        tk.Button(main_frame, text="📂 Upload PDF", command=self.upload_pdf, bg="#ddd", pady=5).pack(fill=tk.X, pady=(0, 10))

        # 2. Text Input
        self.text_area = tk.Text(main_frame, height=12, font=("Consolas", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 3. Humanization Settings
        settings_frame = tk.LabelFrame(main_frame, text="Humanization Settings", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=10)

        # Base Speed
        tk.Label(settings_frame, text="Base Speed (sec):").pack(side=tk.LEFT)
        self.speed_entry = tk.Entry(settings_frame, width=6)
        self.speed_entry.insert(0, "0.08") # Average human speed
        self.speed_entry.pack(side=tk.LEFT, padx=5)

        # Variance (Jitter)
        tk.Label(settings_frame, text="Variance (+/-):").pack(side=tk.LEFT, padx=(10,0))
        self.jitter_entry = tk.Entry(settings_frame, width=6)
        self.jitter_entry.insert(0, "0.04") # Randomness amount
        self.jitter_entry.pack(side=tk.LEFT, padx=5)

        # 4. Controls
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.btn_start = tk.Button(btn_frame, text="▶ START HUMAN TYPING", command=self.start_thread, bg="#27ae60", fg="white", font=("bold", 11), width=22)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_stop = tk.Button(btn_frame, text="⏹ STOP", command=self.stop_typing, bg="#c0392b", fg="white", font=("bold", 11), width=10, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT)

        # Status
        self.status_var = tk.StringVar(value="Ready to mimic human typing...")
        tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w", padx=10, bg="#ecf0f1").pack(side=tk.BOTTOM, fill=tk.X)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.status_var.set("Scanning PDF...")
            self.root.update()
            try:
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted: text += extracted + "\n"
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, text)
                self.status_var.set("PDF Loaded.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def start_thread(self):
        self.is_running = True
        self.btn_start.config(state=tk.DISABLED, bg="#95a5a6")
        self.btn_stop.config(state=tk.NORMAL, bg="#c0392b")
        threading.Thread(target=self.human_typing_engine, daemon=True).start()

    def stop_typing(self):
        self.is_running = False
        self.status_var.set("Stopping...")

    def human_typing_engine(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            self.reset_ui()
            return

        try:
            base_speed = float(self.speed_entry.get())
            jitter = float(self.jitter_entry.get())
        except:
            messagebox.showerror("Error", "Numbers only for speed/jitter")
            self.reset_ui()
            return

        # Countdown
        for i in range(5, 0, -1):
            if not self.is_running: return
            self.status_var.set(f"Starting in {i}... CLICK THE WINDOW!")
            time.sleep(1)

        self.status_var.set("Typing naturally...")

        # === THE HUMAN ALGORITHM ===
        try:
            for char in content:
                if not self.is_running: break

                # 1. Calculate random delay for this specific keystroke
                # Random float between (Speed - Jitter) and (Speed + Jitter)
                # Example: 0.08 +/- 0.04 = Random between 0.04s and 0.12s
                random_interval = random.uniform(base_speed - jitter, base_speed + jitter)
                if random_interval < 0.01: random_interval = 0.01

                # 2. Simulate Key Down and Key Up events individually
                # Websites detect 'Key Duration' (how long the button is held)
                
                pyautogui.keyDown(char) 
                
                # Hold the key for a tiny random amount of time (Human press duration)
                time.sleep(random.uniform(0.05, 0.09)) 
                
                pyautogui.keyUp(char)

                # 3. Wait before the next key (Rhythm)
                time.sleep(random_interval)

                # 4. Occasional "Micro-Pauses" (Simulating thinking or looking at text)
                if random.random() < 0.05: # 5% chance to pause
                     time.sleep(random.uniform(0.3, 0.6))

            self.status_var.set("Finished.")
            if self.is_running: messagebox.showinfo("Success", "Typing Complete")

        except Exception as e:
            self.status_var.set("Error: Special character issue? Try plain text.")
            print(e)

        self.reset_ui()

    def reset_ui(self):
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL, bg="#27ae60")
        self.btn_stop.config(state=tk.DISABLED, bg="#95a5a6")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()