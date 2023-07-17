-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema telegramm
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema telegramm
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `telegramm` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `telegramm` ;

-- -----------------------------------------------------
-- Table `telegramm`.`keys`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `telegramm`.`keys` (
  `key` VARCHAR(100) NOT NULL,
  `official_name` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`key`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `telegramm`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `telegramm`.`messages` (
  `chat_id` BIGINT NULL DEFAULT NULL,
  `message` VARCHAR(1000) NULL DEFAULT NULL,
  `time` DATETIME NULL DEFAULT NULL,
  `message_id` INT NOT NULL AUTO_INCREMENT,
  `is_sent` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`message_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 217
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `telegramm`.`users_main`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `telegramm`.`users_main` (
  `chat_id` BIGINT NOT NULL,
  `first_name` VARCHAR(1000) NULL DEFAULT NULL,
  `username` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`chat_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `telegramm`.`users_optional`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `telegramm`.`users_optional` (
  `chat_id` BIGINT NOT NULL,
  `official_name` VARCHAR(1000) NULL DEFAULT NULL,
  `group` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`chat_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
