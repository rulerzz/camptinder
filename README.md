## installation
- install postgreSQL (make sure to include pgAdmin4 in the installation)
## clone the repositry
- cd backend
## create virtual env
- python -m venv venv
- source/Scripts/venv
## install package
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver
- python manage.py createsuperuser (This user is for accessing the admin panel)
- python manage.py setup_groups (For the organization permissions required for org_admin permissions)
## Create .env file
- SECRET_KEY='your_secret_key'
- DBNAME='camptinderdb'
- DBUSER='postgres'
- DBPASSWORD='your_password'
- DBHOST='localhost'
- DBPORT=5432
## In pgAdmin4 create a database name camptinderdb otherwise connetion not found...
## Admin panel
### **Auth Routes (`localhost/admin/`)**
- Main admin panel for the superuser
### **Auth Routes (`localhost/org-admin/`)**
- Panel for organization admin/staff displays only inside of organization tables.
## API Routes
### **Auth Routes (`/api/auth/`)**
| Method | Route | Description | Request | Response |
|--------|--------|--------|--------|--------|
| POST | `/register/` | Creates a new user | Body: email, first_name, last_name, phone, password, password_confirm | User data, succes status |
| POST | `/login/` | Logs in a user | Body: email, password | Access token in body, refresh token in HttpOnly cookie, user data |
| POST | `/logout/` | Logs out a user | Auth header: Bearer {access_token} | Success message, clears refresh cookie |
| POST | `/refresh/` | Refreshes token | No body needed (uses refresh cookie) | New access token |
 ### **User Routes (`/api/users/`)**
| Method | Route | Description | Request | Response |
|--------|--------|--------|--------|--------|
| GET | `/profile/` | Fetches logged-in user details | Auth header: Bearer {access_token} | User profile data |
| PATCH | `/profile/` | Updates user profile | Auth header: Bearer {access_token}, Body: fields to update | Updated user data |
 ### **Location Routes (`/api/locations/`)**
| Method | Route | Description | Request | Response |
|--------|--------|--------|--------|--------|
| GET | `/locations/` | Fetches all locations | No body needed (does not require token) | Location data (all) |
| GET | `/locations/id/` | Fetches location by id | No body needed (does not require token) | Location data (single) |
 ### **Machine Routes (`/api/machines/`)**
| Method | Route | Description | Request | Response |
|--------|--------|--------|--------|--------|
| GET | `/machines/` | Fetches all machines | No body needed (does not require token) | Machine data (all) |
 ### **Inventory Routes (`/api/machines/inventory//`)**
| Method | Route | Description | Request | Response |
|--------|--------|--------|--------|--------|
| GET | `/machines/inventory/id/` | Fetches machine and inventory by id | No body needed (does not require token) | Machine/Invetory data (all) |

## How to register tables to org-admin panel
### Main admin panel
```
class MainCountryAdmin(admin.ModelAdmin):
    code...
    
try:
    main_admin_site.unregister(Location)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(Location, MainLocationAdmin)
```
### Organization admin panel
```
class OrganizationCountryAdmin(admin.ModelAdmin):
    code...
    
try:
    org_admin_site.unregister(Country)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(Country, OrganizationCountryAdmin)
```
### You can also for loop the registeration
```
for model, admin_class in [
    (ProductType, MainProductTypeAdmin),
    (Product, MainProductAdmin),
    (ProductVariant, MainProductVariantAdmin),
    (LockerType, MainLockerTypeAdmin),
    (Locker, MainLockerAdmin),
]:
    try:
        main_admin_site.unregister(model)
    except admin.sites.NotRegistered:
        pass
    main_admin_site.register(model, admin_class)
```