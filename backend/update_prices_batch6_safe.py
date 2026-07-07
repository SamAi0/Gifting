import os
import django
import re
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

raw_data = """
RC - Cup - 985
Rs. 100
RC - Cup - 986
Rs. 150
RC - Cup - 987
Rs. 250
RC - Cup - 988
Rs. 250
1051
Rs. 250
1052
Rs. 160
1053
Rs. 110
1054
Rs. 110
1055
Rs. 225
1056
Rs. 160
1057
Rs. 130
1058
Rs. 150
1059
Rs. 180
RC - Keychain - 1101
Rs. 15
RC - Keychain - 1102
Rs. 15
RC - Keychain - 1103
Rs. 15
RC - Keychain - 1104
Rs. 24
RC - Keychain - 1105
Rs. 15
RC - Keychain - 1106
Rs. 15
RC - Keychain - 1107
Rs. 18.5
RC - Keychain - 1108
Rs. 23
RC - Keychain - 1109
Rs. 15
RC - Keychain - 1110
Rs. 28
RC - Keychain - 1111
Rs. 28
RC - Keychain - 1112
Rs. 30
RC - Keychain - 1114
Rs. 32
RC - Keychain - 1116
Rs. 32
RC - Keychain - 1115
Rs.32
RC - Keychain - 1117
Rs. 32
RC - Keychain - 1118 Rs. 32
RC - Keychain - 1113
Rs. 35
RC - Keychain - 1119
Rs. 32
RC - Keychain - 1120
Rs. 32
RC - Keychain - 1121 
Rs. 32
RC - Keychain - 1122 Rs. 34
RC - Keychain - 1123 Rs. 45
RC - Keychain - 1124
Rs. 45
RC - Keychain - 1125
Rs. 32
RC - Keychain - 1126
Rs. 32
RC - Keychain - 1127
Rs. 32
RC - Keychain - 1128
Rs. 32
RC - Keychain - 1129
Rs. 32
RC - Keychain - 1130
Rs. 32
RC - Keychain - 1131
Rs. 32
RC - Keychain - 1132 also set in colors
Rs. 8
RC - Keychain - 1133
Rs. 39
RC - Keychain - 1134
Rs. 38
RC - Keychain - 1135
Rs. 9
RC - Keychain - 1136
Rs. 10
RC - Keychain - 1137
Rs. 11
RC - Keychain - 1138
Rs. 24
RC - Keychain - 1139
Rs. 22
RC - Keychain - 1140 also set in colors
Rs. 25
RC - Cardholder - 1201
Rs. 45
RC - Cardholder - 1202
Rs. 60
RC - Cardholder - 1204
Rs. 55
RC - Cardholder - 1203
Rs. 45
RC - Cardholder - 1205
Rs. 45
RC - Cardholder - 1206
Rs. 45
RC - Cardholder - 1208
Rs. 45 
RC - Cardholder - 1207
Rs. 30
RC - Cardholder - 1209
Rs. 45
RC - Cardholder - 1210
Rs. 40
RC - Cardholder - 1211
Rs. 45
RC - Cardholder - 1212
Rs. 45
RC - Cardholder - 1213
Rs. 45
RC - Cardholder - 1214
Rs. 45
RC - Cardholder - 1215
Rs. 45
RC - Cardholder - 1216
Rs. 50
RC - Cardholder - 1217
Rs. 45
RC - Cardholder - 1218
Rs. 60
RC - Cardholder - 1219
Rs. 48
RC - Cardholder - 1220
Rs. 60
RC - Cardholder - 1221
Rs. 45
RC - Cardholder - 1222
Rs. 45
RC - Cardholder - 1223
Rs. 45
RC - Cardholder - 1224
Rs. 45
RC - Cardholder - 1225
Rs. 45
RC - Cardholder - 1226
Rs. 45
RC - Cardholder - 1228
Rs. 45
RC - Cardholder - 1227
Rs. 45
RC - Cardholder - 1229
Rs. 70
RC - Cardholder - 1230
Rs. 45
RC - Cardholder - 1232 Rs. 50
RC - Cardholder - 1231 
Rs. 55
RC - Cardholder - 1233
Rs. 55
RC - Cardholder - 1234
Rs. 80
1398
Rs. 300
1399
Rs. 325
1400
Rs. 325
RC - 18- Pen Stand Teacher - 1401
Rs. 230
RC - 14- Pen Stand CA - 1402
Rs. 230
RC - 13- Pen Stand Advovcate- 1404
Rs. 230
RC - 12- Pen Stand Doctor - 1403
Rs. 230
RC - 15- Pen Stand - 1405
Rs. 350
RC - 08- Pen Stand - 1408
Rs. 225
RC - 6081- Pen Stand - 1407
Rs. 195
RC - 05- Pen Stand - 1409
Rs. 260
RC - 10- Pen Stand - 1410
Rs. 250
RC - 6054- Pen Stand - 1406
Rs. 230
RC - 6045- Pen Stand - 1411
Rs. 220
RC - 6061- Pen Stand - 1412
Rs. 180
RC - 6008- Pen Stand - 1414
Rs. 180
RC - 2750- Pen Stand - 1413
Rs. 280
RC - 6021- Pen Stand - 1415
Rs. 190
RC - 5202- Pen Stand - 1416
Rs. 130
RC - 5154- Pen Stand - 1417
Rs. 115
RC - 5153- Pen Stand - 1418
Rs. 130
RC - 5143 Pen Stand - 1420
Rs. 180
RC - 2043- Pen Stand - 1419
Rs. 180
RC - 2008- Pen Stand - 1421
Rs. 110
RC - 1067- Pen Stand - 1422
Rs. 170
RC - 5202- Pen Stand - 1423
Rs. 135
RC - 5204- Pen Stand - 1424
Rs. 160
RC - 2016- Pen Stand - 1426
Rs. 110
RC - 2008 With Watch- Pen Stand - 1427
Rs. 150
RC - 1003- Pen Stand - 1425
Rs. 280
RC - 7004 - Pen Stand - 1428
Rs. 150
RC - Wooden Pen Stand - A1428
Rs. 125
RC - PLT 2009 - Fish Design with Watch Pen Stand - 1429
Rs. 350
RC - PLT 2029 - Fish Design Pen Stand - 1430
Rs. 250
RC - PLT 2027 - Pen Stand - 1434
Rs. 250
RC - PLT 2023 - Rupees Pen Stand - 1435
Rs. 250
RC - PLT 2006 Antic Colour - Pen Stand - 1432
Rs. 380
RC - PAP 1106 - Ashokstambh - 1439
Rs. 110
RC - PAP 1102 - Ashokstambh - 1436
Rs. 290
RC - PLT 2006 - Pen Stand - 1431
Rs. 350
RC - PLT 2030- Ashoka Pen Stand - 1433
Rs. 250
RC - PAP 1106 - Ashokstambh - 1438
Rs. 180
RC - Digital Pen Stand Square - 1440
Rs. 180
RC - Rotate Pen Stand Jari - 1441
Rs. 250
RC - Pen Stand Jari - 1442
Rs. 280
RC - Hub with Pen Stand - 1445
Rs. 220
RC - Plastic Pen Stand Square - 1444
Rs. 60
RC - Pen Stand Jari - 1443
Rs. 280
RC - Wooden Rotate Pen Stand - 1446
Rs. 250
RC - Wooden Pen Stand - 1447
Rs. 350
RC - Wooden Rotate with Clock Pen Stand - 1448
Rs. 300
RC - Wooden Pen Stand - 1449
Rs. 350
RC - Round Pen Stand Jari - 1450
Rs. 60
RC - Round Pen Stand - 1451
Rs. 250
RC - BTC 439 Pen Stand - 1452
Rs. 550
RC - BTC 4230 Pen Stand - 1453
Rs. 260
RC - BTC 4340 Pen Stand - 1454
Rs. 260
RC - BTC 4343 Pen Stand - 1455
Rs. 450
RC - M523 BTC4225 Pen Stand - 1456
Rs. 170 
RC - M633 Pen Stand - 1457
Rs. 260
RC - M581 Pen Stand - 1458
Rs. 350
RC - M492 Pen Stand - 1459
Rs. 250
RC - BTC 4299 Pen Stand - 1461
Rs. 350
RC -M648 Pen Stand - 1460
Rs. 300
RC - BTC 4231 Pen Stand - 1462
Rs. 400
RC - M542 Pen Stand - 1463
Rs. 325
RC - M540 Pen Stand - 1464
Rs. 275 
RC - BTC 4269 Pen Stand - 1465
Rs. 450
RC - M 512, BTC 320- Pen Stand - 1466
Rs. 200
RC - M311 Pen Stand - 1467
Rs. 380
RC - M 266 Pen Stand - 1468
Rs. 650 
RC - Pen Stand - 1469
Rs. 150
RC - Calender Pen Stand (Metal) - 1470
Rs. 350
RC - Submarine Pen Stand -1471
Rs. 435
RC - Black Certicate Folder (Landscape) - 1501
Rs. 210
RC - Brown Certicate Folder (Landscape)- 1503
Rs. 210
RC - Black Certicate Folder (Portrait) - 1502
Rs. 210
RC - Brown Certicate Folder (Portrait)- 1504
Rs. 210
RC - Jute File - 1505
Rs. 220
RC - Jute File - 1506
Rs. 235
RC - Jute File - 1507
Rs. 260
RC - Jute File - 1508
Rs. 275
RC - Jute Natural Bag - 1509
Rs. 275
RC - Jute White File - 1510
Rs. 275
RC - Pendrive - 1601
Rs. Call
RC - Pendrive - 1602
Rs. Call
RC - Pendrive - 1603
Rs. Call
RC - Pendrive - 1604
Rs. Call
RC - Pendrive - 1605
Rs. Call
RC - Pendrive - 1606
Rs. Call
RC - Pendrive - 1609
Rs. Call
RC - Pendrive - 1608
Rs. Call
RC - Pendrive - 1607
Rs. Call
RC - Pendrive - 1610
Rs. Call
RC - Pendrive - 1611
Rs. Call
RC - Pendrive - 1612
Rs. Call
RC - Pendrive - 1613
Rs. Call
RC - Pendrive - 1614
Rs. Call
RC - Pendrive - 1615
Rs. Call
RC - Pendrive - 1616
Rs. Call
RC - Pendrive - 1617
Rs. Call
RC - Pendrive Box - 1618
Rs. Call
RC - Pendrive Box - 1619
Rs. Call
RC - Pendrive Box - 1620
Rs. Call
RC - Pendrive - 1621
Rs. Call
RC - Pendrive - 1622
Rs. Call
RC - Pendrive - 1623
Rs. Call
RC - Pendrive - 1624
Rs. Call
RC - Pendrive - 1625
Rs. Call
RC - Pendrive - 1626
Rs. Call
RC - Pendrive - 1627
Rs. Call
RC - Pendrive - 1628
Rs. Call
RC - Pendrive - 1629
Rs. Call
RC - Pendrive - 1630
Rs. Call
RC - Pendrive - 1631
Rs. Call
RC - Pendrive - 1632
Rs. Call
RC - Pendrive - 1633
Rs. Call
RC - Pendrive - 1634
Rs. Call
RC - Pendrive - 1635
Rs. Call
RC - Pendrive - 1636
Rs. Call
RC - Pendrive - 1637
Rs. Call
RC - Pendrive - 1638
Rs. Call
RC - Pendrive - 1639
Rs. Call
RC - 10000MH Powerbank - 1640
Rs. 400
RC - 10000MH Powerbank - 1641
Rs. 400
RC - 5000MH Powerbank - 1643
Rs. 250
RC - 5000MH Powerbank - 1642
Rs. 250
RC - Mobile Stand with Card Holder Black - 1701
Rs. 55
RC - Mobile Stand without Card Holder Black - 1702
Rs. 45
RC - Mobile Stand Hola - 1703
Rs. 40
RC - Mobile Stand with Card Holder Silver - 1704
Rs. 75
RC - Mobile Stand without Card Holder Silver - 1705
Rs. 55
RC - Mobile Stand Golden - 1706
Rs. 180
RC - Mobile Stand with Pen Stand Black - 1707
Rs. 85
RC - Mobile Stand with Pen Stand Silver - 1708
Rs. 95
RC - Rotate Metal Mobile Stand - 1709
Rs. 55
RC - Rotate Plastic Mobile Stand Black - 1710
Rs. 45
RC - Foldable Metal Mobile Stand - 1712
Rs. 75
RC - Foldable Plastic Mobile Stand - 1713
Rs. 60
RC - Foldable & Adjustable Mobile Stand Black - 1714
Rs. 40
RC - Foldable & Adjustable Mobile Stand White - 1715
Rs. 40
RC - Rotate Plastic Mobile Stand White - 1711
Rs. 45
RC - Wooden Mobile Stand - 1716
Rs. 60
RC - Paper Holder Mobile Stand - 1717
Rs. 85
RC - Mobile Stand with Card Holder & Back Pen Stand - 1718
Rs. 120
RC - 90 Degree Mobile Stand - 1719
Rs. 150
RC - Mobile Stand with Paper Holder & Pen Stand - 1720
Rs. 150
RC - Mobile Stand without Paper Holder with Pen Stand - 1721
Rs. 125
RC - Mobile Stand with Tea Coaster - 1722
Rs. 110
RC - Temperature Bottle - 1801
Rs. 120
RC - Temperature Bottle - 1802
Rs. 120
RC - Temperature Bottle - 1803
Rs. 120
RC - Temperature Bottle - 1804
Rs. 110
RC - Rubber Coated Bottle - 1808
Rs. 220
RC - Rubber Coated Bottle - 1807
Rs. 220
RC - Transperant Cup Bottle - 1806
Rs. 200
RC - Transperant Cup Bottle - 1805
Rs. 200
RC - Rubber Coated Bottle - 1809
Rs. 220
RC - Rubber Coated Bottle - 1810
Rs. 220
RC - Rope Bottle - 1811
Rs. 160
RC - Rope Bottle - 1812
Rs. 160
RC - Sport Bottle (1Ltr) - 1813
Rs. 110
RC - Cow Bottle (1Ltr) - 1814
Rs. 110
RC - Damroo Bottle (1Ltr) - 1815
Rs. 110
RC - Cola Bottle (1Ltr) - 1816
Rs. 110
RC - Straight Bottle (1Ltr) - 1818
Rs. 110
RC - Handle Straight Bottle (750ml) - 1819
Rs. 100
RC - Handle Straight Bottle (750ml) - 1820
Rs. 125
RC - Warm Handle Bottle (500ml)- 1821
Rs. 200
RC - Warm Bottle (500ml) - 1822
Rs. 220
RC - Borosil Shape Bottle (800ml) - 1823
Rs. 380
RC - Borosil Shape Bottle (600ml) - 1824
Rs. 340
"""

def parse_and_update():
    lines = raw_data.strip().split('\n')
    parsed_items = {}
    current_product = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        if "Rs." in line or "rs." in line.lower():
            parts = re.split(r'Rs\.|rs\.', line, flags=re.IGNORECASE)
            if len(parts) > 1 and parts[0].strip():
                name = parts[0].strip()
                price_str = parts[1].strip()
                current_product = name
            else:
                price_str = parts[-1].strip()
            
            if "Call" in price_str or "call" in price_str.lower():
                parsed_items[current_product] = "Call"
            else:
                price_match = re.search(r'([0-9.]+)', price_str)
                if price_match:
                    parsed_items[current_product] = float(price_match.group(1))
            current_product = ""
        else:
            if current_product: current_product += " " + line
            else: current_product = line
            
    # Normalize DB items
    all_products = list(Product.objects.all())
    
    print("## Batch 6 Price Update (+60%)\n")
    print("| Product | Old Base Price | New Price (+60%) |")
    print("|---|---|---|")
    
    missing = []
    
    for name, price in parsed_items.items():
        if not name: continue
        
        name_clean = name.replace("also set in colors", "").replace("-", " ").lower().split()
        
        # We need a robust matcher: Check if the specific numbers in `name` exist in `db_name`
        # And check if the words match reasonably well
        best_match = None
        
        code_match = re.search(r'([0-9]{3,4})', name)
        target_code = code_match.group(1) if code_match else None
        
        for p in all_products:
            p_name_clean = p.name.replace("-", " ").lower()
            
            if target_code:
                # If target code doesn't exist as a separate word, skip
                # e.g., target_code=1051, p_name_clean="RC 11051" -> split() avoids this
                if target_code not in p_name_clean.split():
                    continue
                    
            # If target code matched (or doesn't exist), ensure the string matches reasonably
            # e.g., name_clean = ["1051"] -> matched
            # name_clean = ["rc", "cup", "985"] -> p_name_clean must have "cup"
            
            # Simple heuristic: if all alphabetic words in name_clean exist in p_name_clean
            alpha_words = [w for w in name_clean if w.isalpha()]
            match = True
            for aw in alpha_words:
                if aw not in p_name_clean:
                    match = False
                    break
            
            if match:
                best_match = p
                break
                
        if best_match:
            if price == "Call":
                # Do nothing, just print
                print(f"| {best_match.name} | Rs. Call | **Rs. Call (No Change)** |")
            else:
                new_price = round(price * 1.60)
                best_match.price = Decimal(str(new_price))
                best_match.save(update_fields=['price'])
                print(f"| {best_match.name} | Rs. {price} | **Rs. {new_price}** |")
        else:
            missing.append(name)
            
    if missing:
        print("\n**Warning: The following products were not found:**")
        for m in missing:
            print(f"- {m}")
            
if __name__ == '__main__':
    parse_and_update()
