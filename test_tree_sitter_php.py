import tree_sitter_php as tsphp
from tree_sitter import Language, Parser

PHP_LANGUAGE = Language(tsphp.language_php())
parser = Parser(PHP_LANGUAGE)

code = b"""<?php
if ($status === 'active') {
    return true;
} else {
    return false;
}
"""
tree = parser.parse(code)
print(tree.root_node.child_count)
print(f"Root node type: {tree.root_node.type}")
for child in tree.root_node.children:
    print(f"  {child.type} at {child.start_point}-{child.end_point}")
