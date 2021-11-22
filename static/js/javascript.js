'use strict'

let market = []

const addToCartFoodBtns = document.querySelectorAll('.btn-add-cart-food')
const addToCartDrinksBtns = document.querySelectorAll('.btn-add-cart-drink')
const badge = document.querySelector('.badge')
const cartBtn = document.querySelector('#show-products-market')

// update the number of products existing in cart
const updateBadge = function () {
    let contentBadge = badge.textContent;
    if (contentBadge === "") contentBadge = 0;
    else contentBadge = Number(contentBadge)
    contentBadge += 1;
    badge.textContent = contentBadge
}

// when a new product is added in cart, it is send to backend to store in list
let productCardElements = [addToCartFoodBtns, addToCartDrinksBtns]
const addToCart = function (btn) {
    return function () {
        market = []
        updateBadge()
        market.push(btn.getAttribute('id'))
        sendProducts(market)
    }

}
productCardElements.forEach(element => {
    element.forEach(button => {
        button.addEventListener("click", addToCart(button))
    })
})

// when scrolling the navbar gets fixed to top
const navbar = document.querySelector('.navbar')
window.addEventListener("scroll", function () {
    if (window.scrollY > 150)
        navbar.classList.add('navbar-fixed-top')
    else
        navbar.classList.remove('navbar-fixed-top')
})

// dropmenu on navbar
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

// moving tags window while scrolling 
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

// open location on map when click on the address string
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

    // initializing position for every drink element
    // calculating the max height of a card
    drinkCards.forEach((card, index) => {
        card.style.left = `${cardWidth * index}px`
        if (card.offsetHeight > maxHeight)
            maxHeight = card.offsetHeight
    })

    // setting every card at max height
    drinkCards.forEach(card => {
        card.style.height = `${maxHeight}px`
    })

    carouselContainer.style.height = `${maxHeight}px`

    // moving card to left or to right when arrow is clicked
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

// order window - progress bar and information about the order
if (document.querySelector("#content-checkout") !== null) {
    // + and - buttons
    const btnsIncr = document.querySelectorAll("#content-checkout .quantity .btn-incr")
    const btnsDecr = document.querySelectorAll("#content-checkout .quantity .btn-decr")
    const quantityInputs = document.querySelectorAll("#content-checkout .quantity input")
    // total cost for each product
    const productTotalPriceSpans = document.querySelectorAll("#content-checkout .product-cost .product-price-total")
    const productBasePriceSpans = document.querySelectorAll("#content-checkout .product-cost .product-price")
    const totalMoneyToPay = document.querySelector("#content-checkout .total-cost .total-money")

    // animation content-pages and left numbers
    let stage = 1
    const nextBtns = document.querySelectorAll("#content-checkout .pager .checkout-next")
    const prevBtns = document.querySelectorAll("#content-checkout .pager .checkout-prev")
    const deliveryCost = document.getElementById("delivery-cost")
    const numberConnectors = document.querySelectorAll(".number-conn-inner")
    const circleNumbers = document.querySelectorAll('.circle-number')

    // containers for every stage
    const productsInfoContainer = document.querySelector("#content-checkout .container-products-info")
    const orderInfoContainer = document.querySelector("#content-checkout .container-order-info")
    const reviewInfoContainer = document.querySelector("#content-checkout .container-review-info")

    // updating the total price of products
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

    // action when added or removed one product from cart
    const updateQuantity = function (indx, val) {
        return function () {
            let currentQuantity = Number(quantityInputs[indx].value)
            currentQuantity += val
            // update the finbal price to pay
            finalPrice += (val * Number(productBasePriceSpans[indx].textContent))
            totalMoneyToPay.textContent = finalPrice + " lei"
            // update the products from cart
            badge.textContent = Number(badge.textContent) + val
            // adding one more product to the products list
            const id = quantityInputs[indx].getAttribute("id")
            market.push(id)

            if (val === 1) { // if number of products is incremented
                sendProducts(market)
            } else { // if number of products is decremented
                let indx = market.indexOf(id)
                if (indx > -1) {
                    updateProducts(market)
                }
            }
            // reset the products which have to be added to products list
            market = []

            if (currentQuantity < 0) { // if we dont want this product anymore
                currentQuantity = 0
                // we have to add its value because we subtracted it before
                finalPrice += Number(productBasePriceSpans[indx].textContent)
                totalMoneyToPay.textContent = finalPrice + " lei"
                // and add +1 to the number of products because we deleted 1 before
                badge.textContent = Number(badge.textContent) + 1
            }
            // setting the current price
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

    // setting the progress bar
    let clicks = 0

    const numConnStyle = function (indx, height, color, delay1, delay2) {
        setTimeout(function () {
            numberConnectors[indx].style.height = height
        }, delay1)
        setTimeout(function () {
            circleNumbers[indx + 1].style.backgroundColor = color
            if (height === "0")
                circleNumbers[indx + 1].style.boxShadow = "0px 0px 0px 0px rgb(35, 155, 224)"
            else
                circleNumbers[indx + 1].style.boxShadow = "0px 0px 5px 2px rgb(35, 155, 224)"
        }, delay2)
    }
    // when next button is pressed, go to next stage
    const btnnextF = function () {
        clicks++
        numConnStyle(clicks - 1, "150%", "rgb(35, 155, 224)", 0, 400)
    }
    // when prev button is pressed, go to prev stage
    const btnprevF = function () {
        clicks--
        numConnStyle(clicks, "0", "white", 100, 0)
    }
    // setting the containers height -> 50px to which are not currently used
    //                               -> 72vh to the one in use
    const setHeightOverflow = function (inUse, ...elements) {
        const height = inUse ? "72vh" : "50px"
        const overflow = inUse ? "auto" : "hidden"
        elements.forEach(element => {
            if (overflow === "hidden")
                element.scrollTop = 0
            element.style.overflow = overflow
            element.style.height = height
        })
    }
    // checking in which stage of placing order we are
    const checkStage = function (func) {
        if (stage === 1) { // when products are displayed
            setHeightOverflow(true, productsInfoContainer)
            setHeightOverflow(false, orderInfoContainer)
        } else if (stage === 2) { // order information
            setHeightOverflow(false, productsInfoContainer, reviewInfoContainer)
            setHeightOverflow(true, orderInfoContainer)
        } else if (stage === 3) { // review the information and accept terms and privacy
            setHeightOverflow(true, reviewInfoContainer)
            setHeightOverflow(false, orderInfoContainer)
        } else if (stage == 4) {
            //no func call
            return 1
        }
        func.call()
    }
    // checking if the delivery is free or not
    nextBtns[0].addEventListener("click", function () {
        if (Number(totalMoneyToPay.textContent.replace(" lei", "")) > 60)
            deliveryCost.textContent = "- Livrator magazin: gratis"
        else
            deliveryCost.textContent = "- Livrator magazin: 10.00 lei"
    })
    // going to next or prev stage
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

    // elements in review stage
    const orderFirstameInput = document.getElementById("order-firstname")
    const orderSurameInput = document.getElementById("order-surname")
    const orderEmailInput = document.getElementById("order-email")
    const orderAddressInput = document.getElementById("order-address")
    const orderPhoneInput = document.getElementById("order-phone")
    const orderInfo = [orderFirstameInput, orderSurameInput, orderEmailInput, orderAddressInput, orderPhoneInput]
    // setting the elements with correct information from the form
    nextBtns[1].addEventListener("click", function () {
        document.getElementById("name-review-order").textContent = orderFirstameInput.value + " " + orderSurameInput.value
        document.getElementById("email-review-order").textContent = orderEmailInput.value
        document.getElementById("phone-review-order").textContent = orderPhoneInput.value
        document.getElementById("address-review-order").textContent = orderAddressInput.value
        document.getElementById("price-review-order").textContent = totalMoneyToPay.textContent
    })
    //checking if there are some products to be bought
    const checkProductExists = function () {
        if (totalMoneyToPay.textContent === "0 lei")
            return false
        return true
    }
    const setBtnFunc = function (btn) {
        return function () {
            if (checkProductExists())
                btn.classList.remove("disabled")
            else
                btn.classList.add("disabled")
        }

    }
    if (productsInfoContainer.children[1].children.length > 0) {
        nextBtns[0].classList.remove("disabled")
    }
    // checking if is accepted to go from stage 1 to stage 2
    btnsDecr[0].addEventListener("click", setBtnFunc(nextBtns[0]))
    btnsIncr[0].addEventListener("click", setBtnFunc(nextBtns[0]))

    // adding event listeners to inputs in the form
    // checking if every input has some value
    for (let i = 0; i < orderInfo.length; i++) {
        const input = orderInfo[i]
        input.addEventListener("keyup", function () {
            let ok = true
            for (let j = 0; j < orderInfo.length; j++) {
                const inp = orderInfo[j]
                if (inp.value === "") ok = false
            }
            if (ok) nextBtns[1].classList.remove("disabled")
            else nextBtns[1].classList.add("disabled")
        })
    }
    // checking if the terms and privacy are checked
    document.getElementById("site-conditions").addEventListener("click", function () {
        if (document.getElementById("site-conditions").checked)
            nextBtns[2].classList.remove("disabled")
        else nextBtns[2].classList.add("disabled")
    })

    // if the user want to download the bill in pdf format
    const downloadBillBtn = document.getElementById("download-bill-btn")
    let submittedOrder = false
    if (downloadBillBtn) {
        downloadBillBtn.addEventListener("click", function () {
            document.getElementById("priceTotal").value = totalMoneyToPay.textContent.replace(" lei", "")
            submittedOrder = true
            document.orderForm.action = "/prepare_bill/"
            document.orderForm.submit()
        })
    }
    // checking if the user want to download the pdf format bill or just send the email with the bill
    document.getElementById("myModal").addEventListener("click", function (e) {
        if (e.target === e.currentTarget || e.target.classList.contains("close") || e.target.id === 'closeModal') {
            if (!submittedOrder) {
                document.getElementById("priceTotal").value = totalMoneyToPay.textContent.replace(" lei", "")
                document.orderForm.action = "/download_bill/"
                document.orderForm.submit()
            }
            setTimeout(function () {
                window.open("/", "_self")
            }, 300)
        }
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