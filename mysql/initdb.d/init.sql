DROP DATABASE IF EXISTS testdb;
CREATE DATABASE testdb;
USE testdb;
DROP TABLE IF EXISTS test;

CREATE TABLE test
(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name TEXT NOT NULL
)DEFAULT CHARACTER
  SET=utf8;

  INSERT INTO test
    (name)
  VALUES
    ("test1"),
    ("test2"),
    ("test3");