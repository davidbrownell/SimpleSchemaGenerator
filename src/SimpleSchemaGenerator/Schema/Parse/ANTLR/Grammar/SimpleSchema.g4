// ----------------------------------------------------------------------
// |
// |  SimpleSchema.g4
// |
// |  David Brownell <db@DavidBrownell.com>
// |      2024-04-10 18:43:50
// |
// ----------------------------------------------------------------------
// |
// |  Copyright David Brownell 2024
// |  Distributed under the MIT License.
// |
// ----------------------------------------------------------------------
grammar SimpleSchema;

// ----------------------------------------------------------------------
tokens { INDENT, DEDENT }

@lexer::header {

from antlr_denter.DenterHelper import DenterHelper
from SimpleSchemaParser import SimpleSchemaParser

}

@lexer::members {

def CustomInitialization(self):
    self._nested_pair_ctr = 0
    self._lexing_include_filename = False

class SimpleSchemaDenter(DenterHelper):
    def __init__(self, lexer, newline_token, indent_token, dedent_token):
        super().__init__(newline_token, indent_token, dedent_token, should_ignore_eof=False)

        self.lexer: SimpleSchemaLexer = lexer

    def pull_token(self):
        return super(SimpleSchemaLexer, self.lexer).nextToken()

def nextToken(self):
    if not hasattr(self, "_denter"):
        self._denter = self.__class__.SimpleSchemaDenter(
            self,
            SimpleSchemaParser.NEWLINE,
            SimpleSchemaParser.INDENT,
            SimpleSchemaParser.DEDENT,
        )

    return self._denter.next_token()

}

// ----------------------------------------------------------------------
// |
// |  Lexer Rules
// |
// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
// Newlines nested within paired brackets are safe to ignore, but newlines outside of paired
// brackets are meaningful.
NEWLINE:                                    '\r'? '\n' {self._nested_pair_ctr == 0}? [ \t]*;
NESTED_NEWLINE:                             '\r'? '\n' {self._nested_pair_ctr != 0}? [ \t]* -> channel(HIDDEN);

LINE_CONTINUATION:                          '\\' '\r'? '\n' [ \t]* -> channel(HIDDEN);

LPAREN:                                     '(' {self._nested_pair_ctr += 1};
RPAREN:                                     ')' {self._nested_pair_ctr -= 1};
LBRACK:                                     '[' {self._nested_pair_ctr += 1};
RBRACK:                                     ']' {self._nested_pair_ctr -= 1};

// ----------------------------------------------------------------------
INCLUDE_FROM:                               'from';
INCLUDE_IMPORT:                             'import';

// ----------------------------------------------------------------------
MULTI_LINE_COMMENT:                         '#/' .*? '/#' -> skip;
SINGLE_LINE_COMMENT:                        '#' ~[\r\n]* -> skip;

HORIZONTAL_WHITESPACE:                      [ \t]+ -> channel(HIDDEN);

NUMBER:                                     '-'? [0-9]* '.' [0-9]+;
INTEGER:                                    '-'? [0-9]+;
IDENTIFIER:                                 [_@$&]? [a-zA-Z\p{Emoji}][a-zA-Z0-9_]*;

DOUBLE_QUOTE_STRING:                        UNTERMINATED_DOUBLE_QUOTE_STRING '"';
UNTERMINATED_DOUBLE_QUOTE_STRING:           '"' ('\\"' | '\\\\' | ~'"')*?;

SINGLE_QUOTE_STRING:                        UNTERMINATED_SINGLE_QUOTE_STRING '\'';
UNTERMINATED_SINGLE_QUOTE_STRING:           '\'' ('\\\'' | '\\\\' | ~'\'')*?;

TRIPLE_DOUBLE_QUOTE_STRING:                 UNTERMINATED_TRIPLE_DOUBLE_QUOTE_STRING '"""';
UNTERMINATED_TRIPLE_DOUBLE_QUOTE_STRING:    '"""' .*?;

TRIPLE_SINGLE_QUOTE_STRING:                 UNTERMINATED_TRIPLE_SINGLE_QUOTE_STRING '\'\'\'';
UNTERMINATED_TRIPLE_SINGLE_QUOTE_STRING:    '\'\'\'' .*?;

// ----------------------------------------------------------------------
// |
// |  Parser Rules
// |
// ----------------------------------------------------------------------
// Note that any rule with a '__' suffix represents a non-binding rule (meaning a rule without
// backing code only here for organizational purposes).

entry_point__:                              NEWLINE* header_statement__* body_statement__* EOF;

// ----------------------------------------------------------------------
// |
// |  Common
// |
// ----------------------------------------------------------------------
identifier:                                 IDENTIFIER;

// ----------------------------------------------------------------------
metadata_clause:                            '{' (metadata_clause_single_line__ | metadata_clause_multi_line__) '}';
metadata_clause_single_line__:              'pass' | (metadata_clause_item (',' metadata_clause_item)* ','?);
metadata_clause_multi_line__:               INDENT (
                                                ('pass' NEWLINE+)
                                                | (metadata_clause_item ','? NEWLINE+)+
                                            ) DEDENT;

metadata_clause_item:                       identifier ':' expression__;

// ----------------------------------------------------------------------
cardinality_clause:                         (
                                                cardinality_clause_optional
                                                | cardinality_clause_zero_or_more
                                                | cardinality_clause_one_or_more
                                                | cardinality_clause_fixed
                                                | cardinality_clause_range__
                                            );

cardinality_clause_optional:                '?';
cardinality_clause_zero_or_more:            '*';
cardinality_clause_one_or_more:             '+';
cardinality_clause_fixed:                   LBRACK integer_expression RBRACK;
cardinality_clause_range__:                 LBRACK integer_expression '..' integer_expression RBRACK;

// ----------------------------------------------------------------------
// |
// |  Expressions
// |
// ----------------------------------------------------------------------
expression__:                               (
    number_expression
    | integer_expression
    | true_expression
    | false_expression
    | none_expression
    | string_expression
    | list_expression
    | tuple_expression
);

number_expression:                          NUMBER;
integer_expression:                         INTEGER;
true_expression:                            'y' | 'Y' | 'yes' | 'Yes' | 'YES' | 'true' | 'True' | 'TRUE' | 'on' | 'On' | 'ON';
false_expression:                           'n' | 'N' | 'no' | 'No' | 'NO' | 'false' | 'False' | 'FALSE' | 'off' | 'Off' | 'OFF';
none_expression:                            'None';
string_expression:                          DOUBLE_QUOTE_STRING | SINGLE_QUOTE_STRING | TRIPLE_DOUBLE_QUOTE_STRING | TRIPLE_SINGLE_QUOTE_STRING;
list_expression:                            LBRACK (expression__ (',' expression__)* ','?)? RBRACK;
tuple_expression:                           LPAREN (tuple_expression_single_item__ | tuple_expression_multi_item__) RPAREN;
tuple_expression_single_item__:             expression__ ',';
tuple_expression_multi_item__:              expression__ (',' expression__)+ ','?;

// ----------------------------------------------------------------------
// |
// |  Statements
// |
// ----------------------------------------------------------------------
header_statement__:                         (
                                                include_statement
                                            );

// ----------------------------------------------------------------------
include_statement:                          INCLUDE_FROM include_statement_from INCLUDE_IMPORT include_statement_import__ NEWLINE+;

include_statement_from:                     '/'? '.'? ((identifier | include_statement_from_parent_dir) '/'?)+;
include_statement_from_parent_dir:          '..';

include_statement_import__:                 include_statement_import_star | include_statement_import_grouped_items__ | include_statement_import_items__;
include_statement_import_star:              '*';
include_statement_import_grouped_items__:   LPAREN include_statement_import_items__ RPAREN;
include_statement_import_items__:           include_statement_import_element (',' include_statement_import_element)* ','?;
include_statement_import_element:           identifier ('as' identifier)?;

// ----------------------------------------------------------------------
body_statement__:                           (
                                                parse_structure_statement
                                                | parse_structure_simplified_statement
                                                | parse_item_statement
                                                | extension_statement
                                            );

extension_statement:                        identifier LPAREN (
                                                (
                                                    (
                                                        (extension_statement_positional_args ',' extension_statement_keyword_args)
                                                        | extension_statement_positional_args
                                                        | extension_statement_keyword_args
                                                    )
                                                    ','?
                                                )?
                                            ) RPAREN NEWLINE+;

extension_statement_positional_args:        expression__ (',' expression__)*;
extension_statement_keyword_args:           extension_statement_keyword_arg (',' extension_statement_keyword_arg)*;
extension_statement_keyword_arg:            identifier '=' expression__;

parse_item_statement:                       identifier ':' parse_type NEWLINE+;

parse_structure_statement:                  (
                                                identifier
                                                    (':' (parse_structure_statement_base_grouped_items__ | parse_structure_statement_base_items__))?
                                                '->'
                                                INDENT (
                                                    ('pass' NEWLINE+)
                                                    | body_statement__+
                                                ) DEDENT
                                                (
                                                    (
                                                        (cardinality_clause NEWLINE* metadata_clause)
                                                        | metadata_clause
                                                        | cardinality_clause
                                                    )
                                                    NEWLINE+
                                                )?
                                            );

parse_structure_statement_base_items__:                 parse_type (',' parse_type)* ','?;
parse_structure_statement_base_grouped_items__:         LPAREN parse_structure_statement_base_items__ RPAREN;

parse_structure_simplified_statement:       identifier metadata_clause NEWLINE+;

// ----------------------------------------------------------------------
// |
// |  Types
// |
// ----------------------------------------------------------------------
parse_type:                                 (
                                                parse_tuple_type
                                                | parse_variant_type
                                                | parse_identifier_type
                                            ) cardinality_clause? metadata_clause?;

parse_identifier_type:                      parse_identifier_type_global? identifier ('.' identifier)*;
parse_identifier_type_global:               '::';

parse_variant_type:                         LPAREN parse_type ('|' parse_type)* '|' parse_type RPAREN;

parse_tuple_type:                           LPAREN (parse_tuple_type_single_item__ | parse_tuple_type_multi_item__) RPAREN;
parse_tuple_type_single_item__:             parse_type ',';
parse_tuple_type_multi_item__:              parse_type (',' parse_type)+ ','?;
