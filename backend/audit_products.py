import os
import django
import re
from collections import defaultdict
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def audit_products():
    print("## Checking for Duplicates and Unupdated Prices")
    
    # 1. Parse all batch scripts to get a mapping of code -> base price
    base_prices = {}
    batch_files = glob.glob('update_prices_batch*.py')
    for fpath in batch_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'raw_data\s*=\s*\"\"\"(.*?)\"\"\"', content, re.DOTALL)
            if match:
                raw_data = match.group(1).strip()
                lines = raw_data.split('\n')
                current_name = ""
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    if "Rs." in line or "Rs" in line or "rs." in line.lower() or "rs " in line.lower():
                        parts = re.split(r'Rs\.?|rs\.?|Rs', line, flags=re.IGNORECASE)
                        if len(parts) > 1 and parts[0].strip():
                            name = parts[0].strip()
                            price_str = parts[1].strip()
                        else:
                            name = current_name
                            price_str = parts[-1].strip()
                            
                        # Extract code from name
                        code_match = re.search(r'([A-Za-z0-9]+)$', name.replace(")", "").replace("(", "").strip())
                        code = code_match.group(1).lower() if code_match else ""
                        if not code.isdigit():
                            n_match = re.search(r'([0-9]{3,4}[A-Za-z]?)', name)
                            code = n_match.group(1).lower() if n_match else code
                            
                        if "Call" not in price_str and "call" not in price_str.lower():
                            p_match = re.search(r'([0-9]+\.?[0-9]*)', price_str.replace(' ', ''))
                            if p_match and code:
                                base_prices[code] = float(p_match.group(1))
                        current_name = ""
                    else:
                        if current_name: current_name += " " + line
                        else: current_name = line
                        
    products = Product.objects.all()
    
    code_groups = defaultdict(list)
    unupdated = []
    
    for p in products:
        name = p.name
        price = float(p.price)
        
        # Extract number code from product name
        code = None
        parts = name.replace("-", " ").replace("(", " ").replace(")", " ").split()
        if parts:
            last = parts[-1].lower()
            if any(char.isdigit() for char in last):
                code = last
            else:
                n_match = re.search(r'([0-9]{3,4}[A-Za-z]?)', name)
                if n_match:
                    code = n_match.group(1).lower()
        
        if code:
            code_groups[code].append(p)
            
            # Check if price is still base price
            if code in base_prices:
                base = base_prices[code]
                expected_new = round(base * 1.6)
                if abs(price - base) < 2:  # Same as old price
                    unupdated.append((p, base, expected_new))
                elif price < base * 1.5 and price != 999.0 and price != 0: 
                    unupdated.append((p, base, expected_new))
    
    # Check duplicate codes
    duplicates = {code: prods for code, prods in code_groups.items() if len(prods) > 1}
    
    out_lines = []
    out_lines.append("# Audit Report\n")
    out_lines.append("## Duplicate Products (Grouped by Number Code)\n")
    if not duplicates:
        out_lines.append("No clear duplicates found based on numeric codes.\n")
    else:
        for code, prods in duplicates.items():
            out_lines.append(f"**Code: {code.upper()}**")
            for p in prods:
                out_lines.append(f"- ID: {p.id} | Name: {p.name} | Price: Rs. {p.price}")
            out_lines.append("")
            
    out_lines.append("\n## Products with Un-updated Prices (Still Base Price)\n")
    if not unupdated:
        out_lines.append("No unupdated prices detected based on parsed raw data.\n")
    else:
        for p, base, exp in unupdated:
            out_lines.append(f"- ID: {p.id} | Name: {p.name} | Current Price: Rs. {p.price} | Base Was: Rs. {base} | Expected: Rs. {exp}")
            
    with open(r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\audit_report.md', 'w', encoding='utf-8') as f:
        f.write("\n".join(out_lines))
        
    print("Audit complete, wrote to audit_report.md")

if __name__ == '__main__':
    audit_products()
