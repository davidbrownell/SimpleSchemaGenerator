# Generated from C:/Code/GitHub/davidbrownell/SimpleSchemaGenerator/src/SimpleSchemaGenerator/Schema/Parse/ANTLR/Grammar/SimpleSchema.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .SimpleSchemaParser import SimpleSchemaParser
else:
    from SimpleSchemaParser import SimpleSchemaParser

# This class defines a complete generic visitor for a parse tree produced by SimpleSchemaParser.

class SimpleSchemaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpleSchemaParser#entry_point__.
    def visitEntry_point__(self, ctx:SimpleSchemaParser.Entry_point__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#identifier.
    def visitIdentifier(self, ctx:SimpleSchemaParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#metadata_clause.
    def visitMetadata_clause(self, ctx:SimpleSchemaParser.Metadata_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#metadata_clause_single_line__.
    def visitMetadata_clause_single_line__(self, ctx:SimpleSchemaParser.Metadata_clause_single_line__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#metadata_clause_multi_line__.
    def visitMetadata_clause_multi_line__(self, ctx:SimpleSchemaParser.Metadata_clause_multi_line__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#metadata_clause_item.
    def visitMetadata_clause_item(self, ctx:SimpleSchemaParser.Metadata_clause_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#cardinality_clause.
    def visitCardinality_clause(self, ctx:SimpleSchemaParser.Cardinality_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#cardinality_clause_optional.
    def visitCardinality_clause_optional(self, ctx:SimpleSchemaParser.Cardinality_clause_optionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#cardinality_clause_zero_or_more.
    def visitCardinality_clause_zero_or_more(self, ctx:SimpleSchemaParser.Cardinality_clause_zero_or_moreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#cardinality_clause_one_or_more.
    def visitCardinality_clause_one_or_more(self, ctx:SimpleSchemaParser.Cardinality_clause_one_or_moreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#cardinality_clause_fixed.
    def visitCardinality_clause_fixed(self, ctx:SimpleSchemaParser.Cardinality_clause_fixedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#cardinality_clause_range__.
    def visitCardinality_clause_range__(self, ctx:SimpleSchemaParser.Cardinality_clause_range__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#expression__.
    def visitExpression__(self, ctx:SimpleSchemaParser.Expression__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#number_expression.
    def visitNumber_expression(self, ctx:SimpleSchemaParser.Number_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#integer_expression.
    def visitInteger_expression(self, ctx:SimpleSchemaParser.Integer_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#true_expression.
    def visitTrue_expression(self, ctx:SimpleSchemaParser.True_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#false_expression.
    def visitFalse_expression(self, ctx:SimpleSchemaParser.False_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#none_expression.
    def visitNone_expression(self, ctx:SimpleSchemaParser.None_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#string_expression.
    def visitString_expression(self, ctx:SimpleSchemaParser.String_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#list_expression.
    def visitList_expression(self, ctx:SimpleSchemaParser.List_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#tuple_expression.
    def visitTuple_expression(self, ctx:SimpleSchemaParser.Tuple_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#tuple_expression_single_item__.
    def visitTuple_expression_single_item__(self, ctx:SimpleSchemaParser.Tuple_expression_single_item__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#tuple_expression_multi_item__.
    def visitTuple_expression_multi_item__(self, ctx:SimpleSchemaParser.Tuple_expression_multi_item__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#header_statement__.
    def visitHeader_statement__(self, ctx:SimpleSchemaParser.Header_statement__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement.
    def visitInclude_statement(self, ctx:SimpleSchemaParser.Include_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_from.
    def visitInclude_statement_from(self, ctx:SimpleSchemaParser.Include_statement_fromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_from_parent_dir.
    def visitInclude_statement_from_parent_dir(self, ctx:SimpleSchemaParser.Include_statement_from_parent_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_import__.
    def visitInclude_statement_import__(self, ctx:SimpleSchemaParser.Include_statement_import__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_import_star.
    def visitInclude_statement_import_star(self, ctx:SimpleSchemaParser.Include_statement_import_starContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_import_grouped_items__.
    def visitInclude_statement_import_grouped_items__(self, ctx:SimpleSchemaParser.Include_statement_import_grouped_items__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_import_items__.
    def visitInclude_statement_import_items__(self, ctx:SimpleSchemaParser.Include_statement_import_items__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#include_statement_import_element.
    def visitInclude_statement_import_element(self, ctx:SimpleSchemaParser.Include_statement_import_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#body_statement__.
    def visitBody_statement__(self, ctx:SimpleSchemaParser.Body_statement__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#extension_statement.
    def visitExtension_statement(self, ctx:SimpleSchemaParser.Extension_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#extension_statement_positional_args.
    def visitExtension_statement_positional_args(self, ctx:SimpleSchemaParser.Extension_statement_positional_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#extension_statement_keyword_args.
    def visitExtension_statement_keyword_args(self, ctx:SimpleSchemaParser.Extension_statement_keyword_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#extension_statement_keyword_arg.
    def visitExtension_statement_keyword_arg(self, ctx:SimpleSchemaParser.Extension_statement_keyword_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_item_statement.
    def visitParse_item_statement(self, ctx:SimpleSchemaParser.Parse_item_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_structure_statement.
    def visitParse_structure_statement(self, ctx:SimpleSchemaParser.Parse_structure_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_structure_statement_base_items__.
    def visitParse_structure_statement_base_items__(self, ctx:SimpleSchemaParser.Parse_structure_statement_base_items__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_structure_statement_base_grouped_items__.
    def visitParse_structure_statement_base_grouped_items__(self, ctx:SimpleSchemaParser.Parse_structure_statement_base_grouped_items__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_structure_simplified_statement.
    def visitParse_structure_simplified_statement(self, ctx:SimpleSchemaParser.Parse_structure_simplified_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_type.
    def visitParse_type(self, ctx:SimpleSchemaParser.Parse_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_identifier_type.
    def visitParse_identifier_type(self, ctx:SimpleSchemaParser.Parse_identifier_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_identifier_type_global.
    def visitParse_identifier_type_global(self, ctx:SimpleSchemaParser.Parse_identifier_type_globalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_variant_type.
    def visitParse_variant_type(self, ctx:SimpleSchemaParser.Parse_variant_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_tuple_type.
    def visitParse_tuple_type(self, ctx:SimpleSchemaParser.Parse_tuple_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_tuple_type_single_item__.
    def visitParse_tuple_type_single_item__(self, ctx:SimpleSchemaParser.Parse_tuple_type_single_item__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSchemaParser#parse_tuple_type_multi_item__.
    def visitParse_tuple_type_multi_item__(self, ctx:SimpleSchemaParser.Parse_tuple_type_multi_item__Context):
        return self.visitChildren(ctx)



del SimpleSchemaParser