from psycopg import errors

ERROR_MAP = {
    errors.SyntaxError: "Syntax error in SQL query.",
    errors.UndefinedTable: "Table does not exist in the database.",
    errors.InvalidCatalogName: "Database does not exist.",
    errors.DuplicateTable: "Table already exists.",
    errors.UniqueViolation: "Attempted to insert duplicate value in a unique column.",
    errors.ForeignKeyViolation: "Foreign key constraint violated.",
    errors.ConnectionDoesNotExist: "The database connection does not exist.",
    errors.OperationalError: "Operational error occurred.",
    Exception: "An unexpected error occurred.",
}
