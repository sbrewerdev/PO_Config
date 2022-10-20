import csv
import sys
import re
import json


def main():
    records = []
    with open("output.txt", "w") as o:
        with open("stock.txt") as s:
            split = "null"
            split2 = "null"
            split3 = "null"
            product_code_list = "null"
            vendor_code_list = "null"
            quantity = "null"
            base_curve = "null"
            diameter = "null"
            plus_or_minus = "null"
            mf_add_power = "null"
            cylinder = "null"
            sphere_1 = "null"
            sphere_2 = "null"
            and_instr = "N"
            norm_instr = "N"
            flag = ""
            for line in s:
                if "Open Section" in line:
                    continue
                if line.startswith(":@pw="):
                    continue
                if line.startswith(":'"):
                    continue
                if line.startswith("STK"):
                    continue
                if line.startswith("::'"):
                    continue
                if line.startswith("S"):
                    stock_or_patient = line[0]
                    po_group = line[1:3]
                    vendor = line[3:line.index(":")] 
                if "AND" in line:
                    split = line.split("AND")
                    for section in split:
                        if '3="' in section and norm_instr == "N":
                            if product_code_list != "null":
                                product_code_list = product_code_list + "*" + section[3:12].strip('"').strip()
                                #print(product_code_list)
                            if product_code_list == "null":
                                if "(" not in section:
                                    product_code_list = section[3:12].strip('"').strip()
                                if "(" in section:
                                    product_code_list = section[5:12].strip('"').strip()
                            #print(product_code_list)
                        if '5 ge' in section:
                            if quantity != "null":
                                quantity = quantity + "*" + section[6:11].strip('"').strip()
                                #print(quantity, po_group)
                            if quantity == "null":
                                quantity = section[6:11].strip('"').strip()
                        if 'mid(4,"11","1")="' in section:
                            mf_add_power = section[18:19]
                        if 'mid(4,"15","1")="' in section:
                            mf_add_power = section[18:19]
                            #print(mf_add_power)
                        if 'mid(4,"15","1") = "' in section:
                            mf_add_power = section[20:21]
                            #print(mf_add_power)
                        if 'mid(4,"6","1")="' in section:
                            plus_or_minus = section[17:18]
                            #print(plus_or_minus)
                        if 'mid(4,"6","1") = "' in section:
                            plus_or_minus = section[19:20]
                            #print(plus_or_minus)
                        if 'mid(4,"11","4")="' in section:
                            cylinder = section[18:22]
                            #print(cylinder)
                        if 'mid(4,"11","4") = "' in section:
                            cylinder = section[20:24]
                            #print(cylinder)
                        if 'mid(4,"11","5")="' in section:
                            cylinder = section[18:22]
                            #print(cylinder)
                        if 'mid(4,"1","2")="' in section:
                            base_curve = section[17:19]
                            #print(base_curve)
                        if 'mid(4,"1","6")="' in section:
                            base_curve = section[17:19]
                            diameter = section[19:22]
                            #print(base_curve, diameter)
                        if 'mid(4,"7","4") ge' in section:
                            sphere_1 = section[20:24]
                            #print(sphere_1)
                        if 'mid(4,"7","4") le' in section:
                            sphere_2 = section[20:24]
                            #print(sphere_2)
                        if "instr(" in section:
                            if "{ 3 {" in section:
                                if product_code_list != "null":
                                    product_code_list = product_code_list + section[9:section.index('",')]
                                    #print(product_code_list)
                                if product_code_list == "null":
                                    product_code_list = section[8:section.index('",')]
                                    #print(product_code_list)
                                and_instr = "Y"
                            if "{ 6 {" in section:
                                vendor_code_list = section[8:section.index('",')]
                                #if vendor_code_list != "null":
                                    #print(vendor_code_list)
                            if "{ 3 {" not in section:
                                product_code_list = "null"
                            if "{ 6 {" not in section:
                                vendor_code_list = "null"
                if " OR " in line:
                    split = line.split(" OR ")
                    for section in split:
                        if '3 ne ' in section:
                            product_code_list = section[6:].replace('"',"").strip()
                            #if product_code_list != "null":
                            #print(product_code_list)
                        if 'mid(4,"6","1") ne ' in section:
                            plus_or_minus = section[19:20]
                            #print(plus_or_minus)
                        if "3=" in section and "4 co" not in split[1]:
                            product_code_list = "*" + split[0][5:].strip('" ') + "*" + split[1][2:split[1].index(":")].strip('" ') + "*"
                        if "4 co" in split[1] and "3=" in split[0] and "3=" in split[1]:
                            split2 = split[1].split(" AND ")
                            product_code_list = "*" + split[0][5:].strip('" ') + "*" + split[1][2:10].strip('" ') + "*"
                            split3 = split2[1].split(":")
                            if "ST" in split3[0]:
                                base_curve = split3[0][6:8]
                                #print(base_curve)
                            if "136" in split3[0]:
                                diameter = split3[0][6:9]
                                #print(diameter)
                if " ne " in line and " OR " not in line and " AND " not in line:
                    if line.startswith(":3 ne "):
                        product_code_list = line[6:14].strip('"').strip()
                        #print(product_code_list, vendor, po_group)
                    if line.startswith(':mid(4,"6","1") ne "'):
                        plus_or_minus = line[20:21]
                        #print(plus_or_minus)
                    if line.startswith(':mid(4,"11","4") ne "'):
                        cylinder = line[21:25]
                        #print(cylinder)
                    if line.startswith(':mid(4,"19","1") ne "'):
                        mf_add_power = line[21:22]
                        #print(mf_add_power)
                if line.startswith(":instr") and and_instr == "N":
                    norm_instr = "Y"
                    if "{ 3 {" in line:
                        if product_code_list != "null":
                            product_code_list = product_code_list + line[9:line.index('",')]
                            #print(product_code_list)
                        if product_code_list == "null":
                            product_code_list = line[8:line.index('",')]
                        #if product_code_list != "null":
                            #print(product_code_list)
                    if "{ 6 {" in line:
                        vendor_code_list = line[8:line.index('",')]
                        #if vendor_code_list != "null":
                            #print(vendor_code_list)
                    if "{ 3 {" not in line:
                        product_code_list = "null"
                    if "{ 6 {" not in line:
                        vendor_code_list = "null"
                if line.startswith(':mid(4,"19","1")'):
                    split = line.split(":")
                    mf_add_power = split[1][20:21]
                    #print(mf_add_power)
                if line.startswith(':3=') and " AND " not in line and " OR " not in line:
                    product_code_list = line[3:12].strip('"').strip()
                    #print(product_code_list)
                if line.startswith("::end:"):
                    if "*" in product_code_list:
                        product_code_list = product_code_list.lstrip("*").rstrip("*")
                        product_code_list = product_code_list.split("*")
                        #print(product_code_list)
                        if "*" not in quantity:
                            for product_code in product_code_list:
                                records.append([{"vendor":vendor, "S|P":stock_or_patient, "PO_Group":po_group, 
                                "Product_Code":product_code, "Vendor_Code_List":vendor_code_list, "Quantity":quantity,
                                "Plus_or_Minus":plus_or_minus, "Base_Curve":base_curve, "Diameter":diameter,
                                "MF_Add_Power":mf_add_power, "Cylinder":cylinder, "Sphere_1":sphere_1,
                                "Sphere_2":sphere_2}])
                        if "*" in quantity:
                            quantity = quantity.split("*")
                            for (i,j) in zip(product_code_list, quantity):
                                records.append([{"vendor":vendor, "S|P":stock_or_patient, "PO_Group":po_group, 
                                "Product_Code":i, "Vendor_Code_List":vendor_code_list, "Quantity":j,
                                "Plus_or_Minus":plus_or_minus, "Base_Curve":base_curve, "Diameter":diameter,
                                "MF_Add_Power":mf_add_power, "Cylinder":cylinder, "Sphere_1":sphere_1,
                                "Sphere_2":sphere_2}])
                        #print(product_code_list, vendor, po_group)
                    else:
                        records.append({"vendor": vendor, "S|P": stock_or_patient, "PO_Group" :po_group, 
                        "Product_Code": product_code_list, "Vendor_Code_List": vendor_code_list, "Quantity": quantity,
                        "Plus_or_Minus": plus_or_minus, "Base_Curve": base_curve, "Diameter": diameter,
                        "MF_Add_Power": mf_add_power, "Cylinder": cylinder, "Sphere_1": sphere_1,
                        "Sphere_2": sphere_2})
                    split = "null"
                    split2 = "null"
                    split3 = "null"
                    product_code_list = "null"
                    vendor_code_list = "null"
                    quantity = "null"
                    vendor = "null"
                    stock_or_patient = "null"
                    po_group = "null"
                    base_curve = "null"
                    diameter = "null"
                    plus_or_minus = "null"
                    mf_add_power = "null"
                    cylinder = "null"
                    sphere_1 = "null"
                    sphere_2 = "null"
                    and_instr = "N"
                    norm_instr = "N"
                    flag = ""            
        o.write(json.dumps(records))
    write_import(records)

def write_import(records):
    with open("import.csv", "w", newline="") as f:
        fieldnames = ["vendor", "S|P", "PO_Group", "Product_Code",
                      "Vendor_Code_List", "Quantity", "Plus_or_Minus", "Base_Curve", 
                      "Diameter", "MF_Add_Power", "Cylinder", "Sphere_1", "Sphere_2"]
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
        for dictionary in records:
            dict_writer.writeheader()
            dict_writer.writerow(dictionary)


if __name__ == "__main__":
    main()
