const quotes = [
  {
    instructor: 'Leanne Hainsby',
    quote: "Done and dusted. Yes to you ! ",
    font: 'Oooh Baby',
    size: '2.5em'
  },
  {
    instructor: 'Jess Sims',
    quote: "You don't have to, you get to.",
    font: 'Fuzzy Bubbles',
    size: '1.7em'
  },
  {
    instructor: 'Tunde Oyeneyin',
    quote: "Your mind is your strongest muscle.",
    font: 'Waiting for the Sunrise',
    size: '2.2em'
  },
  {
    instructor: 'Adrian Williams',
    quote: "If you don't squeeze your glutes no one else will.",
    font: 'Mynerve',
    size: '1.8em'
  },
  {
    instructor: 'Kendall Toole',
    quote: "They can knock you down, but never let them knock you out.",
    font: 'Covered By Your Grace'
  },
  {
    instructor: 'Denis Morton',
    quote: "I make suggestions, you make decisions.",
    font: 'Rock Salt',
    size: '1.7em'
  },
  {
    instructor: 'Alex Toussaint',
    quote: "This ain't daycare.",
    font: 'Permanent Marker',
    size: '2.4em'
  },
  {
    instructor: 'Ally Love',
    quote: "Make modifications, not excuses.",
    font: 'Licorice',
    size: '3em'
  },
  {
    instructor: "Christine D'Ercole",
    quote: "I am. I can. I will. I do.",
    font: 'Gochi Hand',
    size: '2.2em'
  },
  {
    instructor: 'Emma Lovewell',
    quote: "Acknowledge the fear and do it anyway.",
    font: 'Shadows Into Light Two'
  },
  {
    instructor: 'Cody Rigsby',
    quote: "Fix your wig and get your life together, boo.",
    font: 'Indie Flower'
  },
  {
    instructor: 'Olivia Amato',
    quote: "This is tough but you're tougher.",
    font: 'Sedgwick Ave'
  },
  {
    instructor: 'Robin Arzon',
    quote: "It doesn’t get easier. You get stronger.",
    font: 'Caveat',
    size: '2.5em'
  }
];

const random = Math.floor(Math.random() * quotes.length);
const instructor = quotes[random].instructor
const quote = quotes[random].quote
const font = quotes[random].font
const size = quotes[random].size
document.querySelector('#banner-quote').innerText = `"${quote}"`;
document.querySelector('#banner-quote').style.fontFamily = `${font}`;
if (size) {
  document.querySelector('#banner-quote').style.fontSize = `${size}`;
}
document.querySelector('#banner-instructor').innerText = `- ${instructor}`;