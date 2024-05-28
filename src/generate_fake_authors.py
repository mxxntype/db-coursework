import faker
from log.main import create_named_logger

if __name__ == "__main__":
    fake = faker.Faker("ru_RU")

    log = create_named_logger("FAKEDATA")
    log.info("Starting author generation")

    authors = []
    for _ in range(20000):
        name = fake.first_name_male()
        surname = fake.last_name_male()
        middle_name = fake.middle_name_male()
        phone = fake.unique.phone_number()
        log.debug(f"Generated new author: {surname} {name} {middle_name} ({phone})")
        authors.append(f"('{name}', '{surname}', '{middle_name}', '{phone}')")

    log.info("Forming SQL")

    authors = ",\n".join(authors)
    sql: str = f"""
INSERT INTO authors(name, surname, middle_name, phone)
VALUES
{authors};
    """

    print(sql)
