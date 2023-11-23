from archicad import ACConnection
import re

# Connect to Archicad
conn = ACConnection.connect()
assert conn

acc = conn.commands
acu = conn.utilities

# Retrieve all elements
elements = acc.GetAllElements()

# Element ID property
elementIdPropertyId = acu.GetBuiltInPropertyId('General_ElementID')

# Check naming convention
naming_convention = re.compile(r'ELEM_\d+$')
non_conforming_elements = []

# Get property values of elements
propertyValuesForElements = acc.GetPropertyValuesOfElements(elements, [elementIdPropertyId])

# Check each element's ID
for i in range(len(propertyValuesForElements)):
    elementId = elements[i].elementId
    propertyValue = propertyValuesForElements[i].propertyValues[0].propertyValue.value
    if not naming_convention.match(propertyValue):
        non_conforming_elements.append((elementId.guid, propertyValue))

# Print non-conforming elements
if non_conforming_elements:
    print("Non-conforming element IDs:")
    for elem_id, elem_name in non_conforming_elements:
        print(f"Element ID: {elem_id}, Name: {elem_name}")
else:
    print("All elements conform to the naming convention.")
