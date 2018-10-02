-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (x86_64)
--
-- Host: yanoom.mysql.pythonanywhere-services.com    Database: yanoom$affluence
-- ------------------------------------------------------
-- Server version	5.6.27-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `idcategories` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `parent` int(11) DEFAULT NULL,
  PRIMARY KEY (`idcategories`),
  KEY `fkey_parent_idx` (`parent`),
  CONSTRAINT `fkey_categories_parent` FOREIGN KEY (`parent`) REFERENCES `categories` (`idcategories`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'הוצאה חודשית',NULL),(2,'לייפסטייל',NULL),(3,'כיף ותחביבים',NULL),(4,'אוכל בחוץ',NULL),(5,'מצרכים',NULL),(6,'חשבונות',NULL),(7,'תחבורה ודלק',NULL),(8,'טיפול',NULL),(9,'קורסים וסדנאות',2);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expenses` (
  `idexpenses` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `amount` float DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,1,'מתנה לטופי',99,'2018-08-30 09:55:26','2018-08-30 09:55:26',1,2,'אהבה מתוקה שלי',0),(2,1,'בוווווורגר!',30,'2018-08-31 12:00:00','2018-08-31 12:00:00',1,3,'הייתי רעב',0),(3,1,'הוצאה נוספת',22,'2018-09-03 19:19:16','2018-09-03 19:19:16',2,4,NULL,0),(6,1,'\"עכשיו יעבוד!\"',345,'2018-09-03 19:45:15','2018-09-03 19:45:15',2,5,NULL,1),(7,1,'מהווב',11,'2018-09-03 19:54:59','2018-09-03 19:54:59',3,6,NULL,1),(8,1,'שליחת אהבה לדטורי',100,'2018-09-04 09:38:10','2018-09-04 09:38:10',3,3,NULL,0),(9,1,'שליחת אהבה לדטורי +1',100,'2018-09-04 09:39:31','2018-09-04 09:39:31',4,5,NULL,1),(10,1,'Beard oil',5,'2018-09-04 09:41:22','2018-09-04 09:41:22',4,6,NULL,0),(11,1,'קוד 302',3,'2018-09-04 09:42:25','2018-09-04 09:42:25',5,4,NULL,1),(12,1,'הסתדר!!   =)',4,'2018-09-04 09:43:03','2018-09-04 09:43:03',5,3,NULL,0),(13,1,'בלי 301 ב-ADD?',2,'2018-09-04 09:44:09','2018-09-04 09:44:09',6,2,NULL,0),(14,1,'חוקר 301',301,'2018-09-04 09:47:13','2018-09-04 09:47:13',6,1,NULL,1),(15,1,'הוספה ראשונה ב-WEB??',100,'2018-09-20 09:11:35','2018-09-20 09:11:35',NULL,NULL,NULL,0),(16,1,'הוצאה עם קטגוריה ואמצעי תשלום!',66,'2018-09-23 20:39:33','2018-09-23 20:39:33',5,4,NULL,0),(17,1,'הוצאה מהנייד',123,'2018-09-29 11:25:05','2018-09-29 11:25:05',4,6,NULL,1),(19,1,'הוספה לבוטן',123,'2018-09-29 11:27:04','2018-09-29 11:27:04',2,3,NULL,1),(20,2,'דומינוס פיצה + גלידה',120,'2018-10-01 14:39:10','2018-10-01 14:39:10',2,4,NULL,1),(21,2,'דומינוס פיצה + גלידה',120,'2018-10-01 14:44:20','2018-10-01 14:44:20',2,4,NULL,1),(23,1,'הוספה לבדיקה',111,'2018-10-01 18:27:39','2018-10-01 18:27:39',5,7,NULL,1),(24,2,'הוספה לבדיקה',222,'2018-10-01 18:27:59','2018-10-01 18:27:59',NULL,5,NULL,1),(25,2,'הוספה לבדיקה',444,'2018-10-01 18:28:14','2018-10-01 18:28:14',4,NULL,NULL,1),(26,2,'דומינוס פיצה + גלידה',119.8,'2018-10-01 18:42:48','2018-10-01 18:42:48',2,4,NULL,0);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_methods`
--

DROP TABLE IF EXISTS `payment_methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_methods` (
  `idpayment_methods` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idpayment_methods`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_methods`
--

LOCK TABLES `payment_methods` WRITE;
/*!40000 ALTER TABLE `payment_methods` DISABLE KEYS */;
INSERT INTO `payment_methods` VALUES (1,'מזומן',NULL),(2,'כרטיס אשראי',NULL),(3,'העברה בנקאית',NULL),(4,'צ\'ק',NULL),(5,'ביט',NULL),(6,'אחר',NULL);
/*!40000 ALTER TABLE `payment_methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `idroles` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `permissions` smallint(6) DEFAULT '0',
  PRIMARY KEY (`idroles`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'viewer',1),(2,'admin',32767),(3,'basic',2);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `idsettings` int(11) NOT NULL AUTO_INCREMENT,
  `namesettings` varchar(45) NOT NULL,
  `valuetypesettings` int(11) NOT NULL COMMENT '1 = int, 2 = string',
  `valuesettings` int(11) NOT NULL,
  PRIMARY KEY (`idsettings`),
  FULLTEXT KEY `namesettings` (`namesettings`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'monthly_budget',1,11000),(2,'default_language',1,2);
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `idtags` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `expense` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtags`),
  KEY `fkey_tags_expenses_idx` (`expense`),
  CONSTRAINT `fkey_tags_expenses` FOREIGN KEY (`expense`) REFERENCES `expenses` (`idexpenses`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ui_languages`
--

DROP TABLE IF EXISTS `ui_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ui_languages` (
  `idui_languages` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `symbol` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idui_languages`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_languages`
--

LOCK TABLES `ui_languages` WRITE;
/*!40000 ALTER TABLE `ui_languages` DISABLE KEYS */;
INSERT INTO `ui_languages` VALUES (1,'English','en-us','English (United States)'),(2,'Hebrew','he-il','עברית (ישראל)');
/*!40000 ALTER TABLE `ui_languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ui_translations`
--

DROP TABLE IF EXISTS `ui_translations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_translations`
--

LOCK TABLES `ui_translations` WRITE;
/*!40000 ALTER TABLE `ui_translations` DISABLE KEYS */;
INSERT INTO `ui_translations` VALUES (1,'payment_methods','name',1,2,'מזומן'),(2,'payment_methods','name',2,2,'כרטיס אשראי'),(3,'payment_methods','name',3,2,'העברה בנקאית'),(4,'payment_methods','name',4,2,'צ\'ק'),(5,'payment_methods','name',5,2,'ביט'),(6,'payment_methods','name',6,2,'אחר'),(7,'categories','name',1,2,'הוצאה חודשית'),(8,'categories','name',2,2,'לייפסטייל'),(9,'categories','name',3,2,'כיף ותחביבים'),(10,'categories','name',4,2,'אוכל בחוץ'),(11,'categories','name',5,2,'קניות'),(12,'categories','name',6,2,'חשבונות'),(13,'categories','name',7,2,'תחבורה+דלק');
/*!40000 ALTER TABLE `ui_translations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `idusers` int(11) NOT NULL AUTO_INCREMENT,
  `role` int(11) NOT NULL,
  `username` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idusers`),
  UNIQUE KEY `idusers_UNIQUE` (`idusers`),
  KEY `fkey_role_users` (`role`),
  CONSTRAINT `fkey_role_users` FOREIGN KEY (`role`) REFERENCES `roles` (`idroles`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,2,'yanoom','yanoom@gmail.com','0587268754','עושה זאת!'),(2,3,'Toffi','sunlighet@gmail.com','0587743639','My love <3');
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

-- Dump completed on 2018-10-02  5:41:52
