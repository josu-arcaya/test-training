#!/bin/bash

# Structure for ega database
sqlite3 ega.db "

drop table questions;

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
";

echo -e '.separator "*"\n.import ega_questions.csv questions_tmp' | sqlite3 ega.db

sqlite3 ega.db "
insert into questions(question, answer0, answer1, answer2, answer3, solution, id_type, comment_question, id_exam) select * from questions_tmp;

drop table questions_tmp;
";
