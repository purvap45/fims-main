
const form = document.getElementById("form");
const email = document.getElementById("email");
const password = document.getElementById("password");

form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const isValid = validateForm(); 
      if (!isValid) return;
      const formData = new FormData(form);
      try {
            const response = await fetch("http://127.0.0.1:8000/login/", {
                  method: "POST",
                  body: formData
            });
            
            const result = await response.json();
            console.log(result);
            if (!result.success) {
                  for (const field in result.errorMessage) {
                        setErrorMsg(document.getElementById(result.field), result.errorMessage);
                  }
            } 
            else if(result.success == true) {
                  // alert(result.message); 
                  window.location.href = "/dashboard";
                  // form.reset();
            }
            else{
                  console.log("Something went wrong.", err);
            }
      } 
      catch (err) {
            console.log("Something went wrong.", err);
      }
});

function clearError(input) {
      const inputField = input.parentElement;
      const span = inputField.querySelector("span");
      if (span) span.innerText = "";
      input.classList.remove("errorInput");
}

const inputs = document.querySelectorAll("#form input");
inputs.forEach(input => {
      input.addEventListener("input", () => clearError(input));
});

password.addEventListener("input", () => clearError(password));

const isEmail = (emailVal) => {
      var atSymbol = emailVal.indexOf("@");
      if (atSymbol < 1) return false;
      var dot = emailVal.lastIndexOf(".");
      if (dot <= atSymbol + 2) return false;
      if (dot == emailVal.length - 1) return false;
      return true;
};

const validateForm = () => {
      let isValid = true;

      const emailVal = email.value.trim();
      const passwordVal = password.value.trim();

      // Email Validation
      if (emailVal === "") {
            setErrorMsg(email, "Email is Required.");
            isValid = false;
      } else if (!isEmail(emailVal)) {
            setErrorMsg(email, "Invalid Email Format.");
            isValid = false;
      } 

      // Password Validation
      if (passwordVal === "") {
            setErrorMsg(password, "Password is Required.");
            isValid = false;
      } 
      return isValid;
};

function setErrorMsg(input, errorMsg) {
      const inputField = input.parentElement;
      const span = inputField.querySelector("span");
      span.classList.add("errorMsg");
      input.classList.add("errorInput");
      span.innerText = errorMsg;
}
