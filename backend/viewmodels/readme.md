# View models

* Job is to manage exchange of data from client to server
* Validates data that gets exchanged
* Class based

Fields of the view model are a dictionary
*Field values/data are obtained from Services Base view model
*Page specific viewmodels inherit the base view model

* EX:    Make sure every page has login functionality
* EX:    Make sure every form has an error to return

* Pydantic work with View Models
    * Why not just Pydantic by itself? → It just crashes when data doesn’t match (good for API, not for web app with
      HTML)
    

