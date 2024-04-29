#include "database.hpp"

#include <fstream>
#include <iostream>
#include <pqxx/pqxx>

Database::Database() : connection(this->credentials) {}

void Database::run_startup_migrations() {
    try {
        std::ifstream file("migrations/1.sql");
        std::ostringstream oss;
        oss << file.rdbuf();
        std::string migration_sql = oss.str();
        pqxx::work transaction(this->connection);
        pqxx::result result = transaction.exec(migration_sql);
        transaction.commit();
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}
