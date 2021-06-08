import IPython
from IPython.display import display as ipy_display, Javascript

GLUE_PREFIX = "application/papermill.record/"


def glue(name, variable, display=True):
    """Glue a variable into the notebook cell's metadata.

    Parameters
    ----------
    name: string
        A unique name for the variable. You can use this name to refer to the variable
        later on.
    variable: Python object
        A variable in Python for which you'd like to store its display value. This is
        not quite the same as storing the object itself - the stored information is
        what is *displayed* when you print or show the object in a Jupyter Notebook.
    display: bool
        Display the object you are gluing. This is helpful in sanity-checking the
        state of the object at glue-time.
    """
    mime_prefix = "" if display else GLUE_PREFIX
    metadata = {"scrapbook": dict(name=name, mime_prefix=mime_prefix)}
    if "bokeh" in type(variable).__module__:
        # import here to avoid a hard dependency on bokeh
        from bokeh.embed import components
        from bokeh.resources import CDN

        script, div = components(variable, wrap_script=False)
        ipy_display(
            {mime_prefix + "text/html": div},
            raw=True,
            metadata=metadata,
        )
        # Have to use Javascript here to load the BokehJS files
        s, meta = IPython.core.formatters.format_display_data(
            Javascript(script, lib=CDN.js_files)
        )
        metadata.update(meta)
        metadata["scrapbook"]["name"] += "_js"
        ipy_display(
            {mime_prefix + k: v for k, v in s.items()},
            raw=True,
            metadata=metadata,
        )
    else:
        mimebundle, meta = IPython.core.formatters.format_display_data(variable)
        metadata.update(meta)
        ipy_display(
            {mime_prefix + k: v for k, v in mimebundle.items()},
            raw=True,
            metadata=metadata,
        )
