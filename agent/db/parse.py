import sqlparse
from sqlparse.sql import IdentifierList, Identifier


def is_identifier(token):
    return isinstance(token, Identifier) or isinstance(token, IdentifierList)


def extract_table_names(sql_query):
    tables = set()
    parsed_stmt = sqlparse.parse(sql_query)
    for stmt in parsed_stmt:
        for token in stmt.tokens:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    tables.add(identifier.get_real_name())
            elif isinstance(token, Identifier):
                tables.add(token.get_real_name())
    return list(tables)