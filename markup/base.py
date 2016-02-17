"""
Exports the constructors that will serve as foundation for everything
else.
"""

import inspect
import functools
import collections


def partition(p, col):
    pos, neg = [], []
    for e in col: (pos if p(e) else neg).append(e)
    return pos, neg


#: The state of a writer when dumping a token
writer_state = collections.namedtuple('writer_state', 'nest last_token')

initial_state = writer_state(0, u"")


# Some useful writing functions here. A writing function is one
# capable of receiving a string and doing something useful with it.

# Typically you'd want to write to a file. So if *doc* is a document
# and *f* is a file, doc(f.write) writes the document to the file.

def ignore_token(text):
    """
    A writing function that does nothing.
    """
    pass


def print_token(text):
    """
    One that prints with the *print* command.
    """
    print(text)


class Writer(object):
    """
    The basic type. A wrapper around (function -> action).
    """

    def __init__(self, apply_):
        self.apply = apply_

    def __call__(self, fn, state=None):
        if state is None: state = initial_state
        return self.apply(fn, state)

    @staticmethod
    def wrap(f):
        grabs_state = False
        try:
            argspec = inspect.getargspec(f)
            grabs_state = argspec.keywords is not None
            grabs_state = grabs_state or \
                ('state' in argspec.args and argspec.defaults is not None and \
                 len(argspec.args) - len(argspec.defaults) <= \
                 argspec.args.index('state'))
        except: pass
        if not grabs_state:
            def simple(t, state=None):
                f(t)
                return state
            return functools.wraps(f)(simple)
        def forward_state(t, state):
            f(t, state=state)
            return writer_state(nest=state.nest, last_token=t)
        return functools.wraps(f)(forward_state)


# Used to give attributes to a node as a positional argument
class attrs(dict): pass


def make_writer(t):
    """
    The lower-most constructor. Redirects text to a writing procedure.
    A writer is a higher-order function that receives a writing
    function. Writers are also refered in this documentation as
    documents, as in HTML or XML documents.
    """
    return Writer(lambda f, *args: Writer.wrap(f)(t.encode('utf-8'), *args))


# Escape characters. http://wiki.python.org/moin/EscapingHtml
textnode_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
    }

# Limit attribute values heavily.
attribute_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
    '"': "'",
    }

def escape(text, table):
    """
    Produce entities within text.
    """
    return u"".join(table.get(c,c) for c in text)

# A text node.
text = lambda t: make_writer(escape(unicode(t), textnode_table))


def concat_writers(*ws):
    """
    Creates a new writer by concatenating many of them.

    This is nothing more than a glorified function sequencer. It
    combines writers sequentially into a wrapper.
    """
    writers = [text(w) if not isinstance(w, Writer) else w
               for w in ws if w is not None]
    def writer(f, state=None):
        for w in writers: state = w(f, state)
        return state
    return Writer(writer)


def nesting(w):
    def writer(f, state=None):
        state = w(f, state)
        return writer_state(nest=state.nest + 1, last_token=state.last_token)
    return Writer(writer)


def unnesting(w):
    def writer(f, state=None):
        state = w(f, state)
        return writer_state(nest=state.nest - 1, last_token=state.last_token)
    return Writer(writer)


# Markup node generation

def handle_synonyms(attributes):
    """
    Handles attribute synonyms.

    Attributes that end with an underscore are synonyms for attributes
    that don't. For example, 'class_' is the same as 'class'. This is
    to handle reserved words like 'class' and 'type'. If both 'attr_'
    and 'attr' are present, the one without the underscore remains and
    the other one is ignored.
    """
    return {k[:-1] if k[-1] == '_' else k: attributes[k]
            for k in attributes if k[-1] != '_' or k[:-1] not in attributes}


def format_attributes(attributes):
    """
    Formats attributes to be inserted in an opening tag.

    An attribute with value True will be formatted like a boolean
    attribute. For example, the attribute asdf=True will be formatted
    to ' asdf'. This is used for attributes like 'checked',
    'selected', etc. in HTML input nodes. If it's value is False or
    None, it won't be displayed.
    """
    def fmt(key):
        if attributes[key] is True:
            return u" {0}".format(key)
        elif attributes[key] is False or attributes[key] is None:
            return u""
        else:
            return u' {0}="{1}"'.format(
                key,
                escape(unicode(attributes[key]), attribute_table))
    return u"".join(fmt(k) for k in attributes)


def fuse_attributes(dicts):
    "~ reduce(lambda d1, d2: dict(d1, **d2), dicts)"
    r = {}
    for d in dicts: r.update(d)
    return r


def make_node(tag_name=None, closes=True, close_tag=True):
    """
    Builds a new markup node.

    Closes the node if *closes* is True, and uses a different tag to
    close it if *close_tag* is True. Both are True by default. If
    *tag_name* is None, this node won't have opening or closing
    tags.
    """
    def node(*children, **attributes):
        positional_attributes, children = partition(
            lambda child: isinstance(child, attrs), children)
        positional_attributes.append(attributes)
        attributes = fuse_attributes(positional_attributes)
        if len(children) == 1 and inspect.isgenerator(children[0]):
            children = children[0]
        if tag_name is None:
            return concat_writers(*children)
        start_tag = u"<{0}{1}{2}>".format(
            tag_name,
            format_attributes(handle_synonyms(attributes)),
            u" /" if closes and not close_tag else u"")
        start = make_writer(start_tag)
        if close_tag and closes:
            end = make_writer(u"</{0}>".format(tag_name))
            return concat_writers(
                nesting(start),
                unnesting(concat_writers(*children)),
                end)
        else:
            # can't really have children if the node doesn't close or
            # doesn't have a close tag
            return start
    return node


# Prefixing attributes. Used for nodes with attributes to be treated
# as different nodes (e.g. css styling through classes).

def union_replace(old, new):
    """
    An aggressive union operator: replaces old keys.
    """
    merged = {}
    for k in old:
        merged[k] = old[k]
    for k in new:
        merged[k] = new[k]
    return merged


def union_extend(*keys):
    """
    Keys in *keys* are extended by pasting the values together.

    The keys not in *keys* are treated the same way as in
    union_replace.
    """
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
    """
    Builds a node from another, with prefixed attributes.
    """
    def fixed_node(*children, **new_attrs):
        positional_attributes, children = partition(
            lambda child: isinstance(child, attrs), children)
        positional_attributes.append(new_attrs)
        new_attrs = fuse_attributes(positional_attributes)
        return node(
            *children,
             **(union(
                    handle_synonyms(old_attrs),
                    handle_synonyms(new_attrs))))
    return fixed_node


def pretty(doc, indent=2):
    pass
