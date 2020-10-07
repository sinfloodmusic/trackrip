#!/usr/bin/env python3
"""Rips all samples contained by a specified MOD music file to WAV."""

import argparse
from pathlib import Path
import string
import wave
from trackrip import ripper

def main():
    """Parses, opens and extracts samples from a tracker module file."""

    parser = argparse.ArgumentParser()
    parser.add_argument("mod_file", type=Path)

    args = parser.parse_args()

    with open(args.mod_file, "rb") as file:
        mod_file = ripper.parse_module(file)

        print("TITLE: " + mod_file.title)

        for sample in mod_file.samples:
            sample_file_name = ""
            if sample["length"] > 0:
                sample_file_name = str(sample["number"])
                sample["name"] = "".join(filter(lambda x: x in set(string.printable), sample["name"]))
                if sample["name"] != "":
                    sample_file_name += " - " + sample["name"]
                keepcharacters = (" ", ".", "_", "-")
                sample_file_name = "".join(c for c in sample_file_name if
                                           c.isalnum() or c in
                                           keepcharacters).rstrip()
                print("[Exporting Sample] " + sample_file_name)
                sample_file_name += ".wav"

                out = wave.open(sample_file_name, "wb")
                out.setnchannels(1)
                out.setsampwidth(sample["width"])
                out.setframerate(sample["rate"])

                out.writeframes(sample["data"])
                out.close()


if __name__ == "__main__":
    main()
