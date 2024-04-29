#include <cstdlib>
#include <exception>
#include <fstream>
#include <iostream>
#include <pqxx/pqxx>
#include <sstream>
#include <string>
// #include <gtkmm.h>
// #include <glibmm.h>

#include "database.hpp"

int main(int argc, const char* argv[]) {
    int exit_code = EXIT_SUCCESS;

    auto db = Database();
    db.run_startup_migrations();

    return exit_code;
}
