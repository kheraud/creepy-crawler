#!/usr/bin/env python3

def write_md(target_file, content):
    with open(target_file, "w") as file:
        file.write(content)
