import xmltodict
import json

def parse_xml_to_json(xml_text: str) -> dict:
    """
    Converts XML text to a python dictionary
    """
    try:
        return xmltodict.parse(xml_text)
    except Exception as e:
        raise ValueError(f"Error parsing XML: {e}")

## def save_json(data: dict, filepath: str):
    """
    Save dictionary to json file
    """
   ## with open(filepath, "w") as f:
   ##     json.dump(data, f, indent=2)


if __name__ == "__main__":
    with open("sample.xml", "r") as f:
        xml_data = f.read()
    parsed = parse_xml_to_json(xml_data)
    save_json(parsed, "cleaned_sample.json")
