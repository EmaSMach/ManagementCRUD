CREATE TABLE `products` (
  `code` varchar(100) NOT NULL,
  `name` varchar(230) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text,
  `stock` int NOT NULL,
  `available` tinyint(1) NOT NULL DEFAULT '1',
  `product_type` varchar(100) NOT NULL DEFAULT 'product',
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `food` (
  `code` varchar(100) NOT NULL,
  `expiration_date` date DEFAULT NULL,
  PRIMARY KEY (`code`),
  CONSTRAINT `fk_food_code` FOREIGN KEY (`code`) REFERENCES `products` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `electronics` (
  `code` varchar(100) NOT NULL,
  `warranty` int DEFAULT NULL,
  PRIMARY KEY (`code`),
  CONSTRAINT `fk_electronics_code` FOREIGN KEY (`code`) REFERENCES `products` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `clothing` (
  `code` varchar(100) NOT NULL,
  `size` varchar(20) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`),
  CONSTRAINT `fk_clothing_code` FOREIGN KEY (`code`) REFERENCES `products` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
