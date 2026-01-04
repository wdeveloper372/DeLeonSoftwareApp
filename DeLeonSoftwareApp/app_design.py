import customtkinter as ctk
from logic import calculate_estimate
import database_cloud as db # The cloud sync file we created earlier

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Company Estimator v2.0")
        self.geometry("400x600")

        # UI Input Fields
        self.client_name = ctk.CTkEntry(self, placeholder_text="Client Name")
        self.client_name.pack(pady=10)

        self.parts_entry = ctk.CTkEntry(self, placeholder_text="Parts Amount ($)")
        self.parts_entry.pack(pady=5)

        self.labor_entry = ctk.CTkEntry(self, placeholder_text="Labor ($)")
        self.labor_entry.pack(pady=5)

        self.calib_entry = ctk.CTkEntry(self, placeholder_text="Calibration ($)")
        self.calib_entry.pack(pady=5)

        self.kit_check = ctk.CTkCheckBox(self, text="Include Kit ($25 + Tax)")
        self.kit_check.pack(pady=10)

        # Button to trigger your logic
        self.calc_button = ctk.CTkButton(self, text="Calculate & Sync", command=self.process_data)
        self.calc_button.pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="Total: $0.00", font=("Arial", 20, "bold"))
        self.result_label.pack(pady=10)

    def process_data(self):
        # 1. Run your logic using the values from the screen
        results = calculate_estimate(
            self.parts_entry.get(),
            self.kit_check.get(),
            self.labor_entry.get(),
            self.calib_entry.get()
        )

        # 2. Update the Screen
        self.result_label.configure(text=f"Total: ${results['total']}")

        # 3. Save to Cloud (Supabase)
        # This makes it instantly available on mobile!
        db.save_to_cloud(self.client_name.get(), results['total'])
        print("Synced to cloud successfully.")

if __name__ == "__main__":
    app = App()
    app.mainloop()