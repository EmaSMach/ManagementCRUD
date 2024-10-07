# Tables definitions for products

TABLES = {
    "products": (
        "CREATE TABLE IF NOT EXISTS `products` ("
        "  `code` varchar(100) NOT NULL,"
        "  `name` varchar(230) NOT NULL,"
        "  `price` decimal(10,2) NOT NULL,"
        "  `description` text NULL,"
        "  `stock` int(11) NOT NULL,"
        "  `available` boolean NOT NULL DEFAULT 1,"
        "  `product_type` varchar(100) NOT NULL DEFAULT 'product',"
        "  PRIMARY KEY (`code`)"
        ") ENGINE=InnoDB"
    ),
    "electronics": (
        "CREATE TABLE IF NOT EXISTS `electronics` ("
        "  `code` varchar(100) NOT NULL,"
        "  `warranty` int(11) NULL,"
        "  PRIMARY KEY (`code`),"
        "  CONSTRAINT `fk_electronics_code` FOREIGN KEY (`code`) "
        "     REFERENCES `products` (`code`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    ),
    "food": (
        "CREATE TABLE IF NOT EXISTS `food` ("
        "  `code` varchar(100) NOT NULL,"
        "  `expiration_date` date NULL,"
        "  PRIMARY KEY (`code`),"
        "  CONSTRAINT `fk_food_code` FOREIGN KEY (`code`) "
        "     REFERENCES `products` (`code`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    ),
    "clothing": (
        "CREATE TABLE IF NOT EXISTS `clothing` ("
        "  `code` varchar(100) NOT NULL,"
        "  `size` varchar(20) NULL,"
        "  `color` varchar(50) NULL,"
        "  PRIMARY KEY (`code`),"
        "  CONSTRAINT `fk_clothing_code` FOREIGN KEY (`code`) "
        "     REFERENCES `products` (`code`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    ),
}
