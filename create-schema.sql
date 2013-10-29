
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
      `id` bigint(20) UNSIGNED NOT NULL,
      `username` varchar(255) NOT NULL,
      `fullname` varchar(255) NOT NULL,
      `password` char(64) NOT NULL,
      `email` varchar(255) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `x_user_username` (`username`),
      UNIQUE KEY `x_user_email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `sound`;
CREATE TABLE `sound` (
      `id` bigint(20) UNSIGNED NOT NULL,
      `lat` double NOT NULL,
      `lng` double NOT NULL,
      `basename` varchar(255) NOT NULL,
      `title` varchar(255),
      `container` varchar(25),
      `user_id` bigint(20) UNSIGNED NOT NULL,
      PRIMARY KEY (`id`),
      KEY `x_sound_user_id` (`user_id`),
      KEY `x_sound_lat_lng` (`lat`, `lng`),
      KEY `x_sound_container` (`container`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

