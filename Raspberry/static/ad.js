let mouseCursor = document.querySelector(".cursor")
let lis = document.querySelector("li")


window.addEventListener("mousemove", cursor)

window.addEventListener("mousedown",() => {
    mouseCursor.classList.add("mouse-down")
})

window.addEventListener("mouseup",() => {
    mouseCursor.classList.remove("mouse-down")
})


function cursor(e) {
    mouseCursor.style.top = e.pageY + "px"
    mouseCursor.style.left = e.pageX + "px"
    
}