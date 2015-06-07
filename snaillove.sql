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
(NULL, "Snail"),
(NULL, "Bee"),
(NULL, "Starfish");

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
(NULL, "LeeJiHam", "Tea Tree 90 Essence", 40, "An age-old remedy for a spectrum of skin conditions including acne and eczema, tea tree oil reduces redness, soothes, and rejuvinates the skin. Formulated with 90% natural tea tree extract, you can feel its power of revitalization as Tea Tree 90 Essence alleviates uneven skin tone, minimizes redness, refreshes the skin, and improves overall complexion. With over 800x more Vitamin C than an apple, your skin will thank you for the invigorating treatment that leaves it rejuvinated and radiant.", 1, 4, 1),
(NULL, "Skinfood", "Peach Sake Pore Serum", 15, "Description: Rich in Vitamins A, C and Silica Powder derived from rice sake and peach extract, this product is a multi-functional item. Not only does this serum moisture the skin but also helps prevent sebum production while simultaneously minimizing the appearance of pores.", 1, 4, 5),
(NULL, "Banila Co.", "Clean It Zero", 15, "Heralded as one of Allure Magazine's (Korea) Editor's Picks, this award-winning hypoallergenic cleansing cream has finally hit our stores. This unique product applies as a solid balm and then transforms into a silky oil on the skin as you massage the product on your skin. Dissolving the most stubborn makeup and removing any impurities from your skin while keeping your skin's essential oils in tact. Formulated with various Extracts and Vitamins like Papaya Extract and Vitamin C, your skin will feel clean, smooth, and radiant.", 4, 1, 4),
(NULL, "Leaders", "Teatree Relaxing Renewal Mask", 2, "This soothing tea tree sheet mask is infused with organic leaf extracts (birch, hazelnut and olive) that helps control oily, irritated skin and reduces the appearance of unbalanced skin. Its natural extracts repairs damage on the skin and helps exfoliate, purify and soften the complexion giving the skin a radiant glow.", 2, 7, 1),
(NULL, "Missha", "Time Revolution The First Treatment Essence", 50, "Heralded as a miracle water, the First Treatment Essence is a powerful skin experience. The 80% yeast concentrate energizes your skin cells with regenerative properties. First Treatment Essence replenishes elasticity, revives skin tone, and reveals softened, soothed skin. Signs of aging will be rebuffed and the old will be replaced by the new - bringing you closer to a flawless complexion. This essence hydrates, restores, rejuvenates, and gives you a glowing complexion. This product contains Niacinamide, a Vitamin B3 component, to improve skin elasticity, enhance skin barrier function, and revive skin tone and texture. DN-Aid, made from Cassia-Alata Extract, provides vitality to aging skin, protects DNA from aging caused by UV rays, and promotes restoration of damaged DNA.", 2, 3, 2),
(NULL, "Elizavecca", "Milky Piggy Carbonated Bubble Clay Mask", 9, "This bubble clay mask is both a deep-cleansing makeup remover and pore cleanser in one! With its special formulation of charcoal powder, it deeply penetrates the pores to thoroughly get rid of deep-seated dirt while supplying proper nutrients to keep the skin healthy and supple. It not only cleanses, refines and tightens pores but it also helps control excessive sebum which usually causes the pores to be clogged.", 2, 7, 1);


DELETE FROM users;
INSERT INTO users VALUES
(NULL, "jessica@gmail.com", "mypass", "Jessica", "Simpson", "90210", 1, "Oily"),
(NULL, "britney@gmail.com", "mypass", "Britney", "Spears", "90210", 1, "Oily");


DELETE FROM ratings;
INSERT INTO ratings VALUES
(NULL, 1, 1, 5, "I love this stuff. Helps with everything!"),
(NULL, 1, 2, 1, "I hate this stuff. Makes everything worse!");