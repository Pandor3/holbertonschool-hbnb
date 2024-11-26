-- Insert a user (admin)
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$GJ1/6VbWtjT8VweuBGwone78VfuROiPf.iQ5GZPZuzYtcNj5dNiqq',
    TRUE
);

-- Insert amenities (WiFi, Swimming Pool, Air Conditioning)
INSERT INTO Amenity (id, name)
VALUES 
('3c71786f-2bfc-4ee1-a809-bf0aeeebfb91', 'WiFi'),
('d71fae53-00be-4fbd-ace0-34d2dae64bab', 'Swimming Pool'),
('6cb584e6-d13e-4149-9c3b-bb76ea1c5b88', 'Air Conditioning');

-- Delete existing entries from Place (if necessary, first remove dependent data)
DELETE FROM Place_Amenity WHERE place_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
DELETE FROM Place_Amenity WHERE place_id = '4bfc8e2f-3b5a-45c5-98f1-d105f184e6f3';
DELETE FROM Review WHERE place_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
DELETE FROM Review WHERE place_id = '4bfc8e2f-3b5a-45c5-98f1-d105f184e6f3';

-- Deleting from the Place table after dependent data is removed
DELETE FROM Place WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
DELETE FROM Place WHERE id = '4bfc8e2f-3b5a-45c5-98f1-d105f184e6f3';

-- Inserting new data into the Place table with unique IDs
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES 
    ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Riyad', "c'est un super Riyad", 120.50, 44.5115, 0.32151, '36c9050e-ddd3-4c3b-9731-9f487208bbc1'),
    ('4bfc8e2f-3b5a-45c5-98f1-d105f184e6f3', 'Palace', "Magnifique palace", 500.00, 44.6000, 0.3500, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Verifying insertion of places
SELECT * FROM Place WHERE title = 'Riyad';
SELECT * FROM Place WHERE title = 'Palace';

-- Adding a new entry to the Review table (review for the Riyad)
INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES
    ('d09c1f9f-76d0-48f1-957d-5c1f55e5b1f4', 'Super endroit, très agréable!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Verifying the Review table entry
SELECT * FROM Review WHERE user_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1' AND place_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Verifying all amenities
SELECT * FROM Amenity;

-- Adding data to the Place_Amenity table to establish a many-to-many relationship
INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES 
    ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', '3c71786f-2bfc-4ee1-a809-bf0aeeebfb91'); -- WiFi for Riyad

-- Verifying Place_Amenity table relationship
SELECT * FROM Place_Amenity WHERE place_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SELECT * FROM Place_Amenity WHERE place_id = '4bfc8e2f-3b5a-45c5-98f1-d105f184e6f3';
