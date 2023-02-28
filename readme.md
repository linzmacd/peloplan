# PeloPlan

A workout planning and schedule sharing app for Peloton users.

*Now deployed at [PeloPlan.com](http://peloplan.com/)!*

## Technologies
- Backend: Python, Flash, PostgreSQL, SqlAlchemy 
- Frontend: JavaScript, React, AJAX, JSON, Chart.js, HTML, CSS, Flexbox, Bootstrap
- API: Peloton API

## Features

*Please find my full [Demo Video](https://www.youtube.com/watch?v=wR8js2b2S1I) on YouTube.*

- After connecting with a Peloton account, PeloPlan displays a calendar with user's workout history.

<img src='static/img/readme/homepage.jpg' title='PeloPlan'>


- Build schedules with classes from the Peloton catalog or generic workouts that can be decided on later. 
<p><img src='static/img/readme/disciplines.png' title='Disciplines' width=48%><img src='static/img/readme/workouts.png' title='Workouts' width=50%></p>


- Track progress over time to see whether they are sticking to their PeloPlan.  

<img src='static/img/readme/sequenceHD.gif' title='Tracking'>
  

- Reuse or share schedules as well as rate and/or load other users’ publicly shared schedules.  

<img src='static/img/readme/schedules.png' title='Schedules'>


- View workout history broken down by discipline and instructor and track cycling outputs over time. 
<p><img src='static/img/readme/charts.png' title='Charts' width=49%><img src='static/img/readme/outputs.png' title='Outputs' width=49%></p>

- Search for friends by name or email and follow them to share schedules on PeloPlan.


## Set Up
*Please note that you will need to connect to a Peloton account to use this app*

1. Clone git repository
```bash 
    git clone https://github.com/linzmacd/peloplan.git 
```

2. Create and activate a virtual environment inside the directory
```bash 
    create virtualenv env
    source env/bin/activate
```

3. Install requirements
```bash 
    pip3 install -r requirements.txt
```

4. Initialize database
```bash
    python3 init.py
```

5. Run server
```bash
    python3 server.py
```

When you navigate to [http://localhost:5000/](http://localhost:5000/) you will now be able to log in and make your own PeloPlan!

## About Me

Hi! I'm Lindsay, a freshly minted software engineer having recently completed an immersive 12-week full-stack software engineering fellowship at Hackbright Academy. I originally studied bioengineering and business at UC Berkeley and worked in biotech for the better part of a decade before moving into a management role in the hospitality industry. The only constant throughout my career has been my perpetual drive to make things better, be it through problem-solving, improving efficiency, reducing waste, or eliminating redundancies. I look forward to bringing that same curiosity and determination into the next chapter of my career as a software engineer. I hope you enjoyed my web app and demo, please feel free to connect if you have any questions or feedback. Thank you!