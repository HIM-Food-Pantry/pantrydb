# pantrydb

**A Django Project to manage the Heights Interfaith Ministry Food Pantry volunteers and clients. It's built with Python and the Django Web Framework**

This project has the following apps:

* accounts - contains shared information used in the rest of the apps
* volunteers - has volunteer profile and the hours log
* clients - clients of the pantry
* delivery_clients - clients that are delivered to

## Volunteers

### Models
* Volunteer
    * proxy model of user
    * Creates a group called Volunteers if their isn't one when creating a new Volunteer.
    * Volunteer queries will only return users who are in the volunteers group.
* VolunteerProfile
    * Inherits baseProfile 
* VolunteerLog 
    * Dates with sign and out times
    * One Volunteer
    * Custom queryset that gets todays logs without a signout time

### Views
#### CreateVolunteerView
 * Create volunteer
 * Name and a zipcode
 * Nice to show username for future reference
 
#### SignInView
 * Two forms handled with prefixes 
  * Sign out
  * Sign In
  * Link to CreateVolunteerView if volunteer not found.

#### Forms
* CreateSignOutForm
* Sign In
* LogSignOutForm


Each user has extras fields based on if they are staff, volunteer, or client.
 
A specific user is created to be signed in to allow volunteers to be able to access the volunteer page.

Cronjabs are run once a day at 11 pm to clean up and users without a sign in time.


