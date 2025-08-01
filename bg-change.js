const backgrounds = [
  'images/bg1.jpg',
  'images/bg2.jpg',
  'images/bg3.jpg',
  'images/bg4.jpg'
];

let index = 0;
const bgDiv = document.getElementById('background');

function changeBackground() {
  bgDiv.style.backgroundImage = `url('${backgrounds[index]}')`;
  index = (index + 1) % backgrounds.length;
}

setInterval(changeBackground, 3000); // change every 3 seconds
changeBackground(); // set initial
