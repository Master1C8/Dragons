#!/usr/bin/env python3
"""Restore a historical .NET metadata file from a fresh SDK build."""

import argparse
import hashlib
import re
from pathlib import Path

from restore_probe_assets import read_receipt


ATTRIBUTE = re.compile(
    rb'^(\[assembly: System\.Reflection\.(Assembly\w+Attribute)\(")'
    rb'([^"\r\n]*)("\)\])$',
    re.MULTILINE,
)


def restore(receipt, build_dir, historical_path, output):
    record = receipt["outputs"][historical_path]
    template = receipt["templates"][record["template"]]
    source = (build_dir / template["path"]).read_bytes()
    if hashlib.sha256(source).hexdigest() != template["sha256"]:
        raise ValueError("SDK output differs from the recorded template")

    if "attributes" in record:
        attributes = record["attributes"]
        names = {match[2].decode("ascii") for match in ATTRIBUTE.finditer(source)}
        if names != attributes.keys():
            raise ValueError("Recorded assembly attributes differ from the template")

        def replace(match):
            value = attributes[match[2].decode("ascii")].encode("utf-8")
            return match[1] + value + match[4]

        source = ATTRIBUTE.sub(replace, source)

    if "assemblyName" in record:
        name = record["assemblyName"].encode("utf-8")
        source = source.replace(b'"scan/1.0.0"', b'"' + name + b'/1.0.0"')
        source = source.replace(b'"scan.dll"', b'"' + name + b'.dll"')

    if len(source) != record["bytes"] or hashlib.sha256(source).hexdigest() != record["sha256"]:
        raise ValueError("Restored metadata differs from the historical file")
    with output.open("xb") as stream:
        stream.write(source)
    output.chmod(int(record["mode"], 8))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("build_dir", type=Path)
    parser.add_argument("historical_path")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    restore(receipt, args.build_dir, args.historical_path, args.output)


if __name__ == "__main__":
    main()
