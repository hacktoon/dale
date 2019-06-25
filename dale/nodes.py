from collections import defaultdict


class Node:
    def __init__(self):
        self.text = ""
        self.index = (0, 0)

    def __bool__(self):
        return True

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        template = "{}('{}')"
        id = self.id.upper()
        return template.format(id, self)

    def _hook_into(self, parent):
        parent.values.append(self)

    def eval(self):
        return


class StructNode(Node):
    def __init__(self):
        super().__init__()
        self.subnodes = []
        self.tags = set()
        self.props = defaultdict(dict)
        self.values = []

    def __len__(self):
        return len(self.subnodes)

    def __iter__(self):
        for node in self.subnodes:
            yield node

    def __getitem__(self, index):
        return self.subnodes[index]

    def add(self, node):
        self.subnodes.append(node)
        node._hook_into(self)

    def add_tag(self, name):
        self.tags.add(name)

    def add_prop(self, id, name, node):
        self.props[id][name] = node


# ABSTRACT STRUCTS =================================================

class MetaStructNode(StructNode):
    pass


class PathStructNode(StructNode):
    def __init__(self):
        super().__init__()
        self.path = PathNode()


# ROOT STRUCT =========================================================

class RootNode(StructNode):
    id = "root"


# OBJECT STRUCTS ======================================================

class ObjectNode(PathStructNode):
    id = "object"

    def _hook_into(self, parent):
        key = self.key
        parent.add_prop(key.id, key.value, self)

    def eval(self):
        return str(self)


class AnonymObjectNode(MetaStructNode):
    id = "anonym-object"

    def _hook_into(self, parent):
        for node in self.subnodes:
            parent.add(node)


# DEFAULT STRUCTS =================================================

class DefaultFormatKeywordNode(MetaStructNode):
    id = "default-format"

    def _hook_into(self, parent):
        parent.default_format = self


class DefaultDocKeywordNode(MetaStructNode):
    id = "default-doc"

    def _hook_into(self, parent):
        parent.default_doc = self


# QUERY STRUCTS =================================================

class QueryNode(PathStructNode):
    id = "query"


class AnonymQueryNode(MetaStructNode):
    id = "anonym-query"


# EXPRESSION =================================================

class ExpressionNode(Node):
    id = "expression"


class ObjectExpressionNode(Node):
    id = "object-expression"


# RELATION ========================================================

class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.path = PathNode()
        self.value = ValueNode()


class EqualNode(RelationNode):
    id = "equal"


class DifferentNode(RelationNode):
    id = "different"


class GreaterThanNode(RelationNode):
    id = "greater_than"


class GreaterThanEqualNode(RelationNode):
    id = "greater_than_equal"


class LessThanNode(RelationNode):
    id = "less_than"


class LessThanEqualNode(RelationNode):
    id = "less_than_equal"


class InNode(RelationNode):
    id = "in"


class NotInNode(RelationNode):
    id = "not_in"


# VALUE ========================================================

class ValueNode(Node):
    id = "value"


# REFERENCE ========================================================

class ReferenceNode(StructNode):
    id = "reference"


class HeadReferenceNode(Node):
    id = "head-reference"


class ChildReferenceNode(Node):
    id = "child-reference"


# LIST ========================================================

class ListNode(StructNode):
    id = "list"


# KEYWORD ========================================================

class KeywordNode(Node):
    id = "keyword"

    def __init__(self):
        super().__init__()
        self.value = ""


class NameKeywordNode(KeywordNode):
    id = "name-keyword"


class ConceptKeywordNode(NameKeywordNode):
    id = "concept-keyword"


class TagKeywordNode(KeywordNode):
    id = "tag-keyword"

    def _hook_into(self, parent):
        parent.add_tag(self.value)


class LogKeywordNode(KeywordNode):
    id = "log-keyword"


class AliasKeywordNode(KeywordNode):
    id = "alias-keyword"


class CacheKeywordNode(KeywordNode):
    id = "cache-keyword"


class FormatKeywordNode(KeywordNode):
    id = "format-keyword"


class MetaKeywordNode(KeywordNode):
    id = "meta-keyword"


class DocKeywordNode(KeywordNode):
    id = "doc-keyword"


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

    def eval(self, _):
        return self.value


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

class PathNode(StructNode):
    id = "path"


# WILDCARD ========================================================

class WildcardNode(Node):
    id = "wildcard"
