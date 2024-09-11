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
-- Table structure for table `card_effects`
--

DROP TABLE IF EXISTS `card_effects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card_effects` (
  `card_effect_id` int NOT NULL AUTO_INCREMENT,
  `card_id` int NOT NULL,
  `effect_id` int NOT NULL,
  PRIMARY KEY (`card_effect_id`),
  KEY `card_id` (`card_id`),
  KEY `effect_id` (`effect_id`),
  CONSTRAINT `card_effects_ibfk_1` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`) ON DELETE CASCADE,
  CONSTRAINT `card_effects_ibfk_2` FOREIGN KEY (`effect_id`) REFERENCES `effects` (`effect_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card_effects`
--

LOCK TABLES `card_effects` WRITE;
/*!40000 ALTER TABLE `card_effects` DISABLE KEYS */;
INSERT INTO `card_effects` VALUES (1,1,1),(2,2,2),(3,3,1),(4,3,1);
/*!40000 ALTER TABLE `card_effects` ENABLE KEYS */;
UNLOCK TABLES;

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
  `image_path` varchar(255) NOT NULL,
  `card_type` int NOT NULL,
  PRIMARY KEY (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
INSERT INTO `cards` VALUES (1,'test card 1','test class',1,1,'1.png',0),(2,'test card 2','test class',2,2,'2.png',0),(3,'test card 3','test class',3,3,'3.png',0);
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
  KEY `deck_id` (`deck_id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `deck_cards_ibfk_1` FOREIGN KEY (`deck_id`) REFERENCES `decks` (`deck_id`) ON DELETE CASCADE,
  CONSTRAINT `deck_cards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deck_cards`
--

LOCK TABLES `deck_cards` WRITE;
/*!40000 ALTER TABLE `deck_cards` DISABLE KEYS */;
INSERT INTO `deck_cards` VALUES (1,1,1,3),(2,1,2,3),(3,1,3,3),(4,2,1,3),(5,2,2,3),(6,2,3,3);
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
  KEY `user_id` (`user_id`),
  CONSTRAINT `decks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `decks`
--

LOCK TABLES `decks` WRITE;
/*!40000 ALTER TABLE `decks` DISABLE KEYS */;
INSERT INTO `decks` VALUES (1,1,'새로운 덱','0.png',1,'2024-09-07 09:29:21'),(2,2,'새로운 덱','0.png',1,'2024-09-10 05:09:23');
/*!40000 ALTER TABLE `decks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `effects`
--

DROP TABLE IF EXISTS `effects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `effects` (
  `effect_id` int NOT NULL AUTO_INCREMENT,
  `effect_name` varchar(100) NOT NULL,
  `condition` text,
  `cost` text,
  `effect` text,
  PRIMARY KEY (`effect_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `effects`
--

LOCK TABLES `effects` WRITE;
/*!40000 ALTER TABLE `effects` DISABLE KEYS */;
INSERT INTO `effects` VALUES (1,'test effect 1','패','마나 수정 3개 소모','이 카드를 소환하고 카드 한 장을 드로우'),(2,'test effect 2','필드, 이 카드가 공격시','마나 수정 1개와 이 카드를 제물로','공격 대상인 카드를 파괴한다');
/*!40000 ALTER TABLE `effects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_history`
--

DROP TABLE IF EXISTS `game_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_history` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `user1_id` int NOT NULL,
  `user2_id` int NOT NULL,
  `winner_id` int DEFAULT NULL,
  `played_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`game_id`),
  KEY `user1_id` (`user1_id`),
  KEY `user2_id` (`user2_id`),
  KEY `winner_id` (`winner_id`),
  CONSTRAINT `game_history_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `game_history_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `game_history_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_history`
--

LOCK TABLES `game_history` WRITE;
/*!40000 ALTER TABLE `game_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_history_moves`
--

DROP TABLE IF EXISTS `game_history_moves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_history_moves` (
  `move_id` int NOT NULL AUTO_INCREMENT,
  `game_id` int NOT NULL,
  `user_id` int NOT NULL,
  `move_description` text,
  `move_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`move_id`),
  KEY `game_id` (`game_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `game_history_moves_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `game_history` (`game_id`) ON DELETE CASCADE,
  CONSTRAINT `game_history_moves_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
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
-- Table structure for table `game_mods`
--

DROP TABLE IF EXISTS `game_mods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_mods` (
  `mod_id` int NOT NULL AUTO_INCREMENT,
  `mod_name` varchar(50) NOT NULL,
  `is_open` tinyint(1) NOT NULL DEFAULT '0',
  `image_path` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`mod_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_mods`
--

LOCK TABLES `game_mods` WRITE;
/*!40000 ALTER TABLE `game_mods` DISABLE KEYS */;
INSERT INTO `game_mods` VALUES (1,'test',0,'1.png','is test mod');
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
  CONSTRAINT `user_cards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `user_cards_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `cards` (`card_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_cards`
--

LOCK TABLES `user_cards` WRITE;
/*!40000 ALTER TABLE `user_cards` DISABLE KEYS */;
INSERT INTO `user_cards` VALUES (1,1,1,1,'2024-09-07 09:15:55'),(2,1,2,2,'2024-09-07 09:15:55'),(3,1,3,3,'2024-09-07 09:15:55'),(4,1,1,1,'2024-09-10 05:12:45'),(5,1,2,2,'2024-09-10 05:12:45'),(6,1,3,3,'2024-09-10 05:12:45'),(7,2,1,1,'2024-09-10 05:12:45'),(8,2,2,2,'2024-09-10 05:12:45'),(9,2,3,3,'2024-09-10 05:12:45');
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
  KEY `deck_id` (`deck_id`),
  CONSTRAINT `user_deck_selections_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `user_deck_selections_ibfk_2` FOREIGN KEY (`deck_id`) REFERENCES `decks` (`deck_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_deck_selections`
--

LOCK TABLES `user_deck_selections` WRITE;
/*!40000 ALTER TABLE `user_deck_selections` DISABLE KEYS */;
INSERT INTO `user_deck_selections` VALUES (1,2,1,2,'2024-09-10 05:13:52'),(2,1,1,1,'2024-09-10 05:13:56');
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
  `money` int NOT NULL,
  `current_mod_id` int NOT NULL DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`stat_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_stats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_stats`
--

LOCK TABLES `user_stats` WRITE;
/*!40000 ALTER TABLE `user_stats` DISABLE KEYS */;
INSERT INTO `user_stats` VALUES (1,1,'admin',0,1,'2024-09-07 09:12:07'),(2,2,'1',0,1,'2024-09-10 05:09:16');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$mpg09GXKU0VyZonahReOXemEXKP.zb7bVM5OzzdJxz3Q0ngJugrcy','2024-09-07 09:12:07','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3NjczMTEwZC0yZTE3LTRlNDAtYWQwMi1lNGZkYTU5YzUyZjIiLCJleHAiOjE3MjY2NDE0NjYsInVpZCI6MX0.v-dDGqM6kcm1EvHflD_eIAxXzIE2OSbD48Codepesxg','2024-09-18 06:37:46'),(2,'1','$2b$12$/vfFDJwOVbkR.42kY2w7q.0Dj5y.8Jc/iNbPEpYAl3DANZeMUcm/G','2024-09-10 05:09:16','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjYWZkMjQ4Mi1kYWVlLTRlMGQtODBmNi1jOWIxMmRmMTAwOTUiLCJleHAiOjE3MjY2NDE0NzMsInVpZCI6Mn0.pZI7VZbw1NUFzDcRzZM7LaqDYdpzmvsMWEoe9Bamelc','2024-09-18 06:37:53');
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

-- Dump completed on 2024-09-11 15:40:42
