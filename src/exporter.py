import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from datetime import date, datetime
from decimal import Decimal
from abc import ABC, abstractmethod


class ExporterInterface(ABC):
    @abstractmethod
    def export(self, data: Dict[str, List[Dict]]) -> str:
        pass


class JSONExporter(ExporterInterface):
    @staticmethod
    def _json_serializer(obj: Any) -> Any:
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return str(obj)

    def export(self, data: Dict[str, List[Dict]]) -> str:
        return json.dumps(data, indent=2, default=self._json_serializer)


class XMLExporter(ExporterInterface):
    def export(self, data: Dict[str, List[Dict]]) -> str:
        root = ET.Element("results")

        for query_name, items in data.items():
            section = ET.SubElement(root, query_name)
            for item in items:
                row = ET.SubElement(section, "row")
                for field_name, value in item.items():
                    if value is not None:
                        field = ET.SubElement(row, field_name)
                        if isinstance(value, (float, Decimal)):
                            field.text = str(round(float(value), 2))
                        else:
                            field.text = str(value)

        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode")


class ExporterFactory:
    _exporters = {
        "json": JSONExporter,
        "xml": XMLExporter,
    }

    @staticmethod
    def get_exporter(format_type: str) -> ExporterInterface:
        cls = ExporterFactory._exporters.get(format_type.lower())
        if cls is None:
            raise ValueError(f"Unsupported format: {format_type}. Use 'json' or 'xml'.")
        return cls()