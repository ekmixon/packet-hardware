from .. import utils
from lxml import etree

from .component import Component


class Memory(Component):
    @classmethod
    def list(cls, lshw):
        xpath = etree.XPath("//node[description='System Memory']/node")

        return [
            cls(lshw, memory)
            for memory in xpath(lshw)
            if "[empty]" not in utils.xml_ev(lshw, memory, "description")
        ]

    def __init__(self, lshw, element):
        Component.__init__(self, lshw, element)

        self.data = {
            "slot": utils.xml_ev(lshw, element, "slot"),
            "size": (
                str(int(utils.xml_ev(lshw, element, "size")) // 1024000000) + "GB"
            ),
            "clock": int(utils.xml_ev(lshw, element, "clock")) / 1000000
            if utils.xml_ev(lshw, element, "clock")
            else "",
            "type": utils.get_dmidecode_prop(
                "0x"
                + utils.xml_ev(lshw, element, "@handle", True).split(":", 1)[1],
                "17",
                "type",
            ),
            "asset_tag": "Unknown",
        }


        self.name = utils.xml_ev(lshw, element, "description")
        self.model = utils.xml_ev(lshw, element, "product")
        self.vendor = utils.normalize_vendor(utils.xml_ev(lshw, element, "vendor"))
        self.serial = utils.xml_ev(lshw, element, "serial")
        self.firmware_version = "N/A"
