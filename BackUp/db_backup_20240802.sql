-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: card_game
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cards`
--

DROP TABLE IF EXISTS `cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cards` (
  `card_id` int NOT NULL AUTO_INCREMENT,
  `card_name` varchar(100) NOT NULL,
  `card_class` varchar(50) DEFAULT NULL,
  `attack` int DEFAULT NULL,
  `health` int DEFAULT NULL,
  `description` text,
  `image` varchar(255) DEFAULT NULL,
  `cost` int DEFAULT NULL,
  `card_type` int DEFAULT NULL,
  PRIMARY KEY (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
INSERT INTO `cards` VALUES (1,'Test Card 1','Type A',1,1,'This is a test card','1.png',1,0),(2,'Test Card 2','Type B',2,2,'This is another test card','2.png',2,0),(3,'Test Card 3','Type A',3,3,'Yet another test card','3.png',3,0);
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deckcards`
--

DROP TABLE IF EXISTS `deckcards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deckcards` (
  `deck_card_id` int NOT NULL AUTO_INCREMENT,
  `deck_id` int NOT NULL,
  `card_id` int NOT NULL,
  `card_count` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`deck_card_id`),
  KEY `deckcards_ibfk_1` (`deck_id`),
  KEY `deckcards_ibfk_2` (`card_id`),
  CONSTRAINT `deckcards_ibfk_1` FOREIGN KEY (`deck_id`) REFERENCES `decks` (`deck_id`),
  CONSTRAINT `deckcards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deckcards`
--

LOCK TABLES `deckcards` WRITE;
/*!40000 ALTER TABLE `deckcards` DISABLE KEYS */;
INSERT INTO `deckcards` VALUES (1,7,1,1),(2,7,2,2),(3,7,3,3);
/*!40000 ALTER TABLE `deckcards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `decks`
--

DROP TABLE IF EXISTS `decks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `decks` (
  `deck_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `deck_name` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`deck_id`),
  KEY `decks_ibfk_1` (`user_id`),
  CONSTRAINT `decks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `decks`
--

LOCK TABLES `decks` WRITE;
/*!40000 ALTER TABLE `decks` DISABLE KEYS */;
INSERT INTO `decks` VALUES (7,1,'하하','0.png','2024-07-15 06:18:25');
/*!40000 ALTER TABLE `decks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gamemoves`
--

DROP TABLE IF EXISTS `gamemoves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gamemoves` (
  `move_id` int NOT NULL AUTO_INCREMENT,
  `game_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `move_description` text,
  `move_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`move_id`),
  KEY `game_id` (`game_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `gamemoves_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`),
  CONSTRAINT `gamemoves_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gamemoves`
--

LOCK TABLES `gamemoves` WRITE;
/*!40000 ALTER TABLE `gamemoves` DISABLE KEYS */;
/*!40000 ALTER TABLE `gamemoves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `games` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `user1_id` int DEFAULT NULL,
  `user2_id` int DEFAULT NULL,
  `winner_id` int DEFAULT NULL,
  `played_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`game_id`),
  KEY `user1_id` (`user1_id`),
  KEY `user2_id` (`user2_id`),
  KEY `winner_id` (`winner_id`),
  CONSTRAINT `games_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `games_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `games_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games`
--

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;
/*!40000 ALTER TABLE `games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usercards`
--

DROP TABLE IF EXISTS `usercards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usercards` (
  `user_card_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `card_id` int NOT NULL,
  `card_count` int NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_card_id`),
  KEY `user_id` (`user_id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `usercards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `usercards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usercards`
--

LOCK TABLES `usercards` WRITE;
/*!40000 ALTER TABLE `usercards` DISABLE KEYS */;
INSERT INTO `usercards` VALUES (1,1,1,1,'2024-07-15 06:07:46'),(2,1,2,2,'2024-07-15 06:07:46'),(3,1,3,3,'2024-07-15 06:07:46');
/*!40000 ALTER TABLE `usercards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `refresh_token` varchar(255) DEFAULT NULL,
  `refresh_token_expiry` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$FDNXSvNPBQtcLakSzll8jeFML6AKusafQ.LzFtOdokbA8dCqAiMRK','2024-07-12 06:27:29','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsImV4cCI6MTcyMTg4OTM3MiwianRpIjoiM2NhNGU5ODgtYzlmOC00YzBlLWE4NGItNjVmZjY0YzA4YzVmIn0.e2e5JoBk7QR0jhGAjdRx0Qcil1i15VTXrvP5METT78c','2024-07-25 06:36:12');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userstats`
--

DROP TABLE IF EXISTS `userstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userstats` (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `money` int NOT NULL DEFAULT '0',
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`stat_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `userstats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userstats`
--

LOCK TABLES `userstats` WRITE;
/*!40000 ALTER TABLE `userstats` DISABLE KEYS */;
INSERT INTO `userstats` VALUES (1,1,NULL,0,'2024-07-12 06:27:29');
/*!40000 ALTER TABLE `userstats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-18 16:41:16
