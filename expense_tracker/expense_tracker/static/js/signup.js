// Submit Button
const submitButton = document.querySelector(".submitButton");

// Username Validation
const usernameField = document.querySelector("#usernameField");
const invalidUsernameFeedback = document.querySelector(
  "#invalidUsernameFeedback"
);
usernameField.addEventListener("keyup", (e) => {
  const usernameValue = e.target.value;
  usernameField.classList.remove("is-invalid");
  invalidUsernameFeedback.style.display = "none";

  if (usernameValue.length > 0) {
    fetch("/validate_username", {
      body: JSON.stringify({ username: usernameValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.username_error) {
          submitButton.disabled = true;
          usernameField.classList.add("is-invalid");
          invalidUsernameFeedback.style.display = "block";
          invalidUsernameFeedback.innerHTML = `<p>${data.username_error}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});

// Email Validation
const emailField = document.querySelector("#emailField");
const invalidEmailFeedback = document.querySelector("#invalidEmailFeedback");

emailField.addEventListener("keyup", (e) => {
  const emailValue = e.target.value;
  emailField.classList.remove("is-invalid");
  invalidEmailFeedback.style.display = "none";

  if (emailValue.length > 0) {
    fetch("/validate_email", {
      body: JSON.stringify({ email: emailValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.email_error) {
          submitButton.disabled = true;
          emailField.classList.add("is-invalid");
          invalidEmailFeedback.style.display = "block";
          invalidEmailFeedback.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});

// Password Validation
const showPassword = document.querySelector(".showPassword");
const passwordField = document.querySelector("#passwordField");

const handleToggleInput = (e) => {
  if (showPassword.textContent === "SHOW") {
    showPassword.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPassword.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
};

showPassword.addEventListener("click", handleToggleInput);
