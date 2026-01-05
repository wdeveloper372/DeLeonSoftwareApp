import urllib.parse
import flet as ft

def main(page: ft.Page):
    page.title = "DeLeon Glass Estimator"
    page.theme_mode = ft.ThemeMode.DARK
    # Handle window size safely for different Flet versions
    try:
        page.window.width = 400
        page.window.height = 800
    except AttributeError:
        page.window_width = 400
        page.window_height = 800
    page.scroll = "auto"
    page.padding = 20

    # UI Inputs
    parts_input = ft.TextField(label="Parts Cost ($)", keyboard_type=ft.KeyboardType.NUMBER)
    labor_input = ft.TextField(label="Labor Cost ($)", keyboard_type=ft.KeyboardType.NUMBER)
    calib_input = ft.TextField(label="Calibration ($)", keyboard_type=ft.KeyboardType.NUMBER, value="0")
    kit_checkbox = ft.Checkbox(label="Include Installation Kit ($25)")

    # UI Outputs
    res_parts = ft.Text("Parts + Profit: $0.00", size=16)
    res_tax = ft.Text("Tax: $0.00", size=16)
    res_kit = ft.Text("Kit: $0.00", size=16)
    res_total = ft.Text("Grand Total: $0.00", size=24, weight="bold", color="green")

    # Share Function
    def on_share(e):
        # This builds the text message body
        msg = (
            f"DeLeon Glass Estimate\n"
            f"Parts/Profit: {res_parts.value}\n"
            f"Tax: {res_tax.value}\n"
            f"Kit: {res_kit.value}\n"
            f"TOTAL: {res_total.value}"
        )
        encoded_msg = urllib.parse.quote(msg)
        # Opens the native SMS app on your phone
        page.launch_url(f"sms:?body={encoded_msg}")

    # Calculation Logic
    def on_calculate(e):
        try:
            parts = float(parts_input.value or 0)
            profit = parts * 0.45
            sum_parts_profit = parts + profit
            
            tax_rate = 0.1125
            part_tax = sum_parts_profit * tax_rate
            base_total = sum_parts_profit + part_tax
            
            kit_total = 0
            if kit_checkbox.value:
                kit_price = 25
                kit_tax = kit_price * 0.1125
                kit_total = kit_price + kit_tax
                
            labor = float(labor_input.value or 0)
            calibration = float(calib_input.value or 0)
            grand_total = base_total + labor + calibration + kit_total

            res_parts.value = f"Parts + Profit: ${sum_parts_profit:,.2f}"
            res_tax.value = f"Tax: ${part_tax:,.2f}"
            res_kit.value = f"Kit: ${kit_total:,.2f}"
            res_total.value = f"Grand Total: ${grand_total:,.2f}"
            
            # Show the share button only after a calculation is done
            share_btn.visible = True
            
        except ValueError:
            res_total.value = "Error: Numbers only!"
        
        page.update()

    def on_clear(e):
        parts_input.value = ""
        labor_input.value = ""
        calib_input.value = "0"
        kit_checkbox.value = False
        res_total.value = "Grand Total: $0.00"
        share_btn.visible = False # Hide share button on clear
        page.update()

    # Define the share button (hidden by default)
    share_btn = ft.ElevatedButton(
        "Share Estimate", 
        icon=ft.Icons.SHARE, 
        on_click=on_share, 
        visible=False,
        bgcolor="blue",
        color="white"
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("DeLeon Glass", size=32, weight="bold", color="blue"),
                ft.Divider(),
                parts_input,
                labor_input,
                calib_input,
                kit_checkbox,
                ft.Row([
                    ft.ElevatedButton("Calculate", on_click=on_calculate, expand=True),
                    ft.OutlinedButton("Clear", on_click=on_clear),
                ]),
                ft.Divider(),
                res_parts,
                res_tax,
                res_kit,
                res_total,
                share_btn
            ]
        )
    )

ft.app(target=main)