-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               12.0.2-MariaDB - mariadb.org binary distribution
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

-- Drop database if exists and create fresh
DROP DATABASE IF EXISTS `adventurous_traveler_game`;
CREATE DATABASE `adventurous_traveler_game` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `adventurous_traveler_game`;

-- --------------------------------------------------------
-- Table structure for table `airports`
-- --------------------------------------------------------
CREATE TABLE `airports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `airport_size` enum('small','medium','large') DEFAULT NULL,
  `region` enum('Western Europe','Central Europe','Southern Europe','Northern Europe','Eastern Europe','Scandinavia','Baltic','Balkans','Mediterranean','British Isles') DEFAULT NULL,
  `runway_length_m` int(11) DEFAULT 3000,
  `has_international` tinyint(1) DEFAULT 1,
  `is_tourist_destination` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Dumping data for table `airports`
-- --------------------------------------------------------
INSERT INTO `airports` (`id`, `code`, `name`, `city`, `country`, `latitude`, `longitude`, `airport_size`, `region`, `runway_length_m`, `has_international`, `is_tourist_destination`) VALUES
(1, 'EGLL', 'London Heathrow Airport', 'London', 'United Kingdom', 51.47000000, -0.45400000, 'large', 'British Isles', 3900, 1, 1),
(2, 'EGKK', 'London Gatwick Airport', 'London', 'United Kingdom', 51.14800000, -0.19020000, 'large', 'British Isles', 3200, 1, 1),
(3, 'EGCC', 'Manchester Airport', 'Manchester', 'United Kingdom', 53.35370000, -2.27500000, 'large', 'British Isles', 3050, 1, 0),
(4, 'EGPH', 'Edinburgh Airport', 'Edinburgh', 'United Kingdom', 55.95000000, -3.37250000, 'medium', 'British Isles', 2560, 1, 1),
(5, 'EGBB', 'Birmingham Airport', 'Birmingham', 'United Kingdom', 52.45390000, -1.74800000, 'medium', 'British Isles', 2600, 1, 0),
(6, 'EGPF', 'Glasgow Airport', 'Glasgow', 'United Kingdom', 55.87190000, -4.43310000, 'medium', 'British Isles', 2660, 1, 1),
(7, 'EGGD', 'Bristol Airport', 'Bristol', 'United Kingdom', 51.38270000, -2.71910000, 'medium', 'British Isles', 2010, 1, 0),
(8, 'EGNT', 'Newcastle Airport', 'Newcastle', 'United Kingdom', 55.03750000, -1.69167000, 'medium', 'British Isles', 2320, 1, 0),
(9, 'LFPG', 'Charles de Gaulle Airport', 'Paris', 'France', 49.00970000, 2.54780000, 'large', 'Western Europe', 4200, 1, 1),
(10, 'LFPO', 'Paris Orly Airport', 'Paris', 'France', 48.72330000, 2.37940000, 'large', 'Western Europe', 3650, 1, 1),
(11, 'LFMN', 'Nice Côte d\'Azur Airport', 'Nice', 'France', 43.66580000, 7.21500000, 'large', 'Mediterranean', 2940, 1, 1),
(12, 'LFLL', 'Lyon-Saint Exupéry Airport', 'Lyon', 'France', 45.72570000, 5.08110000, 'large', 'Western Europe', 4000, 1, 0),
(13, 'LFML', 'Marseille Provence Airport', 'Marseille', 'France', 43.43920000, 5.22140000, 'large', 'Mediterranean', 3500, 1, 1),
(14, 'LFBO', 'Toulouse-Blagnac Airport', 'Toulouse', 'France', 43.62910000, 1.36380000, 'medium', 'Western Europe', 3500, 1, 0),
(15, 'LFBD', 'Bordeaux-Mérignac Airport', 'Bordeaux', 'France', 44.82830000, -0.71560000, 'medium', 'Western Europe', 3100, 1, 1),
(16, 'LFRS', 'Nantes Atlantique Airport', 'Nantes', 'France', 47.15320000, -1.61070000, 'medium', 'Western Europe', 2900, 1, 0),
(17, 'LFST', 'Strasbourg Airport', 'Strasbourg', 'France', 48.53830000, 7.62820000, 'small', 'Western Europe', 2400, 1, 1),
(18, 'LFQQ', 'Lille Airport', 'Lille', 'France', 50.56330000, 3.08940000, 'small', 'Western Europe', 2300, 1, 0),
(19, 'EDDF', 'Frankfurt Airport', 'Frankfurt', 'Germany', 50.03330000, 8.57060000, 'large', 'Central Europe', 4000, 1, 0),
(20, 'EDDM', 'Munich Airport', 'Munich', 'Germany', 48.35380000, 11.78600000, 'large', 'Central Europe', 4000, 1, 1),
(21, 'EDDB', 'Berlin Brandenburg Airport', 'Berlin', 'Germany', 52.55970000, 13.28770000, 'large', 'Central Europe', 3600, 1, 1),
(22, 'EDDL', 'Düsseldorf Airport', 'Düsseldorf', 'Germany', 51.28950000, 6.76680000, 'large', 'Central Europe', 3000, 1, 0),
(23, 'EDDH', 'Hamburg Airport', 'Hamburg', 'Germany', 53.63040000, 9.98820000, 'large', 'Central Europe', 3660, 1, 1),
(24, 'EDDK', 'Cologne Bonn Airport', 'Cologne', 'Germany', 50.86590000, 7.14270000, 'medium', 'Central Europe', 2450, 1, 0),
(25, 'EDDS', 'Stuttgart Airport', 'Stuttgart', 'Germany', 48.68980000, 9.22200000, 'medium', 'Central Europe', 3345, 1, 0),
(26, 'EDDN', 'Nuremberg Airport', 'Nuremberg', 'Germany', 49.49870000, 11.06680000, 'medium', 'Central Europe', 2700, 1, 0),
(27, 'EDDV', 'Hannover Airport', 'Hannover', 'Germany', 52.46110000, 9.68500000, 'medium', 'Central Europe', 2340, 1, 0),
(28, 'EDDC', 'Dresden Airport', 'Dresden', 'Germany', 51.13280000, 13.76720000, 'small', 'Central Europe', 2850, 1, 1),
(29, 'LEMD', 'Adolfo Suárez Madrid-Barajas Airport', 'Madrid', 'Spain', 40.47230000, -3.56080000, 'large', 'Southern Europe', 4100, 1, 1),
(30, 'LEBL', 'Barcelona-El Prat Airport', 'Barcelona', 'Spain', 41.29710000, 2.07850000, 'large', 'Mediterranean', 3350, 1, 1),
(31, 'LEMG', 'Málaga-Costa del Sol Airport', 'Málaga', 'Spain', 36.67490000, -4.49910000, 'large', 'Mediterranean', 3200, 1, 1),
(32, 'LEPA', 'Palma de Mallorca Airport', 'Palma', 'Spain', 39.55170000, 2.73880000, 'large', 'Mediterranean', 3270, 1, 1),
(33, 'LEVC', 'Valencia Airport', 'Valencia', 'Spain', 39.48930000, -0.48160000, 'large', 'Mediterranean', 3200, 1, 1),
(34, 'LEZL', 'Sevilla Airport', 'Sevilla', 'Spain', 37.41800000, -5.89310000, 'medium', 'Southern Europe', 3360, 1, 1),
(35, 'LEBB', 'Bilbao Airport', 'Bilbao', 'Spain', 43.30110000, -2.91060000, 'medium', 'Southern Europe', 2000, 1, 1),
(36, 'LEAL', 'Alicante-Elche Airport', 'Alicante', 'Spain', 38.28220000, -0.55816000, 'medium', 'Mediterranean', 3000, 1, 1),
(37, 'LEST', 'Santiago de Compostela Airport', 'Santiago', 'Spain', 42.89630000, -8.41510000, 'small', 'Southern Europe', 3200, 1, 1),
(38, 'LEAS', 'Asturias Airport', 'Oviedo', 'Spain', 43.56360000, -6.03460000, 'small', 'Southern Europe', 2200, 1, 0),
(39, 'LIRF', 'Leonardo da Vinci-Fiumicino Airport', 'Rome', 'Italy', 41.80030000, 12.23890000, 'large', 'Mediterranean', 3900, 1, 1),
(40, 'LIMC', 'Milan Malpensa Airport', 'Milan', 'Italy', 45.63000000, 8.72810000, 'large', 'Southern Europe', 3920, 1, 1),
(41, 'LIML', 'Milan Linate Airport', 'Milan', 'Italy', 45.44510000, 9.27650000, 'medium', 'Southern Europe', 2440, 1, 1),
(42, 'LIPZ', 'Venice Marco Polo Airport', 'Venice', 'Italy', 45.50530000, 12.35190000, 'large', 'Mediterranean', 3300, 1, 1),
(43, 'LIRN', 'Naples International Airport', 'Naples', 'Italy', 40.88600000, 14.29080000, 'large', 'Mediterranean', 2680, 1, 1),
(44, 'LICC', 'Catania-Fontanarossa Airport', 'Catania', 'Italy', 37.46680000, 15.06640000, 'medium', 'Mediterranean', 2430, 1, 1),
(45, 'LIPE', 'Bologna Guglielmo Marconi Airport', 'Bologna', 'Italy', 44.53540000, 11.28870000, 'medium', 'Southern Europe', 2800, 1, 1),
(46, 'LIRQ', 'Florence Airport', 'Florence', 'Italy', 43.81000000, 11.20510000, 'small', 'Southern Europe', 1730, 1, 1),
(47, 'LIRP', 'Pisa International Airport', 'Pisa', 'Italy', 43.68390000, 10.39270000, 'small', 'Southern Europe', 2993, 1, 1),
(48, 'LIMF', 'Turin Airport', 'Turin', 'Italy', 45.20080000, 7.64960000, 'small', 'Southern Europe', 3300, 1, 1),
(49, 'EHAM', 'Amsterdam Airport Schiphol', 'Amsterdam', 'Netherlands', 52.30860000, 4.76390000, 'large', 'Western Europe', 3800, 1, 1),
(50, 'EHEH', 'Eindhoven Airport', 'Eindhoven', 'Netherlands', 51.45010000, 5.37450000, 'medium', 'Western Europe', 3000, 1, 0),
(51, 'EHRD', 'Rotterdam The Hague Airport', 'Rotterdam', 'Netherlands', 51.95690000, 4.43720000, 'small', 'Western Europe', 2200, 1, 0),
(52, 'EBBR', 'Brussels Airport', 'Brussels', 'Belgium', 50.90140000, 4.48440000, 'large', 'Western Europe', 3630, 1, 1),
(53, 'EBCI', 'Brussels South Charleroi Airport', 'Charleroi', 'Belgium', 50.45920000, 4.45380000, 'medium', 'Western Europe', 2550, 1, 0),
(54, 'LSZH', 'Zurich Airport', 'Zurich', 'Switzerland', 47.46480000, 8.54910000, 'large', 'Central Europe', 4000, 1, 1),
(55, 'LSGG', 'Geneva Airport', 'Geneva', 'Switzerland', 46.23810000, 6.10950000, 'large', 'Central Europe', 3900, 1, 1),
(56, 'LFSB', 'EuroAirport Basel-Mulhouse-Freiburg', 'Basel', 'Switzerland', 47.59000000, 7.52910000, 'medium', 'Central Europe', 3900, 1, 0),
(57, 'LOWW', 'Vienna International Airport', 'Vienna', 'Austria', 48.11030000, 16.56970000, 'large', 'Central Europe', 3500, 1, 1),
(58, 'LOWS', 'Salzburg Airport', 'Salzburg', 'Austria', 47.79330000, 13.00430000, 'medium', 'Central Europe', 2750, 1, 1),
(59, 'LPPT', 'Lisbon Portela Airport', 'Lisbon', 'Portugal', 38.78140000, -9.13590000, 'large', 'Southern Europe', 3800, 1, 1),
(60, 'LPPR', 'Porto Airport', 'Porto', 'Portugal', 41.24810000, -8.68139000, 'large', 'Southern Europe', 3480, 1, 1),
(61, 'LPFR', 'Faro Airport', 'Faro', 'Portugal', 37.01440000, -7.96590000, 'medium', 'Southern Europe', 2540, 1, 1),
(62, 'LGAV', 'Athens International Airport', 'Athens', 'Greece', 37.93640000, 23.94450000, 'large', 'Mediterranean', 4000, 1, 1),
(63, 'LGTS', 'Thessaloniki Airport', 'Thessaloniki', 'Greece', 40.51970000, 22.97090000, 'medium', 'Mediterranean', 2440, 1, 1),
(64, 'LGIR', 'Heraklion International Airport', 'Heraklion', 'Greece', 35.33970000, 25.18030000, 'medium', 'Mediterranean', 2680, 1, 1),
(65, 'LGRP', 'Rhodes International Airport', 'Rhodes', 'Greece', 36.40540000, 28.08620000, 'small', 'Mediterranean', 3300, 1, 1),
(66, 'ESSA', 'Stockholm Arlanda Airport', 'Stockholm', 'Sweden', 59.65190000, 17.91860000, 'large', 'Scandinavia', 3300, 1, 1),
(67, 'EKCH', 'Copenhagen Airport', 'Copenhagen', 'Denmark', 55.61790000, 12.65610000, 'large', 'Scandinavia', 3600, 1, 1),
(68, 'ENGM', 'Oslo Airport', 'Oslo', 'Norway', 60.19390000, 11.10040000, 'large', 'Scandinavia', 3600, 1, 1),
(69, 'EFHK', 'Helsinki-Vantaa Airport', 'Helsinki', 'Finland', 60.31720000, 24.96330000, 'large', 'Scandinavia', 3500, 1, 1),
(70, 'ESGG', 'Gothenburg Landvetter Airport', 'Gothenburg', 'Sweden', 57.66280000, 12.27980000, 'medium', 'Scandinavia', 3300, 1, 0),
(71, 'ENBR', 'Bergen Airport', 'Bergen', 'Norway', 60.29340000, 5.21814000, 'medium', 'Scandinavia', 2990, 1, 1),
(72, 'EKYT', 'Aalborg Airport', 'Aalborg', 'Denmark', 57.09280000, 9.84920000, 'small', 'Scandinavia', 2650, 1, 0),
(73, 'EFTP', 'Tampere-Pirkkala Airport', 'Tampere', 'Finland', 61.41410000, 23.60440000, 'small', 'Scandinavia', 2700, 1, 0),
(74, 'EPWA', 'Warsaw Chopin Airport', 'Warsaw', 'Poland', 52.16570000, 20.96710000, 'large', 'Eastern Europe', 3690, 1, 1),
(75, 'LKPR', 'Václav Havel Airport Prague', 'Prague', 'Czech Republic', 50.10080000, 14.26000000, 'large', 'Central Europe', 3715, 1, 1),
(76, 'LHBP', 'Budapest Ferenc Liszt International Airport', 'Budapest', 'Hungary', 47.43660000, 19.25560000, 'large', 'Eastern Europe', 3700, 1, 1),
(77, 'LROP', 'Henri Coandă International Airport', 'Bucharest', 'Romania', 44.57220000, 26.10250000, 'large', 'Eastern Europe', 3500, 1, 1),
(78, 'LBSF', 'Sofia Airport', 'Sofia', 'Bulgaria', 42.69500000, 23.41140000, 'medium', 'Balkans', 3600, 1, 1),
(79, 'EPKK', 'John Paul II International Airport', 'Kraków', 'Poland', 50.07770000, 19.78480000, 'medium', 'Eastern Europe', 2550, 1, 1),
(80, 'LZIB', 'M. R. Štefánik Airport', 'Bratislava', 'Slovakia', 48.17020000, 17.21270000, 'small', 'Central Europe', 2900, 1, 1),
(81, 'EVRA', 'Riga International Airport', 'Riga', 'Latvia', 56.92360000, 23.97110000, 'medium', 'Baltic', 3200, 1, 1),
(82, 'EETN', 'Tallinn Airport', 'Tallinn', 'Estonia', 59.41330000, 24.83280000, 'medium', 'Baltic', 3480, 1, 1),
(83, 'EYVI', 'Vilnius Airport', 'Vilnius', 'Lithuania', 54.63410000, 25.28580000, 'medium', 'Baltic', 3250, 1, 1),
(84, 'EIDW', 'Dublin Airport', 'Dublin', 'Ireland', 53.42130000, -6.27010000, 'large', 'British Isles', 2637, 1, 1),
(85, 'EICK', 'Cork Airport', 'Cork', 'Ireland', 51.84130000, -8.49110000, 'small', 'British Isles', 2130, 1, 1),
(86, 'LYBE', 'Belgrade Nikola Tesla Airport', 'Belgrade', 'Serbia', 44.81840000, 20.30910000, 'medium', 'Balkans', 3400, 1, 1),
(87, 'LDZA', 'Zagreb Airport', 'Zagreb', 'Croatia', 45.74290000, 16.06880000, 'medium', 'Balkans', 3250, 1, 1),
(88, 'LJLJ', 'Ljubljana Jože Pučnik Airport', 'Ljubljana', 'Slovenia', 46.22370000, 14.45760000, 'small', 'Balkans', 3300, 1, 1),
(89, 'LWSK', 'Skopje International Airport', 'Skopje', 'North Macedonia', 41.96160000, 21.62140000, 'small', 'Balkans', 3100, 1, 1),
(90, 'LDDU', 'Dubrovnik Airport', 'Dubrovnik', 'Croatia', 42.56140000, 18.26820000, 'small', 'Mediterranean', 3300, 1, 1),
(91, 'ELLX', 'Luxembourg Airport', 'Luxembourg', 'Luxembourg', 49.62330000, 6.20440000, 'medium', 'Western Europe', 4000, 1, 1),
(92, 'BIKF', 'Keflavík International Airport', 'Reykjavik', 'Iceland', 63.98500000, -22.60560000, 'large', 'Scandinavia', 3065, 1, 1),
(93, 'LCLK', 'Larnaca International Airport', 'Larnaca', 'Cyprus', 34.87510000, 33.62490000, 'medium', 'Mediterranean', 3000, 1, 1),
(94, 'LMML', 'Malta International Airport', 'Valletta', 'Malta', 35.85750000, 14.47750000, 'medium', 'Mediterranean', 3540, 1, 1),
(95, 'LIEO', 'Olbia Costa Smeralda Airport', 'Olbia', 'Italy', 40.89870000, 9.51763000, 'small', 'Mediterranean', 2950, 1, 1),
(96, 'LIBD', 'Bari Karol Wojtyła Airport', 'Bari', 'Italy', 41.13890000, 16.76060000, 'medium', 'Mediterranean', 3000, 1, 1),
(97, 'LEVD', 'Valladolid Airport', 'Valladolid', 'Spain', 41.70610000, -4.85194000, 'small', 'Southern Europe', 3100, 1, 0),
(98, 'LEGR', 'Federico García Lorca Granada-Jaén Airport', 'Granada', 'Spain', 37.18860000, -3.77722000, 'small', 'Mediterranean', 2900, 1, 1),
(99, 'LPMA', 'Madeira Airport', 'Funchal', 'Portugal', 32.69420000, -16.77810000, 'medium', 'Southern Europe', 2781, 1, 1),
(100, 'LEIB', 'Ibiza Airport', 'Ibiza', 'Spain', 38.87280000, 1.37312000, 'medium', 'Mediterranean', 2800, 1, 1);

-- --------------------------------------------------------
-- Table structure for table `artifacts`
-- --------------------------------------------------------
CREATE TABLE `artifacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `origin_country` varchar(50) DEFAULT NULL,
  `era` varchar(50) DEFAULT NULL,
  `delivery_reward_money` int(11) DEFAULT 3000,
  `delivery_reward_fuel` int(11) DEFAULT 1000,
  `difficulty_level` enum('easy','medium','hard') DEFAULT 'medium',
  `artifact_order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `artifact_order` (`artifact_order`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Dumping data for table `artifacts`
-- --------------------------------------------------------
INSERT INTO `artifacts` (`id`, `name`, `description`, `origin_country`, `era`, `delivery_reward_money`, `delivery_reward_fuel`, `difficulty_level`, `artifact_order`) VALUES
(1, 'Crown of Charlemagne', 'Ancient crown of the Holy Roman Emperor, adorned with precious gems and gold.', 'Germany/France', 'Medieval', 5000, 1500, 'hard', 1),
(2, 'Viking Runestone', 'A mysterious stone tablet inscribed with ancient Nordic runes.', 'Sweden', 'Viking Age', 4500, 1200, 'medium', 2),
(3, 'Medici Manuscript', 'A priceless Renaissance document from the Medici family archives.', 'Italy', 'Renaissance', 4000, 1000, 'medium', 3),
(4, 'Byzantine Chalice', 'Golden ceremonial cup from the Byzantine Empire.', 'Greece/Turkey', 'Byzantine', 4200, 1100, 'medium', 4),
(5, 'Celtic Torc', 'An ornate golden neck ring worn by ancient Celtic warriors.', 'Ireland', 'Iron Age', 3800, 1000, 'easy', 5),
(6, 'Golden Mask of Agamemnon', 'Legendary funeral mask from ancient Mycenae.', 'Greece', 'Bronze Age', 5500, 1500, 'hard', 6),
(7, 'Fabergé Egg', 'One of the precious Imperial Easter Eggs.', 'Russia', 'Imperial Russia', 6000, 1800, 'hard', 7),
(8, 'Gutenberg Bible Page', 'A single page from the first printed Bible in Europe.', 'Germany', 'Renaissance', 4500, 1300, 'medium', 8),
(9, 'Da Vinci Codex Fragment', 'Lost pages from Leonardo da Vinci\'s notebooks.', 'Italy', 'Renaissance', 5200, 1400, 'hard', 9),
(10, 'Amber Room Panel', 'A reconstructed panel from the legendary Amber Room.', 'Russia/Germany', '18th Century', 5800, 1600, 'hard', 10);

-- --------------------------------------------------------
-- Table structure for table `games`
-- --------------------------------------------------------
CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_name` varchar(40) NOT NULL,
  `money` int(11) DEFAULT 10000,
  `fuel_km` int(11) DEFAULT 2000,
  `max_fuel_capacity` int(11) DEFAULT 5000,
  `travels_remaining` int(11) DEFAULT 20,
  `travels_used` int(11) DEFAULT 0,
  `fuel_efficiency_bonus` int(11) DEFAULT 0,
  `flight_discount_percent` int(11) DEFAULT 0,
  `clue_accuracy_bonus` int(11) DEFAULT 0,
  `has_insurance` tinyint(1) DEFAULT 0,
  `gps_enhancer_active` tinyint(1) DEFAULT 0,
  `fuel_pass_remaining` int(11) DEFAULT 0,
  `current_airport_id` int(11) NOT NULL,
  `artifact_airport_id` int(11) DEFAULT NULL,
  `current_phase` enum('FINDING_ARTIFACTS','DELIVERING_ARTIFACTS') DEFAULT 'FINDING_ARTIFACTS',
  `artifacts_found` int(11) DEFAULT 0,
  `artifacts_delivered` int(11) DEFAULT 0,
  `flights_taken` int(11) DEFAULT 0,
  `game_status` enum('ACTIVE','WON','LOST','QUIT') DEFAULT 'ACTIVE',
  `lose_reason` varchar(100) DEFAULT NULL,
  `total_score` int(11) DEFAULT 0,
  `clue_reveal_chance` float DEFAULT 0.1,
  `marker_reveal_chance` float DEFAULT 0.0,
  `quit_at` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `current_airport_id` (`current_airport_id`),
  KEY `artifact_airport_id` (`artifact_airport_id`),
  CONSTRAINT `games_ibfk_1` FOREIGN KEY (`current_airport_id`) REFERENCES `airports` (`id`) ON DELETE CASCADE,
  CONSTRAINT `games_ibfk_2` FOREIGN KEY (`artifact_airport_id`) REFERENCES `airports` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `player_artifacts`
-- --------------------------------------------------------
CREATE TABLE `player_artifacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `artifact_id` int(11) NOT NULL,
  `status` enum('HIDDEN','FOUND','IN_TRANSIT','DELIVERED') DEFAULT 'HIDDEN',
  `found_at` timestamp NULL DEFAULT NULL,
  `delivered_at` timestamp NULL DEFAULT NULL,
  `delivery_airport_id` int(11) DEFAULT NULL,
  `is_dug` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `game_artifact` (`game_id`, `artifact_id`),
  KEY `game_id` (`game_id`),
  KEY `artifact_id` (`artifact_id`),
  KEY `delivery_airport_id` (`delivery_airport_id`),
  CONSTRAINT `player_artifacts_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  CONSTRAINT `player_artifacts_ibfk_2` FOREIGN KEY (`artifact_id`) REFERENCES `artifacts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `player_artifacts_ibfk_3` FOREIGN KEY (`delivery_airport_id`) REFERENCES `airports` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `player_inventory`
-- --------------------------------------------------------
CREATE TABLE `player_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `item_type` enum('travel_ticket','fuel_pack','mystery_box','fuel_pass','gps_enhancer','time_saver','clue_scanner','artifact_detector','insurance','TRAVEL','FUEL','UPGRADE','LOOTBOX','POWERUP','SERVICE') NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `quantity` int(11) DEFAULT 1,
  `is_active` tinyint(1) DEFAULT 0,
  `remaining_uses` int(11) DEFAULT 1,
  `purchased_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `player_inventory_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `game_clues`
-- --------------------------------------------------------
CREATE TABLE `game_clues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `artifact_id` int(11) DEFAULT NULL,
  `target_airport_id` int(11) DEFAULT NULL,
  `clue_type` enum('DIRECTION','DISTANCE','REGION','AIRPORT_TYPE','COUNTRY','NAME_PATTERN','SPECIFIC','EXACT_LOCATION') NOT NULL,
  `clue_text` text NOT NULL,
  `phase` enum('FINDING','DELIVERING') NOT NULL,
  `quality` enum('low','medium','high','exact') DEFAULT 'medium',
  `is_revealed` tinyint(1) DEFAULT 0,
  `is_used` tinyint(1) DEFAULT 0,
  `discovered_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  KEY `artifact_id` (`artifact_id`),
  KEY `target_airport_id` (`target_airport_id`),
  CONSTRAINT `game_clues_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  CONSTRAINT `game_clues_ibfk_2` FOREIGN KEY (`artifact_id`) REFERENCES `artifacts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `game_clues_ibfk_3` FOREIGN KEY (`target_airport_id`) REFERENCES `airports` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `quests`
-- --------------------------------------------------------
CREATE TABLE `quests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `quest_type` enum('EXPLORATION','TRANSPORT','PUZZLE','TIMED','RISK','SCANNING') NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `requirements` json DEFAULT NULL,
  `target_artifact_id` int(11) DEFAULT NULL,
  `target_airport_id` int(11) DEFAULT NULL,
  `reward_money` int(11) DEFAULT 500,
  `reward_fuel` int(11) DEFAULT 300,
  `reward_travels` int(11) DEFAULT 0,
  `reward_clue_quality` enum('low','medium','high','exact') DEFAULT NULL,
  `penalty_money` int(11) DEFAULT 0,
  `penalty_fuel` int(11) DEFAULT 0,
  `time_limit_minutes` int(11) DEFAULT NULL,
  `is_completed` tinyint(1) DEFAULT 0,
  `is_failed` tinyint(1) DEFAULT 0,
  `progress_current` int(11) DEFAULT 0,
  `progress_required` int(11) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `expires_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  KEY `quest_type` (`quest_type`),
  KEY `is_completed` (`is_completed`),
  CONSTRAINT `quests_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  CONSTRAINT `quests_ibfk_2` FOREIGN KEY (`target_artifact_id`) REFERENCES `artifacts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `quests_ibfk_3` FOREIGN KEY (`target_airport_id`) REFERENCES `airports` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `random_events`
-- --------------------------------------------------------
CREATE TABLE `random_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` enum('POSITIVE','NEGATIVE') NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `trigger_chance_percent` int(11) DEFAULT 15,
  `money_effect` int(11) DEFAULT 0,
  `fuel_effect_percent` int(11) DEFAULT 0,
  `fuel_effect_fixed` int(11) DEFAULT 0,
  `travels_effect` int(11) DEFAULT 0,
  `item_effect` varchar(100) DEFAULT NULL,
  `clue_effect` tinyint(1) DEFAULT 0,
  `cooldown_travels` int(11) DEFAULT 3,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Dumping data for table `random_events`
-- --------------------------------------------------------
INSERT INTO `random_events` (`id`, `event_type`, `name`, `description`, `trigger_chance_percent`, `money_effect`, `fuel_effect_percent`, `fuel_effect_fixed`, `travels_effect`, `item_effect`, `clue_effect`, `cooldown_travels`) VALUES
(1, 'NEGATIVE', 'Storm', 'Severe storm forces rerouting - extra fuel consumed!', 10, -500, -20, 0, 0, NULL, 0, 2),
(2, 'NEGATIVE', 'Cyclone', 'Cyclone warning! Travel cancelled for safety.', 5, 0, 0, 0, -1, NULL, 0, 5),
(3, 'NEGATIVE', 'Maintenance Issue', 'Unexpected maintenance required - pay repair fee!', 8, -800, 0, 0, 0, NULL, 0, 3),
(4, 'NEGATIVE', 'Lost Luggage', 'Some luggage lost during transit!', 7, -300, 0, 0, 0, 'random_item', 0, 4),
(5, 'NEGATIVE', 'Fuel Leak', 'Fuel leak detected during flight!', 6, 0, -25, 0, 0, NULL, 0, 3),
(6, 'POSITIVE', 'Tailwind Boost', 'Strong tailwind reduces fuel consumption!', 12, 0, 30, 0, 0, NULL, 0, 2),
(7, 'POSITIVE', 'Helpful Engineer', 'Friendly engineer performs free maintenance!', 8, 500, 0, 200, 0, NULL, 0, 3),
(8, 'POSITIVE', 'Sponsored Flight', 'Local tourism board sponsors your flight!', 5, 1000, 0, 0, 0, NULL, 0, 6),
(9, 'POSITIVE', 'Mystery Helper', 'Mysterious stranger provides valuable information!', 9, 0, 0, 0, 0, NULL, 1, 4),
(10, 'POSITIVE', 'Tourist Bonus', 'Help tourists with directions - earn reward!', 10, 700, 0, 150, 0, NULL, 0, 3);

-- --------------------------------------------------------
-- Table structure for table `game_events`
-- --------------------------------------------------------
CREATE TABLE `game_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `money_change` int(11) DEFAULT 0,
  `fuel_change` int(11) DEFAULT 0,
  `travels_change` int(11) DEFAULT 0,
  `item_gained` varchar(100) DEFAULT NULL,
  `item_lost` varchar(100) DEFAULT NULL,
  `clue_gained` tinyint(1) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `game_events_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  CONSTRAINT `game_events_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `random_events` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `game_logs`
-- --------------------------------------------------------
CREATE TABLE `game_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `log_type` enum('FLIGHT','ARTIFACT_FOUND','ARTIFACT_DELIVERED','QUEST_STARTED','QUEST_COMPLETED','QUEST_FAILED','EVENT_TRIGGERED','PURCHASE','CLUE_FOUND','PHASE_CHANGE','GAME_STATUS','DIG_ATTEMPT','ARTIFACT_REVEALED') NOT NULL,
  `description` text DEFAULT NULL,
  `money_change` int(11) DEFAULT 0,
  `fuel_change` int(11) DEFAULT 0,
  `travels_change` int(11) DEFAULT 0,
  `artifact_id` int(11) DEFAULT NULL,
  `airport_id` int(11) DEFAULT NULL,
  `quest_id` int(11) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `distance_km` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  KEY `idx_logs_game_created` (`game_id`,`created_at`),
  KEY `log_type` (`log_type`),
  CONSTRAINT `game_logs_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `shop_items`
-- --------------------------------------------------------
CREATE TABLE `shop_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `price` int(11) NOT NULL,
  `category` enum('TRAVEL','FUEL','UPGRADE','LOOTBOX','POWERUP','SERVICE') NOT NULL,
  `effect_type` varchar(50) DEFAULT NULL,
  `effect_value` int(11) DEFAULT NULL,
  `effect_duration` int(11) DEFAULT NULL,
  `max_purchases_per_game` int(11) DEFAULT 3,
  `is_active` tinyint(1) DEFAULT 1,
  `refresh_condition` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Dumping data for table `shop_items`
-- --------------------------------------------------------
INSERT INTO `shop_items` (`id`, `name`, `description`, `price`, `category`, `effect_type`, `effect_value`, `effect_duration`, `max_purchases_per_game`, `refresh_condition`) VALUES
(1, 'Extra Travel Ticket', 'Add +1 travel to your remaining travels', 1500, 'TRAVEL', 'add_travels', 1, NULL, 5, 'artifacts_delivered:2'),
(2, 'Fuel Pack (500km)', 'Add 500km of fuel to your tank', 800, 'FUEL', 'add_fuel', 500, NULL, 10, 'always'),
(3, 'Fuel Pack (1000km)', 'Add 1000km of fuel to your tank', 1500, 'FUEL', 'add_fuel', 1000, NULL, 5, 'always'),
(4, 'Mystery Loot Box', 'Random reward: fuel, money, clue, or item!', 1000, 'LOOTBOX', 'random_reward', NULL, NULL, 3, 'flights_taken:5'),
(5, 'Fuel Pass', 'Free fuel for next 5 travels', 3500, 'UPGRADE', 'fuel_pass', 5, 5, 2, 'phase_changed'),
(6, 'GPS Enhancer', 'Increase clue accuracy by 25% for 10 travels', 2500, 'POWERUP', 'clue_accuracy', 25, 10, 2, 'quests_completed:3'),
(7, 'Time Saver', 'Reduce negative event penalties by 50% for 8 travels', 2000, 'POWERUP', 'event_penalty_reduction', 50, 8, 3, 'events_triggered:5'),
(8, 'Clue Scanner', 'Reveals one random clue about current target', 1200, 'SERVICE', 'reveal_clue', 1, 1, 4, 'always'),
(9, 'Artifact Detector', 'Reveals one delivery airport location (usable 2 times)', 2500, 'SERVICE', 'reveal_delivery', 1, 1, 2, 'phase:DELIVERING_ARTIFACTS');

-- --------------------------------------------------------
-- Table structure for table `player_purchases`
-- --------------------------------------------------------
CREATE TABLE `player_purchases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `shop_item_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 1,
  `total_price` int(11) NOT NULL,
  `purchased_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  KEY `shop_item_id` (`shop_item_id`),
  CONSTRAINT `player_purchases_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  CONSTRAINT `player_purchases_ibfk_2` FOREIGN KEY (`shop_item_id`) REFERENCES `shop_items` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------
-- Create indexes for better performance
-- --------------------------------------------------------
CREATE INDEX idx_airports_region ON airports(region);
CREATE INDEX idx_airports_country ON airports(country);
CREATE INDEX idx_airports_tourist ON airports(is_tourist_destination);
CREATE INDEX idx_games_status ON games(game_status);
CREATE INDEX idx_games_player ON games(player_name);
CREATE INDEX idx_games_phase ON games(current_phase);
CREATE INDEX idx_logs_created ON game_logs(created_at);
CREATE INDEX idx_clues_phase ON game_clues(phase);
CREATE INDEX idx_clues_quality ON game_clues(quality);
CREATE INDEX idx_quests_type ON quests(quest_type);
CREATE INDEX idx_quests_expires ON quests(expires_at);
CREATE INDEX idx_events_type ON random_events(event_type);
CREATE INDEX idx_shop_category ON shop_items(category);
CREATE INDEX idx_inventory_active ON player_inventory(is_active);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;