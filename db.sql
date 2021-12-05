-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: studentmanagementdb
-- ------------------------------------------------------
-- Server version	8.0.13

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `account` (
  `user_id` int(11) NOT NULL,
  `username` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `account_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'GV00001','$2b$12$jw/LB1NqrqGSE/c74S74kuZ2VkvM1lpCt4TBsMQf7Tvze89kgxUXW',2,1,'2021-11-23 01:42:11'),(3,'GV00002','$2b$12$q4vxMht1igN7zH2AoJIR.OI.dW46wqmuYqEhAJrJf85nQvTT1OH9K',2,1,'2021-11-23 19:21:42'),(4,'HS00001','$2b$12$J4q3CksLQOYAIGF/Q7NNvuM/QjwIJg2IRIeqFmkZcc.ZIYldXchVu',3,0,'2021-11-23 20:29:35'),(5,'HS00002','$2b$12$A.qeeBc4HzPonXg8n9oqRuz26Hnk04zLBgEpMDEGPQbBxiUqiTjwK',3,1,'2021-11-23 21:21:06'),(6,'HS00003','$2b$12$puFO7VYSJFh0pymSSukBUuhqexBZRYRcNyQETKKADM2MJTorV4ZdC',3,1,'2021-11-23 21:21:06'),(8,'HS00004','$2b$12$qTs1mguuQZfu66CYBhGgTuwziHVf/Ap.LIO/X3OspYTjo759wN9X.',3,1,'2021-11-30 08:56:02'),(10,'PGV0001','$2b$12$SDH2pzsZS3SdKIRI6OZune/01NRvuq.IXVXLD0qpT4gwxyCbJhOEi',4,1,'2021-12-04 20:45:01'),(21,'admin','$2b$12$z.fcUGWZm6uIqSELQ95ZLOb40RCJn5Rhb/gGKokGUpFVTNZYeFYgi',1,1,'2021-12-05 13:52:34'),(27,'PGV003','$2b$12$Nu4C9IyK.NkyRnC4d3fPBebdNvhTmnQjiS6w9UHq/oWyZJfE6MAPu',4,1,'2021-12-05 12:18:53');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `administrator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `administrator_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
INSERT INTO `administrator` VALUES (2,21,'2021-12-05 11:10:53');
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('bdde44a96627');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `grade_id` int(11) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `class_name` (`class_name`),
  KEY `grade_id` (`grade_id`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'10A1',1,1,'2021-11-21 19:08:24'),(2,'10A2',1,1,'2021-11-21 19:08:24'),(3,'10A3',1,1,'2021-11-21 19:08:24');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classinfo`
--

DROP TABLE IF EXISTS `classinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `classinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` int(11) NOT NULL,
  `school_year_id` int(11) NOT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `amount_std` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `class_id` (`class_id`),
  KEY `school_year_id` (`school_year_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `classinfo_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`),
  CONSTRAINT `classinfo_ibfk_2` FOREIGN KEY (`school_year_id`) REFERENCES `schoolyear` (`id`),
  CONSTRAINT `classinfo_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classinfo`
--

LOCK TABLES `classinfo` WRITE;
/*!40000 ALTER TABLE `classinfo` DISABLE KEYS */;
INSERT INTO `classinfo` VALUES (1,1,1,NULL,NULL),(2,3,2,NULL,NULL);
/*!40000 ALTER TABLE `classinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_year` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_year` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `end_year` (`end_year`),
  UNIQUE KEY `start_year` (`start_year`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Khóa 2021','2021-2024','2021','2024',1);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detailstranscript`
--

DROP TABLE IF EXISTS `detailstranscript`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `detailstranscript` (
  `transcript_id` int(11) NOT NULL,
  `score_type_id` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`transcript_id`,`score_type_id`),
  KEY `score_type_id` (`score_type_id`),
  CONSTRAINT `detailstranscript_ibfk_1` FOREIGN KEY (`score_type_id`) REFERENCES `scoretype` (`id`),
  CONSTRAINT `detailstranscript_ibfk_2` FOREIGN KEY (`transcript_id`) REFERENCES `subjecttranscript` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detailstranscript`
--

LOCK TABLES `detailstranscript` WRITE;
/*!40000 ALTER TABLE `detailstranscript` DISABLE KEYS */;
INSERT INTO `detailstranscript` VALUES (14,1,5,'2021-12-04 22:13:59','2021-12-05 20:15:57'),(14,2,8,'2021-12-04 22:13:59','2021-12-05 01:30:03'),(14,3,10,'2021-12-05 01:34:12','2021-12-05 01:34:12'),(15,1,6,'2021-12-05 01:00:13','2021-12-05 01:04:20'),(15,2,9,'2021-12-05 01:29:53','2021-12-05 01:29:53'),(15,3,2,'2021-12-05 01:30:59','2021-12-05 01:32:07'),(16,1,7.85,'2021-12-05 01:14:14','2021-12-05 01:14:14'),(16,3,9,'2021-12-05 01:34:12','2021-12-05 01:34:12');
/*!40000 ALTER TABLE `detailstranscript` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `educationaloffice`
--

DROP TABLE IF EXISTS `educationaloffice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `educationaloffice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `educationaloffice_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `educationaloffice`
--

LOCK TABLES `educationaloffice` WRITE;
/*!40000 ALTER TABLE `educationaloffice` DISABLE KEYS */;
INSERT INTO `educationaloffice` VALUES (1,10,'2021-12-04 20:45:01'),(2,27,'2021-12-05 12:18:53');
/*!40000 ALTER TABLE `educationaloffice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ethnic`
--

DROP TABLE IF EXISTS `ethnic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `ethnic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ethnic_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ethnic_name` (`ethnic_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ethnic`
--

LOCK TABLES `ethnic` WRITE;
/*!40000 ALTER TABLE `ethnic` DISABLE KEYS */;
INSERT INTO `ethnic` VALUES (1,'Kinh');
/*!40000 ALTER TABLE `ethnic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `familyinfo`
--

DROP TABLE IF EXISTS `familyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `familyinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `full_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `current_residence` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `familyinfo_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `familyinfo`
--

LOCK TABLES `familyinfo` WRITE;
/*!40000 ALTER TABLE `familyinfo` DISABLE KEYS */;
INSERT INTO `familyinfo` VALUES (1,1,'','','','2021-12-01 14:28:05'),(2,1,'','','','2021-12-02 13:20:02'),(3,1,'','','','2021-12-02 14:23:35');
/*!40000 ALTER TABLE `familyinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gender`
--

DROP TABLE IF EXISTS `gender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `gender` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gender_name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gender_name` (`gender_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gender`
--

LOCK TABLES `gender` WRITE;
/*!40000 ALTER TABLE `gender` DISABLE KEYS */;
INSERT INTO `gender` VALUES (1,'Nam'),(2,'Nữ');
/*!40000 ALTER TABLE `gender` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `grade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `grade_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grade_name` (`grade_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,'Khối 10'),(2,'Khối 11'),(3,'Khối 12');
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inputscoretime`
--

DROP TABLE IF EXISTS `inputscoretime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `inputscoretime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `end_date` (`end_date`),
  UNIQUE KEY `start_date` (`start_date`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inputscoretime`
--

LOCK TABLES `inputscoretime` WRITE;
/*!40000 ALTER TABLE `inputscoretime` DISABLE KEYS */;
INSERT INTO `inputscoretime` VALUES (1,'2021-12-05 20:13:00','2021-12-05 20:16:00',1);
/*!40000 ALTER TABLE `inputscoretime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moreinfo`
--

DROP TABLE IF EXISTS `moreinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `moreinfo` (
  `user_id` int(11) NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_residence` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `note` text COLLATE utf8mb4_unicode_ci,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `moreinfo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moreinfo`
--

LOCK TABLES `moreinfo` WRITE;
/*!40000 ALTER TABLE `moreinfo` DISABLE KEYS */;
INSERT INTO `moreinfo` VALUES (1,'19110443@teacher.hcmute.edu.vn','123456666','','wibu chúa','2021-12-01 14:19:01'),(4,'19110042@student.hcmute.edu.vn','','','wibu chua','2021-12-01 14:28:05');
/*!40000 ALTER TABLE `moreinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nationality`
--

DROP TABLE IF EXISTS `nationality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `nationality` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nationality_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nationality_name` (`nationality_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nationality`
--

LOCK TABLES `nationality` WRITE;
/*!40000 ALTER TABLE `nationality` DISABLE KEYS */;
INSERT INTO `nationality` VALUES (1,'Việt Nam');
/*!40000 ALTER TABLE `nationality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resume`
--

DROP TABLE IF EXISTS `resume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `resume` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `uploaded_at` datetime NOT NULL,
  `modified_at` datetime DEFAULT NULL,
  `submitted_at` datetime NOT NULL,
  `confirm` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `resume_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resume`
--

LOCK TABLES `resume` WRITE;
/*!40000 ALTER TABLE `resume` DISABLE KEYS */;
INSERT INTO `resume` VALUES (1,4,'2021-12-04 19:59:38','2021-12-04 19:59:38','2021-12-04 19:59:38',0);
/*!40000 ALTER TABLE `resume` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumeimagefields`
--

DROP TABLE IF EXISTS `resumeimagefields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `resumeimagefields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `field_name` (`field_name`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `resumeimagefields_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumeimagefields`
--

LOCK TABLES `resumeimagefields` WRITE;
/*!40000 ALTER TABLE `resumeimagefields` DISABLE KEYS */;
INSERT INTO `resumeimagefields` VALUES (1,'Bản sao giấy khai sinh',3),(2,'Bản sao giấy tốt nghiệp tạm thời',3),(3,'Bản sao học bạ',3);
/*!40000 ALTER TABLE `resumeimagefields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumeimagestorage`
--

DROP TABLE IF EXISTS `resumeimagestorage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `resumeimagestorage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resume_id` int(11) DEFAULT NULL,
  `field_id` int(11) DEFAULT NULL,
  `image_path` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_public_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `field_id` (`field_id`),
  KEY `resume_id` (`resume_id`),
  CONSTRAINT `resumeimagestorage_ibfk_1` FOREIGN KEY (`field_id`) REFERENCES `resumeimagefields` (`id`) ON DELETE SET NULL,
  CONSTRAINT `resumeimagestorage_ibfk_2` FOREIGN KEY (`resume_id`) REFERENCES `resume` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumeimagestorage`
--

LOCK TABLES `resumeimagestorage` WRITE;
/*!40000 ALTER TABLE `resumeimagestorage` DISABLE KEYS */;
INSERT INTO `resumeimagestorage` VALUES (1,1,1,'https://res.cloudinary.com/dsqpeicna/image/upload/v1638622107/cvf2kc9ipnop70pfe9nh.jpg','cvf2kc9ipnop70pfe9nh'),(2,1,2,'https://res.cloudinary.com/dsqpeicna/image/upload/v1638622108/jcro4wzyiowfbgw4se8m.jpg','jcro4wzyiowfbgw4se8m'),(3,1,3,'https://res.cloudinary.com/dsqpeicna/image/upload/v1638622109/dlizsz4a3m0epn5yzrvb.jpg','dlizsz4a3m0epn5yzrvb');
/*!40000 ALTER TABLE `resumeimagestorage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'Admin','2021-11-23 01:31:39'),(2,'Giáo Viên','2021-11-23 01:31:39'),(3,'Học Sinh','2021-11-23 01:31:39'),(4,'Giáo vụ','2021-12-04 20:45:01');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schoolyear`
--

DROP TABLE IF EXISTS `schoolyear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `schoolyear` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `year` (`year`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schoolyear`
--

LOCK TABLES `schoolyear` WRITE;
/*!40000 ALTER TABLE `schoolyear` DISABLE KEYS */;
INSERT INTO `schoolyear` VALUES (1,'2021-2022',1,'2021-11-21 19:08:24'),(2,'2020-2021',0,'2021-11-22 00:49:39');
/*!40000 ALTER TABLE `schoolyear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scoretype`
--

DROP TABLE IF EXISTS `scoretype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `scoretype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `score_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `multiplier` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `score_name` (`score_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scoretype`
--

LOCK TABLES `scoretype` WRITE;
/*!40000 ALTER TABLE `scoretype` DISABLE KEYS */;
INSERT INTO `scoretype` VALUES (1,'15 phút',1,1),(2,'1 tiết',1,1),(3,'Cuối Kì',2,1);
/*!40000 ALTER TABLE `scoretype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `semester` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_name` (`display_name`),
  UNIQUE KEY `semester_name` (`semester_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'Học Kỳ I','HKI','2021-11-21 19:08:24',1),(2,'Học Kỳ II','HKII','2021-11-21 19:08:24',0);
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'HS00001',4,1,'2021-11-23 20:29:35'),(2,'HS00002',5,1,'2021-11-23 21:21:06'),(3,'HS00003',6,1,'2021-11-23 21:21:06'),(4,'HS00004',8,1,'2021-11-30 08:56:02');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentinclass`
--

DROP TABLE IF EXISTS `studentinclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `studentinclass` (
  `class_info_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`class_info_id`,`student_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `studentinclass_ibfk_1` FOREIGN KEY (`class_info_id`) REFERENCES `classinfo` (`id`),
  CONSTRAINT `studentinclass_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentinclass`
--

LOCK TABLES `studentinclass` WRITE;
/*!40000 ALTER TABLE `studentinclass` DISABLE KEYS */;
INSERT INTO `studentinclass` VALUES (1,1),(1,2),(2,3),(1,4);
/*!40000 ALTER TABLE `studentinclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) NOT NULL,
  `letter_point` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject_name` (`subject_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (1,'Ngữ Văn',1,0,'2021-11-21 19:08:24'),(2,'Toán',1,0,'2021-11-21 19:08:24'),(3,'Giáo Dục Công Dân',1,0,'2021-12-05 12:05:23');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjecttranscript`
--

DROP TABLE IF EXISTS `subjecttranscript`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `subjecttranscript` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `transcript_info_id` int(11) NOT NULL,
  `score_average` float DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`,`student_id`),
  KEY `student_id` (`student_id`),
  KEY `transcript_info_id` (`transcript_info_id`),
  CONSTRAINT `subjecttranscript_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `subjecttranscript_ibfk_2` FOREIGN KEY (`transcript_info_id`) REFERENCES `teachingassignment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjecttranscript`
--

LOCK TABLES `subjecttranscript` WRITE;
/*!40000 ALTER TABLE `subjecttranscript` DISABLE KEYS */;
INSERT INTO `subjecttranscript` VALUES (1,1,36,NULL,'2021-11-30 08:33:05'),(2,2,36,NULL,'2021-11-30 08:33:05'),(3,1,37,NULL,'2021-11-30 08:33:05'),(4,2,37,NULL,'2021-11-30 08:33:05'),(5,4,36,NULL,'2021-11-30 08:56:02'),(6,4,37,NULL,'2021-11-30 08:56:02'),(8,1,36,NULL,'2021-11-30 10:15:14'),(9,1,37,NULL,'2021-11-30 10:15:14'),(11,2,36,NULL,'2021-11-30 10:15:14'),(12,2,37,NULL,'2021-11-30 10:15:14'),(14,1,38,8.25,'2021-12-04 11:33:54'),(15,2,38,4.75,'2021-12-04 11:33:54'),(16,4,38,8.62,'2021-12-04 11:33:54'),(17,1,39,NULL,'2021-12-04 11:33:54'),(18,2,39,NULL,'2021-12-04 11:33:54'),(19,4,39,NULL,'2021-12-04 11:33:54');
/*!40000 ALTER TABLE `subjecttranscript` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`),
  CONSTRAINT `teacher_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (1,'GV00001',1,3,'2021-11-23 01:36:03'),(3,'GV00002',3,1,'2021-11-23 01:42:11');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachingassignment`
--

DROP TABLE IF EXISTS `teachingassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `teachingassignment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `class_info_id` int(11) NOT NULL,
  `semester_id` int(11) NOT NULL,
  `school_year_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `class_info_id` (`class_info_id`),
  KEY `school_year_id` (`school_year_id`),
  KEY `semester_id` (`semester_id`),
  KEY `subject_id` (`subject_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `teachingassignment_ibfk_1` FOREIGN KEY (`class_info_id`) REFERENCES `classinfo` (`id`),
  CONSTRAINT `teachingassignment_ibfk_2` FOREIGN KEY (`school_year_id`) REFERENCES `schoolyear` (`id`),
  CONSTRAINT `teachingassignment_ibfk_3` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`),
  CONSTRAINT `teachingassignment_ibfk_4` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`),
  CONSTRAINT `teachingassignment_ibfk_5` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachingassignment`
--

LOCK TABLES `teachingassignment` WRITE;
/*!40000 ALTER TABLE `teachingassignment` DISABLE KEYS */;
INSERT INTO `teachingassignment` VALUES (36,1,3,1,1,1,'2021-11-30 08:33:05'),(37,1,3,1,2,1,'2021-11-30 08:33:05'),(38,2,1,1,1,1,'2021-12-04 11:33:54'),(39,2,1,1,2,1,'2021-12-04 11:33:54');
/*!40000 ALTER TABLE `teachingassignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender_id` int(11) NOT NULL,
  `birthdate` date NOT NULL,
  `ethnic_id` int(11) NOT NULL,
  `nationality_id` int(11) NOT NULL,
  `permanent_address` varchar(250) COLLATE utf8mb4_unicode_ci NOT NULL,
  `home_town` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `image_id` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ethnic_id` (`ethnic_id`),
  KEY `gender_id` (`gender_id`),
  KEY `nationality_id` (`nationality_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`ethnic_id`) REFERENCES `ethnic` (`id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`gender_id`) REFERENCES `gender` (`id`),
  CONSTRAINT `user_ibfk_3` FOREIGN KEY (`nationality_id`) REFERENCES `nationality` (`id`),
  CONSTRAINT `user_ibfk_4` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Trần Quang',1,'2000-11-13',1,1,'Nam Trà My','Quảng Nam','https://res.cloudinary.com/dsqpeicna/image/upload/v1638680176/tdscb4gf4erq4uqb2gvv.jpg',2,'2021-11-23 01:36:03','tdscb4gf4erq4uqb2gvv'),(3,'Võ Thành Vinh',1,'1997-08-11',1,1,'Quảng Ngãi','Quảng Ngãi',NULL,2,'2021-11-23 01:42:11',NULL),(4,'Nguyễn Quang Vinh',1,'2001-04-03',1,1,'Thủ Đức','Hà Tĩnh','https://res.cloudinary.com/dsqpeicna/image/upload/v1638637182/xcwkxg4wdsp4qyhpcxgq.jpg',3,'2021-11-23 20:29:35','xcwkxg4wdsp4qyhpcxgq'),(5,'Nguyễn Thanh Hoàng',1,'2001-02-07',1,1,'Quận 12','Huế',NULL,3,'2021-11-23 21:21:06',NULL),(6,'Thiều Quang Huy',1,'2001-12-02',1,1,'Tô Ngọc Vân','Thanh Hóa','https://res.cloudinary.com/dsqpeicna/image/upload/v1638679910/ntyozt79ksmjcc2g4gwp.png',3,'2021-11-23 21:21:06','ntyozt79ksmjcc2g4gwp'),(8,'Lưu Quang Vũ',1,'2005-02-14',1,1,'TP Hồ Chí Minh','Vũng Tàu',NULL,3,'2021-11-30 08:56:02',NULL),(10,'Lê Dương Quá',1,'1991-04-14',1,1,'1 Võ Văn Ngân, Thủ Đức','Thanh Hóa',NULL,4,'2021-12-04 20:45:01',NULL),(21,'Nguyễn Văn Trường',1,'2001-08-08',1,1,'Gò Vấp','Quảng Nam','https://res.cloudinary.com/dsqpeicna/image/upload/v1638680354/npf4ypyj9u15te28hj3q.jpg',1,'2021-12-05 11:10:52','npf4ypyj9u15te28hj3q'),(24,'Lê Văn Dương',1,'2008-12-01',1,1,'Tây Thạnh','Bến Tre','https://res.cloudinary.com/dsqpeicna/image/upload/v1638678740/c0ptkz7w9fnyl8xtpn2z.jpg',3,'2021-12-05 11:32:01','c0ptkz7w9fnyl8xtpn2z'),(27,'Lâm Tâm Như',2,'1994-01-12',1,1,'35 Phạm Văn Đồng','Quảng Ninh','https://res.cloudinary.com/dsqpeicna/image/upload/v1638681645/coygtmdmgtsmsamfjn86.jpg',4,'2021-12-05 12:18:53','coygtmdmgtsmsamfjn86');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-05 23:57:22
