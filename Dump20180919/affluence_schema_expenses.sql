CREATE DATABASE  IF NOT EXISTS `affluence_schema` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `affluence_schema`;
-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: affluence_schema
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `expenses` (
  `idexpenses` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `paid` datetime DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  `payment_method` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `deleted` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`idexpenses`),
  UNIQUE KEY `idexpenses_UNIQUE` (`idexpenses`),
  KEY `fkey_users_expenses_idx` (`user`),
  KEY `fkey_categories_expenses_idx` (`category`),
  KEY `fkey_payment_method_expenses_idx` (`payment_method`),
  CONSTRAINT `fkey_categories_expenses` FOREIGN KEY (`category`) REFERENCES `categories` (`idcategories`),
  CONSTRAINT `fkey_payment_method_expenses` FOREIGN KEY (`payment_method`) REFERENCES `payment_methods` (`idpayment_methods`),
  CONSTRAINT `fkey_users_expenses` FOREIGN KEY (`user`) REFERENCES `users` (`idusers`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,1,'מתנה לטופי',99,'2018-08-30 09:55:26','2018-08-30 09:55:26',1,2,'אהבה מתוקה שלי',0),(2,1,'בוווווורגר!',30,'2018-08-31 12:00:00','2018-08-31 12:00:00',1,3,'הייתי רעב',0),(3,1,'הוצאה נוספת',22,'2018-09-03 19:19:16','2018-09-03 19:19:16',2,4,NULL,0),(6,1,'\"עכשיו יעבוד!\"',345,'2018-09-03 19:45:15','2018-09-03 19:45:15',2,5,NULL,1),(7,1,'מהווב',11,'2018-09-03 19:54:59','2018-09-03 19:54:59',3,6,NULL,1),(8,1,'שליחת אהבה לדטורי',100,'2018-09-04 09:38:10','2018-09-04 09:38:10',3,3,NULL,0),(9,1,'שליחת אהבה לדטורי +1',100,'2018-09-04 09:39:31','2018-09-04 09:39:31',4,5,NULL,0),(10,1,'Beard oil',5,'2018-09-04 09:41:22','2018-09-04 09:41:22',4,6,NULL,0),(11,1,'קוד 302',3,'2018-09-04 09:42:25','2018-09-04 09:42:25',5,4,NULL,1),(12,1,'הסתדר!!   =)',4,'2018-09-04 09:43:03','2018-09-04 09:43:03',5,3,NULL,0),(13,1,'בלי 301 ב-ADD?',2,'2018-09-04 09:44:09','2018-09-04 09:44:09',6,2,NULL,0),(14,1,'חוקר 301',301,'2018-09-04 09:47:13','2018-09-04 09:47:13',6,1,NULL,1);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-19  1:19:50
