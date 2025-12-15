-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 14 déc. 2025 à 23:40
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `services_particuliers`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id_categorie` int NOT NULL AUTO_INCREMENT,
  `nom_categorie` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id_categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id_categorie`, `nom_categorie`, `description`) VALUES
(1, 'Jardinage', 'Services liés à l’entretien des espaces verts, pelouses, haies et aménagements paysagers.'),
(2, 'Informatique', 'Services de réparation, assistance et formation dans le domaine des technologies.'),
(3, 'Entretien ménager', 'Services de nettoyage résidentiel et commercial.'),
(4, 'Transport et déménagement', 'Services de livraison, déménagement et transport de biens.'),
(5, 'Cours particuliers', 'Soutien scolaire et formation dans diverses matières et activités.');

-- --------------------------------------------------------

--
-- Structure de la table `compte`
--

DROP TABLE IF EXISTS `compte`;
CREATE TABLE IF NOT EXISTS `compte` (
  `id_compte` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `mdp` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` enum('admin','utilisateur') NOT NULL,
  `credit` int NOT NULL,
  PRIMARY KEY (`id_compte`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `compte`
--

INSERT INTO `compte` (`id_compte`, `nom`, `mdp`, `role`, `credit`) VALUES
(1, 'admin@garneau.ca', '60fb0832336f357512b52f4b54cdb4d1067a5b93cd9fef88a608080e2a2281e86da45b016aae0f5ecfc7350e21233eb1236cb18892ada107f01158dbf76b7781', 'admin', 0),
(12, 'alex.dupont@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(13, 'marie.lavoie@hotmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(14, 'simon.bergeron@yahoo.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(15, 'emma.tremblay@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(16, 'nathan.roy@outlook.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(17, 'julie.fortin@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(18, 'lucas.perron@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(19, 'amelie.gagne@hotmail.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(20, 'kevin.bouchard@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(21, 'sarah.leblanc@videotron.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(23, 'alex.dupont@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(24, 'marie.lavoie@hotmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(25, 'simon.bergeron@yahoo.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(26, 'emma.tremblay@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(27, 'nathan.roy@outlook.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(28, 'julie.fortin@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(29, 'lucas.perron@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(30, 'amelie.gagne@hotmail.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(31, 'kevin.bouchard@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(32, 'sarah.leblanc@videotron.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(33, 'antoine.morin@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(34, 'clara.deschamps@yahoo.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(35, 'yoan.leroux@hotmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(36, 'sophie.renaud@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(37, 'jimmy.paquin@outlook.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(38, 'melissa.darveau@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(39, 'victor.ouellet@live.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(40, 'amelia.carrier@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(41, 'gabriel.fontaine@yahoo.ca', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0),
(42, 'olivia.marchand@gmail.com', '50e27b5afd77a3b8576ebb0caa90964b4a1b8580a1832f07d430a1b7cab6a412018105b3643b6a41657efa725f7b3e6b66b707114b040f05b98d8ca5d780cba0', 'utilisateur', 0);

-- --------------------------------------------------------

--
-- Structure de la table `services`
--

DROP TABLE IF EXISTS `services`;
CREATE TABLE IF NOT EXISTS `services` (
  `id_service` int NOT NULL AUTO_INCREMENT,
  `id_categorie` int NOT NULL,
  `proprietaire` int NOT NULL,
  `titre` varchar(50) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `localisation` varchar(50) NOT NULL,
  `date_creation` datetime DEFAULT CURRENT_TIMESTAMP,
  `actif` tinyint(1) DEFAULT '1',
  `cout` decimal(8,2) DEFAULT '0.00',
  `photo` varchar(50) DEFAULT NULL,
  `locataire` int DEFAULT NULL,
  PRIMARY KEY (`id_service`),
  KEY `id_categorie` (`id_categorie`),
  KEY `fk_proprio` (`proprietaire`),
  KEY `fk_locataire` (`locataire`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `services`
--

INSERT INTO `services` (`id_service`, `id_categorie`, `proprietaire`, `titre`, `description`, `localisation`, `date_creation`, `actif`, `cout`, `photo`, `locataire`) VALUES
(34, 1, 12, 'Tonte de pelouse', 'Tonte professionnelle avec coupe-bordure et ramassage.', 'Québec', '2025-11-15 11:25:09', 1, 35.00, 'pelouse1.jpg', 1),
(35, 1, 18, 'Taille de haies', 'Taille de haies, arbustes, et nettoyage complet.', 'Beauport', '2025-11-15 11:25:09', 1, 55.00, 'haies1.jpg', 1),
(36, 1, 20, 'Déneigement entrée', 'Déneigement manuel de l’entrée et des marches.', 'Charlesbourg', '2025-11-15 11:25:09', 1, 25.00, 'neige.jpg', NULL),
(37, 1, 28, 'Plantation de jardins', 'Plantation de fleurs et légumes selon vos préférences.', 'Lévis', '2025-11-15 11:25:09', 1, 40.00, 'plants.jpg', NULL),
(38, 1, 17, 'Entretien complet terrain', 'Service mensuel incluant tonte, haies, arrosage.', 'Québec', '2025-11-15 11:25:09', 1, 90.00, 'terrain.jpg', NULL),
(39, 2, 14, 'Réparation PC', 'Réparation, nettoyage interne et optimisation complète.', 'Québec', '2025-11-15 11:25:09', 1, 60.00, 'pcfix1.jpg', 1),
(40, 2, 16, 'Installation Windows', 'Installation Windows 10/11 + optimisation.', 'Sainte-Foy', '2025-11-15 11:25:09', 1, 45.00, 'windows.jpg', NULL),
(41, 2, 25, 'Montage PC gamer', 'Montage professionnel, test de stabilité et câblage.', 'Limoilou', '2025-11-15 11:25:09', 1, 80.00, 'pcbuild.jpg', NULL),
(43, 2, 26, 'Nettoyage virus', 'Suppression virus/malware + optimisation.', 'Québec', '2025-11-15 11:25:09', 1, 40.00, 'virus.jpg', NULL),
(44, 3, 15, 'Ménage résidentiel', 'Nettoyage complet cuisine, salle de bain, planchers.', 'Québec', '2025-11-15 11:25:09', 1, 75.00, 'menage1.jpg', NULL),
(45, 3, 21, 'Lavage de vitres', 'Vitres intérieures et extérieures (rez-de-chaussée).', 'Lévis', '2025-11-15 11:25:09', 1, 50.00, 'vitres.jpg', NULL),
(46, 3, 24, 'Nettoyage intensif', 'Grand ménage complet avant inspection.', 'Sillery', '2025-11-15 11:25:09', 1, 120.00, 'intensif.jpg', NULL),
(47, 3, 30, 'Nettoyage bureaux', 'Entretien commercial hebdomadaire.', 'Québec', '2025-11-15 11:25:09', 1, 150.00, 'bureau.jpg', NULL),
(48, 3, 27, 'Désinfection complète', 'Désinfection pièces communes et surfaces.', 'Beauport', '2025-11-15 11:25:09', 1, 65.00, 'sanitize.jpg', NULL),
(49, 4, 23, 'Petit déménagement', 'Transport de meubles et électros.', 'Québec', '2025-11-15 11:25:09', 1, 95.00, 'dem1.jpg', NULL),
(50, 4, 18, 'Livraison locale', 'Livraison petites marchandises Québec–Lévis.', 'Québec', '2025-11-15 11:25:09', 1, 25.00, 'livraison.jpg', NULL),
(51, 4, 29, 'Transport sofa', 'Transport de gros meubles (sofa, matelas, etc.).', 'Charlesbourg', '2025-11-15 11:25:09', 1, 70.00, 'sofa.jpg', NULL),
(52, 4, 21, 'Aide déménagement', 'Aide à l’emballage et chargement/déchargement.', 'Limoilou', '2025-11-15 11:25:09', 1, 60.00, 'box.jpg', NULL),
(53, 4, 13, 'Transport express', 'Livraison urgente le jour même.', 'Québec', '2025-11-15 11:25:09', 1, 40.00, 'express.jpg', NULL),
(54, 5, 12, 'Cours de math', 'Soutien scolaire secondaire 1–5.', 'En ligne', '2025-11-15 11:25:09', 1, 30.00, 'math.jpg', NULL),
(55, 5, 17, 'Cours d’anglais', 'Cours oral/écrit, niveaux débutant à avancé.', 'Québec', '2025-11-15 11:25:09', 1, 25.00, 'english.jpg', NULL),
(56, 5, 26, 'Cours Excel avancé', 'Formules, tableaux croisés, automatisation.', 'En ligne', '2025-11-15 11:25:09', 1, 35.00, 'excel.jpg', NULL),
(58, 5, 30, 'Préparation examens', 'Aide aux révisions + stratégie d’étude.', 'Sainte-Foy', '2025-11-15 11:25:09', 1, 28.00, 'exam.jpg', NULL),
(59, 1, 29, 'Arrosage automatique', 'Installation de système d’arrosage.', 'Lévis', '2025-11-15 11:25:09', 1, 150.00, 'arrosage.jpg', NULL),
(60, 2, 12, 'Support télétravail', 'Installation et configuration Zoom/VPN.', 'Québec', '2025-11-15 11:25:09', 1, 30.00, 'teletravail.jpg', NULL),
(61, 3, 25, 'Nettoyage tapis', 'Shampoing à la machine de tapis et carpettes.', 'Québec', '2025-11-15 11:25:09', 1, 60.00, 'tapis.jpg', NULL),
(62, 4, 27, 'Livraison Montréal–Québec', 'Transport interville à prix fixe.', 'Québec', '2025-11-15 11:25:09', 1, 120.00, 'interville.jpg', NULL),
(63, 5, 24, 'Cours espagnol', 'Introduction à la langue espagnole.', 'En ligne', '2025-11-15 11:25:09', 1, 22.00, 'espagnol.jpg', NULL);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`id_categorie`) REFERENCES `categories` (`id_categorie`),
  ADD CONSTRAINT `services_ibfk_2` FOREIGN KEY (`proprietaire`) REFERENCES `compte` (`id_compte`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `services_ibfk_3` FOREIGN KEY (`locataire`) REFERENCES `compte` (`id_compte`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
