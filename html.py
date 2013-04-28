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

# A void node.
void = base.make_node()

# The base html structure.

doctype = base.make_writer("<!doctype html>")

def html(*children, **attrs):
    return void(
        doctype,
        base.make_node("html")(*children, **attrs))

head = base.make_node("head")
body = base.make_node("body")

# head nodes

meta  = base.make_node("meta", closes=False)
link  = base.make_node("link", closes=False)
style = base.make_node("style")
title = base.make_node("title")

# body-or-head nodes

script = base.make_node("script")

# body nodes

div      = base.make_node("div")
h1       = base.make_node("h1")
h2       = base.make_node("h2")
h3       = base.make_node("h3")
h4       = base.make_node("h4")
h5       = base.make_node("h5")
p        = base.make_node("p")
span     = base.make_node("span")
a        = base.make_node("a")
form     = base.make_node("form")
input    = base.make_node("input", closes=False)
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
img      = base.make_node("img", closes=False)
embed    = base.make_node("embed", closes=False)
object   = base.make_node("object") # overshadows the object type
iframe   = base.make_node("iframe")
video    = base.make_node("video")
audio    = base.make_node("audio")
source   = base.make_node("source", closes=False)
track    = base.make_node("track", closes=False)
br       = base.make_node("br", closes=True, close_tag=False)
hr       = base.make_node("hr", closes=True, close_tag=False)
i        = base.make_node("i")
b        = base.make_node("b")
code     = base.make_node("code")
strong   = base.make_node("strong")
small    = base.make_node("small")

# A constructor for nodes with prefixed attributes.

def with_attributes(node, **attrs):
    """Builds a node from another with prefixed attributes.

    New attributes will replace old ones, except for the 'class'
    attribute which will be extended."""
    return base.with_attributes(
        node,
        base.union_extend("class"),
        **attrs)
