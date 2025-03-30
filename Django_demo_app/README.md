# HW-5. Django start-up application.
You need to create a new Django project and implement 2 applications: courses_app and members_app.
In members_app, implement an input page, a user input display page, and an additional page that will work with request.session. 
In courses_app, implement a page that, 
if the user is authenticated, display the message "This is the Courses page", 
in the opposite case, display "You have no permissions to view this page".

You need to connect PostgreSQL and additionally download screenshots with database creation commands and created post-migration tables

# HW-6. Custom User Model.
It is necessary to create a new application and implement a custom User model.
You can use both AbstractUser and AbstractBaseUser, PermissionMixin.
Fields and their quantity - according to your preferences.

# HW-7. Template tags.
Write at least three different template tags, including: 
- A simple tag (for example, returning the current date or formatting the text). 
- Tag with arguments (for example, combining lines or cropping text to a given length). 
- Inclusive tag (which connects another template or executes a certain logic).
 13 changes: 13 additions & 0 deletions13  
Django_demo_app/course_management/accounts/templates/accounts/tags.html

# HW-8. Admin customization
Basic customization:
Register your main model in admin.py.
Define which model fields will be displayed in the list of objects (e.g. name, date, status).
Add filters for 1-2 key fields that will help you find objects quickly.
Set up a search for 2-3 fields that are unique or important to your project.

Advanced customization:
Enable sorting by 1-2 fields (e.g. date or alphabet).
Make one boolean or simple field (e.g. status) editable directly in the list.
Set a limit on the number of objects per page (e.g. 10 or 15).
If your model does not have a creation date field, add it (auto_now_add=True) and display it in the list.
Divide the fields in the edit form into 2-3 logical groups (fieldsets) depending on their purpose.
Add validation: if a field has an invalid value (e.g., a date in the future, too long text), display a warning to the user.

Additional task (optional):
If your project has a related model (via ForeignKey or ManyToMany), add it as a tab (inline) in the main model edit form.
Implement a column in the list that shows the number of related objects or other aggregated information.

# HW-9. Django mixins
You need to create a mixins.py file in the project and write 10 mixins. At least 3 of them are noteworthy for the luff from your application