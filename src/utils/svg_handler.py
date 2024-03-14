import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)


class SVGHandler:
    NS = {"svg": "http://www.w3.org/2000/svg"}

    @classmethod
    def add_ids_to_svg(cls, svg_path):
        """
        Adds a unique 'data-place-id' attribute to each <path> element in the SVG.
        """
        ET.register_namespace("", cls.NS["svg"])  # Ensure proper namespace handling

        tree = ET.parse(svg_path)
        root = tree.getroot()
        tenants_group = root.find('.//svg:g[@id="tenants"]', namespaces=cls.NS)

        if tenants_group is not None:
            counter = 1
            for path in tenants_group.findall(".//svg:path", namespaces=cls.NS):
                path.set("data-place-id", f"Place {counter}")
                counter += 1

        tree.write(svg_path)
        logger.info("Added IDs to SVG paths successfully.")

    @classmethod
    def parse_svg(cls, svg_path):
        """
        Parses the SVG file to extract path data and assigns a name to each path.
        """
        tree = ET.parse(svg_path)
        root = tree.getroot()
        tenants_group = root.find('.//svg:g[@id="tenants"]', namespaces=cls.NS)
        paths = []

        if tenants_group is not None:
            counter = 1  # Starting with 1 for human-readable ID numbering
            for path in tenants_group.findall(".//svg:path", namespaces=cls.NS):
                paths.append({"d": path.attrib["d"], "name": f"Place {counter}"})
                counter += 1

        logger.info("SVG paths parsed successfully.")
        return paths
