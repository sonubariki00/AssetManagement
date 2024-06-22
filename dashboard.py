import tkinter as tk
from tkinter import messagebox, ttk
import requests
import time
#import webview

class DashboardView:
    def __init__(self, master):
        self.master = master
        self.master.title("Asset Management Dashboard")
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create widgets for dashboard view
        self.create_widgets()

        # Load data from API
        self.load_data()

    def create_widgets(self):
        self.create_asset_catalog()
        self.create_employee_selection()
        self.create_request_buttons()
        self.create_request_status()
        self.create_search_section()

    def create_asset_catalog(self):
        self.asset_catalog_label = tk.Label(self.frame, text="Asset Catalog", font=("Arial", 14))
        self.asset_catalog_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.asset_catalog_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.asset_catalog_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.asset_catalog_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.asset_catalog_scrollbar.grid(row=1, column=1, sticky="ns")

        self.asset_catalog_listbox.config(yscrollcommand=self.asset_catalog_scrollbar.set)
        self.asset_catalog_scrollbar.config(command=self.asset_catalog_listbox.yview)

    def create_employee_selection(self):
        self.employee_label = tk.Label(self.frame, text="Employee", font=("Arial", 14))
        self.employee_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.employee_combobox = ttk.Combobox(self.frame)
        self.employee_combobox.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.asset_label = tk.Label(self.frame, text="Asset", font=("Arial", 14))
        self.asset_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.asset_combobox = ttk.Combobox(self.frame)
        self.asset_combobox.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    def create_request_buttons(self):
        self.request_button = tk.Button(self.frame, text="Make Request", command=self.make_request, font=("Arial", 12))
        self.request_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.log_button = tk.Button(self.frame, text="View Request Log", command=self.view_request_log, font=("Arial", 12))
        self.log_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")

    def create_request_status(self):
        self.status_label = tk.Label(self.frame, text="Request Status", font=("Arial", 14))
        self.status_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.status_text = tk.Text(self.frame, width=100, height=35)
        self.status_text.grid(row=1, column=2, rowspan=7, padx=5, pady=5, sticky="w")

        self.status_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.status_scrollbar.grid(row=1, column=3, rowspan=7, sticky="ns")

        self.status_text.config(yscrollcommand=self.status_scrollbar.set)
        self.status_scrollbar.config(command=self.status_text.yview)

    def create_search_section(self):
        self.search_label = tk.Label(self.frame, text="Search Assets", font=("Arial", 14))
        self.search_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=9, column=0, padx=5, pady=5, sticky="w")

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_assets, font=("Arial", 12))
        self.search_button.grid(row=10, column=0, padx=5, pady=5, sticky="w")

    def load_data(self):
        try:
            response = requests.get("http://20.2.217.8:5000/api/assets")

            if response.status_code == 200:
                asset_data = response.json()
                for asset in asset_data:
                    self.asset_catalog_listbox.insert(tk.END, f"ID: {asset['asset_id']}, Name: {asset['name']}")

            response = requests.get("http://20.2.217.8:5000/api/employees")
            if response.status_code == 200:
                employee_data = response.json()
                self.employee_combobox["values"] = [employee["employee_id"] for employee in employee_data]

            response = requests.get("http://20.2.217.8:5000/api/assets")
            if response.status_code == 200:
                asset_data = response.json()
                self.asset_combobox["values"] = [asset["asset_id"] for asset in asset_data]
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Failed to load data from API")

    def make_request(self):
        asset_id = self.asset_combobox.get()
        employee_id = self.employee_combobox.get()

        if asset_id and employee_id:
            if asset_id.startswith('A') and asset_id[1:].isdigit():
                response = requests.post(
                    "http://20.2.217.8:5000/api/requests",
                    json={"asset_id": asset_id, "employee_id": employee_id, "status": "pending"}
                )

                if response.status_code == 201:
                    messagebox.showinfo("Success", "Request created successfully!")
                else:
                    messagebox.showerror("Error", "Failed to create request")
            else:
                messagebox.showerror("Error", "Invalid asset ID")
        else:
            messagebox.showerror("Error", "Please select an asset and an employee")

    def view_request_log(self):
        response = requests.get("http://20.2.217.8:5000/api/requests/log")
        if response.status_code == 200:
            log_data = response.json()
            self.status_text.delete(1.0, tk.END)
            for log in log_data:
                self.status_text.insert(tk.END, f"ID: {log['id']}, Asset: {log['asset_name']}, Employee: {log['employee_name']}, Status: {log['status']}, Timestamp: {time.ctime(1627908313.717886)}\n")
        else:
            messagebox.showerror("Error", "Failed to retrieve request log")

    def search_assets(self):
        search_query = self.search_entry.get()
        response = requests.get(f"http://20.2.217.8:5000/api/assets/search?q={search_query}")
        if response.status_code == 200:
            asset_data = response.json()
            self.asset_catalog_listbox.delete(0, tk.END)
            for asset in asset_data:
                self.asset_catalog_listbox.insert(tk.END, f"ID: {asset['asset_id']}, Name: {asset['name']}")
        else:
            messagebox.showerror("Error", "Failed to search assets")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardView(root)
    root.mainloop()

