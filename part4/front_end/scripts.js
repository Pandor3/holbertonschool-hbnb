// API routes via variables ---------------------------------------------------------------------//
const API_URL = "http://127.0.0.1:5000/api/v1/auth/login";
const GET_ALL_PLACES = "http://127.0.0.1:5000/api/v1/places";
const GET_PLACE ="http://127.0.0.1:5000/api/v1/places";
const POST_REVIEW = "http://127.0.0.1:5000/api/v1/reviews";
const GET_REVIEW_BY_PLACE = "http://127.0.0.1:5000/api/v1/reviews/places";
const GET_USER_BY_ID = "http://127.0.0.1:5000/api/v1/users";

// HTML URLs via variables ----------------------------------------------------------------------//
const URL_LOGIN = "http://127.0.0.1:5500/part4/front_end/login.html";
const URL_INDEX = "http://127.0.0.1:5500/part4/front_end/index.html";
const URL_PLACE = "http://127.0.0.1:5500/part4/front_end/place.html";
const URL_REVIEW = "http://127.0.0.1:5500/part4/front_end/add_review.html";

const LOGIN = "login.html";
const INDEX = "index.html";
const PLACE = "place.html";
const REVIEW = "add_review.html";

// AUTHENTICATION -------------------------------------------------------------------------------// 
// This function will inspect the cookie in order to see if the user is logged in or not //
function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {
    if (cookie.startsWith(name + "-")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

// This function will see if the user is logged in or not //
function authenticationChecker() {
  const token = getCookie("token");
  const loginLink = document.getElementById("login-link");

  if (!token) {
    loginLink.style.display = "block";
  } else {
    loginLink.style.display = "none";
  }
}

  // This function will decode the JWT token in order to inspect the user ID //
  async function getUserId() {
    const token = getCookie("token");
    const tokenParts = token.split(".");
    if (tokenParts.length !== 3) {
      throw new Error("Invalid token");
    }
    const payload = JSON.parse(atob(tokenParts[1]));
    return payload.sub.id;
  }

  // LOGIN SECTION ------------------------------------------------------------------------------//
  // This function will manage cookies for the website//
  function setAuthCookie(token) {
    const expiryDate = new Date();

    expiryDate.setDate(expiryDate.getDate() + 7);
    document.cookie = `token=${token}; expires=${expiryDate.toUTCString()}; path=/; SameSite-Strict`;
  }

  // This function will check if the user exists in the database //
  function loadLogin() {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
      loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
          const formData = new FormData(event.target);
          const response = await fetch(API_URL, {
            method: "POST",
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: formData.get("email"),
              password: formData.get("password")
            })
          });
          const data = await response.json();
          if (response.ok && data.access_token) {
            setAuthCookie(data.access_token);
            window.location.href = "index.html";
          } else {
            const errorElement = document.getElementById("error-message");
            if (errorElement) {
              errorElement.textContent = data.message || "Echec de la connexion";
              errorElement.style.display = "block";
            } else {
              alert("Echec de la connexion");
            }
          }
        } catch (error) {
          console.error("Error de login:", error);
          alert("Erreur lors de la connexion");
        }
      });
    }
  }

  // INDEX SECTION ------------------------------------------------------------------------------//

async function fetchPlaces() {
  try {
    const response = await fetch(GET_ALL_PLACES);
    if (!response.ok) {
      throw new Error(`Erreur HTTP : ${response.status}`);
    }
    const places = await response.json();
    displayPlaces(places);
    return places;
  } catch (error) {
    console.error("Erreur de chargement des places :", error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';
  places.forEach(place => {
    const placeElement = document.createElement("div");
    placeElement.classList.add("card", "place-card");
    placeElement.dataset.price = place.price;
    placeElement.dataset.placeId = place.id;
    placeElement.innerHTML = `
    <h3 class="place-name">${place.title}</h3>
    <p class="place-price">Price per night: $${place.price}</p>
    <a href="place.html?place_id=${place.id}" class="button login-button">View Details</a>`;
    placesList.appendChild(placeElement);
  });
  priceFilter();
}

  // --------------------------------------------------------------------------------------------//
document.addEventListener('DOMContentLoaded', () => {
  authenticationChecker();
  const currentPage = window.location.pathname.split("/").pop();
  if (currentPage === LOGIN) {
    loadLogin();
  }
  });
