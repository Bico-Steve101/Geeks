document.addEventListener('DOMContentLoaded', function () {
    var menuToggle = document.querySelector('.menu__toggle');
    var headerMenu = document.querySelector('.header__menu');
    var body = document.body;

    menuToggle.addEventListener('click', function () {
        headerMenu.classList.toggle('active');
        menuToggle.classList.toggle('active');
        body.classList.toggle('menu-active');
    });

    var menuItems = document.querySelectorAll('.menu__item');

    menuItems.forEach(function (item) {
        item.addEventListener('click', function () {
            headerMenu.classList.remove('active');
            menuToggle.classList.remove('active');
            body.classList.remove('menu-active');
        });
    });
});
