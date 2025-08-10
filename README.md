# Commerce (Online Auction Site) Project

## Author
**Billy Rono**  
GitHub: [me50/Billyrono](https://github.com/me50/Billyrono)

---

## Video Demo
See the entire project walkthrough on YouTube: [CS50 Project 2 – Commerce](https://youtube.com/)

---

## Description
This project is an **online auction site** built with Django, submitted as **Project 2** for **CS50’s Web Programming with Python and JavaScript**.  
It enables users to create auction listings, place bids, add items to a personal watchlist, post comments, and close auctions.

The platform mirrors key features of real-world auction websites, focusing on **user authentication**, **bid validation**, and **dynamic content management** using Django’s ORM.

---

## Distinctiveness and Complexity
This project goes beyond basic CRUD functionality by:

- **Bid validation logic** ensuring each bid meets/exceeds the starting price and is higher than the current bid.
- **Dynamic watchlist management** allowing users to add/remove items without page reload.
- **Auction state control** where only the creator can close auctions, and winners are displayed after closing.
- **Complex model relationships** between listings, users, bids, and comments.
- **Conditional UI rendering** based on authentication status and user’s relationship to the listing.

This combination of model logic and conditional rendering results in a **robust and interactive platform**.

---

## Features

### 1. User Authentication
- Users can **register, log in, and log out**.
- Only authenticated users can create listings, place bids, comment, and manage watchlists.

### 2. Create Auction Listings
- Form for **title, description, starting bid, optional image URL, and category**.
- Automatically records the creator and starting price.

### 3. Listing Page
- Displays title, description, image, current price, and category.
- Contextual actions:
  - Place bid (if active)
  - Add/remove watchlist
  - Close auction (creator only)
  - Show winner (when closed)
  - Post/view comments

### 4. Watchlist
- Personal watchlist per user.
- Toggle items on/off from listing page.
- Accessible via navigation bar.

### 5. Categories
- Filter listings by category.
- Shows only **active listings** in selected category.

### 6. Bidding
- Users can place bids that:
  - Meet/exceed starting bid
  - Are higher than current bids
- Updates price dynamically.

### 7. Comments
- Authenticated users can post comments.
- Comments shown in chronological order.

### 8. Closing Auctions
- Only listing creator can close auction.
- Highest bidder declared winner.
- Auction marked closed; bidding disabled.

---

## Technical Details
- **Language:** Python 3  
- **Framework:** Django  
- **Frontend:** HTML5, CSS3, Bootstrap5  
- **Database:** SQLite (via Django ORM)  
- **Authentication:** Django’s built-in auth system  

---

## File Structure
commerce/
    auctions/
        migrations/
        static/
        templates/
            auctions/
                auth.html
                categories.html
                category_listings.html
                create.html
                index.html
                layout.html
                listing.html
                login.html
                register.html
                watchlist.htm
        admin.py
        apps.py
        context_processors.py
        models.py
        tests.py
        urls.py
        views.py
    commerce/
        settings.py
        urls.py
        wsgi.py
    db.sqlite3
    manage.py
    README.md

---

## How to Run

1. **Install dependencies**
    ```bash
    pip install django
    ```

2. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

3. **Start the server**
    ```bash
    python manage.py runserver
    ```

4. **Open in browser**
    ```
    http://127.0.0.1:8000/
    ```

---

## Requirements Met
✅ Create listings with title, description, image, and category  
✅ Bid validation implemented  
✅ Watchlist functionality for authenticated users  
✅ Categories page filtering  
✅ Comments and bidding interface on listing page  
✅ Auction closing with winner display  
✅ Authentication and authorization implemented  
✅ Fully styled and functional to CS50W specification  

---

## Testing Instructions
Follow these steps to test all features:

1. **User Registration & Login**  
   - Visit `/register` and create two accounts (e.g., `user1`, `user2`).
   - Log in as `user1` and confirm navigation bar changes.

2. **Creating a Listing**  
   - As `user1`, create a listing.
   - Verify it appears on homepage.

3. **Bidding**  
   - Log in as `user2` and place a valid bid.
   - Attempt invalid bid to see validation error.

4. **Watchlist**  
   - Add a listing to watchlist as `user2`.
   - Confirm appearance in watchlist.
   - Remove and confirm disappearance.

5. **Comments**  
   - Post a comment as `user2`.
   - Confirm it appears under the listing.

6. **Closing Auctions**  
   - Log back in as `user1`.
   - Close auction.
   - Verify winner is displayed and bidding is disabled.

7. **Categories**  
   - Navigate to Categories.
   - Filter by category and verify results.

---

## Additional Notes on Development
- **Styling** – Bootstrap was used for clean design. Some responsiveness is achieved through Bootstrap, but most parts were custom-coded and may not be fully responsive on all devices.
- **AI Assistance** – AI was used for **guidance, structuring, and bug troubleshooting** only. All code were written manually to avoid plagiarism.
- **Pre-filled Comments** – 10 default comments were preloaded per listing for demonstration purposes; new comments append to the list dynamically.

---
