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
if (tagsWindow && productsWindow) {
    if (productsWindow !== null) {
        const offsetEnd = productsWindow.offsetTop + productsWindow.offsetHeight - tagsWindow.offsetHeight
        const tagsOffsetTop = tagsWindow.offsetTop - 50

        window.addEventListener('scroll', function () {
            if (this.scrollY > tagsOffsetTop && this.scrollY < offsetEnd)
                tagsWindow.style.top = String(this.scrollY - tagsOffsetTop + 50) + 'px'
        })
    }
}

const openLocationLinks = document.querySelectorAll('.open-location')
openLocationLinks.forEach(link => link.addEventListener('click', function () {
    const map_string = link.textContent
    const url = 'https://www.google.com/maps/place/' + map_string
    window.open(url, '_blank')
})
)

// drinks carousel
if (document.querySelector('#drinks-carousel')) {
    const drinksCarouselArrows = document.querySelectorAll('.drinks-carousel-arrow')
    const arrowLeft = drinksCarouselArrows[0]
    const arrowRight = drinksCarouselArrows[1]
    const drinkCards = document.querySelectorAll('#drinks-carousel .drinks-carousel-card')
    const firstCard = drinkCards[0]
    const lastCard = drinkCards[drinkCards.length - 1]
    const cardWidth = drinkCards[0].offsetWidth
    const carouselContainer = document.querySelector('.drinks-carousel-content')
    let maxHeight = 0

    drinkCards.forEach((card, index) => {
        card.style.left = `${cardWidth * index}px`
        if (card.offsetHeight > maxHeight)
            maxHeight = card.offsetHeight
    })
    drinkCards.forEach((card, index) => {
        card.style.height = `${maxHeight}px`
    })
    carouselContainer.style.height = `${maxHeight}px`
    const moveCards = function (offset) {
        drinkCards.forEach(card => {
            const currentPosition = card.offsetLeft
            card.style.left = `${currentPosition + offset}px`
        })
    }
    arrowLeft.addEventListener('click', function () {
        if (firstCard.offsetLeft + cardWidth * 2 <= 0)
            moveCards(cardWidth * 2)
        else
            moveCards(0 - firstCard.offsetLeft)
    })
    arrowRight.addEventListener('click', function () {
        const carouselRight = carouselContainer.offsetLeft + carouselContainer.offsetWidth
        const lastCardRight = lastCard.offsetLeft + cardWidth
        if (lastCardRight - cardWidth * 2 >= carouselRight)

            moveCards(-(cardWidth * 2))
        else
            moveCards(carouselRight - lastCardRight - 55)
    })
}


// progress bar and completing informations to order
if (document.querySelector("#content-checkout") !== null) {
    const btnsIncr = document.querySelectorAll("#content-checkout .quantity .btn-incr")
    const btnsDecr = document.querySelectorAll("#content-checkout .quantity .btn-decr")
    const quantityInputs = document.querySelectorAll("#content-checkout .quantity input")

    const updateQuantity = function (indx, val) {
        return function () {
            let currentQuantity = Number(quantityInputs[indx].value)
            currentQuantity += val
            quantityInputs[indx].value = currentQuantity
        }
    }

    btnsIncr.forEach((btn, indx) => {
        btn.addEventListener("click", updateQuantity(indx, 1))

    })
    btnsDecr.forEach((btn, indx) => {
        btn.addEventListener("click", updateQuantity(indx, -1))
    })

    let stage = 1
    const nextBtns = document.querySelectorAll("#content-checkout .pager .checkout-next")
    const prevBtns = document.querySelectorAll("#content-checkout .pager .checkout-prev")

    const productsInfoContainer = document.querySelector("#content-checkout .container-products-info")
    const orderInfoContainer = document.querySelector("#content-checkout .container-order-info")
    const reviewInfoContainer = document.querySelector("#content-checkout .container-review-info")

    const numberConnectors = document.querySelectorAll(".number-conn-inner")
    const circleNumbers = document.querySelectorAll('.circle-number')
    let clicks = 0
    const btnnextF = function () {
        if (clicks == 0) {
            clicks++
            numberConnectors[0].style.height = '150%'
            setTimeout(function () {
                circleNumbers[1].style.backgroundColor = "aqua"
            }, 400)
        } else if (clicks == 1) {
            clicks++
            numberConnectors[1].style.height = '150%'
            setTimeout(function () {
                circleNumbers[2].style.backgroundColor = "aqua"
            }, 400)
        }
    }
    const btnprevF = function () {
        if (clicks == 1) {
            clicks--
            setTimeout(function () {
                numberConnectors[0].style.height = '0'
            }, 100)
            circleNumbers[1].style.backgroundColor = "white"
        } else if (clicks == 2) {
            clicks--
            setTimeout(function () {
                numberConnectors[1].style.height = '0'
            }, 100)
            circleNumbers[2].style.backgroundColor = "white"
        }
    }

    const checkStage = function (func) {
        if (stage === 1) {
            orderInfoContainer.scrollTop = 0;
            productsInfoContainer.style.height = "72vh"
            orderInfoContainer.style.height = "50px"
            productsInfoContainer.style.overflow = "auto"
            orderInfoContainer.style.overflow = "hidden"
        } else if (stage === 2) {
            productsInfoContainer.scrollTop = 0;
            reviewInfoContainer.scrollTop = 0;
            productsInfoContainer.style.height = "50px"
            orderInfoContainer.style.height = "72vh"
            productsInfoContainer.style.overflow = "hidden"
            orderInfoContainer.style.overflow = "auto"
        } else if (stage === 3) {
            orderInfoContainer.scrollTop = 0;
            orderInfoContainer.style.height = "50px"
            reviewInfoContainer.style.height = "72vh"
            orderInfoContainer.style.overflow = "hidden"
            reviewInfoContainer.style.overflow = "auto"
        } else if (stage == 4) {
            console.log("Plaseaza comanda")
        }
        func.call()
    }

    nextBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            stage += 1
            checkStage(btnnextF)
            if (stage === 4) stage = 3;
        })
    })
    prevBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            stage -= 1
            if (stage === 0) stage = 1;
            checkStage(btnprevF)
        })
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