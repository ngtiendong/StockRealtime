DROP TABLE IF EXISTS currency;
DROP TABLE IF EXISTS currency_in_day;
DROP TABLE IF EXISTS stocks;
DROP TABLE IF EXISTS stock_in_day;

CREATE TABLE `currency` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `base` varchar(127) DEFAULT 'EUR',
  `symbol` varchar(127) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `date` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4942 DEFAULT CHARSET=utf8;

CREATE TABLE `currency_in_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `base` varchar(127) DEFAULT 'EUR',
  `symbol` varchar(127) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `change_1` varchar(255) DEFAULT NULL,
  `change_2` varchar(255) DEFAULT '',
  `moment` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1756 DEFAULT CHARSET=utf8;

CREATE TABLE `stocks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(255) DEFAULT '',
  `open` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9597 DEFAULT CHARSET=utf8;

CREATE TABLE `stock_in_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(255) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `change_1` varchar(255) DEFAULT NULL,
  `change_2` varchar(255) DEFAULT NULL,
  `moment` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=225 DEFAULT CHARSET=utf8;