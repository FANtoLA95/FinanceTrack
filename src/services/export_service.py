import os
import json
import csv
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from database.database import get_connection

def _fetch_transactions_with_relations() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            t.transactionID, t.amount, t.type, t.createdAt,
            a.accountID, a.name, a.balance,
            c.categoryID, c.name
        FROM transactions t
        LEFT JOIN accounts a ON t.accountID = a.accountID
        LEFT JOIN categories c ON t.categoryID = c.categoryID
        ORDER BY t.transactionID
    """)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        item = {
            "transactionID": row[0],
            "amount": row[1],
            "type": row[2],
            "createdAt": row[3],
            "account": {
                "accountID": row[4],
                "name": row[5],
                "balance": row[6]
            },
            "category": {
                "categoryID": row[7],
                "name": row[8]
            }
        }
        result.append(item)
    return result

def _save_json(data: list[dict], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def _save_yaml(data: list[dict], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

def _save_csv(data: list[dict], filepath: str) -> None:
    if not data:
        return
    flat_rows = []
    for item in data:
        flat_rows.append({
            "transactionID": item["transactionID"],
            "amount": item["amount"],
            "type": item["type"],
            "createdAt": item["createdAt"],
            "accountID": item["account"]["accountID"],
            "account_name": item["account"]["name"],
            "account_balance": item["account"]["balance"],
            "categoryID": item["category"]["categoryID"],
            "category_name": item["category"]["name"]
        })

    fieldnames = list(flat_rows[0].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_rows)

def _dict_to_xml(parent: ET.Element, data) -> None:
    if isinstance(data, dict):
        for key, val in data.items():
            child = ET.SubElement(parent, str(key))
            _dict_to_xml(child, val)
    elif isinstance(data, list):
        for item in data:
            child = ET.SubElement(parent, "transaction")
            _dict_to_xml(child, item)
    else:
        parent.text = str(data) if data is not None else ""

def _save_xml(data: list[dict], filepath: str) -> None:
    root = ET.Element("transactions")
    _dict_to_xml(root, data)
    
    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="    ", encoding="utf-8")
    
    with open(filepath, "wb") as f:
        f.write(pretty_xml)

def export_all_formats() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    out_dir = os.path.join(project_root, "out")
    
    os.makedirs(out_dir, exist_ok=True)
    
    data = _fetch_transactions_with_relations()
    
    _save_json(data, os.path.join(out_dir, "data.json"))
    _save_csv(data, os.path.join(out_dir, "data.csv"))
    _save_xml(data, os.path.join(out_dir, "data.xml"))
    _save_yaml(data, os.path.join(out_dir, "data.yaml"))
    
    return out_dir