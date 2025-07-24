import sqlite3
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add skill
cursor.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", ("First Aid",))
conn.commit()
cursor.execute("SELECT skill_id FROM skills WHERE name = ?", ("First Aid",))
skill_id = cursor.fetchone()[0]

# Add users
cursor.execute("INSERT OR IGNORE INTO users (full_name, email, location, availability) VALUES (?, ?, ?, ?)",
               ("Request User", "request@example.com", "City A", "Mon 9-12,Wed 14-16"))
cursor.execute("INSERT OR IGNORE INTO users (full_name, email, location, availability) VALUES (?, ?, ?, ?)",
               ("Offer User 1", "offer1@example.com", "City A", "Mon 10-13"))
cursor.execute("INSERT OR IGNORE INTO users (full_name, email, location, availability) VALUES (?, ?, ?, ?)",
               ("Offer User 2", "offer2@example.com", "City B", "Tue 14-16"))
conn.commit()

# Get user IDs
cursor.execute("SELECT user_id FROM users WHERE email = ?", ("request@example.com",))
request_user_id = cursor.fetchone()[0]

cursor.execute("SELECT user_id FROM users WHERE email = ?", ("offer1@example.com",))
offer1_user_id = cursor.fetchone()[0]

cursor.execute("SELECT user_id FROM users WHERE email = ?", ("offer2@example.com",))
offer2_user_id = cursor.fetchone()[0]

# Add listings
cursor.execute("INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km) VALUES (?, ?, 'request', ?, ?, ?, ?)",
               (request_user_id, skill_id, "Need first aid support", "Mon 9-12,Wed 14-16", "City A", 10))

cursor.execute("INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km) VALUES (?, ?, 'offer', ?, ?, ?, ?)",
               (offer1_user_id, skill_id, "Trained first aid volunteer", "Mon 10-13", "City A", 10))

cursor.execute("INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km) VALUES (?, ?, 'offer', ?, ?, ?, ?)",
               (offer2_user_id, skill_id, "Certified first aid provider", "Tue 14-16", "City B", 10))

conn.commit()
conn.close()
print("✅ Test data inserted.")
