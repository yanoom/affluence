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
-- Table structure for table `ui_translations`
--

DROP TABLE IF EXISTS `ui_translations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `ui_translations` (
  `idui_translations` int(11) NOT NULL AUTO_INCREMENT,
  `table` varchar(45) DEFAULT NULL,
  `column` varchar(45) DEFAULT NULL,
  `id_origin` int(11) DEFAULT NULL,
  `language` int(11) DEFAULT NULL,
  `value` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idui_translations`),
  KEY `fk_language_ui_translations_idx` (`language`),
  CONSTRAINT `fk_language_ui_translations` FOREIGN KEY (`language`) REFERENCES `ui_languages` (`idui_languages`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_translations`
--

LOCK TABLES `ui_translations` WRITE;
/*!40000 ALTER TABLE `ui_translations` DISABLE KEYS */;
INSERT INTO `ui_translations` VALUES (1,'payment_methods','name',1,2,'מזומן'),(2,'payment_methods','name',2,2,'כרטיס אשראי'),(3,'payment_methods','name',3,2,'העברה בנקאית'),(4,'payment_methods','name',4,2,'צ\'ק'),(5,'payment_methods','name',5,2,'ביט'),(6,'payment_methods','name',6,2,'אחר'),(7,'categories','name',1,2,'הוצאה חודשית'),(8,'categories','name',2,2,'לייפסטייל'),(9,'categories','name',3,2,'כיף ותחביבים'),(10,'categories','name',4,2,'אוכל בחוץ'),(11,'categories','name',5,2,'קניות'),(12,'categories','name',6,2,'חשבונות'),(13,'categories','name',7,2,'תחבורה+דלק');
/*!40000 ALTER TABLE `ui_translations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-19  1:19:48
