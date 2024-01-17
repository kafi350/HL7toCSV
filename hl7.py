# Description: This file contains a function that parses an HL7 file and writes the data to a CSV file.
# Author: Abdullahil Kafi
from itertools import zip_longest
from hl7apy import parser
from hl7apy.parser import parse_message
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion
import csv

segments = []

segment_final = []

hl7 = open("test.hl7", "r").read()

try:
    msg = parser.parse_message(hl7.replace('\n', '\r'), find_groups=True, validation_level=1)
except UnsupportedVersion:
    msg = parser.parse_message(hl7.replace('\n', '\r'), find_groups=True, validation_level=2)


indent = "    "
indent_seg = "    "
indent_fld = "        "



def subgroup (group, indent):
    indent = indent + "    "
    print (indent , group)
    segment_msg = []
    for group_segment in group.children:
        if isinstance(group_segment, Group):
            subgroup (group_segment)
        else:
            print(indent_seg, indent ,group_segment)
            seg = str(group_segment)
            segments.append(seg)
            for attribute in group_segment.children:
                print(indent_fld, indent ,attribute, attribute.value)
                segment_msg.append(attribute.value)
            segment_final.append(segment_msg)



def showmsg(msg):
    for segment in msg.children:

        if isinstance(segment, Segment):
            print (indent ,segment)
            seg = str(segment)
            segments.append(seg)
            segment_msg = []
            for attribute in segment.children:
                print(indent_fld, indent, attribute, attribute.value)
                segment_msg.append(attribute.value)
                print(segment_msg)
            segment_final.append(segment_msg)
            print( 'final', segment_final)


        if isinstance(segment, Group):
            for group in segment.children:
                print (indent,group)
                for group_segment in group.children:
                    if isinstance (group_segment, Group):
                        subgroup (group_segment, indent)
                    else:
                        print(indent_seg, indent ,group_segment)
                        seg = str(group_segment)
                        segments.append(seg)
                        segment_msg = []
                        for attribute in group_segment.children:
                            print(indent_fld, indent, attribute, attribute.value)
                            segment_msg.append(attribute.value)
                            print(segment_msg)
                        segment_final.append(segment_msg)
                        print('final', segment_final)

showmsg(msg)

print(segments)
s = list(map(lambda elem: elem.replace('>', ''), segments))
s = list(map(lambda elem: elem.replace('<', ''), s))
print(s)
print(segment_final)

transposed_signals = list(zip_longest(*segment_final))
with open('test.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(s)
    write.writerows(transposed_signals)