import os
import django
import re
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

raw_data = """
RC - Aluminium Bottle (750ml) - 1825
Rs. 90
RC - Aluminium Bottle (750ml) - 1826
Rs. 90
RC - Sport Bottle (750ml) - 1831
Rs. 135
RC - Sport Bottle (750ml) - 1832
Rs. 135
RC - Cow Handle Bottle (750ml) - 1833
Rs. 135
RC - Cow Handle Bottle (750ml) - 1834
Rs. 145
RC - Cola Bottle (500ml) - 1835
Rs. 180
RC - Cola Steel Bottle (1Ltr) - 1837
Rs. 280
RC - Pouch Bottle (500ml) - 1840
Rs. 280
RC - Motivation Bottle (900ml) - 1829
Rs. 110
RC - Sport Bottle (750ml) - 1830
Rs. 110
RC - Aluminium Bottle (750ml) - 1827
Rs. 90
RC - Aluminium Bottle (750ml) - 1828
Rs. 90
RC - Cola Bottle (500ml) - 1836
Rs. 180
RC - Cola Steel Bottle (750Ltr) - 1838
Rs. 250
RC - Cola Steel Bottle (500Ltr) - 1839
Rs. 165
RC - Bamboo Bottle (450ml) - 1841
Rs. 250
RC - Wooden Cap Handle Bottle (500ml) - 1842
Rs. 250
RC - Crock Bottle (500ml) - 1843
Rs. 380
RC - Cup Bottle (500ml) - 1844
Rs. 180
RC - Morning Bottle (1Ltr) - 1845
Rs. 260
RC - Morning Bottle (1Ltr) - 1846
Rs. 260
RC - Glass Bottle with Sleeve (500ml) - 1847
Rs. 135
RC - Without Temperature Bottle (500ml) - 1849
Rs. 125
RC - Without Temperature Bottle (500ml) - 1850
Rs. 125
RC - Without Temperature Bottle (500ml) - 1851
Rs. 125
RC - Without Temperature Bottle (500ml) - 1852
Rs. 125
RC - Steel Bottle - 1848
Rs. 120
RC - Ring Bottle (500ml) - 1853
Rs. 260
RC - Sport Rubber Bottle (500ml) - 1856
Rs. 220
RC - Vaccum Handle Bottle(500ml) - 1860
Rs. 300
RC - Vaccum Handle Bottle(500ml) - 1861
Rs. 300
RC - Borosil Glass Bottle(1Ltr) - 1858
Rs. 280
RC - Rubber Coated Wooden Cap Bottle - 1862
Rs. 260
RC - Ring Bottle (500ml) - 1854
Rs. 260
RC - Ring Bottle (500ml) - 1855
Rs. 260
RC - Sport Rubber Bottle (500ml) - 1857
Rs. 220
RC - Glass Bottle(1Ltr) - 1859
Rs. 180
RC - Rubber Coated Wooden Cap Bottle - 1863
Rs. 260
RC Vaccum Flask Set (500ml) - 1865
Rs. 170
RC Vaccum Flask Set (500ml) - 1866
Rs. 170
RC Vaccum Flask Set (500ml) - 1867
Rs. 170
RC Vaccum Flask Set (500ml) - 1868
Rs. 170
RC Vaccum Flask Set (500ml) - 1869
Rs. 170
RC Vaccum Flask Set (500ml) - 1870
Rs. 170
RC Heavy Flask Set (500ml) - 1871
Rs. 280
RC Heavy Flask Set (500ml) - 1872
Rs. 280
RC - Havy Temperature Bottle - 1875
Rs. 250
RC - Dual colour Bottle - 1876
Rs. 140
RC - Printed Cola Bottle - 1877
Rs. 210
RC - Multi Colour Cola Bottle - 1878
Rs. 250
RC - Sports Print Bottle - 1879
Rs. 115
RC - Empire Bottle - 1881
Rs. 135
RC - Rabit Temperature Bottle - 1880
Rs. 140
RC - Gripper Glass Green Tea Bottle - 1883
Rs. 350
RC - Gripper Glass Bottle - 1884
Rs. 260
RC - Hello Master Bottle - 1885
Rs. 60
RC - Nice Bottle - 1886
Rs. 34
RC - Cute Rabbit Bottle - 1887
Rs. 50
RC - Glass Sports Bottle - 1888
Rs. 260
RC - Glass 500ml Bottle - 1889
Rs. 150
RC - Glass 1ltr Bottle - 1890
Rs. 180
RC - My Bottle 500ml - 1891
Rs. 150
RC -Glass Bottle With Wooden Cap - 1892
Rs. 280
RC - Youth Sports Bottle - 1893
Rs. 260
RC - Extreme Tumbler Bottle - 1894
Rs. 240
RC - Leisure 500ml Bottle - 1895
Rs. 325
RC - Silver Ring 800ml Bottle - 1897
Rs. 220
RC - Leisure 1ltr Bottle - 1896
Rs. 350
RC - Silver Ring 1ltr Bottle - 1898
Rs. 240
RC - 400ml Transparent Cap Bottle - 1900
Rs. 220
RC - 400ml Temperature Bottle - 1901
Rs. 250
RC - Mountain Bottle - 1899
Rs. 230
RC - Aluminium Colourful Cap Bottle - 1909
Rs. 120
RC - Thermos Bottle - 1910
Rs. 160
RC - Slim Long Bottle - 1911
Rs. 150
RC - Golden Handle Bottle - 1908
Rs. 200
RC - Sport (1ltr) Bottle - 1907
Rs. 310
RC - Sport (800ltr) Bottle - 1906
Rs. 290
RC - Colourful Damroo Bottle - 1903
Rs. 130
RC - 003 Bottle - 1904
Rs. 180
RC - Hanging Bottle - 1905
Rs. 160
RC - Sport Sipper with Straw & Silicone Grip Bottle - 1912
Rs. 350
RC - Sport Sipper Bottle - 1914
Rs. 260
RC - Bluemen Big Bottle - 1915
Rs. 100
RC - Jony Bottle - 1917
Rs. 160
RC - Straight Vaccum Bottle - 1918
Rs. 180
RC - Cartoon Bottle - 1919
Rs. 160
RC - Thick Bottle - 1920
Rs. 180 
RC - 2200ml Bottle - 1921
Rs. 500
RC - Bluemen Small Bottle - 191
RC - Steel Glass without Clip - 1922
Rs. 110
RC - Steel Glass without Clip - 1923
Rs. 100
RC - Sipper Bottle - 1926
Rs. 400
RC - 2 in 1 Bottle with Glass - 1927
Rs. 110
RC - 1200ml Bottle - 1925
Rs. 400
RC - Ecofriendly Bottle - 1924
Rs. 200
RC - Colour Copper Bottle - 1928
Rs. 480
RC - Spot Copper Bottle - 1929
Rs. 425
RC - Copper Printed Pot - 1931
Rs. 650
RC - Printed Copper Bottle - 1932
Rs. 430
RC - Copper Glass - 1933
Rs. 120
RC - Blue Copper Set - 1934
Rs. 975
RC - Copper Set - 1935
Rs. 690
RC - Printed Copper Set - 1936
Rs. 750
RC - Colour Copper Set - 1937
Rs. 775
RC - Q7 Copper Bottle - 1930
Rs. 380
RC - 2 in 1 Sport Bottle - 1945
Rs. 160
RC - Fuye Bottle - 1943
Rs. 200
RC - Thorn Shaped Bottle - 1938
Rs. 75
RC - Lighter Shape Water Bottle - 1941
Rs. 180
RC - School Bottle - 1939
Rs. 220
RC - Teddy Bottle - 1940
Rs. 180
RC - Plastic Bottle - 1946
Rs. 180
RC - Flipper Bottle - 1948
Rs. 120
RC - Spray Bottle - 1950
Rs. 120
RC - 3 in 1 Bottle - 1951
Rs. 180
RC - Motivational Bottle - 1952
Rs. 110
RC - Flexible Silicon Bottle - 1953
Rs. 140
RC - Football Bottle - 1954
Rs. 160
RC - Bottle - A1954
Rs. 250
RC Slim Touch Pen - 1955
Rs. 11
RC Slim Touch Pen - 1956
Rs. 12
RC Slim Touch Pen - 1957
Rs.12
RC Slim Touch Pen - 1958
Rs. 18
RC Slim Touch Pen - 1959
Rs. 14
RC Slim Touch Pen - 1960
Rs. 16
RC Touch Pen Three Ring - 1961
Rs. 25
RC Touch Pen Three Ring - 1962
Rs. 28
RC Bamboo Touch Pen - 1963
Rs. 15
RC Crock Pen - 1964
Rs. 30 
RC 3 Hole Pen - 1965
Rs. 24
RC Touch Pen Single ring - 1966
Rs. 22
RC Bamboo Pen - 1967
Rs. 13
RC Slim Cross Pen - 1968
Rs. 17
RC Big Clip Pen - 1969
Rs. 40
RC Big Top Pen Mettalic Black - 1970
Rs. 25 
RC Big TOP Pen Golden Clip - 1971
Rs. 27 
RC Big Top Pen Silver Clip - 1972
Rs. 25
RC Parker Pen - 1973
Rs. 28 
RC Structure Parker Pen - 1974
Rs. 35
RC Parker Roller Pen - 1975
Rs. 32
RC U-Clip Mettalic Parker Pen - 1976
Rs. 45
RC U-Clip Parker Rose gold Pen - 1977
Rs. 45 
RC Small Top Pen - 1978
Rs. 25
RC U-Clip Pen - 1979
Rs. 25
RC TIE Shape Clip Pen - 1980
Rs. 55 
RC 12 Pen - 1982
Rs. 14
RC TIE Shape Clip Pen - 1981
Rs. 65
RC Big Top 2 Ring Pen - 1990
Rs. 35
RC Design Pen - 1991
Rs. 50
RC Big Top single Ring Golden Pen - 1992
Rs. 55
RC Leather Finishing Pen - 1993
Rs. 90 
RC Plane TOP Pen - 1994
Rs. 28 
RC Colourful Touch Pen - 1995
Rs. 28
RC Doctor Golden Pen - 1997
Rs. 55
RC Advocate Pen - 1998
Rs. 90
RC CA Pen - 1999
Rs. 90
RC Slim Touch Pen - 1.985
Rs200
RC Tik Tik Pen - 1983
Rs. 45 
RC tik Tik Rubber Coated Pen - 1986
Rs. 20
RC Doctor Silver Pen - 1996
Rs. 35
RC Tik Tik Pen - 1984
Rs. 35
RC Coffee 2 in 1 Pen-1989
Rs.110
RC tik Tik Rubber Coated Pen - 1986
Rs. 20
RC tik Tik Rubber Coated Pen - 1987
Rs. 15
RC Metallic Balck Roller Pen - 1988
Rs. 25
RC Long Clip Pen - 2002
Rs. 28
RC Tik Tik colourful Pen - 2003
Rs. 32
RC Speed Pen - 2002
Rs. 30
RC Slim 3 Ring Pen - 2005
Rs. 25
RC Eco Friendly Pen - 2006
Rs . 8
RC Retractable Pen - 2003
Rs. 20
RC Golden Top Pen - 2004
Rs. 35
RC Leather Sewing Pen - 2005
Rs. 65
RC Round Top Pen - 2006
Rs. 27
RC Parker Silver Clip Pen - 2007
Rs. 25
RC Slender Gold Pen - 2008
Rs. 30
RC Diamond Golden Pen - 2009
Rs. 60
RC Shiny Gold Pen - 2010
Rs. 25
RC Shiny Black Pen - 2011
Rs. 25
RC Uper Thick Body Gold Clip Pen - 2012
Rs. 200
RC Handicraft Design Gold Pen - 2013
Rs. 60
RC Handicraft Design silver Pen - 2014
Rs. 60
RC Speed Pen Golden Clip - 2015
Rs. 30
RC Black Diamond Pen - 2016
Rs. 45
RC Jari Pen Blue- 2017
Rs. 45
RC Jari Pen Black - 2018
Rs. 38
RC Diamond Lower Pen - 2019
Rs. 60
RC Diamond Uper Pen - 2025
Rs. 30
RC Marble Design Pen - 2026
Rs. 200
RC Lining Pattern Pen - 2027
Rs. 38
RC Shine Gray Body magnetic cap Pen - 2028
Rs. 140
RC Golden Gripper Pen - 2029
Rs. 40
RC Crosi Pen - 2030
Rs. 80
RC Crown Pen - 2031
Rs. 75
RC Mini Roller Pen - 2032
Rs. 60
RC Magnetic Closure Cap Pen - 2033
Rs. 105
RC Tik Tik Side Cut Clip Pen - 2034
Rs. 20
RC Goden Ring Mini Pen - 2035
Rs. 130
RC Coffee Pen - 2036
Rs. 50
RC Thick Plastic Pen - 2037
Rs. 3.50
RC Calendar Pen - 2038
Rs. 20
RC Mobile Stand Pen Cap - 2039
Rs. 8
RC Mobile Stand Pen Rotate - 2040
Rs. 8
RC Tik Tik Curve Pen - 2041
Rs. 3.50
RC LED Pen - 2042
Rs. 25
RC Plastic Tik Tik Pen - 2043
Rs. 3.50
RC Engineering Pen - 2044
Rs. 30
RC Screwdriver Pen - 2045
Rs. 25 
RC Laser Pen - 2046
Rs. 80
RC Deskstick Pen - 2047
Rs. 35
RC Multifunctional Pen - 2048
Rs. 55
RC Bag BPK-SKSS - 3001
Rs. 450
RC Bag BPK-SAAS - 3002
Rs. 450
RC German Bagpack - 3003
Rs. 650
RC Bag BPK-SMSP - 3004
Rs. 550
RC Bag BPK-SMSP - 3005
Rs. 550
RC Bag BPK-SMSP - 3006
Rs. 550
RC Bag BPK-SRRRI - 3007
Rs. 300
RC Bag BPK-SMRA - 3008
Rs. 380 
RC Bag BPK-WWIW - 3009
Rs. 900
"""

def parse_and_update():
    lines = raw_data.strip().split('\n')
    parsed_items = {}
    current_product = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        if "Rs." in line or "Rs" in line or "rs." in line.lower() or "rs " in line.lower():
            # some have 'Rs200' or 'Rs. 200' or 'Rs . 8'
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
            if price == "Call":
                out_table.append(f"| {best_match.name} | Rs. Call | **Rs. Call (No Change)** |")
            else:
                new_price = round(price * 1.60)
                best_match.price = Decimal(str(new_price))
                best_match.save(update_fields=['price'])
                out_table.append(f"| {best_match.name} | Rs. {price} | **Rs. {new_price}** |")
        else:
            missing.append(name)
            
    with open(r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\batch7_prices.md', 'w', encoding='utf-8') as f:
        f.write("## Batch 7 Price Update (+60%)\n\n")
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
