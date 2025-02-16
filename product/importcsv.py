import csv
from product.models import Product

def import_products_from_csv():
    csv_file_path = "/home/auriga/Downloads/data.csv"  # Ensure this path is correct

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        products = []

        for row in reader:
            name = row["Name"]
            category = row["Category"]
            tags = eval(row["Tags"]) if row["Tags"] else []  # Convert string list to actual list
            allergy_tags = eval(row["Allergy Tags"]) if row["Allergy Tags"] else []  # Convert string list to actual list

            # Convert allergy tags to match our AllergyTags choices, default to 'NONE' if empty
            allergy_tags = [tag for tag in allergy_tags if tag] or ['NONE']

            standard_expiry_days = int(row["Standard Expiry Days"]) if row["Standard Expiry Days"] else None

            product = Product(
                name=name,
                category=category,
                tags=tags,
                allergy_tags=allergy_tags,
                standard_expiry_days=standard_expiry_days
            )
            products.append(product)

        Product.objects.bulk_create(products)  # Bulk insert for efficiency

    print("Data imported successfully!")

# Call the function to import data
import_products_from_csv()
