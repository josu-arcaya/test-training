#!/bin/bash

# Structure for ega database
sqlite3 ega.db "

create table questions ( 
  id_question integer primary key,
  question text,
  answer0 text,
  answer1 text,
  answer2 text,
  answer3 text,
  solution integer,
  id_type integer,
  comment_question text,
  id_exam integer
);

create table types (
  id_type integer primary key,
  type text
);

create table exams (
  id_exam integer primary key,
  exam text
);
";

# Structure for user database
sqlite3 user.db "

create table register (
  id_question integer primary key,
  id_exam integer,
  total integer,
  correct integer
);

create table history (
  id_history integer primary key autoincrement,
  time timestamp default current_timestamp,
  score integer
)
";

# Fill database ega
sqlite3 ega.db "

create table questions_tmp ( 
  question text,
  answer0 text,
  answer1 text,
  answer2 text,
  answer3 text,
  solution integer,
  id_type integer,
  comment_question text,
  id_exam integer
);

create table types_tmp (
  type text
);

create table exams_tmp (
  exam text
);
";

echo -e '.separator "*"\n.import ega_exams.csv exams_tmp' | sqlite3 ega.db
echo -e '.separator "*"\n.import ega_types.csv types_tmp' | sqlite3 ega.db
echo -e '.separator "*"\n.import ega_questions.csv questions_tmp' | sqlite3 ega.db

sqlite3 ega.db "
insert into exams(exam) select * from exams_tmp;
insert into types(type) select * from types_tmp;
insert into questions(question, answer0, answer1, answer2, answer3, solution, id_type, comment_question, id_exam) select * from questions_tmp;

drop table questions_tmp;
drop table types_tmp;
drop table exams_tmp;
";
