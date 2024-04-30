#include "database.hpp"
#include "monad.hpp"

#include <exception>
#include <fstream>
#include <iostream>
#include <pqxx/pqxx>

Database::Database() : connection(this->credentials) {}

GenericResult Database::run_startup_migrations() {
    GenericResult result = GenericResult::OK;

    try {
        std::ifstream file("migrations/1.sql");
        std::ostringstream oss;
        oss << file.rdbuf();
        std::string migration_sql = oss.str();
        pqxx::work txn(this->connection);
        pqxx::result _result = txn.exec(migration_sql);
        txn.commit();
    } catch (const std::exception& E) {
        std::cerr << E.what() << std::endl;
        result = GenericResult::ERROR;
    }

    return result;
}

GenericResult Database::insert_default_authors(size_t amount) {
    auto result = GenericResult::OK;

    try {
        const std::string txn_name = "insert_default_authors";
        for (size_t i = 0; i < amount; ++i) {
            pqxx::work txn(this->connection);
            this->connection.prepare(
                txn_name, "INSERT INTO authors (name, surname, "
                          "middle_name, phone) VALUES ($1, $2, $3, $4)");
            txn.exec_prepared(txn_name, "Ivan", "Ivanov", "Ivanovich",
                              "+79009001010");
            txn.exec("DEALLOCATE " + txn_name);
            txn.commit();
        }
    } catch (const std::exception& E) {
        std::cerr << E.what() << std::endl;
        result = GenericResult::ERROR;
    }

    return result;
}

// Remove all rows from `table_name`, no questions asked.
GenericResult Database::clear_table(const std::string& table_name) {
    auto result = GenericResult::OK;

    try {
        pqxx::work txn(this->connection);
        txn.exec("DELETE FROM " + table_name + " WHERE true");
        txn.commit();
    } catch (const std::exception& E) {
        std::cerr << E.what() << std::endl;
        result = GenericResult::ERROR;
    }

    return result;
}

std::vector<std::string> Database::get_authors() {
    std::vector<std::string> authors{};

    pqxx::work txn(this->connection);
    auto rows = txn.exec("SELECT phone FROM authors");
    authors.reserve(rows.size());
    for (const auto& row : rows)
        authors.push_back(row[0].as<std::string>());

    return authors;
}
