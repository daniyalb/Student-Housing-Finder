# Student Housing Finder 🏠
 A python web scraping program which helps assist students in finding housing accommodations. The program saves students time in searching for housing by looking through listings on kijiji.ca which match their filters (website filters + additional custom made filters) and displays the results in a txt file, taking far less time than it would for one to search for and read through each listing. The program also provides an automatic search feature which searches for new listings every few minutes, as specified by the user. This allows users to see new listings that match their filters as soon as they are posted, allowing them to be the first to contact the owner and have a higher chance at securing a lease.
 # Screenshots 📸
 Filter Select Screen:
 
<img width="865" alt="Screen Shot 2022-09-08 at 12 41 55 AM" src="https://user-images.githubusercontent.com/63890998/189036314-8f2e7903-99e6-4658-a29d-b8104448071a.png">

Main Menu:

<img width="867" alt="Screen Shot 2022-09-08 at 12 43 26 AM" src="https://user-images.githubusercontent.com/63890998/189036413-0819813f-79fb-4bee-ac81-e8e61ee21244.png">

Search Results:

<img width="865" alt="Screen Shot 2022-09-08 at 12 44 23 AM" src="https://user-images.githubusercontent.com/63890998/189036463-3e325d68-c6e6-4771-85df-3e67c38194b7.png">

Setting Up Auto Search:

<img width="863" alt="Screen Shot 2022-09-08 at 12 44 38 AM" src="https://user-images.githubusercontent.com/63890998/189036526-75df75d6-c895-48bc-b012-52ab2b59caec.png">

Auto Search Running:

<img width="863" alt="Screen Shot 2022-09-08 at 12 44 45 AM" src="https://user-images.githubusercontent.com/63890998/189036577-0679b8c0-2a50-43a4-badc-dae38b189093.png">

# Technologies Used 💻
- Python
- Beautiful Soup 4
- Tkinter
# Installation Instructions
1. Ensure that you have Python 3.9+ installed on your computer
2. Clone this repository onto your computer
3. Install Beautiful Soup by running this command: `pip install beautifulsoup4`
4. Install the parser method used in this program: `pip install lxml`
5. Install the requests library: `pip install requests`
6. Install the Pillow library for displaying images: `pip install Pillow`
7. Install the beepy package for notification sounds: `pip install beepy`
8. Run main_gui.py
# Reflection 🤔
This was a side project I made to continue to improve my programming skills with Python and to also explore something which has always been interesting to me, web scraping.

The idea for this project came from issues I heard from my peers at university about finding housing and rentals in the time before university starts. Their main complaint was that listings would be posted and and removed quickly as many people are looking for housing at that time and so they would have to sit on sites like kijiji.ca and keep reloading until a listing would pop up, then they would have to read through it to see if its a match, and finally contact the owner. When I heard about these problems, I thought that I could make a solution that would save students time in searching for housing and make the whole process a bit easier.

To create this program, I had to first learn about web scraping and the Beautiful Soup library for Python. I thought Beautiful Soup was the best choice as it's best designed for grabbing information from static websites with easily accessible HTML code. I also realised that I would need to create a GUI for this program as that would make it easier for others to quickly understand how to use it. For this, I chose Tkinter as it can create simple yet intuitive GUIs that would work well for what I intended the program to do.

An obstacle I encountered when making this program was understanding how the HTML code of kijiji.ca web pages are structured and devising the best ways to extract useful information from them. I had to learn how the site organized its listings and their information and once I figured it out, I was able to write code that was able to loop through each listing and compare the search filters with the information presented in them.
 Another obstacle was getting my Tkinter UI to interact and work well with the searching code I wrote that utilised Beautiful Soup. This involved getting an in-depth understanding of how Tkinter functions and how the main loop for the UI works, and from there I was able to program the widgets to perform their appropriate function.
