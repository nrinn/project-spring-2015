DELETE FROM concerns;
INSERT INTO concerns VALUES
(NULL, "Acne"),
(NULL, "Aging"),
(NULL, "Dryness"),
(NULL, "Dullness"),
(NULL, "Oiliness"),
(NULL, "Scars");

DELETE FROM beauty_types;
INSERT INTO beauty_types VALUES
(NULL, "Dewdrop"),
(NULL, "Combination"),
(NULL, "Normal"),
(NULL, "Dry");

DELETE FROM product_categories;
INSERT INTO product_categories VALUES
(NULL, "Cleanser 1"),
(NULL, "Cleanser 2"),
(NULL, "Toner/Skin/Treatment Essence"),
(NULL, "Essence/Ampoule/Serum"),
(NULL, "Moisturizer/Lotion/Emulsion"),
(NULL, "Exfoliant"),
(NULL, "Mask"),
(NULL, "Sunscreen");

DELETE FROM products;
INSERT INTO products VALUES
(NULL, "LeeJiHam", "Tea Tree 90 Essence", 40, "An age-old remedy for a spectrum of skin conditions including acne and eczema, tea tree oil reduces redness, soothes, and rejuvinates the skin. Formulated with 90% natural tea tree extract, you can feel its power of revitalization as Tea Tree 90 Essence alleviates uneven skin tone, minimizes redness, refreshes the skin, and improves overall complexion. With over 800x more Vitamin C than an apple, your skin will thank you for the invigorating treatment that leaves it rejuvinated and radiant.", 1, 4);

DELETE FROM ratings;
INSERT INTO ratings VALUES
(NULL, 1, 1, 5);