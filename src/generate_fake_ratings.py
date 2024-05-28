import faker
from log.main import create_named_logger

if __name__ == "__main__":
    fake = faker.Faker("ru_RU")

    log = create_named_logger("FAKEDATA")
    log.info("Starting author generation")

    ratings = []
    for _ in range(2000000):
        rate = fake.random_int(1, 5)
        post_id = fake.random_int(1, 200000)
        rated_at = fake.date_time()
        ratings.append(f"({post_id}, {rate}, '{rated_at}')")

    log.info("Forming SQL")

    ratings = ",\n".join(ratings)
    sql: str = f"""
INSERT INTO ratings(post_id, rate, rated_at)
VALUES
{ratings};
    """

    print(sql)
