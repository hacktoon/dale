import codecs


class Node:
    def __init__(self):
        self._children = []
        self._tokens = []

    def add(self, *args):
        if len(args) == 2:
            name, child = args
            self.__dict__[name] = child
            self._children.append(child)
        else:
            self._children.append(args[0])

    @property
    def value(self):
        if len(self._children) == 1:
            return self._children[0].value
        return [child.value for child in self._children]

    def __getitem__(self, key):
        try:
            if key in self._properties:
                return self._properties[key]
            else:
                return self._children[key]
        except (KeyError, IndexError):
            raise ValueError(key + ' is not a valid key or index')

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        if len(self._children) == 1:
            return repr(self._children[0])
        return repr(self._children)

    def __str__(self):
        return repr(self)


class ExpressionNode(Node):

    @property
    def value(self):
        exp = {'keyword': self.keyword.value}

        if self.parameters.value.items():
            exp['parameters'] = self.parameters.value
        if len(self._children) > 1:
            exp['values'] = [child.value for child in self._children]
        elif len(self._children) == 1:
            exp['values'] = self._children[0].value
        return exp

    def __repr__(self):
        args = [self.keyword.value]
        values = ''
        if self.parameters.value.items():
            args.append(repr(self.parameters))
        if len(self._children) > 1:
            args.append(' '.join(repr(value) for value in self._children))
        elif len(self._children) == 1:
            args.append(repr(self._children[0]))
        return '({})'.format(' '.join(args))


class ParametersNode(Node):
    @property
    def value(self):
        return {key:child.value for key, child in self._properties.items()}

    def __repr__(self):
        items = self._properties.items()
        params = [':{} {}'.format(key, repr(child)) for key, child in items]
        return ' '.join(params)


class QueryNode(Node):
    @property
    def value(self):
        if self.source == 'file':
            try:
                with open(self.content.value, 'r') as file_obj:
                    return file_obj.read()
            except IOError as e:
               raise ParsingError("I/O error: {}".format(e))
            except:
               raise ParsingError("Unexpected error")
        else:
            return self.content.value

    def __repr__(self):
        if self.source:
            return '@ {} {}'.format(self.source, self.content)
        return '@ {}'.format(self.content)


class ReferenceNode(Node):
    def __repr__(self):
        return '.'.join(repr(child) for child in self._children)


class StringNode(Node):
    @property
    def value(self):
        # thanks to @rspeer at https://stackoverflow.com/a/24519338/544184
        ESCAPE_SEQUENCE_RE = re.compile(r'''
           \\( U........    # 8-digit hex escapes
           | u....          # 4-digit hex escapes
           | x..            # 2-digit hex escapes
           | [0-7]{1,3}     # Octal escapes
           | N\{[^}]+\}     # Unicode characters by name
           | [\\'"abfnrtv]  # Single-character escapes
           )''', re.VERBOSE)

        def decode_match(match):
           return codecs.decode(match.group(0), 'unicode-escape')
        value = self._children[0].value
        return ESCAPE_SEQUENCE_RE.sub(decode_match, value[1:-1])



class IntNode(Node):
    @property
    def value(self):
        return int(self._children[0].value)


class FloatNode(Node):
    @property
    def value(self):
        return float(self._children[0].value)


class BooleanNode(Node):
    @property
    def value(self):
        return {'true': True, 'false': False}[self._children[0].value]


class ListNode(Node):
    pass