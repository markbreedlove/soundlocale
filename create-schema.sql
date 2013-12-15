
CREATE TABLE IF NOT EXISTS `user` (
      `id` bigint(20) unsigned NOT NULL,
      `username` varchar(255) NOT NULL,
      `fullname` varchar(255) NOT NULL,
      `password` varchar(255) NOT NULL,
      `auth_token` varchar(255) DEFAULT NULL,
      `email` varchar(255) NOT NULL,
      `status` tinyint(2) NOT NULL DEFAULT '0',
      `created` int(10) DEFAULT NULL,
      `modified` int(10) DEFAULT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `x_user_username` (`username`),
      UNIQUE KEY `x_user_email` (`email`),
      UNIQUE KEY `x_user_authtoken` (`auth_token`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `sound` (
      `id` bigint(20) unsigned NOT NULL,
      `lat` double NOT NULL,
      `lng` double NOT NULL,
      `basename` varchar(255) NOT NULL,
      `title` varchar(255) DEFAULT NULL,
      `container` varchar(25) DEFAULT NULL,
      `user_id` bigint(20) unsigned NOT NULL,
      `flags` int(10) NOT NULL DEFAULT '0',
      `created` int(10) DEFAULT NULL,
      `modified` int(10) DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `x_sound_user_id` (`user_id`),
      KEY `x_sound_lat_lng` (`lat`,`lng`),
      KEY `x_sound_container` (`container`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

