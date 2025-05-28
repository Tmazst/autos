
// document.addEventListener("DOMContentLoaded", function() {
//     var hiddenElement = document.querySelector("#email");
//     if (hiddenElement) {
//         hiddenElement.required = false;
//     }
// });

const divs = document.querySelectorAll(".hidden");
var observer = new IntersectionObserver(entries => {
    entries.forEach(entry =>{
        //console.log(entry.target)
        entry.target.classList.toggle("show", entry.isIntersecting)
        if (entry.isIntersecting) observer.unobserve(entry.target)
        });
    },
    {
    threshold:0.5,
    //rootMargin:"0px"
    }
);

divs.forEach(div =>{
    observer.observe(div)
});

var btn = document.querySelector('#updates-btn');

btn.addEventListener("click",() => {
    let popUp = document.querySelector("#updates-popup");
    let popCont = document.querySelector("#updates-cont");

    popUp.classList.toggle("show-popup");
    popCont.classList.toggle("show-popup");

});

// quoteBtns.forEach(function(btn){
function updatesPopup(id){
        // var popScrnLogo = document.getElementById("updates");
        // popScrnLogo.classList.toggle("show-popup");
     let popup = document.querySelector("#updates-popup-"+id);
     let popCont = document.querySelector('#updates-cont-'+id);
     popup.classList.toggle("show-popup");
     popCont.classList.toggle("show-popup");

     popCont.classList.toggle("updates-cont");

 };

// quoteBtns.forEach(function(btn){
function popUp(id){
    let popup = document.querySelector("#popup_"+id);
    let popCont = document.querySelector('#pop-cont_'+id);
    popup.classList.toggle("show-popup");
    popCont.classList.toggle("show-popup");

};

function closePopup(id){
    let popup = document.querySelector("#popup_"+id);
    let popCont = document.querySelector('#pop-cont_'+id);
    popup.classList.remove("show-popup");
    popCont.classList.remove("show-popup");
};


function closeUpdatesPop(id){
    let popup = document.querySelector("#updates-popup-"+id);
    let popCont = document.querySelector('#updates-cont-'+id);
    popup.classList.remove("show-popup");
    popCont.classList.remove("show-popup");
};