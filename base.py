"""
Exports the constructors that will serve as foundation for everything
else.
"""

# Some useful writing functions here. A writing function is one
# capable of receiving a string and doing something useful with it.

# Typically you'd want to write to a file. So if *doc* is a document
# and *f* is a file, doc(f.write) writes the document to the file.

def w_to_void(text):
    """A writing function that does nothing."""
    pass


def w_to_print(text):
    """One that prints with the *print* command."""
    print(text)


# The lower-most constructor. Redirects text to a writing procedure.
# A writer is a higher-order function that receives a writing
# function. Writers are also refered in these documentation as
# documents, as in HTML or XML documents.
make_writer = lambda t: lambda f: f(t)


# Escape characters. http://wiki.python.org/moin/EscapingHtml
textnode_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def escape(text, table):
    """Produce entities within text."""
    return "".join(table.get(c,c) for c in text)

# A text node.
text = lambda t: make_writer(escape(t, textnode_table))


def concat_writers(*ws):
    """Creates a new writer by concatenating many of them.

    This is nothing more than a glorified function sequencer. It
    combines writers sequentially into a wrapper."""
    def writer(f):
        for w in ws:
            if isinstance(w, str) or isinstance(w, unicode):
                text(w)(f)
            else:
                w(f)
    return writer


# Markup node generation

def format_attributes(attrs):
    """Formats attributes to be inserted in an opening tag.

    An attribute with value None will be formatted like a boolean
    attribute. For example, the attribute asdf=None will be formatted
    to ' asdf'. This is used for attributes like 'checked',
    'selected', etc. in HTML input nodes."""
    def fmt(key):
        if attrs[key] is None:
            return ""
        else:
            return '="' + escape(attrs[key], {'"': "'"}) + '"'
    return "".join(" " + k + fmt(k) for k in attrs)


def make_node(tag_name = None, closes = True, close_tag = True):
    """Builds a new markup node.

    Closes the node if *closes* is True, and uses a different tag to
    close it if *close_tag* is True. Both are True by default. If
    *tag_name* is None, this node won't have opening or closing
    tags."""
    def node(*children, **attributes):
        if not tag_name:
            return concat_writers(*children)
        start_tag = "<" + tag_name
        start_tag += format_attributes(attributes)
        start_tag += " /" if closes and not close_tag else ""
        start_tag += ">"
        start = make_writer(start_tag)
        if close_tag and closes:
            end = make_writer("</" + tag_name + ">")
            return concat_writers(start, *(children + (end,)))
        else:
            # can't really have children if the node doesn't close or
            # doesn't have a close tag
            return start
    return node


# Prefixing attributes. Used for nodes with attributes to be treated
# as different nodes (e.g. css styling through classes).

def union_replace(old, new):
    """An aggressive union operator: replaces old keys."""
    merged = {}
    for k in old:
        merged[k] = old[k]
    for k in new:
        merged[k] = new[k]
    return merged


def union_extend(*keys):
    """Keys in *keys* are extended by pasting the values together.

    The keys not in *keys* are treated the same way as in
    union_replace."""
    def union(old, new):
        merged = {}
        for k in old:
            merged[k] = old[k]
        for k in new:
            if k in keys and k in merged:
                merged[k] += " " + new[k]
            else:
                merged[k] = new[k]
        return merged
    return union


def with_attributes(node, union, **old_attrs):
    """Builds a node from another, with prefixed attributes."""
    def fixed_node(*children, **new_attrs):
        return node(*children, **(union(old_attrs, new_attrs)))
    return fixed_node
