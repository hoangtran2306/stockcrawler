# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.16)
# Database: 24h_stock
# Generation Time: 2017-09-08 04:30:52 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table articles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `articles`;

CREATE TABLE `articles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `title` text,
  `author` varchar(150) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `figure` text,
  `figure_type` varchar(30) DEFAULT NULL,
  `published` varchar(150) DEFAULT NULL,
  `short_content` text,
  `content` mediumtext,
  `html` mediumtext,
  `tags` text,
  `stock_tags` text,
  `com_tags` text,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table crawl_articles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `crawl_articles`;

CREATE TABLE `crawl_articles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `from` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `raw` mediumtext,
  `total` int(11) DEFAULT NULL,
  `new` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table scff_bprofiles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `scff_bprofiles`;

CREATE TABLE `scff_bprofiles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `first_trading_date` varchar(30) DEFAULT NULL,
  `first_price` float DEFAULT NULL,
  `first_vol` bigint(20) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `intro` text,
  `financial_info` mediumtext,
  `basic_info` mediumtext,
  `leadership_ownership` mediumtext,
  `affiliates` mediumtext,
  `financial_reports` mediumtext,
  `template` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table scff_sprofiles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `scff_sprofiles`;

CREATE TABLE `scff_sprofiles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `updated_time` varchar(150) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `price_change` float DEFAULT NULL,
  `price_change_per` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `highest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `nfi_trans` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `remained_room` float DEFAULT NULL,
  `basic_eps` float DEFAULT NULL,
  `diluted_eps` float DEFAULT NULL,
  `pe` float DEFAULT NULL,
  `book_value` float DEFAULT NULL,
  `the_beta` float DEFAULT NULL,
  `avg_trading_vol` int(11) DEFAULT NULL,
  `listed_share_vol` bigint(20) DEFAULT NULL,
  `circulation_vol` bigint(20) DEFAULT NULL,
  `market_cap` float DEFAULT NULL,
  `template` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vcme_companies
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vcme_companies`;

CREATE TABLE `vcme_companies` (
  `symbol` varchar(20) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `trade_center` varchar(20) DEFAULT NULL,
  `profile_link` varchar(255) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `on_board` bit(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vcme_crawl_companies
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vcme_crawl_companies`;

CREATE TABLE `vcme_crawl_companies` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `response` mediumtext,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_cfc
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_cfc`;

CREATE TABLE `vndc_cfc` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `ceiling` varchar(200) DEFAULT NULL,
  `floor` varchar(200) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_commands
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_commands`;

CREATE TABLE `vndc_commands` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL,
  `command` text,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_companies
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_companies`;

CREATE TABLE `vndc_companies` (
  `symbol` varchar(20) NOT NULL DEFAULT '',
  `company` varchar(200) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `company_name_eng` varchar(200) DEFAULT NULL,
  `short_name` varchar(150) DEFAULT NULL,
  `listed_date` date DEFAULT NULL,
  `floor` varchar(20) DEFAULT NULL,
  `industry_name` varchar(200) DEFAULT NULL,
  `index_code` varchar(15) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_cfc
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_cfc`;

CREATE TABLE `vndc_crawl_cfc` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `command` text,
  `response` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_companies
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_companies`;

CREATE TABLE `vndc_crawl_companies` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `response` mediumtext,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_hnx
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_hnx`;

CREATE TABLE `vndc_crawl_hnx` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `command` text,
  `response` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_hnx30
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_hnx30`;

CREATE TABLE `vndc_crawl_hnx30` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `command` text,
  `response` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_hose
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_hose`;

CREATE TABLE `vndc_crawl_hose` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `command` text,
  `response` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_markets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_markets`;

CREATE TABLE `vndc_crawl_markets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `command` text,
  `response` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_upcom
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_upcom`;

CREATE TABLE `vndc_crawl_upcom` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `command` text,
  `response` mediumtext,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_crawl_vn30
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_crawl_vn30`;

CREATE TABLE `vndc_crawl_vn30` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `command` text,
  `response` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_floors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_floors`;

CREATE TABLE `vndc_floors` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_hnx
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_hnx`;

CREATE TABLE `vndc_hnx` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` bigint(20) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_hnx30
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_hnx30`;

CREATE TABLE `vndc_hnx30` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` bigint(20) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_hose
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_hose`;

CREATE TABLE `vndc_hose` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` bigint(20) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_markets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_markets`;

CREATE TABLE `vndc_markets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `market_id` int(11) DEFAULT NULL,
  `total_trade` int(11) DEFAULT NULL,
  `total_share_traded` float DEFAULT NULL,
  `total_value_traded` float DEFAULT NULL,
  `advance` int(5) DEFAULT NULL,
  `decline` int(5) DEFAULT NULL,
  `no_change` int(5) DEFAULT NULL,
  `index_value` float DEFAULT NULL,
  `changed` float DEFAULT NULL,
  `trading_time` time DEFAULT NULL,
  `trading_date` bigint(20) DEFAULT NULL,
  `floor_code` varchar(20) DEFAULT NULL,
  `market_index` float DEFAULT NULL,
  `prior_market_index` float DEFAULT NULL,
  `highest_index` float DEFAULT NULL,
  `lowest_index` float DEFAULT NULL,
  `share_traded` float DEFAULT NULL,
  `status` int(5) DEFAULT NULL,
  `sequence` int(4) DEFAULT NULL,
  `prediction_market_index` float DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_stock_daily
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_stock_daily`;

CREATE TABLE `vndc_stock_daily` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_stock_hourly
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_stock_hourly`;

CREATE TABLE `vndc_stock_hourly` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_stock_monthly
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_stock_monthly`;

CREATE TABLE `vndc_stock_monthly` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_upcom
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_upcom`;

CREATE TABLE `vndc_upcom` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` bigint(20) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_urls
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_urls`;

CREATE TABLE `vndc_urls` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(100) DEFAULT NULL,
  `type` varchar(20) DEFAULT '',
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vndc_vn30
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vndc_vn30`;

CREATE TABLE `vndc_vn30` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `floor_code` varchar(20) DEFAULT NULL,
  `trading_date` bigint(20) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `stock_type` varchar(50) DEFAULT NULL,
  `totalroom` float DEFAULT NULL,
  `current_room` float DEFAULT NULL,
  `basic_price` float DEFAULT NULL,
  `open_price` float DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `current_price` float DEFAULT NULL,
  `current_qtty` int(11) DEFAULT NULL,
  `hieghest_price` float DEFAULT NULL,
  `lowest_price` float DEFAULT NULL,
  `ceiling_price` float DEFAULT NULL,
  `floor_price` float DEFAULT NULL,
  `total_offer_qtty` int(11) DEFAULT NULL,
  `total_bid_qtty` int(11) DEFAULT NULL,
  `match_price` float DEFAULT NULL,
  `match_qtty` int(11) DEFAULT NULL,
  `match_value` float DEFAULT NULL,
  `average_price` float DEFAULT NULL,
  `bid_price01` float DEFAULT NULL,
  `bid_qtty01` int(11) DEFAULT NULL,
  `bid_price02` float DEFAULT NULL,
  `bid_qtty02` int(11) DEFAULT NULL,
  `bid_price03` float DEFAULT NULL,
  `bid_qtty03` int(11) DEFAULT NULL,
  `offer_price01` float DEFAULT NULL,
  `offer_qtty01` int(11) DEFAULT NULL,
  `offer_price02` float DEFAULT NULL,
  `offer_qtty02` int(11) DEFAULT NULL,
  `offer_price03` float DEFAULT NULL,
  `offer_qtty03` int(11) DEFAULT NULL,
  `accumulated_val` float DEFAULT NULL,
  `accumylated_vol` int(11) DEFAULT NULL,
  `buy_foreign_qtty` int(11) DEFAULT NULL,
  `sell_foreign_qtty` int(11) DEFAULT NULL,
  `project_open` float DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
