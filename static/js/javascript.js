'use strict'

const navbar = document.querySelector('.navbar')
window.addEventListener("scroll", function () {
    // navbar.classList.toggle("navbar-fixed-top", window.scrollY > 150)
    if (window.scrollY > 150)
        navbar.classList.add('navbar-fixed-top')
    else
        navbar.classList.remove('navbar-fixed-top')
})

const dropdownPreparate = document.querySelector('.navbar .nav .dropdown .dropdown-toggle')
const dropdownMenu = document.querySelector(".navbar .nav .dropdown .dropdown-menu")

dropdownPreparate.addEventListener('mouseover', function () {
    dropdownMenu.style.display = 'block'
})
dropdownPreparate.addEventListener('mouseout', function () {
    dropdownMenu.style.display = 'none'
})
dropdownMenu.addEventListener('mouseover', function () {
    dropdownMenu.style.display = 'block'
})
dropdownMenu.addEventListener('mouseout', function () {
    dropdownMenu.style.display = 'none'
})

const tagsWindow = document.querySelector('.tags-window')
const productsWindow = document.querySelector('.products-window')
if (productsWindow !== null) {
    const offsetEnd = productsWindow.offsetTop + productsWindow.offsetHeight - tagsWindow.offsetHeight
    const tagsOffsetTop = tagsWindow.offsetTop - 50

    window.addEventListener('scroll', function () {
        if (this.scrollY > tagsOffsetTop && this.scrollY < offsetEnd)
            tagsWindow.style.top = String(this.scrollY - tagsOffsetTop + 50) + 'px'
    })
}


// $('#navbar a').on('click', function (event) {
//     if (this.hash !== '') {
//         event.preventDefault();

//         const hash = this.hash;

//         $('html, body').animate(
//             {
//                 scrollTop: $(hash).offset().top - 110
//             },
//             0
//         );
//     }
// });