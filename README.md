#### Вариант  

| № варианта курсовой работы. | предметная область                                                          | примерные отношения предметной области                                                                                  | Вариант схемы |
| --------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------- |
| 20                          | Информационная система по публикациям в средствах массовой информации (СМИ) | Ведение справочника СМИ и информационной базы вышедших статей и передач. Состав авторов / участников и информация о них | 7             |

![Scheme variant](assets/scheme-variant.png)

![Database scheme](assets/scheme.svg)

#### Задание

Разработать клиент-серверное приложение, серверная часть которого должна быть реализована на **PostgreSQL**, представляющая собой модель предметной области в соответствии с вариантом задания. В рамках заданной предметной области реализовать заданную (по варианту) схему отношений, т.е. выделить сущности и их атрибуты, так чтобы связи между сущностями соответствовали представленной схеме. Допускается небольшое отступление от заданной схемы. В рамках курсовой работы необходимо на стороне сервера реализовать и использовать при демонстрации приложения следующие компоненты:

1. [x] Постоянные таблицы и связи между ними, количество таблиц и наличие связей должно соответствовать заданию, допускается увеличение числа таблиц и их полей для более адекватного представления предметной области;
2. [x] В приложении (на стороне клиента) реализовать не менее пяти запросов для демонстрации навыков работы.
3. Реализовать запросы по заданиям (в любых фрагментах скриптов как на стороне сервера, так и на стороне клиента):
	- [x] `a.` Составной многотабличный запрос с `CASE`-выражением;
	- [x] `b.` Многотабличный `VIEW`, с возможностью его обновления (использовать триггеры или правила);
	- [x] `c.` Материализованное представление;
	- [x] `d.` Запросы, содержащие подзапрос в разделах `SELECT`, `FROM` и `WHERE` (в каждом хотя бы по одному);
	- [x] `e.` Коррелированные подзапросы (минимум 3 запроса).
	- [x] `f.` Многотабличный запрос, содержащий группировку записей, агрегатные функции и параметр, используемый в разделе `HAVING`;
	- [x] `g.` Запросы, содержащие предикаты `ANY` и `ALL` (для каждого предиката);
4. [x] Создать индексы (минимум 3 штуки) для увеличения скорости выполнения запросов; Предусмотреть индексы разных типов. Индексы должны быть созданы для разных таблиц. В отчет включить план запроса, показывающий применение индекса при выполнении запроса.
5. [x] Во всех основных таблицах предусмотреть наличие триггеров на одно из событий (`DELETE`, `UPDATE`, `INSERT`), в каждой хотя бы по одному.
6. [x] Реализовать две собственные триггерные функции, которые будут вызываться при изменениях данных или событиях в базе данных. Данные функции могут быть вызваны из триггеров задания п. 5;
7. [x] Операции добавления, удаления и обновления реализовать в виде хранимых процедур или функций с параметрами для всех таблиц;
8. [x] Реализовать отдельную хранимую процедуру, состоящую из нескольких отдельных операций в виде единой транзакции, которая при определенных условиях может быть зафиксирована или откатана;
9. [x] Реализовать курсор на обновления отдельных данных (вычисления значения полей выбранной таблицы);
10. [x] Реализовать собственную скалярную и векторную функции. Функции сохранить в базе данных;
11. [x] Распределение прав пользователей: предусмотреть не менее двух пользователей с разным набором привилегий. Каждый набор привилегий оформить в виде роли.
12. [x] Предусмотреть в курсовой работе минимум одну таблицу для хранения исторических данных (`OLAP`)

Клиент должен обеспечивать добавление, модификацию и удаление данных по всей предметной области. Добавление, редактирование данных в таблице производить в отдельном окне. Запрещено в качестве вводимых данных, в том числе для связи таблиц, указывать значения первичных и внешних ключей – для обеспечения ссылочной целостности пользователь должен выбирать значения из справочника, а соответствующие значения должны подставляться программно (тем или иным способом – автоматически).

> [!CAUTION]
> Клиент должен быть реализован на средствах (языках программирования), *изученных (изучаемых) в рамках учебной программы*, в том числе смежных дисциплин.

#### Отчет

Отчет должен содержать:

1. [x] Бланк задания (подписанное руководителем курсовой работы и заведующим кафедрой);
2. [x] Расширенное задание, включающее вариант, точную копию строки из таблицы вариантов, копию схемы (по варианту), а таблицу с критериями для оценки;
3. [x] Распечатку схемы таблиц (диаграммы) (в крайнем случае – скриншот) со связями, соответствующими заданию (схеме);
4. [x] Теоретическую информацию, поясняющую предметную область, вопросы и принципы проектирования БД, вопросы нормализации отношений исходной предметной области, приводящие к виду, соответствующему схеме отношений в варианте, особенности реализации ЗАДАННОЙ предметной области с учетом выбранной СУБД;
5. [x] Вопросы (комментарии в пояснительной записке), связанные с повышением эффективности доступа к данным, разграничением доступа (права доступа), обеспечения ссылочной целостности данных;
6. [ ] Протокол настройки СУБД и создания БД (таблиц, индексов (если есть), представлений, хранимых процедур и функций, связей между таблицами, объявлений прав доступа;
7. [ ] Протокол работы программы (клиента), в том числе скриншоты форм ввода и вывода справок (результаты работы запросов, хранимых процедур и триггеров) на стороне клиента.
8. [ ] Полную распечатку SQL-скрипта всех созданных на сервере объектов БД (создание таблиц, представлений, исходные тексты всех хранимых процедур, функций, триггеров) (сложность коих, по сути, и будет оцениваться – кроме всего прочего);
9. [ ] Распечатка исходного кода клиента должна давать представление об использованных подходах работы в рамках клиент-серверной модели;
10. [x] Выводы (заключение)
11. [x] Список источников

#### Порядок защиты

Студент демонстрирует:

- работоспособность клиент-серверного приложения, а именно добавление, удаление и модификацию данных с помощью разработанного клиентского приложения в виде отдельных экранных форм (использование грида (табличного представления данных) с функцией редактирования записи в гриде приведет к снижению баллов за курсовую работу);
- выполнение не менее 50% запросов, указанных в п.2 задания на курсовую работу, должно содержать параметры, указываемые (выбираемые) пользователем на стороне клиента, и передаваемые в запрос, результаты запросов как правило представляются в табличном виде, объяснение ожидаемых и получаемых результатов запроса;
- последовательность действий, приводящих к исполнению разработанного триггера;
- готовность ответить на вопросы по инфологической и даталогической моделям данных, связям и отношениям, первичным и внешним ключам, организации индексов, и представлений;
- готовность ответить на любые вопросы по любому оператору SQL- скрипта, а также понимание принципов его исполнения;
- понимание исполнения операторов языка программирования реализации клиента, особенно в части взаимосвязи с SQL-сервером;
- различие и контроль доступа к данным, определяемым правами, НА СТОРОНЕ СЕРВЕРА, а не приложения;
