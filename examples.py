#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Examples of usage.
"""

from html import *
import sys

# A static document.
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
print ""

# A dynamic document: a table with many rows.
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
print ""
