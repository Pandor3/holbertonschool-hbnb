CREATE TABLE User
(
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place
(
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    CONTRAINT owner_id FOREIGN KEY(user_id) REFERENCES User(id)
);

CREATE TABLE Review
(
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES User(id),
    CONTRAINT fk_place FOREIGN KEY(place_id) REFERENCES Place(id),
    CONSTRAINT unique_user_place UNIQUE(user_id, place_id)
);

CREATE TABLE Amenity
(
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
