GlowBB
============

GlowBB is a web application created by Nicole Rinn for her final project at Hackbright Academy, Spring 2015, Cohort X. It is intended to be used as a tool for skin care product consumers. Namely those interested in purchasing products from Asia. The South Korean skin care market has seen huge growth in the past several years and is currently a $10 billion dollar + industry. Within the past few years major U.S. retailers like Sephora, Urban Outfitters, and Target have each picked up multiple South Korean skin care brands.

The appeal comes from the high quality of the products, coupled together with very reasonable prices. The skin care industry there is also extremely innovative, and comes out with new and exciting products frequently. They use igredients like snail mucous and bee venom, which are not commonly found in Western skin care. The South Korean skin care routine typically consists of 7-12 steps. Each step is targeted toward a specific skin issue. The Western skin care market usually aims more for shoving as many "uses" for their product in as they can.

But with a potential 10 step routine, how do you know what products to purchase? It can be overwhelming due to the massive number of products available. Many people aren't even aware of their skin type, and what sort of products they should be looking for in order to address their personal skin issues. This is where my app, GlowBB comes in. It offers the user personalized product recommendations for each potential step in their routine, based on the way they answer some questions about their skin.

It was created with a Python back end and a Flask framework. I used SQLite for the database and SQLAlchemy for my ORM. When a user sumits their form, an algorithm is run that calculates their "beauty type" based on the way they answered each question. The the highest value calculated by the algorithm coordinates with the appropriate beauty type for the user.

Once the user has received their beauty type and personalized product recommendations they can:
- rate and review products in the database,
- do a general search using a search engine I created, in case they are looking for certain brands, ingredients, etc.
- The application also offers a crowdsourcing feature where the users can ADD products to the database. Those products are filtered by beauty type and product category, and then made available for other users to see and rate.

Nearly everything I used to create this project was taught to me at Hackbright Academy. I am planning to deploy this app to the web, and expand and add additional features in the near future. The features I plan to add in the future (some are already works in progress) include:
- Connectivity to Reddit via their API. Reddit has a thriving Asian Beauty subreddit filled with tons of useful info. Adding the top 10 Reddit results for each product to its detail page would make it even easier for the customer to learn more about which products are right for them.
- I'd also like to expand the product database, as well as make it even easier for users to search for products by specific skin issues.
- As it is sometimes difficult to find these products, I also intend to add a feature that shows where you can purchase the product for the lowest price online, and possibly in the user's own area should they have stores in their areas.
