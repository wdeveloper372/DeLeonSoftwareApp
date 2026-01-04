import customtkinter as ctk
from database import save_estimate, search_estimates, initialize_db

class EstimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        initialize_db() # Ensure the database file exists on startup

        self.title("De Leon Auto Glass Estimate App")
        self.geometry("500x600")

        # --- INPUT SECTION ---
        self.label = ctk.CTkLabel(self, text="New Estimate", font=("Arial", 18, "bold"))
        self.label.pack(pady=10)

        self.client_input = ctk.CTkEntry(self, placeholder_text="Client Name")
        self.client_input.pack(pady=5)

        self.unit_input = ctk.CTkEntry(self, placeholder_text="Units")
        self.unit_input.pack(pady=5)

        self.save_btn = ctk.CTkButton(self, text="Calculate & Save", command=self.handle_save)
        self.save_btn.pack(pady=10)

        # --- SEARCH SECTION ---
        self.h_line = ctk.CTkFrame(self, height=2, fg_color="gray") # Visual separator
        self.h_line.pack(fill="x", padx=20, pady=20)

        self.search_input = ctk.CTkEntry(self, placeholder_text="Search by Client Name...")
        self.search_input.pack(pady=5)
        
        self.search_btn = ctk.CTkButton(self, text="Search History", fg_color="transparent", border_width=2, command=self.handle_search)
        self.search_btn.pack(pady=5)

        # This is where search results will appear
        self.results_frame = ctk.CTkScrollableFrame(self, width=400, height=200)
        self.results_frame.pack(pady=10, padx=10)

    def handle_save(self):
        name = self.client_input.get()
        units = float(self.unit_input.get())
        total = units * 50 # Replace with your actual math function
        
        save_estimate(name, units, total)
        self.client_input.delete(0, 'end')
        self.unit_input.delete(0, 'end')
        print("Saved to Database")

    def handle_search(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Get results from database
        query = self.search_input.get()
        results = search_estimates(query)

        # Display each result as a label in the scrollable box
        for row in results:
            # row structure: (id, date, name, units, total)
            text = f"{row[1]} | {row[2]} | {row[3]} units | Total: ${row[4]:.2f}"
            result_item = ctk.CTkLabel(self.results_frame, text=text, anchor="w")
            result_item.pack(fill="x", pady=2)

if __name__ == "__main__":
    app = EstimateApp()
    app.mainloop()