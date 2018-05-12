## NJ Carbon Dividend Calculator
By the year 2100, climate change could force 100s of thousands of NJ citizens to evacuate the coastline. 

20 students at Princeton are working with state legislators to put a price on carbon in New Jersey. 
The policy is to place a fee on fossil fuels, The majority of revenue returned to households as dividends to handle the increased energy costs. Economists and politicans of both parties support this policy.

How would this policy affect your family? Estimating an individual’s net monetary gain or loss is a technical and laborious process that the average NJ citizen might not have the time for.
This is where our project, the Carbon Dividend Calculator, comes in.

Our simple web app takes in user energy information and outputs the impact on their bottom line.
We provide personalized information in a transparent and nonpartisan way. 
Our vision is a clear, intuitive app that empowers thousands of users to better understand and adapt to this new carbon policy.

### Project Link
Simply visit [http://njcdc.herokuapp.com/calc](http://njcdc.herokuapp.com/calc)!

### Team Members
* Agata Foryciarz (agataf@princeton.edu)
* Changyan Wang (dcw3@princeton.edu)
* Jonathan Lu (jhlu@princeton.edu), Project Leader
* Joseph Abbate (jabbate@princeton.edu)

**TA** Ashley Kling

### Design Document
Check out our Design Document [here](https://docs.google.com/document/d/1fbyBMIPSoOc2NCIeDV0IEIyHV9j41kQMEy9_4SR4y1I/edit?usp=sharing).

## Download guide:
1. Create a new directory, start a virtualenv (make sure you're using Python3!)
```
mkdir ~/njcdc_calc
virtualenv njcdc
source njcdc/bin/activate
```
To ensure you are using Python 3.6, you can run
```
virtualenv njcdc -p /usr/bin/python3.6 njcdc
```
2. Clone this directory
```
git clone git@github.com:lujonathanh/njcdc.git
```
3. Install dependencies
```
pip install Django==2.0.5
pip install whitenoise
```
4. Move local settings to a settings file
```
cd ~/njcdc_calc/njcdc 
mv njcdc/settings.py njcdc/settings_original.py
mv njcdc/settings_local_template.py njcdc/settings.py
```
5. Run manage.py
```
cd ~/njcdc_calc/njcdc
python manage.py migrate
python manage.py runserver 8000
```
This will activate the website on the chosen port 8000 (you can change this number)

You can now access the site at your local browser by pasting
```
http://127.0.0.1:8000/
```

