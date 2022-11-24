import logging
import datetime
import pandas as pd
from model import engine


class PsqlHandler(logging.Handler):
    """
    This class creates a custom handler for writing the api logs to the Postgres DB
    """
    # query to create the table
    initial_sql = """CREATE TABLE IF NOT EXISTS logs(
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP NOT NULL,
        logger VARCHAR,
        message VARCHAR,
        level_name VARCHAR,
        path_name VARCHAR,
        file_name VARCHAR,
        module VARCHAR,
        line_no INT,
        function_name VARCHAR
        )
        """
    def __init__(self):
        super().__init__()

    def emit(self, record):
        conn = engine.connect()
        # create table if it does not exist
        conn.execute(PsqlHandler.initial_sql)

        msg = self.format(record)

        if record.__dict__["created"]:
            record.__dict__["created_at"] = datetime.datetime.fromtimestamp(
                record.__dict__["created"]
            ).strftime("%Y-%m-%d %H:%M:%S")

        df = pd.DataFrame.from_dict(record.__dict__, orient="index").T
        table_columns = [
            "created_at",
            "name",
            "msg",
            "levelname",
            "pathname",
            "filename",
            "module",
            "lineno",
            "funcName",
        ]
        df = df[table_columns].rename(
            columns={
                "name": "logger",
                "msg": "message",
                "levelname": "level_name",
                "pathname": "path_name",
                "filename": "file_name",
                "lineno": "line_no",
                "funcName": "function_name",
            }
        )

        df['message'] = record.message

        # Insert log record to the logs table:
        df.to_sql("logs", con=conn, if_exists="append", index=False)
