// DEPRECATED

// https://codepen.io/Amerey/pen/MWYvLYp

const inputs = document.querySelectorAll('#order'); /* cange '#order' to 'input' for validate all input fields */
const patterns = {
  username: /^[a-z\d]{5,12}$/i,
  password: /^[\d\w@-]{8,20}$/i,
  email: /^([a-z\d\.-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$/,
  phone: /^\d{3}-\d{3}-\d{4}$/,
  order: /^\d{2}-\d{4}$/
};

inputs.forEach((input) => {
  input.addEventListener('keyup', (e) => {
    validate(e.target, patterns[e.target.attributes.id.value]);
  });
});

function validate(field, regex) {
  if (regex.test(field.value)) {
    field.className = 'form-control is-valid';
  } else {
    field.className = 'form-control is-invalid';
  }
}
