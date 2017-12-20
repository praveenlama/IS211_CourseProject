# IS211_CourseProject

<h2>Books for ALL<h2>

By: Praveen Lama

<strong><u>Description:</u></strong>
<p>Books for All is a book catalogging application which uses Google Books API to retrive the data. Just search for any books and add it to your book list. You can also surf through the books by different pre-determined categories in the application and as well add them to you list.</p>

<strong><u>Software Design:</u></strong>

The project is built on python using Flask. 

API: Google Books

Database: storage.db

Schema: Schema.sql

Classes: Book , User, DBConnector
<p>These are object oriented classes and represents the model of the application. It helps the application for data storage and retrieval via it's methods.</p>

Main(): app.py
<p>It is a controller for the application which handles all the http requests and connects them with the views and models.</p>

<strong><u>QA TEST:</u></strong>

To start -> python app.py

Browser -> http://localhost:5000/ (or port you have configured) 

For Login -> email: praveenlama@gmail.com  |  password: pass123

<p>After successful login, user will be taken to the home page where they can make a search. The search result as well as the items displayed in the slideshow/carousel can be added to the user's list.</p>
<p>A user can to their books list (/books), and browse through the list of books owned by them and also delete the books from it.</p>
<p>Finally, a user can log out and go out of the application.</p>

*** Some of the fields might be missing or have null or 0 because the API does not have the field in their JSON Response.
*** When going to Categories Page, you might have a slight delay loading the page because it is making multiple api calls to Google Books Api to load the carousels
*** Any other user will have his/her own list of books which are added by themselves.

<strong><u>Sitemap:</u></strong>
<ul>
<li>Home -> /</li>
<li>Categories -> /categories</li>
<li>Your Books -> /books</li>
<li>Add a Book -> /addBook</li>
</ul>
