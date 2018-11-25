# Item Catalog Project
This is a project for Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)
## Project Description:
The task is to develop an application that provides a list of items within a variety of categories as well as provide a user 
registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
## Features:
1. Proper authentication and authorisation check.
1. Full CRUD support using SQLAlchemy and Flask.
1. JSON endpoints.
1. Implements oAuth using Google Sign-in API.
1. Project Structure
## The Project Setup:
This project is run in a virutal machine created using Vagrant so there are a few steps
to get set up:
#### Setting up the files:
1. Install [Vagrant](https://www.vagrantup.com/)
1. Install [VirtualBox](https://www.virtualbox.org/)
1. Download the vagrant setup files from [Udacity's Github](https://github.com/udacity/fullstack-nanodegree-vm)
These files configure the virtual machine and install all the tools needed to run this project.
1. Download this project: [Item-Catalog](https://github.com/Lohith94/Item-Catalog.git)
1. Upzip as needed and copy all files into the vagrant directory into a folder called Item_Catalog
#### Start the Virtual Machine:
1. Open Terminal and navigate to the project folders we setup above.
1. cd into the vagrant directory
1. Run ``` vagrant up ``` to build the VM for the first time.
1. Once it is built, run ``` vagrant ssh ``` to connect.
1. cd into the correct project directory: ``` cd /vagrant/Item_Catalog ```
#### Installing the dependencies:
* Install or upgrade Flask:
```sudo python -m pip install --upgrade flask```
* Run the following command to set up the database:
```python database_setup.py```
* Run the following command to insert dummy values. If you don't run this, the application will not run.
```python stock_library.py```
* Run this application:
```python app.py```
* Open [http://localhost:5000](http://localhost:5000) in your favourite Web browser.
#### Access the JSON API endpoints by using the URLs below:
* Access a list of all the books:[http://localhost:8000/api/v1/genre/JSON](http://localhost:8000/api/v1/genre/JSON)
* Access a list of all the genre:[http://localhost:8000/api/v1/books/JSON](http://localhost:8000/api/v1/books/JSON)
* Access a list of all the books in a particular genre: [http://localhost:8000/api/v1/genre/<int:genre_id>/books/JSON](http://localhost:8000/api/v1/genre/<int:genre_id>/books/JSON)
* Access data for an individual book bu book_id and genra_id: [http://localhost:8000/api/v1/genre/<int:genre_id>/book/<int:book_id>/JSON](http://localhost:8000/api/v1/genre/<int:genre_id>/book/<int:book_id>/JSON)
