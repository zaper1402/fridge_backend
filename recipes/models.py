from django.db import models

# Create your models here.
#Collumn : Name	Image URL	Time to Cook	Difficulty	Servings	Description	Cuisine Tags	Ingredients	Instructions																	
#Sample Row : Kids Can Make: Strawberry French Toast Roll-Ups	https://d2vsf1hynzxim7.cloudfront.net/production/media/22479/responsive-images/foodnetwork-image-e69cd580-23f3-4388-aa08-539a0ffd3a43___default_283_212.jpeg	1 HRS 5 MINS	EASY	4	These fun, crunchy and sweet roll-ups are the kind of breakfast food that both kids and adults will like. Get kids involved in the cooking. For little and big kids: Let them help with rolling the bread out and filling and coating the roll-ups. For an easy variation, swap out the cream cheese and sugar in the filling for 1/4 cup chocolate-hazelnut spread.	EGG RECIPES, BREAKFAST RECIPES, BRUNCH RECIPES, SCHOOL HOLIDAY RECIPES TO KEEP THE KIDS OCCUPIED, TOAST WITH THE MOST: DELIGHTFUL FRENCH TOAST RECIPES	[Cooking spray], [45g cream cheese, at room temperature], [2 tablespoons plus 100g sugar], [6 slices stale white sandwich bread, crusts removed], [5 or 6 strawberries, diced], [60ml heavy cream], [2 large eggs, beaten], [1 tablespoon ground cinnamon], [Maple syrup, optional]	[  Preheat the oven to 190 degrees C. Line a baking sheet with parchment, and spray the parchment with cooking spray.  ], [Mix together the cream cheese and 2 tablespoons sugar in a small bowl. Roll each slice of bread flat with a rolling pin, and spread with 1 heaping teaspoon of the cream cheese mixture. Place 2 heaping teaspoons of the diced strawberries at one end of each slice. Starting at that end, roll up each slice. Pinch and press the seam and ends so each roll-up is sealed, and push back in any ingredients that may have snuck out of the ends.  ], [Whisk the cream and eggs together in a small bowl. Combine the remaining 100g sugar and the cinnamon in a shallow dish. Dip each roll-up in the egg mixture until completely submerged, shake off excess egg, then cover completely in the cinnamon sugar. Arrange the roll-ups, seam-side down and evenly spaced, on the prepared baking sheet.  ], []																	
# create model for this schema above

class Recipe(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    image_url = models.URLField()
    time_to_cook = models.IntegerField(null=True)
    difficulty = models.CharField(max_length=255)
    servings = models.IntegerField(null=True)
    description = models.TextField()
    cuisine_tags = models.JSONField()
    ingredients = models.JSONField(null=False, blank=False)
    instructions = models.JSONField(null=False, blank=False)

    unique_together = ('name', 'description')

    def __str__(self):
        return self.name
    



