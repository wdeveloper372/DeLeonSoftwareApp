import customtkinter as ctk
from calculator import calculate_estimate
import database_cloud as db # Ensure you have your Supabase setup here

class EstimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Company Estimator")
        self.geometry("500x700")

        # --- INPUTS ---
        self.client_name = ctk.CTkEntry(self, placeholder_text="Client Name")
        self.client_name.pack(pady=5)

        self.parts_entry = ctk.CTkEntry(self, placeholder_text="Parts Amount ($)")
        self.parts_entry.pack(pady=5)

        self.labor_entry = ctk.CTkEntry(self, placeholder_text="Labor ($)")
        self.labor_entry.pack(pady=5)

        self.calib_entry = ctk.CTkEntry(self, placeholder_text="Calibration ($)")
        self.calib_entry.pack(pady=5)

        self.kit_checkbox = ctk.CTkCheckBox(self, text="Needs Kit?")
        self.kit_checkbox.pack(pady=5)

        # --- ACTIONS ---
        self.calc_btn = ctk.CTkButton(self, text="Calculate & Save", command=self.run_calc)
        self.calc_btn.pack(pady=10)

        # --- RESULTS DISPLAY ---
        self.res_label = ctk.CTkLabel(self, text="Total: $0.00", font=("Arial", 20, "bold"))
        self.res_label.pack(pady=10)

        # --- SEARCH AREA ---
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search Past Clients...")
        self.search_entry.pack(pady=(20, 0))
        self.search_btn = ctk.CTkButton(self, text="Search History", command=self.search_history)
        self.search_btn.pack(pady=5)

        self.history_frame = ctk.CTkScrollableFrame(self, height=200)
        self.history_frame.pack(fill="x", padx=20, pady=10)

    def run_calc(self):
        try:
            # Run your logic
            data = calculate_estimate(
                self.parts_entry.get(),
                self.kit_checkbox.get(),
                self.labor_entry.get(),
                self.calib_entry.get()
            )
            
            # Update UI
            self.res_label.configure(text=f"Total: ${data['total']}")
            
            # Save to Cloud
            db.save_to_cloud(self.client_name.get(), data['total'])
            
        except ValueError:
            self.res_label.configure(text="Error: Enter valid numbers")

    def search_history(self):
        # Clear old results
        for widget in self.history_frame.winfo_children(): widget.destroy()
        
        results = db.search_cloud(self.search_entry.get())
        for item in results:
            text = f"{item['client']} | Total: ${item['total']}"
            ctk.CTkLabel(self.history_frame, text=text).pack()

if __name__ == "__main__":
    app = EstimateApp()
    app.mainloop()