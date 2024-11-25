from app.persistence.repository import InMemoryRepository
from app.models.users import User
from app.models.places import Place
from app.models.amenities import Amenity
from app.models.reviews import Review


class HBnBFacade:
    def __init__(self):
        if not hasattr(self, "user_repo"):
            self.user_repo = InMemoryRepository()
            self.place_repo = InMemoryRepository()
            self.review_repo = InMemoryRepository()
            self.amenity_repo = InMemoryRepository()


# ######USER##############################################################################################################


    def create_user(self, user_data):
        """Create an user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve user's data."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update the user's data."""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        self.user_repo.update(user_id, user_data)
        return user


    #############################################################################################################
#REVIEW BLOCK####################################################################################################
    def create_review(self, user, place, review_data):
        """Create a review"""
        try:
            review_data = {k: v for k, v in review_data.items() if k not in ['user_id', 'place_id']}
        
        
            review = Review(user=user, place=place,**review_data)
        
            self.review_repo.add(review)
            return review
        except ValueError as e:
            raise ValueError(f"Failed to create review: {str(e)}")

            return review.to_dict()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to create review: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while creating the review: {str(e)}")

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        owner_id = review_data.get('owner_id')
        if owner_id is None:
            raise ValueError("owner_id is required to update the place")

        place_id = review_data.get('place_id')
        if place_id is None:
            raise ValueError("place_id is required to update the place")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with id {owner_id} does not exist")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} does not exist")

        try:
            self.review_repo.update(review_id, review_data)
            if place:
                # Retire l'ancienne review et met à jour la liste des reviews
                place.remove_review(review_id)  # retire l'ancienne version
                # Ajoute la review mise à jour à la liste
                updated_review = self.review_repo.get(review_id)  # Récupère la review mise à jour
                place.add_review(updated_review)  # Ajoute la nouvelle version
                # Met à jour le place dans le repository
                self.place_repo.update(place.id, place.to_dict())

            return review
        except ValueError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"An error occurred while updating the review: {str(e)}")

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} does not exist")

        place = self.place_repo.get(review.place_id)
        if place:
            # Retirer la review de la liste des reviews de ce place
            place.remove_review(review_id)
            # Mettre à jour le place dans le repository
            self.place_repo.update(place.id, place.to_dict())

        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}, 200



    ###########################################################################################################
# ####PLACES##############################################################################################################


    def create_place(self, place_data):
        """Create an place."""
        try:
            owner_id = place_data.get('owner_id')
            if not owner_id:
                raise ValueError("owner_id is required")

            user = self.user_repo.get(owner_id)
            if not user:
                raise ValueError(f"User with id {owner_id} does not exist")

            place = Place(**place_data)
            self.place_repo.add(place)

            user.add_place(place)
            self.user_repo.update(user.id, user.to_dict())

            return place.to_dict()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to create place: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while creating the place: {str(e)}")

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all users."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner_id = place_data.get('owner_id')
        if owner_id is None:
            raise ValueError("owner_id is required to update the place")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with id {owner_id} does not exist")

        try:
            self.place_repo.update(place_id, place_data)
            return place
        except ValueError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"An error occurred while updating the place: {str(e)}")


# ########################################################################################################################
#AMENITIES BLOCK##########################################################################################################

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    def create_amenity(self, amenity_data):
        if not amenity_data:
            return None
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)  # Vérifiez que l'amenity est trouvé ici
        if not amenity:
            return None

        amenity.update(amenity_data)  # Mettez à jour les données
        return amenity
#########################################################################################################################
