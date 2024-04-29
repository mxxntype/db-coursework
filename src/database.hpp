#include <pqxx/pqxx>
#include <string>

class Database {
  private:
    // The credentials needed to connect to the PostgreSQL database.
    const std::string credentials =
        "user=user password=password host=localhost port=5432 "
        "dbname=coursework";
    // The connection to the PostgreSQL database.
    pqxx::connection connection;

  public:
    Database();
    void run_startup_migrations();
};
