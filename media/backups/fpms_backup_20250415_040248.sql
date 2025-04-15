/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.6.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: FPMSdb
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `administration_activitylog`
--

DROP TABLE IF EXISTS `administration_activitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_activitylog` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `action` varchar(10) NOT NULL,
  `model` varchar(100) NOT NULL,
  `object_id` varchar(100) NOT NULL,
  `details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`details`)),
  `ip_address` char(39) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `administration_activ_user_id_f7dec6cf_fk_administr` (`user_id`),
  CONSTRAINT `administration_activ_user_id_f7dec6cf_fk_administr` FOREIGN KEY (`user_id`) REFERENCES `administration_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_activitylog`
--

LOCK TABLES `administration_activitylog` WRITE;
/*!40000 ALTER TABLE `administration_activitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_activitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_backupconfig`
--

DROP TABLE IF EXISTS `administration_backupconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_backupconfig` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `schedule_type` varchar(10) NOT NULL,
  `schedule_time` time(6) NOT NULL,
  `last_run` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `retain_days` int(10) unsigned NOT NULL CHECK (`retain_days` >= 0),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_backupconfig`
--

LOCK TABLES `administration_backupconfig` WRITE;
/*!40000 ALTER TABLE `administration_backupconfig` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_backupconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_backuprecord`
--

DROP TABLE IF EXISTS `administration_backuprecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_backuprecord` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `backup_file` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `file_size` int(10) unsigned NOT NULL CHECK (`file_size` >= 0),
  `is_automated` tinyint(1) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `administration_backu_created_by_id_0c5a2106_fk_administr` (`created_by_id`),
  CONSTRAINT `administration_backu_created_by_id_0c5a2106_fk_administr` FOREIGN KEY (`created_by_id`) REFERENCES `administration_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_backuprecord`
--

LOCK TABLES `administration_backuprecord` WRITE;
/*!40000 ALTER TABLE `administration_backuprecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_backuprecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_department`
--

DROP TABLE IF EXISTS `administration_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_department` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_department`
--

LOCK TABLES `administration_department` WRITE;
/*!40000 ALTER TABLE `administration_department` DISABLE KEYS */;
INSERT INTO `administration_department` VALUES
(1,'Production','');
/*!40000 ALTER TABLE `administration_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_healthmetric`
--

DROP TABLE IF EXISTS `administration_healthmetric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_healthmetric` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `cpu_usage` double NOT NULL,
  `memory_usage` double NOT NULL,
  `disk_usage` double NOT NULL,
  `disk_space` double NOT NULL,
  `response_time` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_healthmetric`
--

LOCK TABLES `administration_healthmetric` WRITE;
/*!40000 ALTER TABLE `administration_healthmetric` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_healthmetric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_role`
--

DROP TABLE IF EXISTS `administration_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `permissions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`permissions`)),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_role`
--

LOCK TABLES `administration_role` WRITE;
/*!40000 ALTER TABLE `administration_role` DISABLE KEYS */;
INSERT INTO `administration_role` VALUES
(1,'operator','','[]');
/*!40000 ALTER TABLE `administration_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_systemsetting`
--

DROP TABLE IF EXISTS `administration_systemsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_systemsetting` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `key` varchar(100) NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`value`)),
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_systemsetting`
--

LOCK TABLES `administration_systemsetting` WRITE;
/*!40000 ALTER TABLE `administration_systemsetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_systemsetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_user`
--

DROP TABLE IF EXISTS `administration_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `account_status` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `department_id` bigint(20) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `administration_user_department_id_12dea468_fk_administr` (`department_id`),
  KEY `administration_user_role_id_07f79130_fk_administration_role_id` (`role_id`),
  CONSTRAINT `administration_user_department_id_12dea468_fk_administr` FOREIGN KEY (`department_id`) REFERENCES `administration_department` (`id`),
  CONSTRAINT `administration_user_role_id_07f79130_fk_administration_role_id` FOREIGN KEY (`role_id`) REFERENCES `administration_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_user`
--

LOCK TABLES `administration_user` WRITE;
/*!40000 ALTER TABLE `administration_user` DISABLE KEYS */;
INSERT INTO `administration_user` VALUES
(1,'pbkdf2_sha256$870000$D5w1JhSeKEheD2c7t2GbNo$d+HHZ1WZGhI9lGH2oRfc3czG9i00fJ/dWOmCKGgNKZk=',NULL,0,'','',0,1,'2025-04-15 00:34:40.912049','younis','+9876543210',1,'younis@gmail.com',1,1);
/*!40000 ALTER TABLE `administration_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_user_groups`
--

DROP TABLE IF EXISTS `administration_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `administration_user_groups_user_id_group_id_97943ac2_uniq` (`user_id`,`group_id`),
  KEY `administration_user_groups_group_id_43b1e17e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `administration_user__user_id_fcbab611_fk_administr` FOREIGN KEY (`user_id`) REFERENCES `administration_user` (`id`),
  CONSTRAINT `administration_user_groups_group_id_43b1e17e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_user_groups`
--

LOCK TABLES `administration_user_groups` WRITE;
/*!40000 ALTER TABLE `administration_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administration_user_user_permissions`
--

DROP TABLE IF EXISTS `administration_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administration_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `administration_user_user_user_id_permission_id_1258dc72_uniq` (`user_id`,`permission_id`),
  KEY `administration_user__permission_id_5b940bd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `administration_user__permission_id_5b940bd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `administration_user__user_id_69e83b80_fk_administr` FOREIGN KEY (`user_id`) REFERENCES `administration_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administration_user_user_permissions`
--

LOCK TABLES `administration_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `administration_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `administration_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add Token',6,'add_token'),
(22,'Can change Token',6,'change_token'),
(23,'Can delete Token',6,'delete_token'),
(24,'Can view Token',6,'view_token'),
(25,'Can add Token',7,'add_tokenproxy'),
(26,'Can change Token',7,'change_tokenproxy'),
(27,'Can delete Token',7,'delete_tokenproxy'),
(28,'Can view Token',7,'view_tokenproxy'),
(29,'Can add backup config',8,'add_backupconfig'),
(30,'Can change backup config',8,'change_backupconfig'),
(31,'Can delete backup config',8,'delete_backupconfig'),
(32,'Can view backup config',8,'view_backupconfig'),
(33,'Can add department',9,'add_department'),
(34,'Can change department',9,'change_department'),
(35,'Can delete department',9,'delete_department'),
(36,'Can view department',9,'view_department'),
(37,'Can add health metric',10,'add_healthmetric'),
(38,'Can change health metric',10,'change_healthmetric'),
(39,'Can delete health metric',10,'delete_healthmetric'),
(40,'Can view health metric',10,'view_healthmetric'),
(41,'Can add role',11,'add_role'),
(42,'Can change role',11,'change_role'),
(43,'Can delete role',11,'delete_role'),
(44,'Can view role',11,'view_role'),
(45,'Can add system setting',12,'add_systemsetting'),
(46,'Can change system setting',12,'change_systemsetting'),
(47,'Can delete system setting',12,'delete_systemsetting'),
(48,'Can view system setting',12,'view_systemsetting'),
(49,'Can add User',13,'add_user'),
(50,'Can change User',13,'change_user'),
(51,'Can delete User',13,'delete_user'),
(52,'Can view User',13,'view_user'),
(53,'Can add activity log',14,'add_activitylog'),
(54,'Can change activity log',14,'change_activitylog'),
(55,'Can delete activity log',14,'delete_activitylog'),
(56,'Can view activity log',14,'view_activitylog'),
(57,'Can add backup record',15,'add_backuprecord'),
(58,'Can change backup record',15,'change_backuprecord'),
(59,'Can delete backup record',15,'delete_backuprecord'),
(60,'Can view backup record',15,'view_backuprecord'),
(61,'Can add work center',16,'add_workcenter'),
(62,'Can change work center',16,'change_workcenter'),
(63,'Can delete work center',16,'delete_workcenter'),
(64,'Can view work center',16,'view_workcenter'),
(65,'Can add workstation',17,'add_workstation'),
(66,'Can change workstation',17,'change_workstation'),
(67,'Can delete workstation',17,'delete_workstation'),
(68,'Can view workstation',17,'view_workstation'),
(69,'Can add maintenance',18,'add_maintenance'),
(70,'Can change maintenance',18,'change_maintenance'),
(71,'Can delete maintenance',18,'delete_maintenance'),
(72,'Can view maintenance',18,'view_maintenance'),
(73,'Can add bom',19,'add_bom'),
(74,'Can change bom',19,'change_bom'),
(75,'Can delete bom',19,'delete_bom'),
(76,'Can view bom',19,'view_bom'),
(77,'Can add inspection checkpoint',20,'add_inspectioncheckpoint'),
(78,'Can change inspection checkpoint',20,'change_inspectioncheckpoint'),
(79,'Can delete inspection checkpoint',20,'delete_inspectioncheckpoint'),
(80,'Can view inspection checkpoint',20,'view_inspectioncheckpoint'),
(81,'Can add work center',21,'add_workcenter'),
(82,'Can change work center',21,'change_workcenter'),
(83,'Can delete work center',21,'delete_workcenter'),
(84,'Can view work center',21,'view_workcenter'),
(85,'Can add component',22,'add_component'),
(86,'Can change component',22,'change_component'),
(87,'Can delete component',22,'delete_component'),
(88,'Can view component',22,'view_component'),
(89,'Can add product',23,'add_product'),
(90,'Can change product',23,'change_product'),
(91,'Can delete product',23,'delete_product'),
(92,'Can view product',23,'view_product'),
(93,'Can add stage',24,'add_stage'),
(94,'Can change stage',24,'change_stage'),
(95,'Can delete stage',24,'delete_stage'),
(96,'Can view stage',24,'view_stage'),
(97,'Can add workflow',25,'add_workflow'),
(98,'Can change workflow',25,'change_workflow'),
(99,'Can delete workflow',25,'delete_workflow'),
(100,'Can view workflow',25,'view_workflow'),
(101,'Can add production line',26,'add_productionline'),
(102,'Can change production line',26,'change_productionline'),
(103,'Can delete production line',26,'delete_productionline'),
(104,'Can view production line',26,'view_productionline'),
(105,'Can add production order',27,'add_productionorder'),
(106,'Can change production order',27,'change_productionorder'),
(107,'Can delete production order',27,'delete_productionorder'),
(108,'Can view production order',27,'view_productionorder'),
(109,'Can add rescheduling',28,'add_rescheduling'),
(110,'Can change rescheduling',28,'change_rescheduling'),
(111,'Can delete rescheduling',28,'delete_rescheduling'),
(112,'Can view rescheduling',28,'view_rescheduling'),
(113,'Can add Work Instruction',29,'add_workinstruction'),
(114,'Can change Work Instruction',29,'change_workinstruction'),
(115,'Can delete Work Instruction',29,'delete_workinstruction'),
(116,'Can view Work Instruction',29,'view_workinstruction'),
(117,'Can add Work Order',30,'add_workorder'),
(118,'Can change Work Order',30,'change_workorder'),
(119,'Can delete Work Order',30,'delete_workorder'),
(120,'Can view Work Order',30,'view_workorder'),
(121,'Can add Job Card',31,'add_jobcard'),
(122,'Can change Job Card',31,'change_jobcard'),
(123,'Can delete Job Card',31,'delete_jobcard'),
(124,'Can view Job Card',31,'view_jobcard'),
(125,'Can add inspection',32,'add_inspection'),
(126,'Can change inspection',32,'change_inspection'),
(127,'Can delete inspection',32,'delete_inspection'),
(128,'Can view inspection',32,'view_inspection'),
(129,'Can add inspection checklist',33,'add_inspectionchecklist'),
(130,'Can change inspection checklist',33,'change_inspectionchecklist'),
(131,'Can delete inspection checklist',33,'delete_inspectionchecklist'),
(132,'Can view inspection checklist',33,'view_inspectionchecklist'),
(133,'Can add rework request',34,'add_reworkrequest'),
(134,'Can change rework request',34,'change_reworkrequest'),
(135,'Can delete rework request',34,'delete_reworkrequest'),
(136,'Can view rework request',34,'view_reworkrequest'),
(137,'Can add issue',35,'add_issue'),
(138,'Can change issue',35,'change_issue'),
(139,'Can delete issue',35,'delete_issue'),
(140,'Can view issue',35,'view_issue'),
(141,'Can add report',36,'add_report'),
(142,'Can change report',36,'change_report'),
(143,'Can delete report',36,'delete_report'),
(144,'Can view report',36,'view_report');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_administration_user_id` FOREIGN KEY (`user_id`) REFERENCES `administration_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_administration_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_administration_user_id` FOREIGN KEY (`user_id`) REFERENCES `administration_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(14,'administration','activitylog'),
(8,'administration','backupconfig'),
(15,'administration','backuprecord'),
(9,'administration','department'),
(10,'administration','healthmetric'),
(11,'administration','role'),
(12,'administration','systemsetting'),
(13,'administration','user'),
(3,'auth','group'),
(2,'auth','permission'),
(6,'authtoken','token'),
(7,'authtoken','tokenproxy'),
(4,'contenttypes','contenttype'),
(32,'quality_control','inspection'),
(33,'quality_control','inspectionchecklist'),
(34,'quality_control','reworkrequest'),
(35,'reports','issue'),
(36,'reports','report'),
(5,'sessions','session'),
(31,'work_instructions','jobcard'),
(29,'work_instructions','workinstruction'),
(30,'work_instructions','workorder'),
(18,'workcentre','maintenance'),
(16,'workcentre','workcenter'),
(17,'workcentre','workstation'),
(19,'workflow','bom'),
(22,'workflow','component'),
(20,'workflow','inspectioncheckpoint'),
(23,'workflow','product'),
(26,'workflow','productionline'),
(27,'workflow','productionorder'),
(28,'workflow','rescheduling'),
(24,'workflow','stage'),
(21,'workflow','workcenter'),
(25,'workflow','workflow');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-04-15 00:15:42.004108'),
(2,'contenttypes','0002_remove_content_type_name','2025-04-15 00:15:42.076816'),
(3,'auth','0001_initial','2025-04-15 00:15:42.341670'),
(4,'auth','0002_alter_permission_name_max_length','2025-04-15 00:15:42.425305'),
(5,'auth','0003_alter_user_email_max_length','2025-04-15 00:15:42.441308'),
(6,'auth','0004_alter_user_username_opts','2025-04-15 00:15:42.471376'),
(7,'auth','0005_alter_user_last_login_null','2025-04-15 00:15:42.485362'),
(8,'auth','0006_require_contenttypes_0002','2025-04-15 00:15:42.487357'),
(9,'auth','0007_alter_validators_add_error_messages','2025-04-15 00:15:42.505556'),
(10,'auth','0008_alter_user_username_max_length','2025-04-15 00:15:42.555942'),
(11,'auth','0009_alter_user_last_name_max_length','2025-04-15 00:15:42.576942'),
(12,'auth','0010_alter_group_name_max_length','2025-04-15 00:15:42.618995'),
(13,'auth','0011_update_proxy_permissions','2025-04-15 00:15:42.641475'),
(14,'auth','0012_alter_user_first_name_max_length','2025-04-15 00:15:42.676747'),
(15,'administration','0001_initial','2025-04-15 00:15:43.189159'),
(16,'admin','0001_initial','2025-04-15 00:15:43.359740'),
(17,'admin','0002_logentry_remove_auto_add','2025-04-15 00:15:43.367863'),
(18,'admin','0003_logentry_add_action_flag_choices','2025-04-15 00:15:43.443890'),
(19,'authtoken','0001_initial','2025-04-15 00:15:43.595952'),
(20,'authtoken','0002_auto_20160226_1747','2025-04-15 00:15:43.721150'),
(21,'authtoken','0003_tokenproxy','2025-04-15 00:15:43.730611'),
(22,'authtoken','0004_alter_tokenproxy_options','2025-04-15 00:15:43.736600'),
(23,'workflow','0001_initial','2025-04-15 00:15:44.400051'),
(24,'workflow','0002_productionline_productionorder_rescheduling','2025-04-15 00:15:45.036829'),
(25,'workcentre','0001_initial','2025-04-15 00:15:45.392242'),
(26,'workcentre','0002_maintenance_assigned_staff','2025-04-15 00:15:45.547756'),
(27,'work_instructions','0001_initial','2025-04-15 00:15:46.333538'),
(28,'quality_control','0001_initial','2025-04-15 00:15:47.149215'),
(29,'quality_control','0002_remove_inspection_created_at_and_more','2025-04-15 00:15:48.183765'),
(30,'quality_control','0003_inspection_created_at_inspection_updated_at_and_more','2025-04-15 00:15:49.322226'),
(31,'reports','0001_initial','2025-04-15 00:15:49.815877'),
(32,'sessions','0001_initial','2025-04-15 00:15:49.992142'),
(33,'workcentre','0003_alter_workstation_machines_and_more','2025-04-15 00:15:50.932293'),
(34,'workcentre','0004_alter_workstation_machines_alter_workstation_tools','2025-04-15 00:15:50.962203');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quality_control_inspection`
--

DROP TABLE IF EXISTS `quality_control_inspection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quality_control_inspection` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `defect_type` varchar(100) NOT NULL,
  `severity` varchar(20) NOT NULL,
  `affected_component` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `final_decision` varchar(20) NOT NULL,
  `work_order_id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quality_control_insp_work_order_id_bfc28d39_fk_work_inst` (`work_order_id`),
  CONSTRAINT `quality_control_insp_work_order_id_bfc28d39_fk_work_inst` FOREIGN KEY (`work_order_id`) REFERENCES `work_instructions_workorder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quality_control_inspection`
--

LOCK TABLES `quality_control_inspection` WRITE;
/*!40000 ALTER TABLE `quality_control_inspection` DISABLE KEYS */;
/*!40000 ALTER TABLE `quality_control_inspection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quality_control_inspectionchecklist`
--

DROP TABLE IF EXISTS `quality_control_inspectionchecklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quality_control_inspectionchecklist` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `state` varchar(10) DEFAULT NULL,
  `note` longtext DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `inspection_id` bigint(20) NOT NULL,
  `job_card_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quality_control_insp_inspection_id_035e7b2e_fk_quality_c` (`inspection_id`),
  KEY `quality_control_insp_job_card_id_b717f918_fk_work_inst` (`job_card_id`),
  CONSTRAINT `quality_control_insp_inspection_id_035e7b2e_fk_quality_c` FOREIGN KEY (`inspection_id`) REFERENCES `quality_control_inspection` (`id`),
  CONSTRAINT `quality_control_insp_job_card_id_b717f918_fk_work_inst` FOREIGN KEY (`job_card_id`) REFERENCES `work_instructions_jobcard` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quality_control_inspectionchecklist`
--

LOCK TABLES `quality_control_inspectionchecklist` WRITE;
/*!40000 ALTER TABLE `quality_control_inspectionchecklist` DISABLE KEYS */;
/*!40000 ALTER TABLE `quality_control_inspectionchecklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quality_control_reworkrequest`
--

DROP TABLE IF EXISTS `quality_control_reworkrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quality_control_reworkrequest` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `inspection_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inspection_id` (`inspection_id`),
  CONSTRAINT `quality_control_rewo_inspection_id_c8d31b4e_fk_quality_c` FOREIGN KEY (`inspection_id`) REFERENCES `quality_control_inspection` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quality_control_reworkrequest`
--

LOCK TABLES `quality_control_reworkrequest` WRITE;
/*!40000 ALTER TABLE `quality_control_reworkrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `quality_control_reworkrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_issue`
--

DROP TABLE IF EXISTS `reports_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_issue` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `category` varchar(100) NOT NULL,
  `affected_item` varchar(100) NOT NULL,
  `priority` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_issue`
--

LOCK TABLES `reports_issue` WRITE;
/*!40000 ALTER TABLE `reports_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_report`
--

DROP TABLE IF EXISTS `reports_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `report_type` varchar(20) NOT NULL,
  `shift` varchar(20) NOT NULL,
  `date_range_type` varchar(20) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `defect_type` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `production_line_id` bigint(20) NOT NULL,
  `workstation_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reports_report_production_line_id_e89bb171_fk_workflow_` (`production_line_id`),
  KEY `reports_report_workstation_id_e6644446_fk_workcentr` (`workstation_id`),
  CONSTRAINT `reports_report_production_line_id_e89bb171_fk_workflow_` FOREIGN KEY (`production_line_id`) REFERENCES `workflow_productionline` (`id`),
  CONSTRAINT `reports_report_workstation_id_e6644446_fk_workcentr` FOREIGN KEY (`workstation_id`) REFERENCES `workcentre_workstation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_report`
--

LOCK TABLES `reports_report` WRITE;
/*!40000 ALTER TABLE `reports_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_instructions_jobcard`
--

DROP TABLE IF EXISTS `work_instructions_jobcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `work_instructions_jobcard` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) NOT NULL,
  `required_tools` longtext NOT NULL,
  `required_materials` longtext NOT NULL,
  `status` varchar(50) NOT NULL,
  `assigned_to_id` bigint(20) DEFAULT NULL,
  `work_order_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `work_instructions_jo_assigned_to_id_897385e3_fk_workcentr` (`assigned_to_id`),
  KEY `work_instructions_jo_work_order_id_3bcb9d13_fk_work_inst` (`work_order_id`),
  CONSTRAINT `work_instructions_jo_assigned_to_id_897385e3_fk_workcentr` FOREIGN KEY (`assigned_to_id`) REFERENCES `workcentre_workcenter` (`id`),
  CONSTRAINT `work_instructions_jo_work_order_id_3bcb9d13_fk_work_inst` FOREIGN KEY (`work_order_id`) REFERENCES `work_instructions_workorder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_instructions_jobcard`
--

LOCK TABLES `work_instructions_jobcard` WRITE;
/*!40000 ALTER TABLE `work_instructions_jobcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `work_instructions_jobcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_instructions_workinstruction`
--

DROP TABLE IF EXISTS `work_instructions_workinstruction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `work_instructions_workinstruction` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `task_steps` longtext NOT NULL,
  `tools_required` longtext NOT NULL,
  `materials_required` longtext NOT NULL,
  `step_description` longtext NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_instructions_workinstruction`
--

LOCK TABLES `work_instructions_workinstruction` WRITE;
/*!40000 ALTER TABLE `work_instructions_workinstruction` DISABLE KEYS */;
/*!40000 ALTER TABLE `work_instructions_workinstruction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_instructions_workorder`
--

DROP TABLE IF EXISTS `work_instructions_workorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `work_instructions_workorder` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `quantity_required` int(10) unsigned NOT NULL CHECK (`quantity_required` >= 0),
  `due_date` datetime(6) NOT NULL,
  `priority` varchar(50) NOT NULL,
  `production_line_id` bigint(20) DEFAULT NULL,
  `work_instruction_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `work_instructions_wo_production_line_id_d6eb738b_fk_workflow_` (`production_line_id`),
  KEY `work_instructions_wo_work_instruction_id_142d1ffb_fk_work_inst` (`work_instruction_id`),
  CONSTRAINT `work_instructions_wo_production_line_id_d6eb738b_fk_workflow_` FOREIGN KEY (`production_line_id`) REFERENCES `workflow_productionline` (`id`),
  CONSTRAINT `work_instructions_wo_work_instruction_id_142d1ffb_fk_work_inst` FOREIGN KEY (`work_instruction_id`) REFERENCES `work_instructions_workinstruction` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_instructions_workorder`
--

LOCK TABLES `work_instructions_workorder` WRITE;
/*!40000 ALTER TABLE `work_instructions_workorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `work_instructions_workorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workcentre_maintenance`
--

DROP TABLE IF EXISTS `workcentre_maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workcentre_maintenance` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `maintenance_date` date NOT NULL,
  `maintenance_time` time(6) NOT NULL,
  `recurrence` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `staff_notes` longtext DEFAULT NULL,
  `workstation_id` bigint(20) NOT NULL,
  `assigned_staff` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`assigned_staff`)),
  PRIMARY KEY (`id`),
  KEY `workcentre_maintenan_workstation_id_1982da72_fk_workcentr` (`workstation_id`),
  CONSTRAINT `workcentre_maintenan_workstation_id_1982da72_fk_workcentr` FOREIGN KEY (`workstation_id`) REFERENCES `workcentre_workstation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workcentre_maintenance`
--

LOCK TABLES `workcentre_maintenance` WRITE;
/*!40000 ALTER TABLE `workcentre_maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `workcentre_maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workcentre_workcenter`
--

DROP TABLE IF EXISTS `workcentre_workcenter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workcentre_workcenter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `remarks` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workcentre_workcenter`
--

LOCK TABLES `workcentre_workcenter` WRITE;
/*!40000 ALTER TABLE `workcentre_workcenter` DISABLE KEYS */;
/*!40000 ALTER TABLE `workcentre_workcenter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workcentre_workstation`
--

DROP TABLE IF EXISTS `workcentre_workstation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workcentre_workstation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `capacity` int(11) NOT NULL,
  `description` longtext DEFAULT NULL,
  `machines` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`machines`)),
  `tools` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`tools`)),
  `work_center` longtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workcentre_workstation`
--

LOCK TABLES `workcentre_workstation` WRITE;
/*!40000 ALTER TABLE `workcentre_workstation` DISABLE KEYS */;
/*!40000 ALTER TABLE `workcentre_workstation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_bom`
--

DROP TABLE IF EXISTS `workflow_bom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_bom` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `product_code` varchar(50) NOT NULL,
  `version` varchar(50) NOT NULL,
  `status` varchar(20) NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `created_by` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_bom`
--

LOCK TABLES `workflow_bom` WRITE;
/*!40000 ALTER TABLE `workflow_bom` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_bom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_component`
--

DROP TABLE IF EXISTS `workflow_component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_component` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `part_number` varchar(50) NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `unit` varchar(20) NOT NULL,
  `unit_cost` decimal(10,2) NOT NULL,
  `bom_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_component_bom_id_e5c1b43b_fk_workflow_bom_id` (`bom_id`),
  CONSTRAINT `workflow_component_bom_id_e5c1b43b_fk_workflow_bom_id` FOREIGN KEY (`bom_id`) REFERENCES `workflow_bom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_component`
--

LOCK TABLES `workflow_component` WRITE;
/*!40000 ALTER TABLE `workflow_component` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_inspectioncheckpoint`
--

DROP TABLE IF EXISTS `workflow_inspectioncheckpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_inspectioncheckpoint` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `checkpoint_name` varchar(255) NOT NULL,
  `inspection_criteria` longtext NOT NULL,
  `tools_equipment_required` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_inspectioncheckpoint`
--

LOCK TABLES `workflow_inspectioncheckpoint` WRITE;
/*!40000 ALTER TABLE `workflow_inspectioncheckpoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_inspectioncheckpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_product`
--

DROP TABLE IF EXISTS `workflow_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `category` varchar(100) NOT NULL,
  `specifications` longtext NOT NULL,
  `bom_id` bigint(20) NOT NULL,
  `workflow_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_product_workflow_id_6a5eddc7_fk_workflow_workflow_id` (`workflow_id`),
  KEY `workflow_product_bom_id_41a3fabf_fk_workflow_bom_id` (`bom_id`),
  CONSTRAINT `workflow_product_bom_id_41a3fabf_fk_workflow_bom_id` FOREIGN KEY (`bom_id`) REFERENCES `workflow_bom` (`id`),
  CONSTRAINT `workflow_product_workflow_id_6a5eddc7_fk_workflow_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `workflow_workflow` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_product`
--

LOCK TABLES `workflow_product` WRITE;
/*!40000 ALTER TABLE `workflow_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_productionline`
--

DROP TABLE IF EXISTS `workflow_productionline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_productionline` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `line_name` varchar(255) NOT NULL,
  `capacity_limit` int(10) unsigned NOT NULL CHECK (`capacity_limit` >= 0),
  `oee_target` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `maintenance_schedule` varchar(50) NOT NULL,
  `preferred_shift` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_productionline`
--

LOCK TABLES `workflow_productionline` WRITE;
/*!40000 ALTER TABLE `workflow_productionline` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_productionline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_productionline_work_centers`
--

DROP TABLE IF EXISTS `workflow_productionline_work_centers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_productionline_work_centers` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `productionline_id` bigint(20) NOT NULL,
  `workcenter_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `workflow_productionline__productionline_id_workce_7f97112b_uniq` (`productionline_id`,`workcenter_id`),
  KEY `workflow_productionl_workcenter_id_70751a20_fk_workflow_` (`workcenter_id`),
  CONSTRAINT `workflow_productionl_productionline_id_64a163e2_fk_workflow_` FOREIGN KEY (`productionline_id`) REFERENCES `workflow_productionline` (`id`),
  CONSTRAINT `workflow_productionl_workcenter_id_70751a20_fk_workflow_` FOREIGN KEY (`workcenter_id`) REFERENCES `workflow_workcenter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_productionline_work_centers`
--

LOCK TABLES `workflow_productionline_work_centers` WRITE;
/*!40000 ALTER TABLE `workflow_productionline_work_centers` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_productionline_work_centers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_productionorder`
--

DROP TABLE IF EXISTS `workflow_productionorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_productionorder` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_name` varchar(255) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `production_line_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_productiono_product_id_1e0d4870_fk_workflow_` (`product_id`),
  KEY `workflow_productiono_production_line_id_99b66afd_fk_workflow_` (`production_line_id`),
  CONSTRAINT `workflow_productiono_product_id_1e0d4870_fk_workflow_` FOREIGN KEY (`product_id`) REFERENCES `workflow_product` (`id`),
  CONSTRAINT `workflow_productiono_production_line_id_99b66afd_fk_workflow_` FOREIGN KEY (`production_line_id`) REFERENCES `workflow_productionline` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_productionorder`
--

LOCK TABLES `workflow_productionorder` WRITE;
/*!40000 ALTER TABLE `workflow_productionorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_productionorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_rescheduling`
--

DROP TABLE IF EXISTS `workflow_rescheduling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_rescheduling` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `new_start_time` datetime(6) NOT NULL,
  `new_end_time` datetime(6) NOT NULL,
  `reason_for_rescheduling` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `production_order_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_reschedulin_production_order_id_bd42e4f2_fk_workflow_` (`production_order_id`),
  CONSTRAINT `workflow_reschedulin_production_order_id_bd42e4f2_fk_workflow_` FOREIGN KEY (`production_order_id`) REFERENCES `workflow_productionorder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_rescheduling`
--

LOCK TABLES `workflow_rescheduling` WRITE;
/*!40000 ALTER TABLE `workflow_rescheduling` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_rescheduling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_stage`
--

DROP TABLE IF EXISTS `workflow_stage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_stage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `work_order` varchar(255) NOT NULL,
  `duration` int(11) NOT NULL,
  `assigned_work_center_id` bigint(20) DEFAULT NULL,
  `workflow_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_stage_workflow_id_71fcf0b3_fk_workflow_workflow_id` (`workflow_id`),
  KEY `workflow_stage_assigned_work_center_6e682ce8_fk_workflow_` (`assigned_work_center_id`),
  CONSTRAINT `workflow_stage_assigned_work_center_6e682ce8_fk_workflow_` FOREIGN KEY (`assigned_work_center_id`) REFERENCES `workflow_workcenter` (`id`),
  CONSTRAINT `workflow_stage_workflow_id_71fcf0b3_fk_workflow_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `workflow_workflow` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_stage`
--

LOCK TABLES `workflow_stage` WRITE;
/*!40000 ALTER TABLE `workflow_stage` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_stage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_stage_inspection_checkpoints`
--

DROP TABLE IF EXISTS `workflow_stage_inspection_checkpoints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_stage_inspection_checkpoints` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `stage_id` bigint(20) NOT NULL,
  `inspectioncheckpoint_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `workflow_stage_inspectio_stage_id_inspectioncheck_b2a25840_uniq` (`stage_id`,`inspectioncheckpoint_id`),
  KEY `workflow_stage_inspe_inspectioncheckpoint_6c45941e_fk_workflow_` (`inspectioncheckpoint_id`),
  CONSTRAINT `workflow_stage_inspe_inspectioncheckpoint_6c45941e_fk_workflow_` FOREIGN KEY (`inspectioncheckpoint_id`) REFERENCES `workflow_inspectioncheckpoint` (`id`),
  CONSTRAINT `workflow_stage_inspe_stage_id_c9d56161_fk_workflow_` FOREIGN KEY (`stage_id`) REFERENCES `workflow_stage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_stage_inspection_checkpoints`
--

LOCK TABLES `workflow_stage_inspection_checkpoints` WRITE;
/*!40000 ALTER TABLE `workflow_stage_inspection_checkpoints` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_stage_inspection_checkpoints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_workcenter`
--

DROP TABLE IF EXISTS `workflow_workcenter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_workcenter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_workcenter`
--

LOCK TABLES `workflow_workcenter` WRITE;
/*!40000 ALTER TABLE `workflow_workcenter` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_workcenter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_workflow`
--

DROP TABLE IF EXISTS `workflow_workflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_workflow` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `assigned_work_center_id` bigint(20) DEFAULT NULL,
  `product_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_workflow_assigned_work_center_e80ebe58_fk_workflow_` (`assigned_work_center_id`),
  KEY `workflow_workflow_product_id_441b6156_fk_workflow_product_id` (`product_id`),
  CONSTRAINT `workflow_workflow_assigned_work_center_e80ebe58_fk_workflow_` FOREIGN KEY (`assigned_work_center_id`) REFERENCES `workflow_workcenter` (`id`),
  CONSTRAINT `workflow_workflow_product_id_441b6156_fk_workflow_product_id` FOREIGN KEY (`product_id`) REFERENCES `workflow_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_workflow`
--

LOCK TABLES `workflow_workflow` WRITE;
/*!40000 ALTER TABLE `workflow_workflow` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_workflow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_workflow_stages`
--

DROP TABLE IF EXISTS `workflow_workflow_stages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_workflow_stages` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `workflow_id` bigint(20) NOT NULL,
  `stage_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `workflow_workflow_stages_workflow_id_stage_id_78d11c37_uniq` (`workflow_id`,`stage_id`),
  KEY `workflow_workflow_stages_stage_id_1ae9d189_fk_workflow_stage_id` (`stage_id`),
  CONSTRAINT `workflow_workflow_st_workflow_id_a6ee41aa_fk_workflow_` FOREIGN KEY (`workflow_id`) REFERENCES `workflow_workflow` (`id`),
  CONSTRAINT `workflow_workflow_stages_stage_id_1ae9d189_fk_workflow_stage_id` FOREIGN KEY (`stage_id`) REFERENCES `workflow_stage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_workflow_stages`
--

LOCK TABLES `workflow_workflow_stages` WRITE;
/*!40000 ALTER TABLE `workflow_workflow_stages` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_workflow_stages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-15  4:02:49
