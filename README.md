markup
======

An experiment in procedural markup generation.

The idea is to have documents and templates as python functions. In
Haskell's type notation, a document's type would be:

```Haskell
Monad m => (String -> m a) -> m ()
```

Where `m` would usually model a useful stateful operation. A document
is then a function that receives a writing procedure (a python
function that receives text) and does something with it.

So to write a document `doc` to a file `f`, you'd do `doc(f.write)`.

Read the source in base.py for further explanation.

## Build documents

Documents are built by nesting nodes. A node is a function that
receives other nodes and attributes as keyword arguments. Evaluating a
node gives you a document, which you can later write to a file as
explained above.

An example follows, and more examples are given in examples.py.

### Example

```python
from markup.html import *
import sys

doc = html(
    head(title("Example")),
    body(
        p("This is a p node with red text", style="color: red;"),
        h1("This is a title below the red text")))

# write the document to standard output
doc(sys.stdout.write)
```