import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)


def add_ids_to_svg(svg_path):
    ns = {"svg": "http://www.w3.org/2000/svg"}
    ET.register_namespace("", ns["svg"])  # Register namespace to maintain 'svg' prefix

    tree = ET.parse(svg_path)
    root = tree.getroot()

    tenants_group = root.find('.//svg:g[@id="tenants"]', namespaces=ns)
    if tenants_group is not None:
        counter = 1
        for path in tenants_group.findall(".//svg:path", namespaces=ns):
            # Add 'data-place-id' attribute with incrementing counter
            path.set("data-place-id", f"Place {counter}")
            counter += 1

    # Write changes back to the SVG file
    tree.write(svg_path)


def parse_svg(svg_path):
    ns = {"svg": "http://www.w3.org/2000/svg"}
    tree = ET.parse(svg_path)
    root = tree.getroot()
    tenants_group = root.find('.//svg:g[@id="tenants"]', namespaces=ns)
    paths = []
    if tenants_group is not None:
        counter = 0
        for path in tenants_group.findall(".//svg:path", namespaces=ns):
            paths.append({"d": path.attrib["d"], "name": f"Place {counter}"})
            counter += 1
    return paths
