DROP DATABASE IF EXISTS testdb;
CREATE DATABASE testdb;
USE testdb;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `body` varchar(300) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `admin` boolean NOT NULL DEFAULT false,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `todo_list`
--

DROP TABLE IF EXISTS `todo_list`;
CREATE TABLE `todo_list` (
  `todolist_id` int NOT NULL AUTO_INCREMENT,
  `listname` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`todolist_id`),
  UNIQUE KEY `listname` (`listname`)
) DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `user_id` int NOT NULL,
  `todolist_id` int NOT NULL,
  PRIMARY KEY (`user_id`, `todolist_id`),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (todolist_id) REFERENCES todo_list(todolist_id)
) DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `todo_item`
--

DROP TABLE IF EXISTS `todo_item`;
CREATE TABLE `todo_item` (
  `task_id` int NOT NULL AUTO_INCREMENT,
  `taskname` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `detail` varchar(200) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `todolist_id` int NOT NULL,
  PRIMARY KEY (`task_id`),
  FOREIGN KEY (todolist_id) REFERENCES todo_list(todolist_id)
) DEFAULT CHARSET=utf8mb3;
