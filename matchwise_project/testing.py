import sqlite3
import os

# Set DB path relative to script
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add skill
cursor.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", ("First Aid",))
conn.commit()
cursor.execute("SELECT skill_id FROM skills WHERE name = ?", ("First Aid",))
skill_id = cursor.fetchone()[0]

# Add users with real locations
cursor.execute("INSERT OR IGNORE INTO users (full_name, email, location, availability) VALUES (?, ?, ?, ?)",
               ("Requester QC", "reqqc@example.com", "Quezon City, Philippines", "Mon 9-12,Wed 14-16"))

cursor.execute("INSERT OR IGNORE INTO users (full_name, email, location, availability) VALUES (?, ?, ?, ?)",
               ("Offerer Manila", "offermla@example.com", "Manila, Philippines", "Mon 10-12"))

cursor.execute("INSERT OR IGNORE INTO users (full_name, email, location, availability) VALUES (?, ?, ?, ?)",
               ("Offerer Cebu", "offercebu@example.com", "Cebu City, Philippines", "Tue 14-16"))

conn.commit()

# Get user IDs
cursor.execute("SELECT user_id FROM users WHERE email = ?", ("reqqc@example.com",))
req_id = cursor.fetchone()[0]
cursor.execute("SELECT user_id FROM users WHERE email = ?", ("offermla@example.com",))
mla_id = cursor.fetchone()[0]
cursor.execute("SELECT user_id FROM users WHERE email = ?", ("offercebu@example.com",))
cebu_id = cursor.fetchone()[0]

# Insert listings
cursor.execute("INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km) VALUES (?, ?, 'request', ?, ?, ?, ?)",
               (req_id, skill_id, "Needs first aid help in QC", "Mon 9-12,Wed 14-16", "Quezon City, Philippines", 50))

cursor.execute("INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km) VALUES (?, ?, 'offer', ?, ?, ?, ?)",
               (mla_id, skill_id, "First aid volunteer based in Manila", "Mon 10-12", "Manila, Philippines", 50))

cursor.execute("INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km) VALUES (?, ?, 'offer', ?, ?, ?, ?)",
               (cebu_id, skill_id, "Certified provider in Cebu", "Tue 14-16", "Cebu City, Philippines", 50))

conn.commit()
conn.close()
print("✅ Real location test data inserted.")
