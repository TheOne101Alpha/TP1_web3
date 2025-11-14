-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 30 sep. 2025 à 02:17
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
-- Structure de la table `services`
--

DROP TABLE IF EXISTS `services`;
CREATE TABLE IF NOT EXISTS `services` (
  `id_service` int NOT NULL AUTO_INCREMENT,
  `id_categorie` int NOT NULL,
  `titre` varchar(50) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `localisation` varchar(50) NOT NULL,
  `date_creation` datetime DEFAULT CURRENT_TIMESTAMP,
  `actif` tinyint(1) DEFAULT '1',
  `cout` decimal(8,2) DEFAULT '0.00',
  `photo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_service`),
  KEY `id_categorie` (`id_categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `services`
--

INSERT INTO `services` (`id_service`, `id_categorie`, `titre`, `description`, `localisation`, `date_creation`, `actif`, `cout`, `photo`) VALUES
(1, 1, 'Tonte de pelouse', 'Entretien régulier de votre pelouse, incluant coupe et ramassage du gazon.', 'Montréal', '2025-09-29 00:00:00', 0, 40.00, 'pelouse.jpg'),
(2, 1, 'Taille de haies', 'Taille et entretien des haies et arbustes avec équipement professionnel.', 'Québec', '2025-09-24 22:53:17', 1, 55.00, 'haies.jpg'),
(3, 1, 'Aménagement paysager', 'Conception et réalisation de plates-bandes et jardins décoratifs.', 'Sherbrooke', '2025-09-24 22:53:17', 1, 200.00, 'paysager.jpg'),
(4, 1, 'Déneigement résidentiel', 'Pelletage et déglaçage des entrées et trottoirs durant l’hiver.', 'Laval', '2025-09-24 22:53:17', 1, 45.00, 'deneigement.jpg'),
(5, 2, 'Réparation ordinateur', 'Diagnostic et réparation d’ordinateurs portables ou de bureau.', 'Trois-Rivières', '2025-09-24 22:53:17', 1, 85.00, 'reparation_pc.jpg'),
(6, 2, 'Installation Wi-Fi', 'Configuration et optimisation d’un réseau Wi-Fi domestique.', 'Montréal', '2025-09-24 22:53:17', 1, 100.00, 'wifi.jpg'),
(7, 2, 'Suppression de virus', 'Nettoyage de logiciels malveillants et installation d’antivirus.', 'Québec', '2025-09-24 22:53:17', 1, 70.00, 'antivirus.jpg'),
(8, 2, 'Cours bureautique', 'Formation sur Word, Excel et PowerPoint pour débutants.', 'Gatineau', '2025-09-24 22:53:17', 1, 50.00, 'bureautique.jpg'),
(9, 3, 'Ménage résidentiel', 'Nettoyage complet hebdomadaire ou mensuel d’appartements et maisons.', 'Longueuil', '2025-09-24 22:53:17', 1, 90.00, 'menage_residentiel.jpg'),
(10, 3, 'Grand ménage saisonnier', 'Nettoyage en profondeur au printemps ou à l’automne.', 'Montréal', '2025-09-24 22:53:17', 1, 180.00, 'menage_saisonnier.jpg'),
(11, 3, 'Entretien de bureaux', 'Service de nettoyage pour espaces de travail et locaux commerciaux.', 'Québec', '2025-09-24 22:53:17', 1, 250.00, 'menage_bureau.jpg'),
(12, 3, 'Nettoyage de tapis', 'Shampooing et assainissement de tapis et carpettes.', 'Sherbrooke', '2025-09-24 22:53:17', 1, 120.00, 'nettoyage_tapis.jpg'),
(13, 4, 'Déménagement local', 'Transport complet de biens dans la même ville avec camion et équipe.', 'Montréal', '2025-09-24 22:53:17', 1, 600.00, 'demenagement_local.jpg'),
(14, 4, 'Livraison de meubles', 'Transport de meubles neufs ou usagés avec protection et manutention.', 'Québec', '2025-09-24 22:53:17', 1, 90.00, 'livraison_meubles.jpg'),
(15, 4, 'Transport de colis', 'Livraison rapide de colis volumineux ou fragiles entre villes.', 'Gatineau', '2025-09-24 22:53:17', 1, 110.00, 'transport_colis.jpg'),
(16, 4, 'Covoiturage Québec-Montréal', 'Trajet partagé entre Québec et Montréal, prix par passager.', 'Québec', '2025-09-24 22:53:17', 1, 30.00, 'covoiturage.jpg'),
(17, 5, 'Cours de mathématiques', 'Soutien scolaire en mathématiques niveau secondaire et collégial.', 'Sherbrooke', '2025-09-24 22:53:17', 1, 35.00, 'cours_math.jpg'),
(18, 5, 'Cours de français', 'Aide en grammaire, lecture et rédaction pour élèves du secondaire.', 'Montréal', '2025-09-24 22:53:17', 1, 30.00, 'cours_francais.jpg'),
(19, 5, 'Cours d’anglais', 'Cours de conversation et grammaire anglaise pour débutants.', 'Québec', '2025-09-24 22:53:17', 1, 40.00, 'cours_anglais.jpg'),
(20, 5, 'Cours de guitare', 'Leçons individuelles de guitare acoustique ou électrique.', 'Trois-Rivières', '2025-09-24 22:53:17', 1, 50.00, 'cours_guitare.jpg');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `services`
--

ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`id_categorie`) REFERENCES `categories` (`id_categorie`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
