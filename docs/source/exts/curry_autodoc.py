"""
Extension to document curried functions as normal functions

See: https://docs.celeryq.dev/en/latest/_modules/celery/contrib/sphinx.html
and: https://github.com/sphinx-doc/sphinx/issues/10221
"""

from sphinx.ext.autodoc import FunctionDocumenter

from pipe_utils import curry


class CurryDocumenter(FunctionDocumenter):
    """Document task definitions."""

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return (
              isinstance(member, curry)
              or super().can_document_member(member, membername, isattr, parent)
        )


def setup(app):
    """Setup Sphinx extension."""
    app.setup_extension('sphinx.ext.autodoc')
    app.add_autodocumenter(CurryDocumenter)

    return {
        'parallel_read_safe': True
    }
