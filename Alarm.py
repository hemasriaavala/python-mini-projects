from pygame import mixer
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from datetime import datetime, timedelta
import threading
import os
import json


class Alarm:
    def __init__(self, alarm_id, hour, minute, second, music_path, snooze_duration, label=""):
        self.id = alarm_id
        self.hour = hour
        self.minute = minute
        self.second = second
        self.music_path = music_path
        self.snooze_duration = snooze_duration
        self.label = label
        self.enabled = True
        self.alarm_time = None
        self.thread = None
        self.calculate_alarm_time()

    def calculate_alarm_time(self):
        now = datetime.now()
        self.alarm_time = now.replace(hour=self.hour, minute=self.minute,
                                      second=self.second, microsecond=0)
        if self.alarm_time <= now:
            self.alarm_time += timedelta(days=1)

    def get_time_until(self):
        if not self.enabled:
            return None
        now = datetime.now()
        diff = self.alarm_time - now
        if diff.total_seconds() < 0:
            self.calculate_alarm_time()
            diff = self.alarm_time - now
        return diff

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


class AlarmClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⏰ Multi-Alarm Clock")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        mixer.init()

        # Variables
        self.alarms = {}
        self.next_alarm_id = 1
        self.alarm_file = "alarms.json"

        self.setup_menu()
        self.setup_ui()
        self.update_current_time()
        self.load_alarms()

    def setup_menu(self):
        menubar = Menu(self.root, bg="#16213e", fg="#ffffff",
                       activebackground="#00d9ff", activeforeground="#1a1a2e")
        self.root.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0, bg="#16213e", fg="#ffffff",
                         activebackground="#00d9ff", activeforeground="#1a1a2e")
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Alarm", command=self.open_new_alarm_dialog,
                              accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Save Alarms", command=self.save_alarms,
                              accelerator="Ctrl+S")
        file_menu.add_command(label="Load Alarms", command=self.load_alarms)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Alarm Menu
        alarm_menu = Menu(menubar, tearoff=0, bg="#16213e", fg="#ffffff",
                          activebackground="#00d9ff", activeforeground="#1a1a2e")
        menubar.add_cascade(label="Alarms", menu=alarm_menu)
        alarm_menu.add_command(label="Enable All", command=self.enable_all_alarms)
        alarm_menu.add_command(label="Disable All", command=self.disable_all_alarms)
        alarm_menu.add_command(label="Delete All", command=self.delete_all_alarms)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0, bg="#16213e", fg="#ffffff",
                         activebackground="#00d9ff", activeforeground="#1a1a2e")
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        self.root.bind('<Control-n>', lambda e: self.open_new_alarm_dialog())
        self.root.bind('<Control-s>', lambda e: self.save_alarms())

    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=15)

        title = tk.Label(title_frame, text="⏰ MULTI-ALARM CLOCK",
                         font=("Arial", 24, "bold"),
                         fg="#00d9ff", bg="#1a1a2e")
        title.pack()
        self.current_time_frame = tk.Frame(self.root, bg="#16213e", bd=2, relief="ridge")
        self.current_time_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(self.current_time_frame, text="Current Time",
                 font=("Arial", 11), fg="#a0a0a0", bg="#16213e").pack(pady=3)

        self.current_time_label = tk.Label(self.current_time_frame,
                                           text="00:00:00",
                                           font=("Digital-7", 32, "bold"),
                                           fg="#00ff00", bg="#16213e")
        self.current_time_label.pack(pady=3)

        self.current_date_label = tk.Label(self.current_time_frame,
                                           text="",
                                           font=("Arial", 10),
                                           fg="#a0a0a0", bg="#16213e")
        self.current_date_label.pack(pady=3)
        alarms_frame = tk.LabelFrame(self.root, text="Active Alarms",
                                     font=("Arial", 14, "bold"),
                                     fg="#00d9ff", bg="#16213e", bd=2)
        alarms_frame.pack(pady=15, padx=20, fill="both", expand=True)
        canvas = tk.Canvas(alarms_frame, bg="#16213e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(alarms_frame, orient="vertical", command=canvas.yview)
        self.alarms_container = tk.Frame(canvas, bg="#16213e")

        self.alarms_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.alarms_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        self.no_alarms_label = tk.Label(self.alarms_container,
                                        text="No alarms set\nClick 'File > New Alarm' to add one",
                                        font=("Arial", 12),
                                        fg="#a0a0a0", bg="#16213e")
        self.no_alarms_label.pack(pady=50)
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="➕ New Alarm",
                  font=("Arial", 13, "bold"),
                  bg="#00d9ff", fg="#1a1a2e",
                  activebackground="#00b8d4",
                  command=self.open_new_alarm_dialog,
                  cursor="hand2", bd=0,
                  padx=30, pady=12, width=15).pack()
        self.status_bar = tk.Label(self.root, text="Ready",
                                   font=("Arial", 9),
                                   fg="#a0a0a0", bg="#0f0f1e",
                                   anchor="w", padx=10)
        self.status_bar.pack(side="bottom", fill="x")

    def update_current_time(self):
        now = datetime.now()
        self.current_time_label.config(text=now.strftime("%H:%M:%S"))
        self.current_date_label.config(text=now.strftime("%A, %B %d, %Y"))

        self.update_all_countdowns()
        self.check_alarms()

        active_count = sum(1 for a in self.alarms.values() if a.enabled)
        self.status_bar.config(text=f"Active Alarms: {active_count} | Total Alarms: {len(self.alarms)}")

        self.root.after(1000, self.update_current_time)

    def update_all_countdowns(self):
        for alarm_id, alarm in self.alarms.items():
            if hasattr(self, f'countdown_label_{alarm_id}'):
                label = getattr(self, f'countdown_label_{alarm_id}')
                if alarm.enabled:
                    time_diff = alarm.get_time_until()
                    if time_diff:
                        hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
                        minutes, seconds = divmod(remainder, 60)
                        label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}", fg="#ffd700")
                else:
                    label.config(text="Disabled", fg="#666666")

    def check_alarms(self):
        now = datetime.now()
        for alarm in list(self.alarms.values()):
            if alarm.enabled and alarm.alarm_time:
                if now >= alarm.alarm_time:
                    self.trigger_alarm(alarm)

    def open_new_alarm_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Alarm")
        dialog.geometry("450x400")
        dialog.configure(bg="#16213e")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="Set New Alarm", font=("Arial", 16, "bold"),
                 fg="#00d9ff", bg="#16213e").pack(pady=15)
        label_frame = tk.Frame(dialog, bg="#16213e")
        label_frame.pack(pady=10)
        tk.Label(label_frame, text="Label:", font=("Arial", 11),
                 fg="#ffffff", bg="#16213e").pack(side="left", padx=5)
        label_entry = tk.Entry(label_frame, font=("Arial", 11), width=30)
        label_entry.pack(side="left", padx=5)
        label_entry.insert(0, "My Alarm")
        time_frame = tk.Frame(dialog, bg="#16213e")
        time_frame.pack(pady=15)

        tk.Label(time_frame, text="Hour", font=("Arial", 10),
                 fg="#ffffff", bg="#16213e").grid(row=0, column=0, padx=8)
        hour_var = tk.StringVar(value=datetime.now().strftime("%H"))
        hour_spin = ttk.Spinbox(time_frame, from_=0, to=23,
                                textvariable=hour_var,
                                width=5, font=("Arial", 14, "bold"),
                                justify="center")
        hour_spin.grid(row=1, column=0, padx=8)

        tk.Label(time_frame, text=":", font=("Arial", 20, "bold"),
                 fg="#00d9ff", bg="#16213e").grid(row=1, column=1)

        tk.Label(time_frame, text="Minute", font=("Arial", 10),
                 fg="#ffffff", bg="#16213e").grid(row=0, column=2, padx=8)
        minute_var = tk.StringVar(value="00")
        minute_spin = ttk.Spinbox(time_frame, from_=0, to=59,
                                  textvariable=minute_var,
                                  width=5, font=("Arial", 14, "bold"),
                                  justify="center")
        minute_spin.grid(row=1, column=2, padx=8)

        tk.Label(time_frame, text=":", font=("Arial", 20, "bold"),
                 fg="#00d9ff", bg="#16213e").grid(row=1, column=3)

        tk.Label(time_frame, text="Second", font=("Arial", 10),
                 fg="#ffffff", bg="#16213e").grid(row=0, column=4, padx=8)
        second_var = tk.StringVar(value="00")
        second_spin = ttk.Spinbox(time_frame, from_=0, to=59,
                                  textvariable=second_var,
                                  width=5, font=("Arial", 14, "bold"),
                                  justify="center")
        second_spin.grid(row=1, column=4, padx=8)

        snooze_frame = tk.Frame(dialog, bg="#16213e")
        snooze_frame.pack(pady=10)
        tk.Label(snooze_frame, text="Snooze (min):", font=("Arial", 11),
                 fg="#ffffff", bg="#16213e").pack(side="left", padx=5)
        snooze_var = tk.StringVar(value="5")
        ttk.Spinbox(snooze_frame, from_=1, to=30, textvariable=snooze_var,
                    width=5, font=("Arial", 11)).pack(side="left", padx=5)
        music_frame = tk.Frame(dialog, bg="#16213e")
        music_frame.pack(pady=15)

        music_path = {"path": None}
        music_label = tk.Label(music_frame, text="No music selected",
                               font=("Arial", 10), fg="#ff6b6b",
                               bg="#16213e", wraplength=300)
        music_label.pack(pady=5)

        def select_music():
            path = filedialog.askopenfilename(
                title="Select Alarm Music",
                filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
            )
            if path:
                music_path["path"] = path
                music_label.config(text=f"Selected: {os.path.basename(path)}", fg="#00ff00")

        tk.Button(music_frame, text="🎵 Select Music",
                  font=("Arial", 10, "bold"),
                  bg="#4a5568", fg="#ffffff",
                  command=select_music,
                  cursor="hand2", bd=0, padx=15, pady=6).pack()
        btn_frame = tk.Frame(dialog, bg="#16213e")
        btn_frame.pack(pady=20)

        def create_alarm():
            if not music_path["path"]:
                messagebox.showwarning("No Music", "Please select music for the alarm!", parent=dialog)
                return

            try:
                hour = int(hour_var.get())
                minute = int(minute_var.get())
                second = int(second_var.get())
                snooze = int(snooze_var.get())
                label = label_entry.get().strip() or "Alarm"

                alarm = Alarm(self.next_alarm_id, hour, minute, second,
                              music_path["path"], snooze, label)
                self.alarms[self.next_alarm_id] = alarm
                self.next_alarm_id += 1

                self.add_alarm_to_ui(alarm)
                self.start_alarm_thread(alarm)

                dialog.destroy()
                messagebox.showinfo("Success", f"Alarm '{label}' created successfully!")

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid values!", parent=dialog)

        tk.Button(btn_frame, text="Create Alarm",
                  font=("Arial", 11, "bold"),
                  bg="#00d9ff", fg="#1a1a2e",
                  command=create_alarm,
                  cursor="hand2", bd=0,
                  padx=20, pady=8, width=12).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Cancel",
                  font=("Arial", 11, "bold"),
                  bg="#666666", fg="#ffffff",
                  command=dialog.destroy,
                  cursor="hand2", bd=0,
                  padx=20, pady=8, width=12).pack(side="left", padx=5)

    def add_alarm_to_ui(self, alarm):
        self.no_alarms_label.pack_forget()
        # Alarm Card
        card = tk.Frame(self.alarms_container, bg="#0f1626", bd=2, relief="raised")
        card.pack(fill="x", padx=5, pady=5)
        # Left side - Info
        left_frame = tk.Frame(card, bg="#0f1626")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        # Label
        tk.Label(left_frame, text=alarm.label,
                 font=("Arial", 13, "bold"),
                 fg="#00d9ff", bg="#0f1626").pack(anchor="w")
        # Time
        tk.Label(left_frame, text=str(alarm),
                 font=("Arial", 20, "bold"),
                 fg="#ffffff", bg="#0f1626").pack(anchor="w", pady=3)

        # Countdown
        countdown_label = tk.Label(left_frame, text="00:00:00",
                                   font=("Arial", 11),
                                   fg="#ffd700", bg="#0f1626")
        countdown_label.pack(anchor="w")
        setattr(self, f'countdown_label_{alarm.id}', countdown_label)

        # Music file
        music_name = os.path.basename(alarm.music_path)
        if len(music_name) > 35:
            music_name = music_name[:32] + "..."
        tk.Label(left_frame, text=f"🎵 {music_name}",
                 font=("Arial", 9),
                 fg="#a0a0a0", bg="#0f1626").pack(anchor="w", pady=2)

        # Right side - Controls
        right_frame = tk.Frame(card, bg="#0f1626")
        right_frame.pack(side="right", padx=10, pady=10)

        # Toggle button
        toggle_btn = tk.Button(right_frame, text="✓ ON" if alarm.enabled else "✗ OFF",
                               font=("Arial", 10, "bold"),
                               bg="#00ff00" if alarm.enabled else "#666666",
                               fg="#1a1a2e" if alarm.enabled else "#ffffff",
                               command=lambda: self.toggle_alarm(alarm, toggle_btn),
                               cursor="hand2", bd=0,
                               padx=15, pady=5, width=6)
        toggle_btn.pack(pady=3)

        # Delete button
        tk.Button(right_frame, text="🗑️ Delete",
                  font=("Arial", 9, "bold"),
                  bg="#ff6b6b", fg="#ffffff",
                  command=lambda: self.delete_alarm(alarm, card),
                  cursor="hand2", bd=0,
                  padx=10, pady=5).pack(pady=3)

    def toggle_alarm(self, alarm, button):
        alarm.enabled = not alarm.enabled
        if alarm.enabled:
            button.config(text="✓ ON", bg="#00ff00", fg="#1a1a2e")
            alarm.calculate_alarm_time()
            self.start_alarm_thread(alarm)
        else:
            button.config(text="✗ OFF", bg="#666666", fg="#ffffff")

    def delete_alarm(self, alarm, card):
        if messagebox.askyesno("Delete Alarm", f"Delete alarm '{alarm.label}'?"):
            alarm.enabled = False
            del self.alarms[alarm.id]
            card.destroy()

            if not self.alarms:
                self.no_alarms_label.pack(pady=50)

    def start_alarm_thread(self, alarm):
        if alarm.thread and alarm.thread.is_alive():
            return

        def worker():
            while alarm.enabled and alarm.id in self.alarms:
                now = datetime.now()
                if now >= alarm.alarm_time:
                    self.root.after(0, lambda: self.trigger_alarm(alarm))
                    break
                threading.Event().wait(0.5)

        alarm.thread = threading.Thread(target=worker, daemon=True)
        alarm.thread.start()

    def trigger_alarm(self, alarm):
        try:
            mixer.music.load(alarm.music_path)
            mixer.music.play(-1)

            # Alarm popup
            alarm_window = tk.Toplevel(self.root)
            alarm_window.title(f"⏰ {alarm.label}")
            alarm_window.geometry("450x280")
            alarm_window.configure(bg="#ff6b6b")
            alarm_window.attributes('-topmost', True)

            tk.Label(alarm_window, text="⏰ WAKE UP! ⏰",
                     font=("Arial", 26, "bold"),
                     fg="#ffffff", bg="#ff6b6b").pack(pady=20)

            tk.Label(alarm_window, text=alarm.label,
                     font=("Arial", 16, "bold"),
                     fg="#ffffff", bg="#ff6b6b").pack(pady=5)

            tk.Label(alarm_window, text=str(alarm),
                     font=("Arial", 24, "bold"),
                     fg="#ffffff", bg="#ff6b6b").pack(pady=10)

            button_frame = tk.Frame(alarm_window, bg="#ff6b6b")
            button_frame.pack(pady=20)

            def stop():
                mixer.music.stop()
                alarm.enabled = False
                alarm_window.destroy()

            def snooze():
                mixer.music.stop()
                alarm_window.destroy()
                alarm.alarm_time = datetime.now() + timedelta(minutes=alarm.snooze_duration)
                self.start_alarm_thread(alarm)

            tk.Button(button_frame, text=f"💤 Snooze ({alarm.snooze_duration}m)",
                      font=("Arial", 12, "bold"),
                      bg="#ffd700", fg="#1a1a2e",
                      command=snooze,
                      cursor="hand2", bd=0,
                      padx=20, pady=10, width=15).pack(side="left", padx=10)

            tk.Button(button_frame, text="✓ Stop",
                      font=("Arial", 12, "bold"),
                      bg="#00d9ff", fg="#1a1a2e",
                      command=stop,
                      cursor="hand2", bd=0,
                      padx=20, pady=10, width=15).pack(side="left", padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to play alarm: {str(e)}")

    def enable_all_alarms(self):
        for alarm in self.alarms.values():
            alarm.enabled = True
            alarm.calculate_alarm_time()
            self.start_alarm_thread(alarm)
        self.refresh_ui()
        messagebox.showinfo("Success", "All alarms enabled!")

    def disable_all_alarms(self):
        for alarm in self.alarms.values():
            alarm.enabled = False
        self.refresh_ui()
        messagebox.showinfo("Success", "All alarms disabled!")

    def delete_all_alarms(self):
        if messagebox.askyesno("Delete All", "Delete all alarms?"):
            self.alarms.clear()
            self.refresh_ui()

    def refresh_ui(self):
        for widget in self.alarms_container.winfo_children():
            widget.destroy()

        if not self.alarms:
            self.no_alarms_label = tk.Label(self.alarms_container,
                                            text="No alarms set\nClick 'File > New Alarm' to add one",
                                            font=("Arial", 12),
                                            fg="#a0a0a0", bg="#16213e")
            self.no_alarms_label.pack(pady=50)
        else:
            for alarm in self.alarms.values():
                self.add_alarm_to_ui(alarm)

    def save_alarms(self):
        try:
            data = []
            for alarm in self.alarms.values():
                data.append({
                    'id': alarm.id,
                    'hour': alarm.hour,
                    'minute': alarm.minute,
                    'second': alarm.second,
                    'music_path': alarm.music_path,
                    'snooze_duration': alarm.snooze_duration,
                    'label': alarm.label,
                    'enabled': alarm.enabled
                })

            with open(self.alarm_file, 'w') as f:
                json.dump({'alarms': data, 'next_id': self.next_alarm_id}, f, indent=2)

            messagebox.showinfo("Saved", "Alarms saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def load_alarms(self):
        try:
            if os.path.exists(self.alarm_file):
                with open(self.alarm_file, 'r') as f:
                    data = json.load(f)

                self.alarms.clear()
                self.next_alarm_id = data.get('next_id', 1)

                for alarm_data in data.get('alarms', []):
                    if os.path.exists(alarm_data['music_path']):
                        alarm = Alarm(
                            alarm_data['id'],
                            alarm_data['hour'],
                            alarm_data['minute'],
                            alarm_data['second'],
                            alarm_data['music_path'],
                            alarm_data['snooze_duration'],
                            alarm_data['label']
                        )
                        alarm.enabled = alarm_data['enabled']
                        self.alarms[alarm.id] = alarm

                        if alarm.enabled:
                            self.start_alarm_thread(alarm)

                self.refresh_ui()
        except Exception as e:
            print(f"Error loading alarms: {e}")

    def show_about(self):
        messagebox.showinfo("About",
                            "Multi-Alarm Clock v2.0\n\n"
                            "Features:\n"
                            "• Multiple alarms\n"
                            "• Custom music per alarm\n"
                            "• Countdown timers\n"
                            "• Snooze functionality\n"
                            "• Save/Load alarms\n\n"
                            "Created with Python & Tkinter")


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockGUI(root)
    root.mainloop()
