const form = document.getElementById("updateForm");
console.log(form)
console.log("hiii")
form.addEventListener("click", async() => {
        e.preventDefault();
        const formData = new FormData(form);
        console.log(formData)
  try {
      const response = await fetch(`/update_family/${head}`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    console.log(result);
    document.querySelectorAll('.errorMsg').forEach(span => span.innerText = '');
    document.querySelectorAll('.errorInput').forEach(input => input.classList.remove('errorInput'));

    if (!result.success) {
      // Head form errors
      if (result.head_errors) {
        for (const field in result.head_errors) {
          const input = document.querySelector(`[name="${field}"]`);
          if (input) {
            setErrorMsg(input, result.head_errors[field][0]);
          }
        }
      }
    } else if (result.success === true) {
      console.log("true");
      // alert(result.message);
      window.location.href = "/";
      // form.reset();
    } else {
      console.log("Something went wrong.", err);
    }
  } catch (err) {
    console.log("Something went wrong.", err);
  }
});


  //   const isValid = validateForm();
  //   if (!isValid) return;
  


function setErrorMsg(input, errorMsg) {
  if (!input) return;
    let inputField = input.closest("div");
    // For radio buttons, 
    if (input.type === "radio") {
        while (inputField && !inputField.querySelector("span.errorMsg")) {
            inputField = inputField.parentElement;
        }
    }
    if (!inputField) return;
    const span = inputField.querySelector("span.errorMsg");
    if (!span) return;
  
  span.classList.add("errorMsg");
  input.classList.add("errorInput");
  span.innerText = errorMsg;
}

$(document).on("input", 'input[type="text"], input[type="date"], input[type="file"]', function () {
  let span = $(this).parent().find(".errorMsg");
  span.text("");
  $(this).removeClass("errorInput");
});

// $(document).on('change', 'input[type="radio"]', function() {
//     // Find the container with the errorMsg span
//     let container = $(this).closest('div').parent(); // adjust if needed
//     let span = container.find('.errorMsg');
//     span.text('');
//     container.find('input[type="radio"]').removeClass('errorInput');
// });
