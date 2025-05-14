import tkinter as tk
from threading import Thread, Event
import time
import keyboard
import pygetwindow as gw

class TabRefresherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Browser Tab Switcher")
        self.root.geometry("320x280")

        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # ignore icon errors

        self.switch_interval = tk.IntVar(value=5)
        self.refresh_delay = tk.IntVar(value=1)
        self.selected_browser = tk.StringVar(value="Chrome")
        self.stop_event = Event()

        self.create_widgets()
        self.bind_hotkeys()

    def create_widgets(self):
        tk.Label(self.root, text="فاصله بین سوییچ تب‌ها (ثانیه):").pack()
        tk.Entry(self.root, textvariable=self.switch_interval).pack()

        tk.Label(self.root, text="تاخیر بین سوییچ و رفرش (ثانیه):").pack()
        tk.Entry(self.root, textvariable=self.refresh_delay).pack()

        tk.Label(self.root, text="انتخاب مرورگر:").pack()
        browsers = ["Chrome", "Firefox", "Edge", "Opera"]
        tk.OptionMenu(self.root, self.selected_browser, *browsers).pack()

        self.status_label = tk.Label(self.root, text="وضعیت: متوقف", fg="red")
        self.status_label.pack(pady=10)

        tk.Label(self.root, text="F8: شروع | F9: توقف").pack(pady=5)

        tk.Label(self.root, text="H. Mahmoodzadeh", font=("Arial", 3), anchor="e").pack(side="bottom", anchor="se", padx=5, pady=5)

    def bind_hotkeys(self):
        keyboard.add_hotkey("F8", self.start)
        keyboard.add_hotkey("F9", self.stop)

    def start(self):
        self.stop_event.clear()
        self.status_label.config(text="وضعیت: در حال اجرا", fg="green")
        Thread(target=self.run_loop, daemon=True).start()

    def stop(self):
        self.stop_event.set()
        self.status_label.config(text="وضعیت: متوقف", fg="red")

    def run_loop(self):
        while not self.stop_event.is_set():
            self.bring_browser_to_front()
            keyboard.send("ctrl+tab")
            time.sleep(self.refresh_delay.get())
            keyboard.send("f5")
            time.sleep(self.switch_interval.get())

    def bring_browser_to_front(self):
        browser_titles = {
            "Chrome": "Google Chrome",
            "Firefox": "Mozilla Firefox",
            "Edge": "Microsoft Edge",
            "Opera": "Opera"
        }
        browser_title = browser_titles.get(self.selected_browser.get())

        try:
            windows = gw.getWindowsWithTitle(browser_title)
            if windows:
                win = windows[0]
                try:
                    win.activate()
                    win.maximize()
                except Exception as e:
                    print("خطا در فعال‌سازی پنجره:", e)
            else:
                print(f"پنجره‌ای از {browser_title} پیدا نشد.")
        except Exception as e:
            print("خطا در دسترسی به پنجره مرورگر:", e)


if __name__ == "__main__":
    root = tk.Tk()
    app = TabRefresherApp(root)
    root.mainloop()
