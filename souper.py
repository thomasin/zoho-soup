#!/usr/bin/env python

from bs4 import BeautifulSoup, NavigableString
import stringcase
import re
import json


def create_cls_def(cls_name, fields):
    if len(fields) == 0:
        print(f"🤒  no fields found for {cls_name}")
        return

    print(f"🍻 {len(fields)} {cls_name} fields found")

    cls_def = f"class Zoho{cls_name}Fields(Enum):\n"
    for field in fields:
        # There are other divs like 'Show Documentation' that we dont care about
        field_name, *_ = field.find(class_="data1").contents

        # If its not a string field name, we want to ignore it.
        if not isinstance(field_name, NavigableString):
            continue

        if field_name is not None:
            field_name = field_name.strip()
            # Generate \tFIELD_NAME="fieldName"\n
            cls_def += f"\t"
            cls_def += stringcase.constcase(field_name)
            cls_def += f"=\"{field_name}\"\n"

    return cls_def


def create_resource_def(resource_name):
    print(f"🕵️‍♀️  finding {resource_name} fields...")

    resource = soup.find(id=f"{resource_name}s")
    if resource is None:
        print(f"🤒 {resource_name} not found")
        return

    field_definitions = resource.find(class_="productlist")
    # The first value is the table header
    _, *fields = field_definitions.find_all(class_="data", recursive=False)
    resource_def = create_cls_def(resource_name, fields)

    nested_resources = field_definitions.find_all(class_=re.compile("show_attributes$"), recursive=False)
    # TODO: Create class defs for the nested resources

    return resource_def


print("📥 loading html...")
with open("./html_doc.html") as doc:
    print("📖 parsing html...")
    soup = BeautifulSoup(doc, 'html.parser')

    resource_defs = list(filter(None, [
        create_resource_def("Ticket")
    ]))

    print("🍰 definitions generated:\n")
    print("\n\n".join(resource_defs))
