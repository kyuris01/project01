const levelUp = document.getElementById("up");
const levelDown = document.getElementById("down");
let level = document.getElementById("champ_level").innerText;
level = Number(level);

function increaseLevel () {
    if (level < 18) {
        level += 1;
        document.getElementById("champ_level").innerText = level;
    }
}

function decreaseLevel () {
    if (level > 1) {
        level -= 1;
        document.getElementById("champ_level").innerText = level;
    }
}

levelUp.addEventListener('click', increaseLevel);
levelDown.addEventListener('click', decreaseLevel);


