# Crenshaw-JobFit
Manual assessment type application written for CITS3403 project 2, 2020.
This is a flask app that mimicks online psychometric testing websites. The app can be used by clients to assess whether a candidate is worthy of progressing in their application for a job or just general testing of individuals.
Users will be given tasks that they need to do complete. That data will get stored in a database and admin can assess that data. According to the data, they can give custom feedback to the user regarding their testing.

## Supported Features
### Admin
- create emotional intelligence assessments
- create behavioural sets
- add questions to behavioural sets with custom time limits
- add verbal reasoning questions
- add user
- delete users
- create custom feedback just for that user
- add tasks for users
### Non-admin user
- Can log in and out using their username and password.
- respond to all sorts of questions available to them or questions that only they've been asked to do.
- receive custom feedback
- "forgot password"

## Assessment types
### Behavioural questions
e.g "describe a stressful work situation and what you did about it."
### Verbal Reasoning
e.g "Some older people dont like technology. According to above question we can say that every single old person in the world doesnt like technology"

The user has the answer options of:
- "True (the statement follows logically from the information or opinions contained in the passage)"
- "False (the statement is logically false from the information or opinions contained in the passage)"
- "Cannot say (cannot determine whether the statement is true or false without further information)"

### Emotional Intelligence
e.g " I enjoy routine more than others"
User has answer options:
-"Strongly Disagree, Disagree, Neutral, Agree, Stronly Agree"

#### PLEASE NOTE ANSWER OPTIONS FOR VERBAL REASONING AND EMOTIONAL INTELLIGENCE ARE NOT LIMITED TO TRUE-FALSE-CANNOT SAY AND STRONGLY DISAGREE-DISAGREE-NUETRAL-AGREE-STRONGLY-STRONGLY AGREE RESPECTIVELY. IN REALITY ADMIN CAN INPUT WHATEVER ANSWER OPTIONS THEY WANT BUT THE ASSESSMENTS ARE CREATED WITH THOSE TYPES OF QUESTIONS KEPT IN MIND.

## MODELS
- The relational database scheme has been attatched in the github repo. It is titled CITS3403 Data Scheme.pdf

## EXECUTION
- flask run

## INSTALLATION
- make sure latest version of python is installed. You can check for this by typing "python3 --version" in your terminal. if nothing comes up it means you havent installed it. Therefore you need to download it externally.
- Change your working directory to desktop in your terminal.
- Type "mkdir crenshaw" and press enter
- Type "cd crenshaw" and press enter
- Then type "git clone https://github.com/chamk21/Crenshaw-JobFit.git"
- Type "cd Crenshaw-JobFit"
- python3 -m venv venv
- source venv/bin/activate
- pip3 install -r requirements.txt
- export FLASK_APP=quiz.py
- flask run
  
## Current User Accounts
- Admin account with username "Admin" and password "Admin123"
- Example user account with username "Michael Jordan" and password "Michael123"
- You are free to make any user account as you would like
   
## AUTHORS
- Chamika Kariyawasam(22508087)
- Shathish Nagulan(22485727)

## Libraries and acknowledgements
- Font Awesome
- darkcode.info
- W3SCHOOLS
- https://www.darkcode.info/2019/02/responsive-services-section-using-only.html?fbclid=IwAR3KYscJlX4eS249GsfWtACWCSTfy3rGFR1B8Gg_iccdoC1cDiIbrkx9ySk

- Dark theme: https://www.darkcode.info/2018/10/social-media-buttons-with-amazing.html?fbclid=IwAR2qyd4k2XM9YjD8ln6zInkRY0AO3YwpYDYffOJlCbRUYanAeTShDb9z7Vo

- NavBar Theme:https://webdesign.tutsplus.com/tutorials/building-an-admin-dashboard-layout-with-css-and-a-touch-of-javascript--cms-33964?fbclid=IwAR1LiHoKpnYzWorLAFhZVMGCATX9NM6t8ABAFnzJASfv1awzdnZ-nW7Z2TE

## Demo
- If you would like a demonstration of the site, please download the video file titled "admin-demo" and open it using a video player of your choice.


