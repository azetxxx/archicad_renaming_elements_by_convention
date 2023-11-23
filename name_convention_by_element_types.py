from archicad import ACConnection
import re

# Connect to Archicad
conn = ACConnection.connect()
assert conn

acc = conn.commands
acu = conn.utilities

# Naming convention patterns
naming_conventions = {
    'Wall': re.compile(r'WALL_\d{3}$'),
    'Door': re.compile(r'DOOR_\d{3}$'),
    'Window': re.compile(r'WIND_\d{3}$'),
    'Slab': re.compile(r'SLAB_\d{3}$'),
    'Beam': re.compile(r'BEAM_\d{3}$'),
    'Column': re.compile(r'COLU_\d{3}$')
}

# Function to check elements against naming convention
def check_naming_convention(elements, element_type):
    non_conforming_elements = []
    elementIdPropertyId = acu.GetBuiltInPropertyId('General_ElementID')
    propertyValuesForElements = acc.GetPropertyValuesOfElements(elements, [elementIdPropertyId])

    for i in range(len(propertyValuesForElements)):
        elementId = elements[i].elementId
        propertyValue = propertyValuesForElements[i].propertyValues[0].propertyValue.value
        if not naming_conventions[element_type].match(propertyValue):
            non_conforming_elements.append((elementId.guid, propertyValue))

    return non_conforming_elements

# Check each element type
all_non_conforming_elements = {}
for element_type in naming_conventions.keys():
    elements = acc.GetElementsByType(element_type)
    non_conforming_elements = check_naming_convention(elements, element_type)
    if non_conforming_elements:
        all_non_conforming_elements[element_type] = non_conforming_elements

# Print non-conforming elements
if all_non_conforming_elements:
    print("Non-conforming element IDs:")
    for element_type, elements in all_non_conforming_elements.items():
        print(f"\n{element_type} Elements:")
        for elem_id, elem_name in elements:
            print(f"Element ID: {elem_id}, Name: {elem_name}")
else:
    print("All elements conform to their naming conventions.")
