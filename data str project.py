from collections import deque
import random
import heapq

# Define the place class
class Place:
    def __init__(self, name, category, subcategory, distance, website):
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.distance = distance
        self.website = website

    def __str__(self):
        return f"{self.name} - {self.subcategory} ({self.distance} miles away) - {self.website}"


# Define the main app
class HiddenGemsApp:
    def __init__(self):
        self.places = []
        self.tree = {}
        self.nav_stack = []
        self.history = []
        self.favorites = []

    def add_place(self, place):
        self.places.append(place)

        # Add place to category tree
        if place.category not in self.tree:
            self.tree[place.category] = {}
        if place.subcategory not in self.tree[place.category]:
            self.tree[place.category][place.subcategory] = []
        self.tree[place.category][place.subcategory].append(place)

    def main_menu(self):
        print("\n📍 What are you looking for today?")
        print("[1] Food 🍜")
        print("[2] Drinks/Cafe 🧋")
        print("[3] Shopping 🛍️")
        print("[4] Nature & Parks 🌳")
        print("[5] Services 💼")
        print("[6] Places Nearby 🌍")
        print("[7] Surprise Me! 🎲")
        print("[8] Search 🔍")
        print("[9] BFS / DFS Traversal 🌐")
        print("[10]. Recommend based on...")
        print("[h] History 📜")
        print("[q] Exit")
        return input("\nEnter your choice: ").strip()

    def category_lookup(self, choice):
        categories = {
            "1": "Food", "2": "Drinks/Cafe", "3": "Shopping & Entertainment", "4": "Nature & Parks", "5": "Services",
            "6": "Places Nearby"
        }
        return categories.get(choice, None)

    def display_history(self):
        print("\n📜 Recently Viewed Places:")
        if not self.history:
            print("❌ No history available.")
        else:
            for item in self.history:
                print(f"- {item}")
        input("\nPress Enter to continue...")

    def display_places(self, places):
        if not places:
            print("❌ No places to show.")
            return False
        for i, place in enumerate(places):
            print(f"[{i + 1}] {place.name} ({place.distance} mi)")

        print("\nOptions: [number] View Details, [b] Go Back 🔙, [h] Home 🏠, [f] View Favorites ⭐")
        choice = input("Enter your choice: ").strip()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(places):
                self.view_place_details(places[index])
        elif choice == "b":
            if self.nav_stack:
                self.nav_stack.pop()
        elif choice == "h":
            self.nav_stack = []
        elif choice == "f":
            self.view_favorites()
        else:
            print("❌ Invalid option.")
        return True

    def view_place_details(self, place):
        self.history.append(place)
        print(f"\n📌 {place.name}")
        print(f"Category: {place.category}")
        print(f"Subcategory: {place.subcategory}")
        print(f"Distance: {place.distance} miles")
        print(f"Website: {place.website}")
        print("\nOptions: [f] Favorite ⭐  [r] Recommend 🔁  [b] Back")

        choice = input("Enter your choice: ").strip().lower()
        if choice == "f":
            if place not in self.favorites:
                self.favorites.append(place)
                print("✅ Added to favorites!")
            else:
                print("⭐ Already in favorites.")
        elif choice == "r":
            self.recommend_places(place)
        elif choice == "b":
            return
        else:
            print("❌ Invalid choice.")

    def list_places(self):
        if not self.places:
            print("\n❌ No places added yet.")
            return
        print("\n📍 All Places:")
        for i, place in enumerate(self.places, 1):
            print(f"{i}. {place.name} - {place.subcategory} ({place.distance} mi)")

    def recommend_places(self, place):
        print(f"\n🔁 Recommendations based on {place.name}:")
        same_sub = self.tree.get(place.category, {}).get(place.subcategory, [])
        recommendations = [p for p in same_sub if p.name != place.name]

        if not recommendations:
            for sub, plist in self.tree.get(place.category, {}).items():
                for p in plist:
                    if p.name != place.name and p not in recommendations:
                        recommendations.append(p)

        if recommendations:
            for rec in recommendations[:5]:
                print(f"- {rec.name} ({rec.subcategory}, {rec.distance} mi)")
        else:
            print("❌ No similar places found.")
        input("Press Enter to continue...")

    def view_favorites(self):
        print("\n⭐ Your Favorite Places:")
        if not self.favorites:
            print("No favorites yet!")
        else:
            self.display_places(self.favorites)
        input("Press Enter to continue...")

    def search_places(self, query):
        print(f"\n🔍 Searching for '{query}'...")
        results = [place for place in self.places if query.lower() in place.name.lower()]
        self.display_places(results)

    def filter_places_by_distance(self, max_distance):
        print(f"\n🌍 Places within {max_distance} miles:")
        filtered = [place for place in self.places if place.distance <= max_distance]
        self.display_places(filtered)

    def dfs_traversal(self, category=None, subcategory=None):
        if not category:
            for category in self.tree:
                print(f"\n{category} Category:")
                self.dfs_traversal(category)

        if subcategory:
            print(f"  - {subcategory} Subcategory:")
            for place in self.tree[category][subcategory]:
                print(f"    - {place.name} ({place.distance} miles away)")

        if category and not subcategory:
            for subcategory in self.tree[category]:
                self.dfs_traversal(category, subcategory)

    def bfs_traversal(self):
        queue = deque(self.tree.keys())
        while queue:
            category = queue.popleft()
            print(f"\n{category} Category:")

            for subcategory in self.tree[category]:
                print(f"  - {subcategory} Subcategory:")
                for place in self.tree[category][subcategory]:
                    print(f"    - {place.name} ({place.distance} miles away)")


    def recommend_closest(self, place):
        print(f"\n📍 Closest places to {place.name}:")
        others = [p for p in self.places if p.name != place.name]

        closest = heapq.nsmallest(5, others, key=lambda x: abs(x.distance - place.distance))

        if closest:
            for p in closest:
                print(f"- {p.name} ({p.subcategory}, {p.distance} mi)")
        else:
            print("❌ No other places to recommend.")

        input("Press Enter to continue...")

    def run(self):
        print("🌟 Welcome to Hidden Gems Warm Springs — SFBU Students Edition! 🌟")
        if self.places:
            print("✨ Random Pick: ", random.choice(self.places))
        else:
            print("✨ No places added yet.")

        while True:
            if not self.nav_stack:
                choice = self.main_menu()
                if choice == "7":
                    if self.places:
                        print("🎲 Surprise Pick:", random.choice(self.places))
                    else:
                        print("🎲 No places to pick from!")
                    continue
                elif choice == "h":
                    self.display_history()
                    continue
                elif choice == "q":
                    print("👋 Thanks for exploring with us!")
                    break
                elif choice == "8":
                    query = input("Enter search term: ").strip()
                    self.search_places(query)
                    continue
                elif choice == "9":
                    print("\n[1] DFS Traversal\n[2] BFS Traversal")
                    traversal_choice = input("Choose traversal: ").strip()
                    if traversal_choice == "1":
                        self.dfs_traversal()
                    elif traversal_choice == "2":
                        self.bfs_traversal()
                    else:
                        print("❌ Invalid choice.")
                    continue
                elif choice == "10":
                    if not app.places:
                        print("\n⚠️ No places in the list. Please add places first.")
                        input("Press Enter to continue...")
                        continue

                    print("\n🔍 Recommend based on:")
                    print("1. Closeness")
                    print("2. Similarity")
                    sub_choice = input("Enter your choice: ")

                    # Let user pick a reference place
                    app.list_places()
                    try:
                        index = int(input("Choose a reference place by number: ")) - 1
                        if index < 0 or index >= len(app.places):
                            print("❌ Invalid selection.")
                            continue
                        ref_place = app.places[index]
                    except ValueError:
                        print("❌ Invalid input.")
                        continue

                    if sub_choice == "1":
                        app.recommend_closest(ref_place)
                    elif sub_choice == "2":
                        app.recommend_places(ref_place)
                    else:
                        print("❌ Invalid option.")

                else:
                    category = self.category_lookup(choice)
                    if category:
                        self.nav_stack.append(category)

                    else:
                        print("❌ Invalid choice. Please choose a valid option.")



            elif len(self.nav_stack) == 1:
                category = self.nav_stack[-1]
                print(f"\n📂 Subcategories in {category}:" if category == "Food" else f"\n📂 Places under {category}:")

                if category in self.tree and not any(self.tree[category].values()):
                    print(f"❌ No places to show under {category}. Returning to homepage...")
                    self.nav_stack = []
                    continue

                if category == "Food":
                    subcategories = list(self.tree[category].keys())
                    for i, sub in enumerate(subcategories):
                        print(f"[{i + 1}] {sub}")
                    print("[b] Go Back 🔙  [h] Home 🏠")
                    print("[b] Go Back 🔙")
                    sub_choice = input("Choose a subcategory or go back: ").strip()
                    if sub_choice == "b":
                        self.nav_stack.pop()
                    elif sub_choice.isdigit():
                        index = int(sub_choice) - 1
                        if 0 <= index < len(subcategories):
                            self.nav_stack.append(subcategories[index])
                            self.history.append(subcategories[index])
                        else:
                            print("❌ Invalid selection.")
                    else:
                        print("❌ Invalid input.")
                else:
                    # Not 'Food' – just list all places under this category
                    all_places = []
                    for sublist in self.tree.get(category, {}).values():
                        all_places.extend(sublist)
                    self.display_places(all_places)

            elif len(self.nav_stack) == 2:
                # Display places under a specific subcategory
                category, subcategory = self.nav_stack
                places = self.tree.get(category, {}).get(subcategory, [])
                self.display_places(places)


# Initialize app and add places
app = HiddenGemsApp()

# Add places to the app
app.add_place(Place("Teaspoon Boba", "Food", "Boba", 0.5, "www.teaspoon.com"))
app.add_place(Place("Rose Tea Boba", "Food", "Boba", 0.4, "www.roseteaboba.com"))
app.add_place(Place("Paris Baguette", "Food", "Bakery", 1.2, "www.parisbaguette.com"))
app.add_place(Place("Carls Jr", "Food", "Fast Food", 1.5, "www.carlsjr.com"))
app.add_place(Place("Guma Gumalu", "Food", "Restaurant", 2.0, "www.gumagumalu.com"))
app.add_place(Place("Donut Place", "Food", "Bakery", 0.3, "www.donutplace.com"))
app.add_place(Place("M Dumplings", "Food", "Restaurant", 1.0, "www.mdumplings.com"))
app.add_place(Place("Success Hair Services", "Services", "Braiding and natural hair care", 1.0, "www.successhairservices"))
app.add_place(Place("Wells Fargo", "Services", "Bank", 0.2, "www.wellsfargo.com"))
app.add_place(Place("Warm Springs BART", "Services", "Transportation", 0.3, "www.bart.gov"))
app.add_place(Place("Milpitas BART", "Services", "Transportation", 2.5, "www.bart.gov"))
app.add_place(Place("Lake Elizabeth", "Nature & Parks", "Park", 1.8, "www.lakeelizabethpark.com"))

# Add more places to the app
app.add_place(Place("Round1 Bowling & Amusement", "Shopping & Entertainment", "Arcade, bowling, karaoke", 0.6, "www.round1usa.com"))
app.add_place(Place("Dave & Buster’s", "Shopping & Entertainment", "Games, food, sports bar", 1.0, "www.daveandbusters.com"))
app.add_place(Place("Color Me Mine Fremont", "Shopping & Entertainment", "Paint-your-own pottery", 1.2, "www.colormemine.com"))
app.add_place(Place("The Art Beat Milpitas", "Shopping & Entertainment", "Art classes and creative workshops", 1.3, "www.theartbeatmilpitas.com"))
app.add_place(Place("Fremont Main Library", "Services", "Quiet study, reading, events", 1.4, "www.fremontlibrary.org"))
app.add_place(Place("Milpitas Library", "Services", "Spacious library, Wi-Fi, programs", 1.5, "www.santaclaracounty.gov"))
app.add_place(Place("Pacific Commons", "Shopping & Entertainment", "Outdoor mall with shops & dining", 1.6, "www.pacificcommons.com"))
app.add_place(Place("Fremont Hub", "Shopping & Entertainment", "Trader Joe’s, Marshalls, and more", 1.7, "www.fremonthub.com"))
app.add_place(Place("Great Mall", "Shopping & Entertainment", "Indoor outlet with top brands", 1.8, "www.greatmall.com"))
app.add_place(Place("Warm Springs Plaza", "Shopping & Entertainment", "Small plaza with Asian eats", 2.0, "www.warmspringsplaza.com"))
app.add_place(Place("Gateway Plaza", "Shopping & Entertainment", "Food, dessert, gym spots", 2.2, "www.gatewayplazamilpitas.com"))
app.add_place(Place("Auto Mall Parkway Retail Area", "Shopping & Entertainment", "Restaurants, services", 2.3, "www.automallparkway.com"))
app.add_place(Place("Mission Peak Regional Preserve", "Nature & Parks", "Epic hiking and views", 3.0, "www.park.ca.gov"))
app.add_place(Place("Lake Elizabeth / Central Park", "Nature & Parks", "Paddle boats, walks, chill", 2.5, "www.fremont.gov"))
app.add_place(Place("Alviso Marina County Park", "Nature & Parks", "Wetlands, bird watching", 2.7, "www.alvisomarina.com"))
app.add_place(Place("Coyote Creek Trail", "Nature & Parks", "Bike/walk trail through nature", 2.8, "www.coyotecreektrail.com"))
app.add_place(Place("Rose Tea Spot", "Drinks/Cafe", "Rose milk tea, boba", 1.0, "www.roseteaspot.com"))
app.add_place(Place("Happy Lemon", "Drinks/Cafe", "Bubble tea with salted cheese foam", 1.1, "www.happylemonusa.com"))
app.add_place(Place("Gong Cha", "Drinks/Cafe", "Taiwan-based boba chain", 1.2, "www.gongcha.com"))
app.add_place(Place("85°C Bakery Café", "Drinks/Cafe", "Sea salt coffee, taro bread", 1.3, "www.85cafe.com"))
app.add_place(Place("Tea Top", "Drinks/Cafe", "Taiwan tea drinks", 1.4, "www.teatop.com"))
app.add_place(Place("TP Tea", "Drinks/Cafe", "Premium tea-based drinks", 1.5, "www.tptea.com"))
app.add_place(Place("T4", "Drinks/Cafe", "Taiwanese boba and snacks", 1.6, "www.t4.com"))
app.add_place(Place("Sharetea", "Drinks/Cafe", "Classic milk and fruit teas", 1.7, "www.sharetea.com"))
app.add_place(Place("Yi Fang Taiwan Fruit Tea", "Drinks/Cafe", "Fruity, refreshing boba", 1.8, "www.yifangus.com"))
app.add_place(Place("Old Taro", "Drinks/Cafe", "Niche taro-based tea drinks", 1.9, "www.oldtaro.com"))
app.add_place(Place("Amami Sushi", "Food", "General", 2.0, "www.amamisushi.com"))
app.add_place(Place("Toro Sushi Stone Grill & Bar", "Food", "General", 2.1, "www.torosushigrill.com"))
app.add_place(Place("Kakuna Sushi", "Food", "General", 2.2, "www.kakunasushi.com"))
app.add_place(Place("Spoon Korean Bistro", "Food", "General", 2.3, "www.spoonkoreanbistro.com"))
app.add_place(Place("Wingstop", "Food", "General", 2.8, "www.wingstop.com"))
app.add_place(Place("Cold Stone Creamery", "Food", "General", 2.9, "www.coldstonecreamery.com"))
app.add_place(Place("McDonald's", "Food", "Fast Food", 3.0, "www.mcdonalds.com"))
app.add_place(Place("Mission San Jose", "Cultural Sites", "Historic Spanish mission with a rich history", 4.0, "www.missionsanjose.org"))
app.add_place(Place("Niles Essanay Silent Film Museum", "Places Nearby", "A historic site dedicated to silent films", 4.1, "www.nilessanay.org"))
app.add_place(Place("Fremont Cultural Arts Center", "Places Nearby", "Art exhibitions, cultural events", 4.2, "www.fremontartscenter.com"))
app.add_place(Place("Fremont Union Cemetery", "Places Nearby", "Historic cemetery, memorials, tours", 4.3, "www.fremontcemetery.com"))
app.add_place(Place("Boiling Point", "Food", "General", 1.5, "www.boilingpoint.com"))


# Run the app
app.run()