/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50553
Source Host           : localhost:9306
Source Database       : zhilian

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-03-13 16:17:12
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for job
-- ----------------------------
DROP TABLE IF EXISTS `job`;
CREATE TABLE `job` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `co_name` varchar(250) NOT NULL,
  `area` varchar(250) NOT NULL,
  `salary` varchar(250) DEFAULT NULL,
  `exp` varchar(250) NOT NULL,
  `edu` varchar(250) DEFAULT NULL,
  `num` varchar(250) NOT NULL,
  `time` varchar(250) NOT NULL,
  `otherq` varchar(255) DEFAULT NULL,
  `welfare` varchar(250) DEFAULT NULL,
  `info` text NOT NULL,
  `local` varchar(250) NOT NULL,
  `co_url` varchar(250) NOT NULL,
  `co_type` varchar(250) NOT NULL,
  `spider_name` varchar(20) NOT NULL,
  `target_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`co_name`,`spider_name`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
