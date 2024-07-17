#!/usr/bin/env python3

import re
import subprocess as sp


# to convert the copyparty --help to html, run this in xfce4-terminal @ 140x43:
_ = r""""
echo; for a in '' -accounts -flags -handlers -hooks -urlform -exp -ls -dbd -pwhash -zm; do
./copyparty-sfx.py --help$a 2>/dev/null; printf '\n\n\n%0139d\n\n\n'; done  # xfce4-terminal @ 140x43
"""
# click [edit] => [select all]
# click [edit] => [copy as html]
# and then run this script


def readclip():
    cmds = [
        "xsel -ob",
        "xclip -selection CLIPBOARD -o",
        "pbpaste",
    ]
    for cmd in cmds:
        try:
            return sp.check_output(cmd.split()).decode("utf-8")
        except:
            pass


def cnv(src):
    yield '<html style="background:#222;color:#fff"><body>'
    skip_sfx = False
    in_sfx = 0
    in_salt = 0

    while True:
        ln = next(src)
        if "<font" in ln:
            if not ln.startswith("<pre>"):
                ln = "<pre>" + ln
            yield ln
            break

    for ln in src:
        ln = ln.rstrip()
        if re.search(r"^<font[^>]+>copyparty v[0-9]", ln):
            in_sfx = 3
        if in_sfx:
            in_sfx -= 1
            if not skip_sfx:
                yield ln
            continue
        if '">uuid:' in ln:
            ln = re.sub(r">uuid:[0-9a-f-]{36}<", ">autogenerated<", ln)
        if "-salt SALT" in ln:
            in_salt = 3
        if in_salt:
            in_salt -= 1
            t = ln
            ln = re.sub(r">[0-9a-zA-Z/+]{24}<", ">24-character-autogenerated<", ln)
            ln = re.sub(r">[0-9a-zA-Z/+]{40}<", ">40-character-autogenerated<", ln)
            if t != ln:
                in_salt = 0
        ln = ln.replace(">/home/ed/", ">~/")
        if ln.startswith("0" * 20):
            skip_sfx = True
        yield ln

    yield "</pre>eof</body></html>"


def main():
    src = readclip()
    src = re.split("0{100,200}", src[::-1], 1)[1][::-1]
    with open("helptext.html", "wb") as fo:
        for ln in cnv(iter(src.split("\n")[:-3])):
            fo.write(ln.encode("utf-8") + b"\r\n")


if __name__ == "__main__":
    main()
