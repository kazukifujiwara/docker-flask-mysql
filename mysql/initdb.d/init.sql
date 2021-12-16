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
-- Table structure for table `todo-list`
--

DROP TABLE IF EXISTS `todo-list`;
CREATE TABLE `todo-list` (
  `todolist-id` int NOT NULL AUTO_INCREMENT,
  `listname` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`todolist-id`),
  UNIQUE KEY `listname` (`listname`)
) DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `user-id` int NOT NULL,
  `todolist-id` int NOT NULL,
  PRIMARY KEY (`user-id`, `todolist-id`),
) DEFAULT CHARSET=utf8mb3;

--
-- Table structure for table `todo-item`
--

DROP TABLE IF EXISTS `todo-item`;
CREATE TABLE `todo-item` (
  `item-id` int NOT NULL AUTO_INCREMENT,
  `itemname` varchar(30) DEFAULT NULL,
  `todolist-id` int NOT NULL,
  PRIMARY KEY (`item-id`)
) DEFAULT CHARSET=utf8mb3;