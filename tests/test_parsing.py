import pytest

from mel.nodes import Node
from mel.parsing import Parser
from mel.parsing.stream import Stream
from mel.parsing.grammar import Grammar
from mel.exceptions import ParsingError


# STREAM TESTS ========================================

def test_valid_pattern_texts():
    stream = Stream('abc 24')
    text, _ = stream.read_pattern(r'[a-z]+')
    assert text == 'abc'


def test_valid_pattern_index():
    stream = Stream('foo')
    _, index = stream.read_pattern(r'[a-z]+')
    assert index == (0, 3)


def test_invalid_pattern():
    stream = Stream('54')
    with pytest.raises(ParsingError):
        assert stream.read_pattern(r'4')


def test_valid_symbols():
    stream = Stream('[]{}')
    assert stream.read_string('[')
    assert stream.read_string(']')
    assert stream.read_string('{')
    assert stream.read_string('}')


def test_save_restore():
    stream = Stream('    ')
    index = stream.save()
    try:
        stream.read_pattern(r'foo')
    except ParsingError:
        stream.restore(index)
    assert stream.read_pattern(r'\s+')


def test_read_pattern_advances_index():
    stream = Stream('    \n         ')
    stream.read_pattern(r'\s+')
    assert stream.index == len(stream.text)


# PARSER TESTS ========================================

def test_rule_parser():
    g = Grammar()
    g.root(g.p(r'\d+'))
    parser = Parser(g)
    assert str(parser.parse('42')) == '42'


def test_parser_returns_node():
    g = Grammar()
    g.root(g.p(r'-\d+'))
    parser = Parser(g)
    assert isinstance(parser.parse('-333'), Node)


def test_seq_parser():
    g = Grammar()
    g.rule('int', g.p(r'\d+'))
    g.root(g.seq(g.r('int'), g.p('foo')))
    assert Parser(g).parse('42foo')


def test_seq_parser_children_count():
    g = Grammar()
    g.rule('abc', g.p(r'[abc]+'))
    g.root(g.seq(g.r('abc'), g.s('--')))
    node = Parser(g).parse('abbbcaa--')
    assert len(node) == 2


def test_zero_many_children_count():
    g = Grammar()
    g.rule('digit', g.p(r'[0-9]'))
    g.root(g.zero_many(g.r('digit')))
    node = Parser(g).parse('145')
    assert len(node) == 3


def test_one_of_parser():
    g = Grammar()
    g.rule('digit', g.p(r'[0-9]'))
    g.rule('char', g.p(r'[a-z]'))
    g.root(g.one_of(g.r('digit'), g.r('char')))
    parser = Parser(g)
    assert parser.parse('5')
    assert parser.parse('f')


def test_space_skip():
    g = Grammar()
    g.skip('space', r'\s+')
    g.rule('name', g.p(r'\w+'))
    g.root(g.r('name'))
    assert Parser(g).parse('    556   ')


def test_space_skip_between_rules():
    g = Grammar()
    g.skip('space', r'\s+')
    g.rule('name', g.p(r'\w+'))
    g.root(g.zero_many(g.r('name')))
    node = Parser(g).parse('   foo  bar ')
    assert node[0].text == 'foo'
    assert node[1].text == 'bar'
