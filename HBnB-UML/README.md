<<<<<<< HEAD
<h1 align="left">HBnB - UML</h1>

###

<h3 align="left">1. Introduction</h3>

###

<p align="left">This document provides a comprehensive technical overview of the HBnB Evolution application, a simplified AirBnB-like platform. The purpose of this documentation is to serve as a guide for understanding the system's architecture, design, and how the core components interact. The document is intended for developers working on the project and will serve as a reference during the implementation phases.</p>

###

<h3 align="left">2. Project Overview</h3>

###

<p align="left">The HBnB Evolution application allows users to perform key operations such as managing user accounts, creating and listing places, submitting reviews, and associating amenities with places. The system is divided into three main entities:<br><br>• User Management: Users can register, update profiles, and be categorized as regular users or administrators.<br>• Place Management: Users can list places, add amenities, and set details like location and price.<br>• Review Management: Users can leave ratings and comments for places they have visited.<br>• Amenity Management: Amenities can be created, listed, and associated with places.<br><br>The system is structured using a layered architecture pattern, which separates concerns into the Presentation, Business Logic, and Persistence layers.</p>

###

<h3 align="left">3. High-Level Architecture</h3>

###

<p align="left">The HBnB Evolution application follows a three-layer architecture:<br><br>1. Presentation Layer: This includes the services and API through which users interact with the system. The API handles requests such as user registration, place creation, and review submission.<br><br>2. Business Logic Layer: Contains the core models (User, Place, Review, Amenity) and the logic that governs the system’s behavior. For example, this layer ensures that a user cannot review a place unless they have visited it.<br><br>3. Persistence Layer: Manages the database interactions, ensuring that all entities such as users, places, reviews, and amenities are stored and retrieved properly.</p>

###

<p align="left">The layers communicate through the Facade Pattern, which simplifies interaction by providing a unified interface.</p>

###

<h3 align="left">Diagram</h3>

###

<p align="left"></p>

###

<p align="left"></p>

###

<h3 align="left">4. Business Logic Layer</h3>

###

<p align="left">The core entities of the business logic are User, Place, Review, and Amenity. Each entity is defined by its attributes and methods. Below is the detailed structure for these entities:<br><br>User Entity<br>• Attributes: First name, last name, email, password, is_admin (boolean).<br>• Methods: Register, update profile, delete profile.<br><br>Place Entity<br>• Attributes: Title, description, price, latitude, longitude, owner (user), list of amenities.<br>• Methods: Create, update, delete, list.<br><br>Review Entity<br>• Attributes: Rating, comment, user, place.<br>• Methods: Submit, update, delete, list by place.<br><br>Amenity Entity<br>• Attributes: Name, description.<br>• Methods: Create, update, delete, list.</p>

###

<h3 align="left">Class Diagram</h3>

###

<p align="left"></p>

###

<h3 align="left">5. API Interaction Flow</h3>

###

<p align="left">The system exposes several API endpoints that allow users to perform different actions. Below is an outline of four key API calls:<br><br>1. User Registration: Handles user sign-up by validating and storing user data.<br>2. Place Creation: Allows a user to list a new place, including title, description, and price.<br>3. Review Submission: Allows a user to submit a review for a specific place.<br>4. Fetching a List of Places: Returns a list of places based on user-defined criteria.</p>

###

<h3 align="left">6. Sequence Diagrams</h3>

###

<h4 align="left">The following sequence diagrams represent how the application processes various API calls, illustrating the interaction between the Presentation Layer, Business Logic Layer, and Persistence Layer.</h4>

###

<p align="left">1. User Registration</p>

###

<h4 align="left"></h4>

###

<p align="left"></p>

###

<h4 align="left">2. Place Creation</h4>

###

<p align="left"></p>

###

<h3 align="left">7. Conclusion</h3>

###

<p align="left">This documentation provides a detailed blueprint for the HBnB Evolution application. The layered architecture, class diagrams, and sequence diagrams offer a clear understanding of the system's design and how various components interact. These diagrams and explanations will guide the implementation process, ensuring that all functional and business requirements are met.</p>

###

<h4 align="left">Licence</h4>

###

<p align="left">This project is licensed under the MIT license. You are free to use, modify and distribute it under the terms of the license.</p>

###

<h4 align="left"></h4>

###
=======
# HBnB - HolbertonBnB Project

This repository contains the implementation of **HBnB**, a web-based platform inspired by AirBnB. The project includes several features like user registration, place creation, review submission, and fetching a list of places, all while following a clean architecture and best practices.

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
  - [Sequence Diagrams](#sequence-diagrams)
  - [Class Diagrams](#class-diagrams)
  - [Layered Architecture](#layered-architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)

---

## Project Overview

The **HBnB** project is a system that allows users to:
- Register and manage their profile.
- Create and list places.
- Leave reviews for places.
- View places and reviews from other users.

It follows a **layered architecture** to separate concerns, with an emphasis on security, data validation, and error handling. Key components include an API for communication between the user interface and business logic, and a database that stores user, place, and review data.

---

## Architecture

### Sequence Diagrams

The project follows a typical web-based architecture where:
- **User** interacts with the **API** to send requests such as `register()`, `createPlace()`, and `leaveReview()`.
- The **API** layer handles requests, authenticates users, and forwards the information to the **Business Logic Layer**.
- The **Business Logic Layer** manages operations like data encryption, data validation, and database interactions.
- The **Database** stores user information, places, reviews, and amenities.

Key HTTP response codes and errors handled:
- **HTTP 201**: Successful creation of resources.
- **HTTP 200**: Successful retrieval of data.
- **Error 409**: Conflict in data (e.g., duplicate entries).
- **Error 400**: Bad request (invalid data or syntax).

If you want to take a look at our [Sequence Diagram](https://www.zupimages.net/up/24/40/nblh.jpg)

### Class Diagrams

The system includes the following main classes:
- **User**: Handles registration, profile updates, and deletion.
- **Place**: Manages place creation, deletion, and listing.
- **Review**: Allows users to create, update, and list reviews.
- **Amenity**: Stores amenities associated with places.

Each class has corresponding attributes like `id`, `created_at`, and methods for CRUD operations.

If you want to take a look at our [Class Diagram](https://www.zupimages.net/up/24/40/fgdd.jpg)

### Layered Architecture

The project is built using a **layered architecture** pattern:
1. **Presentation Layer**: Interfaces for User, Place, Review, and Amenity.
2. **Business Logic Layer**: Implements the core logic for managing users, places, reviews, and amenities.
3. **Database Layer**: Handles database operations through repositories (`UserRepository`, `PlaceRepository`, etc.).

The **Facade Pattern** is used between the presentation and business logic layers to simplify the interaction and provide a unified interface.

Here is an example of our Layered Architecture:

![Layered Architecture](https://www.zupimages.net/up/24/40/zgs2.jpg)
---

## Features

- **User Registration**: Register with an email, username, and password.
- **Profile Management**: Update and delete user profiles.
- **Place Creation**: Create, list, and delete places.
- **Review Submission**: Leave reviews for places.
- **Amenity Management**: Add and update amenities for places.
- **Error Handling**: Comprehensive error handling with specific exceptions for invalid inputs (e.g., `InvalidEmailException`, `InvalidReviewException`).

---

## Installation

To run the **HBnB** project locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hbnb.git
```
2. Navigate into the project directory:
```bash
cd HBnB-UML
```

## Authors

This project is being done by [Nour Chaouch](https://github.com/NChaouch/), [Clement Chassemon](https://github.com/UsagerLambda) and [Florian Bombeeck](https://github.com/Pandor3)
>>>>>>> 366eb679b3b66804371fd845d276383b61e0dad6
