import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

thread_table = pd.read_csv('threads.txt', sep='\s+', header=None)
drill_table = pd.read_csv('drills.txt', sep='\s+', header=None)

# Frame format: [Name, Size, TPI, Major, Pitch 2B, Pitch 3B, Minor, Aluminum Drill, Steel Drill]
final_table = pd.DataFrame()
final_table['Name'] = thread_table[0] + thread_table[1].str.replace(r"\(.*?\)", "", regex=True)
final_table['Size'] = thread_table[1].str.extract('.*\((.*)\).*')
final_table['TPI'] = final_table['Name'].str.split('-').str[-1]
final_table['Major'] = thread_table[14].astype(str)
final_table['Pitch 2B'] = thread_table[6].astype(str)
final_table['Pitch 3B'] = thread_table[5].astype(str)
final_table['Minor'] = round((thread_table[13] + thread_table[12])/2, 4)
final_table['Minor'] = final_table['Minor'].astype(str)
final_table['Aluminum Drill'] = drill_table[3].str.extract('.*\((.*)\).*')
final_table['Steel Drill'] = drill_table[5].str.extract('.*\((.*)\).*')
final_table = final_table.reset_index()

root = ET.Element('ThreadType') 
ET.SubElement(root, 'Name').text = 'Imperial STI Threads'
ET.SubElement(root, 'CustomName').text = 'Imperial STI Threads'
ET.SubElement(root, 'Unit').text = 'in'
ET.SubElement(root, 'Angle').text = '60'
ET.SubElement(root, 'SortOrder').text = '1'

for index, row in final_table.iterrows():

    # Only create a new size if none exists
    list = root.findall('ThreadSize[Size="{}"]'.format(row['Size']))
    for size in list:
        thread = size
    if not list:
        thread = ET.SubElement(root, 'ThreadSize')
        ET.SubElement(thread, 'Size').text = row['Size']

    designation = ET.Element('Designation')
    ET.SubElement(designation, 'ThreadDesignation').text = row['Name']
    ET.SubElement(designation, 'CTD').text = row['Name']
    ET.SubElement(designation, 'TPI').text = row['TPI']

    thread_alu_2B = ET.SubElement(designation, 'Thread')
    ET.SubElement(thread_alu_2B, 'Gender').text = 'internal'
    ET.SubElement(thread_alu_2B, 'Class').text = 'Aluminum 2B'
    ET.SubElement(thread_alu_2B, 'MajorDia').text = row['Major']
    ET.SubElement(thread_alu_2B, 'PitchDia').text = row['Pitch 2B']
    ET.SubElement(thread_alu_2B, 'MinorDia').text = row['Minor']
    ET.SubElement(thread_alu_2B, 'TapDrill').text = row['Aluminum Drill']

    thread_alu_3B = ET.SubElement(designation, 'Thread')
    ET.SubElement(thread_alu_3B, 'Gender').text = 'internal'
    ET.SubElement(thread_alu_3B, 'Class').text = 'Aluminum 3B'
    ET.SubElement(thread_alu_3B, 'MajorDia').text = row['Major']
    ET.SubElement(thread_alu_3B, 'PitchDia').text = row['Pitch 3B']
    ET.SubElement(thread_alu_3B, 'MinorDia').text = row['Minor']
    ET.SubElement(thread_alu_3B, 'TapDrill').text = row['Aluminum Drill']

    thread_steel_2B = ET.SubElement(designation, 'Thread')
    ET.SubElement(thread_steel_2B, 'Gender').text = 'internal'
    ET.SubElement(thread_steel_2B, 'Class').text = 'Steel, Plastic 2B'
    ET.SubElement(thread_steel_2B, 'MajorDia').text = row['Major']
    ET.SubElement(thread_steel_2B, 'PitchDia').text = row['Pitch 2B']
    ET.SubElement(thread_steel_2B, 'MinorDia').text = row['Minor']
    ET.SubElement(thread_steel_2B, 'TapDrill').text = row['Steel Drill']

    thread_steel_3B = ET.SubElement(designation, 'Thread')
    ET.SubElement(thread_steel_3B, 'Gender').text = 'internal'
    ET.SubElement(thread_steel_3B, 'Class').text = 'Steel, Plastic 3B'
    ET.SubElement(thread_steel_3B, 'MajorDia').text = row['Major']
    ET.SubElement(thread_steel_3B, 'PitchDia').text = row['Pitch 3B']
    ET.SubElement(thread_steel_3B, 'MinorDia').text = row['Minor']
    ET.SubElement(thread_steel_3B, 'TapDrill').text = row['Steel Drill']

    thread.append(designation)

tree = ET.ElementTree(root)

pretty = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="\t")
with open('../ImperialSTI.xml', "w") as f: 
    f.write(pretty)  
