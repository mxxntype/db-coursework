from os import environ


class Credentials:
    user: str | None
    passwd: str | None
    dbname: str | None
    host: str | None
    port: int | None

    def __init__(
        self,
        user: str | None = None,
        passwd: str | None = None,
        dbname: str | None = environ["DB_NAME"],
        host: str | None = "localhost",
        port: int | None = 5432,
    ) -> None:
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.host = host
        self.port = port


# Common credentials.
READER: Credentials = Credentials(user="reader", passwd="12345")
AUTHOR: Credentials = Credentials(user="author", passwd="12345")

# Admin credentials.
__ADMIN_NAME: str = environ.get("DB_USER") or "admin"
__ADMIN_PASSWD: str = environ.get("DB_PASSWORD") or "admin"
ADMIN: Credentials = Credentials(user=__ADMIN_NAME, passwd=__ADMIN_PASSWD)
