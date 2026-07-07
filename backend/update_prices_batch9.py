import os
import django
import re
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

raw_data = """
RC - Cup - 918
Rs. 145
RC - Cup - 920
Rs. 155
RC - Cup - 919
Rs. 145
RC - Cup - 921
Rs. 155
RC - Cup - 925
Rs. 185
RC - Cup - 924
Rs. 185
RC - Cup - 923
Rs. 150
RC - Cup - 922
Rs. 150
RC - Cup - 929
Rs. 190
RC - Cup - 928
Rs. 190
RC - Cup - 927
Rs. 175
RC - Cup - 926
Rs. 175
RC - Cup - 930
Rs. 150
RC - Cup - 931
Rs. 150
RC - Cup - 932
Rs. 150
RC - Cup - 933
Rs. 150
RC - Cup - 938
Rs. 210
RC - Cup - 937
Rs. 145
RC - Cup - 936
Rs. 145
RC - Cup - 935
Rs. 165
RC - Cup - 934
Rs. 165
RC - Cup - 940
Rs. 250
RC - Cup - 939
Rs. 210
RC - Self Steering Cup
(Glass) - 941
Rs. 350
RC - Magic Mug - 942
Rs. 100 
RC - Warm Cup - 943
Rs. 210
RC - Coral Cup - 944
Rs. 75
RC - Coral Cup - 945
Rs. 75
RC - Coral Cup - 946
Rs. 75 
RC - Coral Cup - 947
Rs. 75
RC - Two Tone Cup - 948
Rs. 70 
RC - Sublemation Cup - 949
Rs. 35
RC - Full Color Cup - 950
Rs. 75
RC - Full Color Cup - 951
Rs. 75 
RC - Full Color Cup - 952
Rs. 75
RC - Cup - 914
Rs. 60 
RC - Cup - 953
Rs. 110
RC - Cup - 954
Rs. 160
RC - Cup - 955
Rs. 160
RC - Cup - 956
Rs. 160
RC - Cup - 957
Rs. 160
RC - Cup - 959
Rs. 90
RC - Cup - 958
Rs. 60
RC - Transparent Glass - 960A
Rs. 320
RC - 6pcs Glass - 960B
Rs. 600
RC - 6pcs Glass - 960C
Rs. 370
RC - Cup - 961
Rs. 100
RC - Cup - 962
Rs. 90
RC - Cup - 963
Rs. 100
RC - Cup - 964
Rs. 95
RC - Cup - 965
Rs. 130
RC - Cup - 966
Rs. 130
RC - Cup - 967
Rs. 250
RC - Cup - 968
Rs. 250
RC - Cup - 969
Rs. 250
RC - Cup - 970
Rs. 140
RC - Cup - 971
Rs. 240
RC - Cup - 972
Rs. 180
RC - Cup - 973
Rs. 250 
RC - Cup - 974
Rs. 280
RC - Cup - 975
Rs. 280
RC - Cup - 976
Rs. 210
RC - Cup - 977
Rs. 165
RC - Cup - 981
Rs. 180
RC - Cup - 980
Rs. 350
RC - Cup - 979
Rs. 600
RC - Cup - 978
Rs. 250
RC - Cup - 982
Rs. 300
RC - Cup - 983 
Rs. 160
RC - Cup - 984
Rs. 160
"""

def parse_and_update():
    lines = raw_data.strip().split('\n')
    parsed_items = {}
    current_product = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if "Rs." in line or "Rs" in line or "rs." in line.lower() or "rs " in line.lower():
            parts = re.split(r'Rs\.?|rs\.?|Rs', line, flags=re.IGNORECASE)
            
            if len(parts) > 1 and parts[0].strip():
                name = parts[0].strip()
                price_str = parts[1].strip()
                current_product = name
            else:
                price_str = parts[-1].strip()
            
            if "Call" in price_str or "call" in price_str.lower():
                parsed_items[current_product] = "Call"
            else:
                price_match = re.search(r'([0-9]+\.?[0-9]*)', price_str.replace(' ', ''))
                if price_match:
                    parsed_items[current_product] = float(price_match.group(1))
            current_product = ""
        else:
            if current_product: current_product += " " + line
            else: current_product = line
            
    all_products = list(Product.objects.all())
    
    out_table = []
    missing = []
    
    for name, price in parsed_items.items():
        if not name: continue
        
        name_clean = name.replace("-", " ").replace("(", " ").replace(")", " ").lower().split()
        
        best_match = None
        
        # Check if there is an exact number code in the name
        code_match = re.search(r'([A-Za-z0-9]+)', name.split()[-1])
        target_code = code_match.group(1).lower() if code_match else None
        if target_code and target_code.isdigit():
            # if the last part is a number, it's definitely the code.
            pass
        else:
            # find any number
            n_match = re.search(r'([0-9]{3,4}[A-Za-z]?)', name)
            target_code = n_match.group(1).lower() if n_match else None
            
        for p in all_products:
            p_name_clean = p.name.replace("-", " ").replace("(", " ").replace(")", " ").lower()
            
            if target_code:
                if target_code not in p_name_clean.split():
                    continue
                    
            alpha_words = [w for w in name_clean if w.isalpha()]
            match = True
            for aw in alpha_words:
                if aw not in p_name_clean:
                    match = False
                    break
            
            if match:
                best_match = p
                break
                
        if not best_match:
            # Fallback: check exact name case insensitive
            best_match = next((p for p in all_products if name.lower() in p.name.lower()), None)
                
        if best_match:
            if price == "Call":
                out_table.append(f"| {best_match.name} | Rs. Call | **Rs. Call (No Change)** |")
            else:
                new_price = round(price * 1.60)
                best_match.price = Decimal(str(new_price))
                best_match.save(update_fields=['price'])
                out_table.append(f"| {best_match.name} | Rs. {price} | **Rs. {new_price}** |")
        else:
            missing.append(name)
            
    with open(r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\batch9_prices.md', 'w', encoding='utf-8') as f:
        f.write("## Batch 9 Price Update (+60%)\n\n")
        f.write("| Product Name | Old Base Price | New Price (+60%) |\n")
        f.write("|---|---|---|\n")
        f.write('\n'.join(out_table))
        f.write('\n\n')
        if missing:
            f.write("> [!WARNING]\n")
            f.write("> **The following products were not found:**\n")
            for m in missing:
                f.write(f"- {m}\n")
            
if __name__ == '__main__':
    parse_and_update()
