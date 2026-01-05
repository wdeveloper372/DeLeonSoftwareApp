def calculate_estimate(parts_val, needs_kit, labor_val, calib_val):
    """Your core math logic refactored for a GUI"""
    # 1. Parts & Profit
    parts = float(parts_val)
    profit = parts * 0.45
    sum_parts_profit = parts + profit
    
    # 2. Taxes
    tax_rate = 0.1125
    part_tax = sum_parts_profit * tax_rate
    base_total = sum_parts_profit + part_tax
    
    # 3. Kit Logic
    kit_total = 0
    if needs_kit: # 'y' from your logic is now a True/False checkbox
        kit_price = 25
        kit_tax = kit_price * 0.1125
        kit_total = kit_price + kit_tax
        
    # 4. Final Sum
    labor = float(labor_val)
    calibration = float(calib_val)
    grand_total = base_total + labor + calibration + kit_total
    
    # Return a dictionary so the GUI knows what to display
    return {
        "parts_profit": round(sum_parts_profit, 2),
        "tax": round(part_tax, 2),
        "kit": round(kit_total, 2),
        "total": round(grand_total, 2)
    }
