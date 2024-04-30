#pragma once

#include "monad.hpp"
#include <pqxx/pqxx>
#include <string>
#include <vector>

class Database {
  private:
    // The credentials needed to connect to the PostgreSQL database.
    //
    // TODO: Read these dynamically.
    const std::string credentials =
        "user=user password=password host=localhost port=5432 "
        "dbname=coursework";

    // The connection to the PostgreSQL database.
    pqxx::connection connection;

  public:
    Database();
    GenericResult run_startup_migrations();
    GenericResult insert_default_authors(size_t amount);
    GenericResult clear_table(const std::string& table_name);

    std::vector<std::string> get_authors();
};
