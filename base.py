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

# A synonym. Represents a text node.
text = make_writer


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
    return "".join([" " + k + ("=\"" + attrs[k] + "\"" if attrs[k] else "")
                    for k in attrs])


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


def with_attributes(node, **attrs):
    """Builds a node from another, with fixed attributes."""
    def fixed_node(*children):
        return node(*children, **attrs)
    return fixed_node
