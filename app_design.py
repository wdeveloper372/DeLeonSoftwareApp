import customtkinter as ctk
from logic import calculate_estimate
import database_cloud as db # Now active!
from export_pdf import generate_pdf


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("De Leon Auto Glass Estimator")
        self.geometry("450x750")

        # Ensure database table exists
        db.initialize_db()

        try:
            self.iconbitmap("logo.ico")
        except:
            pass

        self.pdf_button = ctk.CTkButton(self, text="Export PDF", fg_color="darkgreen", command=self.create_pdf)
        self.pdf_button.pack(pady=5)        

        # --- SECTION 1: CALCULATOR ---
        ctk.CTkLabel(self, text="New Estimate", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.client_name = ctk.CTkEntry(self, placeholder_text="Client Name")
        self.client_name.pack(pady=5)

        self.parts_entry = ctk.CTkEntry(self, placeholder_text="Parts Amount ($)")
        self.parts_entry.pack(pady=5)

        self.labor_entry = ctk.CTkEntry(self, placeholder_text="Labor ($)")
        self.labor_entry.pack(pady=5)

        self.calib_entry = ctk.CTkEntry(self, placeholder_text="Calibration ($)")
        self.calib_entry.pack(pady=5)

        self.kit_check = ctk.CTkCheckBox(self, text="Include Kit ($25 + Tax)")
        self.kit_check.pack(pady=10)

        self.calc_button = ctk.CTkButton(self, text="Calculate & Sync", command=self.process_data)
        self.calc_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="Total: $0.00", font=("Arial", 20, "bold"))
        self.result_label.pack(pady=10)

        # --- SECTION 2: SEARCH ---
        ctk.CTkLabel(self, text="Search Past Estimates", font=("Arial", 16, "bold")).pack(pady=(30, 10))
        
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search Client Name...")
        self.search_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(self, text="Search Database", fg_color="gray", command=self.run_search)
        self.search_button.pack(pady=5)

        self.search_results = ctk.CTkLabel(self, text="Results will appear here", wraplength=350)
        self.search_results.pack(pady=10)

    def create_pdf(self):
        try:
            # 1. Get current results
            results = calculate_estimate(
                self.parts_entry.get(),
                self.kit_check.get(),
                self.labor_entry.get(),
                self.calib_entry.get()
            )
            
            # 2. Generate the PDF
            fname = generate_pdf(
                self.client_name.get(),
                results,
                self.labor_entry.get(),
                self.calib_entry.get()
            )
            print(f"PDF saved as {fname}")
        except Exception as e:
            print(f"Error generating PDF: {e}")

    def process_data(self):
        try:
            results = calculate_estimate(
                self.parts_entry.get(),
                self.kit_check.get(),
                self.labor_entry.get(),
                self.calib_entry.get()
            )

            self.result_label.configure(text=f"Total: ${results['total']}")

            # Save to Supabase
            db.save_estimate(self.client_name.get(), 1, results['total'])
            print(f"Saved {self.client_name.get()} to Cloud.")
            
        except Exception as e:
            self.result_label.configure(text="Error in calculation/sync")
            print(f"Error: {e}")

    def run_search(self):
        query = self.search_entry.get()
        data = db.search_estimates(query)
        
        if data:
            # Format the first few results for the label
            display_text = ""
            for item in data[:5]: # Show top 5 results
                display_text += f"Client: {item[2]} | Total: ${item[4]}\n"
            self.search_results.configure(text=display_text)
        else:
            self.search_results.configure(text="No clients found.")

if __name__ == "__main__":
    app = App()
    app.mainloop()