import psutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
import requests
from tkinter import simpledialog
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageTk  # For logo handling

DANGEROUS_IPS = ["45.", "185.", "103.", "91.", "198."]  # Non-Iranian/Suspicious IPs

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window frame
        self.root.configure(bg="#121f1f")  # Dark theme background

        # Center the splash screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width, height = 500, 300
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Logo (replace 'logo.png' with actual logo path if available)
        try:
            logo = Image.open("logo.png").resize((100, 100), Image.ANTIALIAS)
            logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=logo_img, bg="#121f1f").pack(pady=10)
            self.root.logo_img = logo_img  # Keep reference to avoid garbage collection
        except Exception as e:
            print(f"Logo not loaded: {e}")
            tk.Label(self.root, text="👁‍🗨", font=("Arial", 50), bg="#121f1f", fg="lightgreen").pack(pady=10)

        # Title and subtitle
        tk.Label(self.root, text="AetherosSec", font=("B Titr", 24), bg="#121f1f", fg="lightgreen").pack(pady=5)
        tk.Label(self.root, text="Cyber Defense by AetherosTech", font=("Arial", 12), bg="#121f1f", fg="white").pack(pady=5)

        # Developer info
        tk.Label(self.root, text="Developed by Shayan Taherkhani", font=("Arial", 10), bg="#121f1f", fg="lightblue").pack(pady=5)
        linkedin_lbl = tk.Label(self.root, text="LinkedIn: linkedin.com/in/shayantaherkhani", font=("Arial", 10), bg="#121f1f", fg="lightblue", cursor="hand2")
        linkedin_lbl.pack()
        linkedin_lbl.bind("<Button-1>", lambda e: self.open_links("https://linkedin.com/in/shayantaherkhani"))

        github_lbl = tk.Label(self.root, text="GitHub: github.com/shayanthn", font=("Arial", 10), bg="#121f1f", fg="lightblue", cursor="hand2")
        github_lbl.pack()
        github_lbl.bind("<Button-1>", lambda e: self.open_links("https://github.com/shayanthn"))

        tk.Label(self.root, text="Email: shayanthn78@gmail.com", font=("Arial", 10), bg="#121f1f", fg="lightblue").pack()

        # Auto-close after 3 seconds
        self.root.after(3000, self.close_splash)

    def open_links(self, url):
        import webbrowser
        webbrowser.open(url)

    def close_splash(self):
        self.root.destroy()

class LiveMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AetherosSec LiveNet Supreme 👁‍🗨")
        self.root.geometry("1200x700")
        self.root.configure(bg="#121f1f")

        # Add scrollable frame
        self.canvas = tk.Canvas(root, bg="#121f1f")
        self.scrollable_frame = tk.Frame(self.canvas, bg="#121f1f")
        self.scrollbar_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        tk.Label(self.scrollable_frame, text="🛡️ ShaySecure LiveNet Supreme", font=("B Titr", 18), bg="#121f1f", fg="lightgreen").pack(pady=5)

        self.filter_var = tk.StringVar()
        filter_entry = tk.Entry(self.scrollable_frame, textvariable=self.filter_var, width=40, font=("Courier", 10))
        filter_entry.pack(pady=5)
        self.ui_elements = {
            "title": self.root,
            "save_log": None,
            "refresh": None,
            "traffic_graph": None,
            "filter_label": None,
            "security_check": None,
            "disconnect_suspicious": None,
        }
        self.ui_elements["filter_label"] = tk.Label(self.scrollable_frame, text="🔍 Filter by App or Port", fg="white", bg="#121f1f")
        self.ui_elements["filter_label"].pack()

        # Language selection
        self.language_var = tk.StringVar(value="en")
        lang_frame = tk.Frame(self.scrollable_frame, bg="#121f1f")
        lang_frame.pack(pady=5)
        tk.Label(lang_frame, text="🌐 Language:", bg="#121f1f", fg="white").pack(side="left", padx=5)
        tk.Radiobutton(lang_frame, text="English", variable=self.language_var, value="en", command=self.update_language, bg="#121f1f", fg="white").pack(side="left")
        tk.Radiobutton(lang_frame, text="فارسی", variable=self.language_var, value="fa", command=self.update_language, bg="#121f1f", fg="white").pack(side="left")

        # Dark/Light mode toggle
        self.theme_var = tk.StringVar(value="dark")
        theme_frame = tk.Frame(self.scrollable_frame, bg="#121f1f")
        theme_frame.pack(pady=5)
        tk.Label(theme_frame, text="🎨 Theme:", bg="#121f1f", fg="white").pack(side="left", padx=5)
        tk.Radiobutton(theme_frame, text="Dark", variable=self.theme_var, value="dark", command=self.update_theme, bg="#121f1f", fg="white").pack(side="left")
        tk.Radiobutton(theme_frame, text="Light", variable=self.theme_var, value="light", command=self.update_theme, bg="#121f1f", fg="white").pack(side="left")

        # Developer info
        dev_label = tk.Label(self.scrollable_frame, text="👨‍💻 Shayan Taherkhani - Email: shayanthn78@gmail.com - LinkedIn: linkedin.com/in/shayantaherkhani",
                             font=("Courier", 10), bg="#121f1f", fg="lightblue", cursor="hand2")
        dev_label.pack(pady=10)
        dev_label.bind("<Button-1>", lambda e: self.open_link("https://linkedin.com/in/shayantaherkhani"))

        columns = ("App", "Path", "Local", "Remote", "Status")
        self.tree = ttk.Treeview(self.scrollable_frame, columns=columns, show="headings", height=16)
        for col in columns:
            self.tree.heading(col, text=col)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e2b2b", foreground="white", rowheight=25, fieldbackground="#1e2b2b")
        style.map("Treeview", background=[("selected", "#264d4d")])

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.scrollable_frame, bg="#121f1f")
        btn_frame.pack(pady=5)

        self.ui_elements["save_log"] = tk.Button(btn_frame, text="📥 Save Report", command=self.save_log, font=("B Nazanin", 12))
        self.ui_elements["save_log"].pack(side="left", padx=10)

        self.ui_elements["refresh"] = tk.Button(btn_frame, text="🔄 Manual Refresh", command=self.update_table, font=("B Nazanin", 12))
        self.ui_elements["refresh"].pack(side="left", padx=10)

        self.ui_elements["traffic_graph"] = tk.Button(btn_frame, text="📊 Traffic Graph", command=self.show_graph, font=("B Nazanin", 12))
        self.ui_elements["traffic_graph"].pack(side="left", padx=10)

        self.ui_elements["disconnect_suspicious"] = tk.Button(
            btn_frame, 
            text="❌ Disconnect Suspicious IPs", 
            command=self.disconnect_suspicious_ips, 
            font=("B Nazanin", 12)
        )
        self.ui_elements["disconnect_suspicious"].pack(side="left", padx=10)

        self.translations = {
            "fa": {
                "title": "شای‌سکیور لایونت سوپریم",
                "save_log": "📥 ذخیره گزارش",
                "refresh": "🔄 بروزرسانی دستی",
                "traffic_graph": "📊 گراف ترافیک",
                "filter_label": "🔍 فیلتر با نام برنامه یا پورت",
                "security_check": "🔐 چک‌لیست امنیتی",
                "disconnect_suspicious": "❌ قطع ارتباط آی‌پی‌های مشکوک",
            },
            "en": {
                "title": "ShaySecure LiveNet Supreme",
                "save_log": "📥 Save Report",
                "refresh": "🔄 Manual Refresh",
                "traffic_graph": "📊 Traffic Graph",
                "filter_label": "🔍 Filter by App or Port",
                "security_check": "🔐 Security Checklist",
                "disconnect_suspicious": "❌ Disconnect Suspicious IPs",
            }
        }

        self.ui_elements["security_check"] = tk.Button(btn_frame, text=self.translations[self.language_var.get()]["security_check"], command=self.security_check, font=("B Nazanin", 12))
        self.ui_elements["security_check"].pack(side="left", padx=10)

        # Add right-click menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Show Full Connection Details", command=self.show_connection_details)
        self.context_menu.add_command(label="Show GeoIP", command=self.show_geoip)
        self.context_menu.add_command(label="Copy IP", command=self.copy_ip)
        self.context_menu.add_command(label="Copy Port", command=self.copy_port)
        self.context_menu.add_command(label="Disconnect IP", command=self.disconnect_selected_ip)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.traffic_data = []
        self.load_config()
        self.update_language()
        self.update_loop()

    def update_loop(self):
        self.update_table()
        self.root.after(5000, self.update_loop)

    def resolve_process(self, pid):
        try:
            p = psutil.Process(pid)
            return p.name(), p.exe()
        except:
            return "Unknown", "Unknown"

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        conns = psutil.net_connections(kind='inet')
        keyword = self.filter_var.get().lower()
        count = 0

        for conn in conns:
            if conn.status == 'ESTABLISHED':
                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                proc_name, proc_path = self.resolve_process(conn.pid) if conn.pid else ("N/A", "N/A")

                if keyword and keyword not in proc_name.lower() and keyword not in local and keyword not in remote:
                    continue

                status = "🔴 Suspicious" if any(remote.startswith(ip) for ip in DANGEROUS_IPS) else "🟢 Safe"
                tag = "danger" if "Suspicious" in status else "safe"

                self.tree.insert("", "end", values=(proc_name, proc_path, local, remote, status), tags=(tag,))
                count += 1

        self.tree.tag_configure("danger", background="#4d1f1f")
        self.tree.tag_configure("safe", background="#1f2f1f")
        self.traffic_data.append(count)

    def save_log(self):
        filetypes = [("Text Files", "*.txt"), ("JSON Files", "*.json"), ("CSV Files", "*.csv")]
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes, title="Save Report")
        if not filename:
            return

        try:
            data = [{col: self.tree.item(row)["values"][i] for i, col in enumerate(("App", "Path", "Local", "Remote", "Status"))} for row in self.tree.get_children()]
            if filename.endswith(".json"):
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            elif filename.endswith(".csv"):
                import csv
                with open(filename, "w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=("App", "Path", "Local", "Remote", "Status"))
                    writer.writeheader()
                    writer.writerows(data)
            else:
                with open(filename, "w", encoding="utf-8") as f:
                    for row in data:
                        f.write(" | ".join(row.values()) + "\n")
            messagebox.showinfo("Success", "Report saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report:\n{e}")

    def show_graph(self):
        graph_window = tk.Toplevel(self.root)
        graph_window.title(self.translations[self.language_var.get()]["traffic_graph"])
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_title("Connection Graph Over Time")
        ax.set_ylabel("Number of Connections")
        ax.set_xlabel("Time (5-second intervals)")
        ax.grid(True)

        def update(frame):
            ax.clear()
            ax.plot(self.traffic_data[-20:], marker='o', linestyle='-', color='lime')
            ax.set_title("Connection Graph Over Time")
            ax.set_ylabel("Number of Connections")
            ax.set_xlabel("Time (5-second intervals)")
            ax.grid(True)

        ani = FuncAnimation(fig, update, interval=5000)
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def get_geoip_info(self, ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"GeoIP request failed: {e}")
            return None

    def load_config(self):
        config_path = os.path.join(os.path.expanduser("~"), ".aetherossec", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.language_var.set(config.get("language", "en"))
                    self.theme_var.set(config.get("theme", "dark"))
                    self.filter_var.set(config.get("filter", ""))
            except Exception as e:
                print(f"Error loading config: {e}")
                self.language_var.set("en")
                self.theme_var.set("dark")
                self.filter_var.set("")
        else:
            self.language_var.set("en")
            self.theme_var.set("dark")
            self.filter_var.set("")

    def save_config(self):
        config_path = os.path.join(os.path.expanduser("~"), ".aetherossec", "config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        try:
            config = {
                "language": self.language_var.get(),
                "theme": self.theme_var.get(),
                "filter": self.filter_var.get()
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def on_close(self):
        self.save_config()
        self.root.destroy()

    def update_language(self):
        self.language = self.language_var.get()
        self.root.title(self.translations[self.language]["title"])
        for key, element in self.ui_elements.items():
            if element and hasattr(element, "config") and "text" in element.keys():  # Check if widget supports 'text'
                element.config(text=self.translations[self.language].get(key, element.cget("text")))

    def update_theme(self):
        def recursive_widget_update(widget, bg_color, fg_color):
            try:
                widget.configure(bg=bg_color, fg=fg_color)
            except:
                pass
            for child in widget.winfo_children():
                recursive_widget_update(child, bg_color, fg_color)

        theme = self.theme_var.get()
        bg_color = "#121f1f" if theme == "dark" else "#ffffff"
        fg_color = "white" if theme == "dark" else "black"
        recursive_widget_update(self.root, bg_color, fg_color)

    def security_check(self):
        firewall_status = "Active" if self.is_firewall_active() else "Inactive"
        antivirus_status = "Active" if self.is_antivirus_running() else "Inactive"
        open_ports = self.get_open_ports()
        message = f"Firewall: {firewall_status}\nAntivirus: {antivirus_status}\nOpen Ports: {', '.join(open_ports) if open_ports else 'None'}"
        messagebox.showinfo("Security Checklist", message)

    def is_firewall_active(self):
        import subprocess
        try:
            result = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True)
            return "State ON" in result.stdout
        except:
            return False

    def is_antivirus_running(self):
        try:
            for proc in psutil.process_iter(['name']):
                if "antivirus" in proc.info['name'].lower():
                    return True
            return False
        except Exception as e:
            print(f"Error checking antivirus: {e}")
            return False

    def get_open_ports(self):
        # Get list of open ports
        return ["80", "443"]

    def disconnect_suspicious_ips(self):
        conns = psutil.net_connections(kind='inet')
        disconnected = []
        for conn in conns:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                remote_ip = conn.raddr.ip
                if any(remote_ip.startswith(ip) for ip in DANGEROUS_IPS):
                    try:
                        psutil.Process(conn.pid).terminate()
                        disconnected.append(remote_ip)
                    except Exception as e:
                        print(f"Failed to disconnect {remote_ip}: {e}")
        if disconnected:
            messagebox.showinfo("Disconnect Suspicious IPs", f"Disconnected IPs: {', '.join(disconnected)}")
        else:
            messagebox.showinfo("Disconnect Suspicious IPs", "No suspicious IPs found to disconnect.")

    def disconnect_selected_ip(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            remote_ip = values[3].split(":")[0]
            conns = psutil.net_connections(kind='inet')
            for conn in conns:
                if conn.raddr and conn.raddr.ip == remote_ip:
                    try:
                        psutil.Process(conn.pid).terminate()
                        messagebox.showinfo("Disconnect IP", f"Disconnected IP: {remote_ip}")
                        return
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to disconnect {remote_ip}: {e}")
                        return
            messagebox.showinfo("Disconnect IP", "No matching connection found.")

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def show_connection_details(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            details = f"App: {values[0]}\nPath: {values[1]}\nLocal: {values[2]}\nRemote: {values[3]}\nStatus: {values[4]}"
            messagebox.showinfo("Connection Details", details)

    def show_geoip(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            remote_ip = values[3].split(":")[0]
            geo_info = self.get_geoip_info(remote_ip)
            if geo_info:
                message = f"Country: {geo_info['country']}\nCity: {geo_info['city']}\nISP: {geo_info['isp']}"
                messagebox.showinfo("GeoIP Info", message)
            else:
                messagebox.showerror("Error", "GeoIP information not found.")

    def copy_ip(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            remote_ip = values[3].split(":")[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(remote_ip)
            self.root.update()
            messagebox.showinfo("Copy", "IP copied successfully.")

    def copy_port(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            remote_port = values[3].split(":")[1]
            self.root.clipboard_clear()
            self.root.clipboard_append(remote_port)
            self.root.update()
            messagebox.showinfo("Copy", "Port copied successfully.")

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)


def show_splash_then_main():
    splash_root = tk.Tk()
    splash = SplashScreen(splash_root)
    splash_root.mainloop()

    root = tk.Tk()
    app = LiveMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    show_splash_then_main()