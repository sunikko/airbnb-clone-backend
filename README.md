# airbnb-clone-backend
Django, React

# install poetry - python3.10 or above
```
curl -sSL https://install.python-poetry.org | python3 -
```
Poetry uses a pyproject.toml file to define a project's metadata and configuration, which can be used by tools like Poetry to manage dependencies, build the project, and perform other tasks

```
poetry init
```
```
poetry add django
```

- All Models 
	- Users
		- Profile Photo
		- Gender
		- Language
		- Currency Options

	- Rooms
		- Country
		- City
		- Price Per Night
		- Description
		- Owner
		- the number of Rooms
		- the number of Toilet
		- Address
		- Pet Friendly
		- Category
		- Type of Place (Entire Place| Private Room| Shared Room)
		- Amenities (Many to Many) 
			- Name

	- Experiences
		- Country
		- City
		- Name
		- Host
		- Price
		- Description
		- Address
		- Start Time
		- End Time
		- Category
		- Materials (Many to Many)
			- Name
			- Description

	- Categories
		- Kind (Room|Experience)
		- Name

	- Reviews
		- Review
		- Rating
		- Room
		- Experience
		- User

	- Wishlists
		- Name
		- Rooms
		- Experiences
		- User

	- Bookings
		- Kind (Room|Experience)
		- Room
		- Experience
		- Check In
		- Check Out
		- Experience Date

	- Photos
		- File
		- Description
		- Room
		- Experience
        
	- Messages
		- Room
			- Users
		- Message
			- Text
			- User
			- Room
