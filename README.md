# Buskisterclansa
a sort of social media/forum about movies inspired by pages like IMDB, FilmAffinity or Rotten Tomatoes. It counts with reviews by stars and like/dislike systems, several simple filter systems like orders and advanced pagination, search and login/singin. It is obvously not perfect, it needs and will have many other things in future updates, like a responsive frontend (yes, it isn't responsive yet), more models and better user expiriences.

Video (click the 720 resolution to watch it better): https://www.youtube.com/watch?v=j_O-HbEQruQ

## Required knowledge
- Intermediate/advanced Python and Django.
- Basic HTML and CSS.
- SQL and MySQL (or any SQL manager like PostgreSQL or SQLite3)
- Git.

## Database
#### Independant models
It counts with five independant models, Movie, Movie_Staff, Company, CustomUser and Genre.

1. **Movie**: The movies per se, with their name, synopsis, Image etc.
2. **Movie_Staff**: The workers of the movies, they can be directors, actors, producer or even extras, they can be in several movies and the movies have several workers, it ends being an independant model considering that all the relations are ManyToMany (Cast, Director, Producer and Script).
3. **Company**: The companies that a movie belongs, such as Movie_Staff, all the relations with the movies are ManyToMany.
4. **CustomUser**: Model to add and modify fields of the original user model.
5. **Genre**: The genres of a movie.

#### Dependant models
Ignoring the ManyToMany relations, there are four dependant models.

1. **Review**: The review a user can write about a movie. It has a star rating system and the user may only write one review, it has no sense to write several reviews actually.
2. **ReviewLike/ReviewDislike:** The relation between a user and a review to like or dislike a review.
3. **ReviewComment**: Comments that user can write about a review.

#### Flowchart
![](https://i.postimg.cc/DZ1gJJzj/buskisterclansa-flowchart.jpg)

## Apps
The project is divided in eight apps.

##### accounts
Every authentication system is in this app, the views for logging in and signing in and the CustomUser model.
###### Views
- **SingInView**: Singing in process, the user has to fill in an auth form, if the filled form is valid, it returns to the login view, if not, returns the same template with the current errors. If the user is already authenticated the view won't be available.
- **CustomLoginView**: In the default login view that Django has, does not return any error if there is, I modified that in this custom view to be able to return errors.

##### companies
The company model and the view for a company are in this app. The company model is created here
###### Views
- **CompanyView**: Shows the main information of a company and the movies that belong to it. It has a filtering system to sort the movies by years and the quantity of reviews those movies have.

##### extra_logic
Any extra algorythm I need for the rest of the project is in this app, pagination or reusable algorithms for example.

##### genres
The app of the genres of the movies. The genre model is created here
###### Views
- **GenreView**: Shows the movies belonging to a genre, filtered by most, best and worst rated in relation to their reviews.

##### home
The home page.

##### movie_staff
The app of the workers of a movie. The movie staff model is created here.
###### Views
- **MovieStaffView**: Shows the main info of a staff and the movies it's been. They movies can be filtered by ones the staff has been as director, cast, producer or script and all its movies.

##### movies
The jewel in the crown. The movies and anything related to them are used in this app. It is a pipe that connects and uses the rest of the apps.
###### Views
- **MovieView**: Shows all the information of the queried movie, synopsis, image, main characters, directors and producers, the companies it belongs, and the its lastest reviews.
- **DragMovieStaffView**: This view is to change the order in which the staff of a movie is showed. In a movie there are more important characters than others, you won't show an extra before the main characters, they must have an order of appearance, and, changeable, this is achieved with a draggable list with JS. To access to this view the user must authenticated and have the is_admin attribute checked (checked or unchecked by the main admin of the project), if not, 404 is raised.
- **MovieReviewsListView**: Shows all the reviews belonging to a movie. The reviews can be filtered by stars (5, 4, 3, 2 or 1) and ordered by higher or lower stars rating, as well as pagination system.
- **AddReviewView**: Where the user can write a review. Just one review can be written, so if the user has one already that's the one that will be showed and changeable. It is a login_required view.
- **DeleteReviewView**: Just a post view to delete a review by its user.
- **ReviewDetailView**: Shows a review, here's the like/dislike system and also the comments of that review that other users can write.
- **LikeDislikeReviewView**: A post view to add like or dislike to a review.
- **AddCommentReviewView**: View to add a comment to a review.
- **StaffOfAMovieView**: Show all the staff of a movie divided by director, cast, producer and scriptwriter.
