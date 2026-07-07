import os
import django
import re
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

raw_data = """
DCPK - 522 Rs. 280(set in colour)
DCPK - 523 Rs. 320(set in colour)
DCPK - 524 Rs. 350(set in colour)
DCPK - 525 Rs. 325(set in colour)
DCPK - 526 Rs. 325(set in colour)
DCPK - 527 Rs. 325(set in colour)
DCPK - 528 Rs. 325(set in colour)
DCPK - 529 Rs. 325(set in colour)
DCPK - 530 Rs. 325
DCPK - 531 Rs. 325
DCPK - 532 Rs. 325
DCPK - 533 Rs. 350
DCPK - 534 Rs. 350(set in colour)
DCPK - 535 Rs. 350
DCPK - 536 Rs. 340
DLPP - 537 Rs. 550
PPMP - 538 Rs. 1050
DMPK - 539 Rs. 450
DPPK - 540 Rs. 350
BKPC - 601 Rs. 475(set in colour)
DBKPC - 602 Rs. 55(set in colour)
DBKPC - 603 Rs. 680(Set in colour)
DBKPC - 604 Rs. 700
DBKPC - 605 Rs. 540
DBKPC - 606 Rs. 540
DBKPC - 607 Rs. 540
DBKPC - 608 Rs. 900
DBKPC - 609 Rs. 550
DBKPC - 610 Rs. 550
DPKPC - 611 Rs. 700
DBCKPC - 701 Rs. 700
DPBPKP - 702 Rs. 2500
DBMCPK - 703 Rs. 975
DBMCPK - 704 Rs. 925
DBMCPP - 705 Rs. 1050
DBDCPK - 706 Rs. 800
OBMCPK - 707 Rs. 1300
DBDCPK - 708 Rs. 750
DBCCPK - 709 Rs. 850
DBCCPK - 710 Rs. 1050
DBCCPK - 711 Rs. 1250
DBCMPK - 712 Rs. 700(set in colour)
DCPKMPB - 713 Rs. 800
DCPKCMB - 714 Rs. 700
DCPPBMP - 715 Rs. 980    
DCPPBCM - 716 Rs. 800
DMPPCBM - 717 Rs. 1020
DMPPPBM - 718 Rs. 1210
DMPKCBM - 719 Rs. 1060
DBCMCPK - 720 Rs. 1025
PB - 801 Rs. 550
PB - 802 Rs. 600
PB - 803 Rs. 950
PB - 804 Rs. 850
PPK - 805 Rs. 250
PP - 806 Rs. 70
PK - 807 Rs. 60
PK - 808 Rs. 155
PP - 809 Rs. 170
PPKC - 810 Rs. 375
PP - 811 Rs. 200
PPKB - 812 Rs. 480
PPCK - 814 Rs. 310
PL - 815 Rs. 150(set in colour)
MPK - 816 Rs. 120
BP - 818 Rs. 180
RC - Cup - 897 Rs. 325(set in colour)
RC - Cup - 898 Rs. 180
RC - Cup - 899 Rs. 180
RC - Cup - 900 Rs. 240
RC - Cup - 901 Rs. 130
RC - Cup - 902 Rs. 130
RC - Cup - 903 Rs. 225
RC - Cup - 904 Rs. 280
RC - Cup - 905 Rs. 290
RC - Cup - 906 Rs. 240
RC - Cup - 907 Rs. 240
RC - Cup - 908 Rs. 190
RC - Cup - 909 Rs. 210
RC - Cup - 910 Rs. 120
RC - Cup - 911 Rs. 165
RC - Cup - 912 Rs. 280
RC - Cup 1200 ML - 913 Rs. 325
RC - Cup - 914 Rs. 60
RC - Cup 900ML - 999 Rs. 280
RC - Cup - 915 Rs. 220
RC - Cup - 916 Rs. 300
RC - Cup - 917 Rs. 300
RC - Cup - 989 Rs. 280 
RC - Cup - 992 Rs. 240 
RC - Cup - 990 Rs. 220 
RC - Cup - 991 Rs. 325 
RC - Cup - 993 Rs. 150 
RC - Cup - 995 Rs. 60 
RC - Cup - 996 Rs. 60 
RC - Cup - 994 Rs. 80 
RC - Cup - 997 Rs. 150
RC - Cup - 998 Rs. 60
"""

def parse_and_update():
    lines = raw_data.strip().split('\n')
    parsed_items = {}
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # We need to extract the product name and the price
        # Format is usually: NAME Rs. PRICE(optional notes)
        
        match = re.search(r'^(.*?)Rs\.\s*([0-9.]+)(.*)$', line, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            price = float(match.group(2))
            parsed_items[name] = price
            
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
            n_match = re.search(r'([0-9]{3,4})', name)
            target_code = n_match.group(1) if n_match else None
            
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
            new_price = round(price * 1.60)
            best_match.price = Decimal(str(new_price))
            best_match.save(update_fields=['price'])
            out_table.append(f"| {best_match.name} | Rs. {price} | **Rs. {new_price}** |")
        else:
            missing.append(name)
            
    with open(r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\batch8_prices.md', 'w', encoding='utf-8') as f:
        f.write("## Batch 8 Price Update (+60%)\n\n")
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
