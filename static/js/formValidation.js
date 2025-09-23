const form = document.getElementById("familyForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const isValid = validateForm();
  console.log(isValid)
  if (!isValid) return;
  const formData = new FormData(form);
  try {
    const response = await fetch("/family_form/", {
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
      // Hobby formset errors
      if (Array.isArray(result.hobby_errors)) {
        result.hobby_errors.forEach((formErrors, i) => {
          for (const field in formErrors) {
            const input = document.querySelector(
              `[name="hobbies-${i}-${field}"]`
            );
            if (input) {
              setErrorMsg(input, formErrors[field][0]);
            }
          }
        });
      }
      // Member formset errors
      if (Array.isArray(result.member_errors)) {
        result.member_errors.forEach((formErrors, i) => {
          for (const field in formErrors) {
            const input = document.querySelector(
              `[name="members-${i}-${field}"]`
            );
            if (input) {
              setErrorMsg(input, formErrors[field][0]);
            }
          }
        });
      }
    } else if (result.success === true) {
      alert(result.message);
      window.location.href = "/family_list/";
      form.reset();
    } else {
      console.log("Something went wrong.", err);
    }
  } catch (err) {
    console.log("Something went wrong.", err);
  }
});

function setErrorMsg(input, errorMsg) {
  if (!input) return;
  let inputField = input.closest("div");
  if (input.type === "radio") {
    while (inputField && !inputField.querySelector("span.errorMsg")) {
      inputField = inputField.parentElement;
    }
  }
  inputField.scrollIntoView({
    behavior: 'smooth',
    block: 'center'
  });
  if (!inputField) return;
  const span = inputField.querySelector("span.errorMsg");
  if (!span) return;
  // console.log(span)
  span.classList.add("errorMsg");
  input.classList.add("errorInput");
  span.innerText = errorMsg;
}

$(document).on("input", 'input[type="text"], input[type="date"], input[type="file"], select, textarea',
  function () {
    let span = $(this).parent().find(".errorMsg");
    span.text("");
    // $(this).removeClass("errorInput");
  }
);

$(document).on("change", 'input[type="radio"]', function () {
  $(this).closest(".maritalDiv, .mem_msDiv")
    .find(".errorMsg").text("");
});

const validateForm = () => {
  const headValid = validateHead();
  const hobbyValid = validateHobby();
  const memberValid = validateMember();
  return headValid && hobbyValid && memberValid;
};

function validateHead() {
  let isValid = true;

  // Name
  let name = $('input[type="text"][name="name"]')[0];
  const nameVal = name.value.trim();
  if (nameVal === "") {
    setErrorMsg(name, "Name is Required.");
    isValid = false;
  } else if (nameVal.length < 3) {
    setErrorMsg(name, "Name should have minimum 3 charaters.");
    isValid = false;
  } else if (/\d/.test(nameVal)) {
    setErrorMsg(name, "Name should not contain digits.");
    isValid = false;
  }

  // Surname
  let surname = $('input[type="text"][name="surname"]')[0];
  const surnameVal = surname.value.trim();
  if (surnameVal === "") {
    setErrorMsg(surname, "Surname is Required.");
    isValid = false;
  } else if (surnameVal.length < 3) {
    setErrorMsg(surname, "Surname should have minimum 3 charaters.");
    isValid = false;
  } else if (/\d/.test(surnameVal)) {
    setErrorMsg(surname, "Surname should not contain digits.");
    isValid = false;
  }

  // DOB
  let dob = $('input[type="date"][name="dob"]')[0];
  const dobVal = dob.value.trim();
  const today = new Date();
  const bDate = new Date(dobVal);
  const age = today.getFullYear() - bDate.getFullYear();
  const month = today.getMonth() - bDate.getMonth();
  if (dobVal === "") {
    setErrorMsg(dob, "Birth Date is Required.");
    isValid = false;
  } else if (age < 21 || (age === 10 && month < 0)) {
    setErrorMsg(dob, "Age must be at least 21 years old.");
    isValid = false;
  }

  // Mobile No
  let mobno = $('input[type="text"][name="mobno"]')[0];
  const mobnoVal = mobno.value.trim();
  if (mobnoVal === "") {
    setErrorMsg(mobno, "Mobile No. is Required.");
    isValid = false;
  } else if (!/^\d{10}$/.test(mobnoVal)) {
    setErrorMsg(mobno, "Mobile No. should have 10 Digits.");
    isValid = false;
  }

  // Address
  let address = $('[name="address"]')[0];
  const addressVal = address.value.trim();
  if (addressVal === "") {
    setErrorMsg(address, "Address is Required.");
    isValid = false;
  }

  // State
  let state = $('[name="state"]')[0];
  const stateVal = state.value.trim();
  if (!stateVal) {
    setErrorMsg(state, "State is Required.");
  }

  // City
  let city = $('[name="city"]')[0];
  const cityVal = city.value.trim();
  if (!cityVal) {
    setErrorMsg(city, "City is Required.");
  }

  // Pincode
  let pincode = $('input[type="text"][name="pincode"]')[0];
  const pincodeVal = pincode.value.trim();
  if (pincodeVal === "") {
    setErrorMsg(pincode, "Pincode is Required.");
  }

  // Marital Status
  let marital = document.getElementsByName("marital_status");
  if (!(marital[0].checked || marital[1].checked)) {
    setErrorMsg(marital[0], "Please Select Marital Status.");
    isValid = false;
  }

  // Wedding date 
  if (marital[0].checked) {
    const wed_date = document.getElementById("id_wedding_date");
    const wed_dateVal = wed_date.value.trim();
    if (wed_dateVal === "") {
      setErrorMsg(wed_date, "Wedding date is required if married.")
    }
  }

  // Photo
  let photo = document.getElementById("id_photo");
  const photoPathVal = photo.value;
  var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
  if (photoPathVal === "") {
    setErrorMsg(photo, "Photo is Required.");
    isValid = false;
  } else if (!allowedExtensions.exec(photoPathVal)) {
    setErrorMsg(photo, "Invalid file type. Only PNG, JPG, JPEG are allowed.");
    isValid = false;
  } else {
    var photoSize = photo.files[0].size / 1000 / 1000;
    // console.log(photoSize);
    if (photoSize > 2) {
      setErrorMsg(photo, "Photo Size should be less than 2MB.");
      isValid = false;
    }
  }
  return isValid;
};

function validateHobby() {
  let isValid = true;
  // First hobby
  let firstHobby = $('#hobby-container .hobby-row:first input[type="text"]')[0];
  $('#hobby-container .hobby-row:first .errorMsg').text('');
  if (!firstHobby.value.trim()) {
    setErrorMsg(firstHobby, 'At least one hobby is required.');
    isValid = false;
  }
  return isValid;
}

function validateMember() {
  let isValid = true;
  $("#member-container .member-row").each(function () {
    let row = $(this);
    // Name
    let m_name = row.find('input[type="text"][name$="member_name"]')[0];
    if (!m_name.value.trim()) {
      setErrorMsg(m_name, "Name is required.");
      isValid = false;
    } else if (/\d/.test(m_name.value.trim())) {
      setErrorMsg(m_name, "Name should not contain digits.");
      isValid = false;
    }

    // DOB
    let m_dob = row.find('input[type="date"][name$="member_dob"]')[0];
    if (!m_dob.value.trim()) {
      setErrorMsg(m_dob, "Birth Date is required.");
      isValid = false;
    }

    // Marital status
    let m_marital = row.find('input[type="radio"][name$="member_marital"]');
    if (!(m_marital[0].checked || m_marital[1].checked)) {
      setErrorMsg(m_marital[0], "Please Select Marital Status.");
      isValid = false;
    }

    // Wedding date 
    if (m_marital[0].checked) {
      let m_wed_date = row.find('input[type="date"][name$="member_wedDate"]')[0];
      let m_wed_dateVal = m_wed_date.value.trim();
      if (m_wed_dateVal === "") {
        setErrorMsg(m_wed_date, "Wedding date is required if married.")
      }
    }

    // Relation
    // let relation = row.find('input[type="text"][name$="relation"]')[0];
    // if (!relation.value.trim()) {
    //   setErrorMsg(relation, "Relation is required.");
    //   isValid = false;
    // } else if (/\d/.test(relation.value.trim())) {
    //   setErrorMsg(relation, "Relation should not contain digits.");
    //   isValid = false;
    // }

    // Photo
    let m_photo = row.find('input[type="file"][name$="member_photo"]')[0];
    let photoVal = m_photo.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
    if (photoVal) {
      if (!allowedExtensions.exec(photoVal)) {
        setErrorMsg(m_photo, "Invalid file type. Only PNG, JPG, JPEG are allowed.");
        isValid = false;
      } else {
        var photoSize = m_photo.files[0].size / 1000 / 1000;
        if (photoSize > 2) {
          setErrorMsg(m_photo, "Photo Size should be less than 2MB.");
          isValid = false;
        }
      }
    }

  });
  return isValid;
}