def create_sql_server_connection(connection_string: str):
    try:
        import pyodbc
    except ImportError as error:
        raise ImportError("Install pyodbc before connecting to SQL Server.") from error

    return pyodbc.connect(connection_string)
