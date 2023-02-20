var counter = 0;

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function showSlides2() {
    let slides = document.getElementsByClassName("number");
    let itog = 0;
    let it = 0;
    if (24 == counter) {
            clearTimeout(timerId);
            return anim();
    }
    while (true){
        let ind = getRandomInt(document.getElementsByClassName("number").length);
        if (slides[ind].style.backgroundColor != 'black'){
            slides[ind].style.backgroundColor = 'black';
            counter += 1;
            break;
        }
    }
    for (let i=0; i < 25; i++){
        if (slides[i].style.backgroundColor != 'black'){
            itog += Number(slides[i].textContent);
            it += 1;
        }
    }
    let aa = document.getElementById("itog");
    aa.innerHTML = Math.floor(itog / it);
}

function anim(){
    let slides = document.getElementsByClassName("number");
    while (true){
        let ind = getRandomInt(document.getElementsByClassName("number").length);
        if (slides[ind].style.backgroundColor != 'black'){
            console.log(slides[ind].style.top);
            slides[ind].style.transform = 'translateX(calc(50vw - ' + slides[ind].style.left
             +')) translateY(calc(50vh - ' + slides[ind].style.top +'))  translate(-50%, -50%) translateX(-100px) scale(10, 10) rotate(720deg)';
            break;
        }
    }
}
timerId = setInterval(showSlides2, 100);
