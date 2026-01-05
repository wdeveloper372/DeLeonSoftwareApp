import flet as ft
from logic import calculate_estimate # Your existing math logic!

def main(page: ft.Page):
    # App Settings
    page.title = "De Leon Estimator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive" # Allows scrolling on small phones
    page.padding = 20

    # UI Elements (Mobile friendly - Large and Tap-ready)
    client_name = ft.TextField(label="Client Name", prefix_icon=ft.icons.PERSON)
    parts_input = ft.TextField(label="Parts Amount ($)", keyboard_type=ft.KeyboardType.NUMBER)
    labor_input = ft.TextField(label="Labor ($)", keyboard_type=ft.KeyboardType.NUMBER)
    calib_input = ft.TextField(label="Calibration ($)", keyboard_type=ft.KeyboardType.NUMBER)
    kit_check = ft.Checkbox(label="Include Installation Kit", value=False)
    
    result_text = ft.Text("Total: $0.00", size=30, weight="bold", color="blue")

    def on_calc_click(e):
        try:
            # Running your exact same logic file
            results = calculate_estimate(
                parts_input.value or 0,
                float(parts_input.value or 0),
                kit_check.value,
                labor_input.value or 0,
                calib_input.value or 0
                float(labor_input.value or 0),
                float(calib_input.value or 0)
            )
            result_text.value = f"Total: ${results['total']}"
            page.update()
        except Exception as ex:
            result_text.value = "Input Error"
            page.update()

    # Add components to the screen
    page.add(
        ft.Column(
            [
                ft.Text("De Leon Auto Glass", size=25, weight="bold"),
                client_name,
                parts_input,
                labor_input,
                calib_input,
                kit_check,
                ft.ElevatedButton(
                    "Calculate Estimate", 
                    on_click=on_calc_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    height=50
                ),
                ft.Divider(),
                result_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Run the app
ft.app(target=main)