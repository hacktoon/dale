from .lexing import TokenStream
from .data import nodes
from .data import tokens
from .data.errors import LexingError, ParsingError


class Parser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        try:
            self.stream = TokenStream(self.text)
            return self._parse_root()
        except LexingError as error:
            raise ParsingError(error, self.text)

    def _read_token(self, type_name):
        return self.stream.consume(type_name)

    def _parse_root(self):
        node = nodes.Node()
        while not self.stream.is_eof():
            node.add(self._parse_value())
        return node

    def _parse_expression(self):
        node = nodes.Expression()
        self._read_token('StartExpression')
        node.add('keyword', self._read_token('Keyword'))
        node.add('parameters', self._parse_parameters())
        self._parse_expression_value(node)
        self._parse_expression_end(node)
        return node

    def _parse_expression_value(self, node):
        while not isinstance(self.stream.get(), tokens.EndExpressionToken):
            if self.stream.is_eof():
                break
            node.add(self._parse_value())

    def _parse_expression_end(self, node):
        end = self._read_token('EndExpression')
        if len(end.value()) > 1 and end.value() != node.keyword.value():
            raise ParsingError('expected a matching keyword', self.text)

    def _parse_parameters(self):
        node = nodes.Parameters()
        while isinstance(self.stream.get(), tokens.ParameterToken):
            if self.stream.is_eof():
                break
            parameter = self._read_token('Parameter')
            node.add(parameter.value(), self._parse_value())
        return node

    def _parse_value(self):
        parser_method = {
            tokens.StartExpressionToken: self._parse_expression,
            tokens.OpenListToken: self._parse_list,
            tokens.ReferenceToken: self._parse_reference,
            tokens.BooleanToken: self._parse_boolean,
            tokens.StringToken: self._parse_string,
            tokens.FloatToken: self._parse_float,
            tokens.QueryToken: self._parse_query,
            tokens.IntToken: self._parse_int
        }
        token = self.stream.get()

        try:
            node = parser_method[token.__class__]()
        except KeyError:
            message = 'unexpected {!r} while parsing'.format(token.id)
            raise LexingError(message, token.index)
        return node

    def _parse_list(self):
        node = nodes.List()
        self._read_token('OpenList')
        while not isinstance(self.stream.get(), tokens.CloseListToken):
            if self.stream.is_eof():
                break
            node.add(self._parse_value())
        self._read_token('CloseList')
        return node

    def _parse_reference(self):
        node = nodes.Reference()
        node.add(self._read_token('Reference'))
        return node

    def _parse_string(self):
        node = nodes.String()
        node.add(self._read_token('String'))
        return node

    def _parse_query(self):
        node = nodes.Query()
        node.add(self._read_token('Query'))
        return node

    def _parse_float(self):
        node = nodes.Float()
        node.add(self._read_token('Float'))
        return node

    def _parse_int(self):
        node = nodes.Int()
        node.add(self._read_token('Int'))
        return node

    def _parse_boolean(self):
        node = nodes.Boolean()
        node.add(self._read_token('Boolean'))
        return node
