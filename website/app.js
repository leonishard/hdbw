const menu = document.querySelector('#moblie-menu');
const meunLinks = document.querySelector('.navbar__menu');

menu.addEventListener('click', function() {
    menu.classList.toggle('is-active');
    meunLinks.classList.toggle('active');
});