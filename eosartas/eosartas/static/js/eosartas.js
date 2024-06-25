document.addEventListener('DOMContentLoaded', function () {
    // Get all image-zoom links
    var imageLinks = document.querySelectorAll('.image-zoom');

    // Attach click event listener to each image-zoom link
    imageLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            // Get the modal ID from href attribute
            var targetModalId = this.getAttribute('href');

            // Show the modal
            var targetModal = document.querySelector(targetModalId);
            targetModal.classList.add('is-active');
        });
    });

    // Close modal when modal-close button or modal-background is clicked
    var modalCloseButtons = document.querySelectorAll('.modal-close, .modal-background');
    modalCloseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var modal = this.closest('.modal');
            modal.classList.remove('is-active');
        });
    });
});



document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Add a click event on each of them
  $navbarBurgers.forEach( el => {
    el.addEventListener('click', () => {

      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);
      const $navbarDropdowns = Array.prototype.slice.call(document.querySelectorAll('.navbar-dropdown'), 0);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');
      $navbarDropdowns.forEach( dropdown => {dropdown.classList.add('hidden')})
    });
  });

  const $dropdownLinks = Array.prototype.slice.call(document.querySelectorAll('.navbar-link'), 0);
  $dropdownLinks.forEach( el => {
    el.addEventListener('click', () => {
      const dropdown = el.nextElementSibling;
      dropdown.classList.toggle('hidden');
    })
 })
});