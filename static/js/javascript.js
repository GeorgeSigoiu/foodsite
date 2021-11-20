'use strict'

let market = []

const addToCartFoodBtns = document.querySelectorAll('.btn-add-cart-food')
const addToCartDrinksBtns = document.querySelectorAll('.btn-add-cart-drink')
const badge = document.querySelector('.badge')
const cartBtn = document.querySelector('#show-products-market')

const updateBadge = function () {
    let contentBadge = badge.textContent;
    if (contentBadge === "") contentBadge = 0;
    else contentBadge = Number(contentBadge)
    contentBadge += 1;
    badge.textContent = contentBadge
}
addToCartFoodBtns.forEach(btn => {
    btn.addEventListener("click", function () {
        market = []
        updateBadge()
        market.push(btn.getAttribute('id'))
        sendProducts(market)

    })
})
addToCartDrinksBtns.forEach(btn => {
    btn.addEventListener('click', function () {
        market = []
        updateBadge()
        market.push(btn.getAttribute('id'))
        sendProducts(market)
    })
})



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
    // + and - buttons
    const btnsIncr = document.querySelectorAll("#content-checkout .quantity .btn-incr")
    const btnsDecr = document.querySelectorAll("#content-checkout .quantity .btn-decr")
    const quantityInputs = document.querySelectorAll("#content-checkout .quantity input")
    // total cost for each product
    const productTotalPriceSpans = document.querySelectorAll("#content-checkout .product-cost .product-price-total")
    const productBasePriceSpans = document.querySelectorAll("#content-checkout .product-cost .product-price")
    const totalMoneyToPay = document.querySelector("#content-checkout .total-cost .total-money")

    const updatePrices = function (index) {
        const basePrice = Number(productBasePriceSpans[index].textContent)
        const quantity = Number(quantityInputs[index].value)
        const totalPrice = basePrice * quantity
        productTotalPriceSpans[index].textContent = totalPrice
        return totalPrice
    }

    let finalPrice = 0
    for (let i = 0; i < productTotalPriceSpans.length; i++) {
        const totalPrice = updatePrices(i)
        finalPrice += totalPrice
    }
    totalMoneyToPay.textContent = finalPrice + " lei"
    const updateQuantity = function (indx, val) {
        return function () {
            let currentQuantity = Number(quantityInputs[indx].value)
            currentQuantity += val
            finalPrice += (val * Number(productBasePriceSpans[indx].textContent))
            badge.textContent = Number(badge.textContent) + val
            const id = quantityInputs[indx].getAttribute("id")
            market.push(id)
            if (val === 1) {
                sendProducts(market)
            } else {
                let indx = market.indexOf(id)
                if (indx > -1) {
                    updateProducts(market)
                }
            }
            market = []
            totalMoneyToPay.textContent = finalPrice + " lei"
            if (currentQuantity < 0) {
                currentQuantity = 0
                finalPrice += Number(productBasePriceSpans[indx].textContent)
                badge.textContent = Number(badge.textContent) + 1
                totalMoneyToPay.textContent = finalPrice + " lei"
            }
            quantityInputs[indx].value = currentQuantity
            updatePrices(indx)
        }
    }

    btnsIncr.forEach((btn, indx) => {
        btn.addEventListener("click", updateQuantity(indx, 1))
    })

    btnsDecr.forEach((btn, indx) => {
        btn.addEventListener("click", updateQuantity(indx, -1))
    })

    // animation content-pages and left numbers
    let stage = 1
    const nextBtns = document.querySelectorAll("#content-checkout .pager .checkout-next")
    const prevBtns = document.querySelectorAll("#content-checkout .pager .checkout-prev")

    const productsInfoContainer = document.querySelector("#content-checkout .container-products-info")
    const orderInfoContainer = document.querySelector("#content-checkout .container-order-info")
    const reviewInfoContainer = document.querySelector("#content-checkout .container-review-info")

    const numberConnectors = document.querySelectorAll(".number-conn-inner")
    const circleNumbers = document.querySelectorAll('.circle-number')

    let clicks = 0

    const numConnStyle = function (indx, height, color, delay1, delay2) {
        setTimeout(function () {
            numberConnectors[indx].style.height = height
        }, delay1)
        setTimeout(function () {
            circleNumbers[indx + 1].style.backgroundColor = color
        }, delay2)
    }
    const btnnextF = function () {
        clicks++
        numConnStyle(clicks - 1, "150%", "aqua", 0, 400)
    }
    const btnprevF = function () {
        clicks--
        numConnStyle(clicks, "0", "white", 100, 0)
    }

    const scrollTop = function (...elements) {
        const myList = elements
        myList.forEach(element => element.scrollTop = 0)
    }
    const setHeightOverflow = function (height, overflow, ...elements) {
        const myList = elements
        myList.forEach(element => {
            element.style.overflow = overflow
            element.style.height = height
        })
    }

    const checkStage = function (func) {
        if (stage === 1) {
            scrollTop(orderInfoContainer)
            setHeightOverflow("72vh", "auto", productsInfoContainer)
            setHeightOverflow("50px", "hidden", orderInfoContainer)
        } else if (stage === 2) {
            scrollTop(productsInfoContainer, reviewInfoContainer)
            setHeightOverflow("50px", "hidden", productsInfoContainer, reviewInfoContainer)
            setHeightOverflow("72vh", "auto", orderInfoContainer)
        } else if (stage === 3) {
            scrollTop(orderInfoContainer)
            setHeightOverflow("72vh", "auto", reviewInfoContainer)
            setHeightOverflow("50px", "hidden", orderInfoContainer)
        } else if (stage == 4) {
            //no func call
            console.log("Plaseaza comanda")
            return 1
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