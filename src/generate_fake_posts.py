import faker
from log.main import create_named_logger

if __name__ == "__main__":
    fake = faker.Faker("ru_RU")

    log = create_named_logger("FAKEDATA")
    log.info("Starting post generation")

    posts = []
    for _ in range(20000):
        text = fake.sentence(20)
        title = fake.sentence(10)
        author_id = fake.random_int(1, 2000)
        created_at = fake.date_time()
        posts.append(f"('{text}', '{title}', {author_id}, '{created_at}')")

    log.info("Forming SQL")

    posts = ",\n".join(posts)
    sql: str = f"""
TRUNCATE TABLE posts RESTART IDENTITY CASCADE;
INSERT INTO posts(text, title, author_id, created_at)
VALUES
{posts};
    """

    print(sql)
