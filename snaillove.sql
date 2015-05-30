DELETE FROM product_categories;
INSERT INTO product_categories VALUES
(NULL, "Cleanser 1"),
(NULL, "Cleanser 2"),
(NULL, "Toner/Lotion/Skin/Treatment Essence"),
(NULL, "Essence/Ampoule/Serum"),
(NULL, "Moisturizer/Lotion/Emulsion"),
(NULL, "Eye Cream"),
(NULL, "Exfoliant"),
(NULL, "Mask"),
(NULL, "Sleeping Pack"),
(NULL, "Sunscreen");

DELETE FROM beauty_types;
INSERT INTO beauty_types VALUES
(NULL, "Dewdrop"),
(NULL, "Combination"),
(NULL, "Normal"),
(NULL, "Dry");

DELETE FROM concerns;
INSERT INTO concerns VALUES
(NULL, "Acne"),
(NULL, "Aging"),
(NULL, "Dryness"),
(NULL, "Dullness"),
(NULL, "Oiliness"),
(NULL, "Scars");