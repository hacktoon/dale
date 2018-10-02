import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context
from dale.exceptions import UnexpectedTokenError


def create_tree(text):
    stream = TokenStream(text)
    return Parser(stream).parse()


def eval(text, context_class=Context):
    context = context_class()
    context.tree = tree = create_tree(text)
    return tree.eval(context)


def test_empty_input_string():
    node = create_tree('')
    assert node.id == 'Node'


def test_one_sized_tree_returns_the_child_node():
    node = create_tree('44')
    assert node.id == 'IntNode'


def test_node_index():
    node = create_tree('44 12')
    assert node.nodes[0].index == (0, 2)
    assert node.nodes[1].index == (3, 5)


@pytest.mark.parametrize('test_input', [
    ('56.75 (a b)'),
    ('-0.75'),
    ('-.099999'),
    ('-0.75e10/55 etc'),
    ('+1.45e-10'),
    ('True'),
    ('False'),
    ('"string"'),
    ("'string'"),
    ("@name 2"),
    ('?foo "test"')
])
def test_string_representation(test_input):
    tree = create_tree(test_input)
    assert str(tree) == test_input


@pytest.mark.parametrize('test_input, expected', [
    ('-215', 'IntNode(-215)'),
    ('56.75', 'FloatNode(56.75)'),
    ('(bar 42)', 'ScopeNode(bar 42)'),
    ('bar/42', 'ReferenceNode(bar/42)'),
    ('bar/42 "text"', 'Node(bar/42 "text")'),
])
def test_object_representation(test_input, expected):
    tree = create_tree(test_input)
    assert repr(tree) == expected


#  SCOPE TESTS

def test_unclosed_scope_raises_error():
    with pytest.raises(UnexpectedTokenError):
        create_tree('(')


def test_scope_key_assumes_first_reference():
    node = create_tree('(foo 42)')
    assert str(node.key) == 'foo'
