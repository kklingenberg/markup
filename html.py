"""
Exports the main HTML5 nodes.

Nodes don't check for the correct structure of the HTML they
generate.

Node specs (if they close or not) copied from
http://www.whatwg.org/specs/web-apps/current-work/multipage/
"""

import base

# Reexport the text node.
text = base.text

doctype = text("<!doctype html>\n")

def html(*children, **attrs):
    return base.make_node()(
        doctype,
        base.make_node("html")(*children, **attrs))

head = base.make_node("head")
body = base.make_node("body")

# head nodes

meta  = base.make_node("meta", closes = False)
link  = base.make_node("link", closes = False)
style = base.make_node("style")
title = base.make_node("title")

# body-or-head nodes

script = base.make_node("script")

# body nodes

div      = base.make_node("div")
p        = base.make_node("p")
span     = base.make_node("span")
a        = base.make_node("a")
form     = base.make_node("form")
input    = base.make_node("input", closes = False)
button   = base.make_node("button")
textarea = base.make_node("textarea")
label    = base.make_node("label")
ul       = base.make_node("ul")
ol       = base.make_node("ol")
li       = base.make_node("li")
table    = base.make_node("table")
thead    = base.make_node("thead")
tbody    = base.make_node("tbody")
tr       = base.make_node("tr")
th       = base.make_node("th")
td       = base.make_node("td")
caption  = base.make_node("caption")
fieldset = base.make_node("fieldset")
img      = base.make_node("img", closes = False)
embed    = base.make_node("embed", closes = False)
object   = base.make_node("object")
iframe   = base.make_node("iframe")
video    = base.make_node("video")
audio    = base.make_node("audio")
source   = base.make_node("source", closes = False)
track    = base.make_node("track", closes = False)
