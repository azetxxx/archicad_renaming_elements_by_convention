from archicad import ACConnection
import re

# Ensure the `act` module is imported
conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types  # This line was missing
acu = conn.utilities

# Naming convention patterns
naming_conventions = {
    'Wall': re.compile(r'WALL_(\d{3})$'),
    'Door': re.compile(r'DOOR_(\d{3})$'),
    'Window': re.compile(r'WIND_(\d{3})$'),
    'Slab': re.compile(r'SLAB_(\d{3})$'),
    'Beam': re.compile(r'BEAM_(\d{3})$'),
    'Column': re.compile(r'COLU_(\d{3})$')
}

# Function to find and rename non-conforming elements
def rename_non_conforming_elements(element_type, pattern):
    elements = acc.GetElementsByType(element_type)
    elementIdPropertyId = acu.GetBuiltInPropertyId('General_ElementID')
    propertyValuesForElements = acc.GetPropertyValuesOfElements(elements, [elementIdPropertyId])

    highest_counter = -1
    non_conforming_elements = []

    # Find the highest counter and non-conforming elements
    for i in range(len(propertyValuesForElements)):
        elementId = elements[i].elementId
        propertyValue = propertyValuesForElements[i].propertyValues[0].propertyValue.value
        match = pattern.match(propertyValue)

        if match:
            highest_counter = max(highest_counter, int(match.group(1)))
        else:
            non_conforming_elements.append(elementId)

    # Rename non-conforming elements
    for elementId in non_conforming_elements:
        highest_counter += 1
        new_name = f"{pattern.pattern.split('_')[0]}_{highest_counter:03d}"
        acc.SetPropertyValuesOfElements([act.ElementPropertyValue(elementId, elementIdPropertyId, act.NormalStringPropertyValue(new_name))])

    return len(non_conforming_elements)

# Rename non-conforming elements for each type
renamed_elements_count = {}
for element_type, pattern in naming_conventions.items():
    count = rename_non_conforming_elements(element_type, pattern)
    if count > 0:
        renamed_elements_count[element_type] = count

# Print summary
if renamed_elements_count:
    print("Renamed non-conforming elements:")
    for element_type, count in renamed_elements_count.items():
        print(f"{count} {element_type} elements were renamed.")
else:
    print("All elements already conform to their naming conventions.")
