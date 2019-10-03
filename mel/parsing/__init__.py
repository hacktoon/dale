from .constants import ROOT
from .base import BaseParser

from ..exceptions import ParsingError

from . import ( # noqa
    root,
    keyword,
    literal,
    path,
    reference,
    relation,
    struct,
    value,
)


class Parser(BaseParser):
    def parse(self):
        node = self.parse_rule(ROOT)
        if not self.stream.is_eof():
            raise ParsingError
        return node
