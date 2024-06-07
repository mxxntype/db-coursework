-- TRUNCATE TABLE attachments RESTART IDENTITY CASCADE;
INSERT INTO attachments
    (description, data, author_id)
VALUES
    ('Отчет по курсовой работе Вартанян А.А.', '/home/user/Documents/report.pdf'::bytea, 91),
    ('Отчет по курсовой работе',               '/home/user/Documents/report.pdf'::bytea, 82),
    ('Уровни изоляции транзакций SQL',         '/home/user/Documents/report.pdf'::bytea, 73),
    ('Message passing with Iggy.rs',           '/home/user/Documents/report.pdf'::bytea, 64),
    ('Вложение без описания №1',               '/home/user/Documents/report.pdf'::bytea, 55),
    ('Вложение без описания №2',               '/home/user/Documents/report.pdf'::bytea, 46),
    ('Вложение без описания №3',               '/home/user/Documents/report.pdf'::bytea, 37),
    ('Вложение без описания №4',               '/home/user/Documents/report.pdf'::bytea, 28),
    ('Вложение без описания №5',               '/home/user/Documents/report.pdf'::bytea, 19);
