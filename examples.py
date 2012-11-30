#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Examples of usage.
"""

from html import *
import sys

# 1. A static document.
doc = html(
    head(
        title("This is a test")),
    body(
        p("This is text inside a p node."),
        p(u"This is unicode text inside a p node: áéíóú."),
        p(
            "This is text combined with ",
            a("a link", href="#"),
            " and a ",
            span("span element"))))

doc(sys.stdout.write)
print "\n-----------"

# 2. A dynamic document: a table with many rows.
def table_with_data(column_names, rows):
    header = tr(*[th(col) for col in column_names])
    body = [tr(*[td(cell) for cell in row]) for row in rows]
    return table(
        thead(header),
        tbody(*body))


t = table_with_data(
    ["hey", "yo", "wow"],
    [["a", "b", "c"],
     ["d", "e", "f"],
     ["g", "h", "i"]])

t(sys.stdout.write)
print "\n-----------"

# 3. A bootstrap button.

btbutton = with_attributes(button, **{"class": "btn", "type": "submit"})

# The type gets overwritten and the class extended.
btn_doc = btbutton("Push me", **{"type": "button", "class": "btn-primary"})

# Wrapping the keyword arguments in a dictionary is cumbersome, but
# needed since 'class' and 'type' are reserved words.

btn_doc(sys.stdout.write)
print "\n-----------"

# 4. The input node seems to replace the input keyword.

input(**{"type": "text", "name": "some-input"})(sys.stdout.write)
print "\n-----------"

# 5. Printing to a string. Since strings are immutable (I think), I
# suggest using a list and then joining everything together.

target = []

somediv = div(
    h1("The big title"),
    h2("A subtitle"),
    div(
        p("A paragraph."),
        p("And another paragraph.", style="padding-top: 10px"),
        **{
            "class": "block",
            "id"   : "block-body"
            }))

somediv(target.append)
print "".join(target)
print "-----------"

# 6. Creating a template. I suggest making a function; default
# arguments could then act as the predetermined behaviour for the
# template.

def template_base(block_a = p("This is a placeholder."),
                  block_b = p("This too is a placeholder")):
    doc = html(
        head(
            title("A template example")),
        body(
            div(block_a, id = "a-block"),
            div(block_b, id = "b-block")))
    return doc

# With the defaults.
instance1 = template_base()

instance1(sys.stdout.write)
print "\n-----------"

instance2 = template_base(
    button("Now it's a button.", **{"type": "button"}),
    void(
        "This is text inside the b block.",
        span("And a span")))

instance2(sys.stdout.write)
print "\n-----------"