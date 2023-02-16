const quotes = [
  {
    instructor: 'Leanne Hainsby',
    quote: "Yes to you! Done and dusted."
  },
  {
    instructor: 'Jess Sims',
    quote: "You don't have to, you get to."
  },
  {
    instructor: 'Tunde Oyeneyin',
    quote: "Your mind is your strongest muscle."
  },
  {
    instructor: 'Adrian Williams',
    quote: "If you don't squeeze your glutes no one else will."
  },
  {
    instructor: 'Kendall Toole',
    quote: "They can knock you down, but never let them knock you out."
  },
  {
    instructor: 'Denis Morton',
    quote: "I make suggestions, you make decisions."
  },
  {
    instructor: 'Alex Toussaint',
    quote: "This ain't daycare."
  },
  {
    instructor: 'Ally Love',
    quote: "Make modifications, not excuses."
  },
  {
    instructor: "Christine D'Ercole",
    quote: "I am. I can. I will. I do."
  },
  {
    instructor: 'Emma Lovewell',
    quote: "I got you."
  },
  {
    instructor: 'Cody Rigsby',
    quote: "Fix your wig and get your life together, boo."
  },
  {
    instructor: 'Olivia Amato',
    quote: "This is tough but you're tougher."
  },
  {
    instructor: 'Robin Arzon',
    quote: "Yes, you can."
  }]

  const random = Math.floor(Math.random() * quotes.length);
  const instructor = quotes[random].instructor
  const quote = quotes[random].quote
  document.querySelector('#banner-quote').innerText = `"${quote}"`
  document.querySelector('#banner-instructor').innerText = `- ${instructor}`
  

