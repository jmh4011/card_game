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
  `image_path` varchar(255) DEFAULT NULL,
  `card_type` int DEFAULT NULL,
  PRIMARY KEY (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
INSERT INTO `cards` VALUES (1,'Test Card 1','Type A',1,1,'This is a test card','1.png',0),(2,'Test Card 2','Type B',2,2,'This is another test card','2.png',0),(3,'Test Card 3','Type A',3,3,'Yet another test card','3.png',0);
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deck_cards`
--

DROP TABLE IF EXISTS `deck_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deck_cards` (
  `deck_card_id` int NOT NULL AUTO_INCREMENT,
  `deck_id` int NOT NULL,
  `card_id` int NOT NULL,
  `card_count` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`deck_card_id`),
  KEY `deckcards_ibfk_1` (`deck_id`),
  KEY `deckcards_ibfk_2` (`card_id`),
  CONSTRAINT `deck_cards_ibfk_1` FOREIGN KEY (`deck_id`) REFERENCES `decks` (`deck_id`),
  CONSTRAINT `deck_cards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deck_cards`
--

LOCK TABLES `deck_cards` WRITE;
/*!40000 ALTER TABLE `deck_cards` DISABLE KEYS */;
INSERT INTO `deck_cards` VALUES (1,7,1,1),(2,7,2,2),(3,7,3,2);
/*!40000 ALTER TABLE `deck_cards` ENABLE KEYS */;
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
  `image_path` varchar(255) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL DEFAULT '0',
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
INSERT INTO `decks` VALUES (7,1,'히히','0.png',1,'2024-07-15 06:18:25');
/*!40000 ALTER TABLE `decks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_history_moves`
--

DROP TABLE IF EXISTS `game_history_moves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_history_moves` (
  `move_id` int NOT NULL AUTO_INCREMENT,
  `game_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `move_description` text,
  `move_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`move_id`),
  KEY `game_id` (`game_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `game_history_moves_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `game_historys` (`game_id`),
  CONSTRAINT `game_history_moves_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_history_moves`
--

LOCK TABLES `game_history_moves` WRITE;
/*!40000 ALTER TABLE `game_history_moves` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_history_moves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_historys`
--

DROP TABLE IF EXISTS `game_historys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_historys` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `user1_id` int DEFAULT NULL,
  `user2_id` int DEFAULT NULL,
  `winner_id` int DEFAULT NULL,
  `played_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`game_id`),
  KEY `user1_id` (`user1_id`),
  KEY `user2_id` (`user2_id`),
  KEY `winner_id` (`winner_id`),
  CONSTRAINT `game_historys_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `game_historys_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `game_historys_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_historys`
--

LOCK TABLES `game_historys` WRITE;
/*!40000 ALTER TABLE `game_historys` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_historys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_mods`
--

DROP TABLE IF EXISTS `game_mods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_mods` (
  `mod_id` int NOT NULL AUTO_INCREMENT,
  `mod_name` varchar(50) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `is_open` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`mod_id`),
  KEY `ix_game_mods_mod_id` (`mod_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_mods`
--

LOCK TABLES `game_mods` WRITE;
/*!40000 ALTER TABLE `game_mods` DISABLE KEYS */;
INSERT INTO `game_mods` VALUES (1,'test','0.png','test mod',1),(2,'test2','1.png','test mod 2',1);
/*!40000 ALTER TABLE `game_mods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_cards`
--

DROP TABLE IF EXISTS `user_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_cards` (
  `user_card_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `card_id` int NOT NULL,
  `card_count` int NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_card_id`),
  KEY `user_id` (`user_id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `user_cards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `user_cards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_cards`
--

LOCK TABLES `user_cards` WRITE;
/*!40000 ALTER TABLE `user_cards` DISABLE KEYS */;
INSERT INTO `user_cards` VALUES (1,1,1,1,'2024-07-15 06:07:46'),(2,1,2,2,'2024-07-15 06:07:46'),(3,1,3,3,'2024-07-15 06:07:46');
/*!40000 ALTER TABLE `user_cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_deck_selections`
--

DROP TABLE IF EXISTS `user_deck_selections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_deck_selections` (
  `selection_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `mod_id` int NOT NULL,
  `deck_id` int NOT NULL,
  `selection_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`selection_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_deck_selections_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_deck_selections`
--

LOCK TABLES `user_deck_selections` WRITE;
/*!40000 ALTER TABLE `user_deck_selections` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_deck_selections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_stats`
--

DROP TABLE IF EXISTS `user_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_stats` (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `nickname` varchar(100) NOT NULL,
  `money` int NOT NULL DEFAULT '0',
  `current_mod_id` int NOT NULL DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`stat_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_stats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_stats`
--

LOCK TABLES `user_stats` WRITE;
/*!40000 ALTER TABLE `user_stats` DISABLE KEYS */;
INSERT INTO `user_stats` VALUES (1,1,'test',0,1,'2024-08-29 06:21:37'),(2,3,'1',0,1,'2024-08-29 06:21:45'),(3,4,'2',0,1,'2024-08-29 06:21:48');
/*!40000 ALTER TABLE `user_stats` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$FDNXSvNPBQtcLakSzll8jeFML6AKusafQ.LzFtOdokbA8dCqAiMRK','2024-07-12 06:27:29','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMmNjYzk2Yy05YzExLTQzODEtYWJhZS00ZTA3MmZiZTQ0MTUiLCJleHAiOjE3MjU0MzI1OTksInVpZCI6MX0.o-aAkhVcMCih7HkpZUb_HHgK10Ez8XpuaSOgFgHekkQ','2024-09-04 06:49:59'),(3,'1','$2b$12$b/9ghFQ4RO.fuUPQkFCzI.nCHLF53KMuMho2MU92W2wMWY85XaB9e','2024-08-14 03:17:04',NULL,'2024-09-04 04:43:45'),(4,'2','$2b$12$wlN.15mI/C1YZYM.MBKZYO/HHePSDxucVYwXuanrmykNzrKaNUZe.','2024-08-14 04:20:44','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5NzVkYWNjMS1jZWY4LTRmNzUtOTJmNS05OWQ1MTc2ZTUwMzYiLCJleHAiOjE3MjQyMTc2MjIsInVpZCI6NH0.imTPmJG5LSxsdtH5t85v_lt7LbqGiZ8GrbNPH55N9D4','2024-08-21 05:20:22');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-29 16:48:28
