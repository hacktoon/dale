
class Node:
    def __init__(self):
        self.expressions = []
        self.text = ""
        self.index = (0, 0)

    def __bool__(self):
        return True

    def __len__(self):
        return len(self.expressions)

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        template = "{}('{}')"
        id = self.id.upper()
        return template.format(id, self)

    def __getitem__(self, index):
        return self.expressions[index]

    def __iter__(self):
        for node in self.expressions:
            yield node

    def add(self, node):
        self.expressions.append(node)


# ROOT =================================================

class RootNode(Node):
    id = "root"


# EXPRESSSION =================================================

class ExpressionNode(Node):
    id = "expression"


class ObjectExpressionNode(Node):
    id = "object-expression"


# RELATION ========================================================

class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.key = None
        self.sign = None
        self.value = None


class SignNode(Node):
    id = "sign"


class EqualNode(SignNode):
    id = "equal"


class DifferentNode(SignNode):
    id = "different"


class GreaterThanNode(SignNode):
    id = "greater_than"


class GreaterThanEqualNode(SignNode):
    id = "greater_than_equal"


class LessThanNode(SignNode):
    id = "less_than"


class LessThanEqualNode(SignNode):
    id = "less_than_equal"


class InNode(SignNode):
    id = "in"


class NotInNode(SignNode):
    id = "not_in"


# VALUE ========================================================

class ValueNode(Node):
    id = "value"


# REFERENCE ========================================================

class ReferenceNode(Node):
    id = "reference"


class HeadReferenceNode(Node):
    id = "head-reference"


class ChildReferenceNode(Node):
    id = "child-reference"


# STRUCT ========================================================

class StructNode(Node):
    def __init__(self):
        super().__init__()
        self.key = None
        self.expressions = []


class ObjectNode(StructNode):
    id = "object"


class AnonymObjectNode(StructNode):
    id = "anonym-object"


class DefaultFormatNode(StructNode):
    id = "default-format"


class DefaultDocNode(StructNode):
    id = "default-doc"


class QueryNode(StructNode):
    id = "query"


class AnonymQueryNode(StructNode):
    id = "anonym-query"


# LIST ========================================================

class ListNode(Node):
    id = "list"


# KEYWORD ========================================================

class KeywordNode(Node):
    id = "keyword"

    def __init__(self):
        super().__init__()
        self.value = ""


class NameNode(KeywordNode):
    id = "name"


class ConceptNode(NameNode):
    id = "concept"


class TagNode(KeywordNode):
    id = "tag"


class LogNode(KeywordNode):
    id = "log"


class AliasNode(KeywordNode):
    id = "alias"


class CacheNode(KeywordNode):
    id = "cache"


class FormatNode(KeywordNode):
    id = "format"


class MetaNode(KeywordNode):
    id = "meta"


class DocNode(KeywordNode):
    id = "doc"


# RANGE ========================================================

class RangeNode(Node):
    id = "range"

    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None


# LITERAL ========================================================

class LiteralNode(Node):
    id = "literal"

    def __init__(self):
        super().__init__()
        self.value = None


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"


class TemplateStringNode(LiteralNode):
    id = "template-string"


# PATH ========================================================

class PathNode(Node):
    id = "path"


# WILDCARD ========================================================

class WildcardNode(Node):
    id = "wildcard"
