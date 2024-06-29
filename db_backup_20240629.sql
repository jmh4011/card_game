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
  `deck_id` int DEFAULT NULL,
  `card_id` int DEFAULT NULL,
  PRIMARY KEY (`deck_card_id`),
  KEY `deck_id` (`deck_id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `deckcards_ibfk_1` FOREIGN KEY (`deck_id`) REFERENCES `decks` (`deck_id`),
  CONSTRAINT `deckcards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deckcards`
--

LOCK TABLES `deckcards` WRITE;
/*!40000 ALTER TABLE `deckcards` DISABLE KEYS */;
INSERT INTO `deckcards` VALUES (20,1,1);
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
  `player_id` int DEFAULT NULL,
  `deck_name` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`deck_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `decks_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `decks`
--

LOCK TABLES `decks` WRITE;
/*!40000 ALTER TABLE `decks` DISABLE KEYS */;
INSERT INTO `decks` VALUES (1,1,'새로운 덱','0.png','2024-06-21 01:57:52'),(2,1,'새로운 덱','0.png','2024-06-21 02:01:44'),(3,1,'새로운 덱','0.png','2024-06-21 02:06:08'),(4,1,'새로운 덱','0.png','2024-06-21 03:42:23'),(5,1,'새로운 덱','0.png','2024-06-21 03:49:10');
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
  `player_id` int DEFAULT NULL,
  `move_description` text,
  `move_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`move_id`),
  KEY `game_id` (`game_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `gamemoves_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`),
  CONSTRAINT `gamemoves_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
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
  `player1_id` int DEFAULT NULL,
  `player2_id` int DEFAULT NULL,
  `winner_id` int DEFAULT NULL,
  `played_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`game_id`),
  KEY `player1_id` (`player1_id`),
  KEY `player2_id` (`player2_id`),
  KEY `winner_id` (`winner_id`),
  CONSTRAINT `games_ibfk_1` FOREIGN KEY (`player1_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `games_ibfk_2` FOREIGN KEY (`player2_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `games_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `players` (`player_id`)
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
-- Table structure for table `player_stats`
--

DROP TABLE IF EXISTS `player_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_stats` (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `current_deck_id` int DEFAULT NULL,
  `money` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`stat_id`),
  KEY `player_id` (`player_id`),
  KEY `current_deck_id` (`current_deck_id`),
  KEY `ix_player_stats_stat_id` (`stat_id`),
  CONSTRAINT `player_stats_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `player_stats_ibfk_2` FOREIGN KEY (`current_deck_id`) REFERENCES `decks` (`deck_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_stats`
--

LOCK TABLES `player_stats` WRITE;
/*!40000 ALTER TABLE `player_stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `player_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playercards`
--

DROP TABLE IF EXISTS `playercards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playercards` (
  `player_card_id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `card_id` int NOT NULL,
  `card_count` int NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`player_card_id`),
  KEY `player_id` (`player_id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `playercards_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `playercards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playercards`
--

LOCK TABLES `playercards` WRITE;
/*!40000 ALTER TABLE `playercards` DISABLE KEYS */;
INSERT INTO `playercards` VALUES (1,1,1,1,'2024-06-21 00:38:40'),(2,1,2,2,'2024-06-21 00:38:40'),(3,1,3,3,'2024-06-21 00:38:40');
/*!40000 ALTER TABLE `playercards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `player_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,'admin','$2b$12$bloAGOlRG..clIoQS2nUoeaB2EEwIXWAkSrrIvavwTPUFsri.6IlC','2024-06-20 03:31:51');
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playerstats`
--

DROP TABLE IF EXISTS `playerstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playerstats` (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `player_name` varchar(100) DEFAULT NULL,
  `current_deck_id` int DEFAULT NULL,
  `money` int NOT NULL DEFAULT '0',
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`stat_id`),
  KEY `player_id` (`player_id`),
  KEY `current_deck_id` (`current_deck_id`),
  CONSTRAINT `playerstats_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `playerstats_ibfk_2` FOREIGN KEY (`current_deck_id`) REFERENCES `decks` (`deck_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playerstats`
--

LOCK TABLES `playerstats` WRITE;
/*!40000 ALTER TABLE `playerstats` DISABLE KEYS */;
INSERT INTO `playerstats` VALUES (1,1,NULL,NULL,0,'2024-06-20 03:31:51');
/*!40000 ALTER TABLE `playerstats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'card_game'
--

--
-- Dumping routines for database 'card_game'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-29 18:35:32
