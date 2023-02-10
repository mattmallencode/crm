# Sherpa: A Free and Open-Source CRM
![Sherpa logo: a picture of a Yak beneath a mountain range with the text "Sherpa".`enter code here](https://raw.githubusercontent.com/mattmallencode/crm/main/static/sherpa_logo.png)
<br>  
Oliver Linger, 120444372<br>  
Matt Mallen, 120355103<br>  
Eimantas Pusinskas, 120312336<br>  
Aria Shahi, 119522223
## Table of Contents
 - [Table of Contents](#table-of-contents) 
 - [Introduction](#introduction)  
 - [Project Specification](#project-specification)
	 - [User Stories](#user-stories) 
		 - [Team Invitation Creation](#team-invitation-creation)
		 - [Team Invitation Acceptance](#team-invitation-acceptance)
		 - [View contacts](#view-contacts)
		 - [Add contacts](#add-contacts)
		 - [Edit contacts](#edit-contacts)
		 - [Remove contacts](#remove-contacts)
		 - [User Logout](#user-logout)
		 - [View user profile](#view-user-profile)
		 - [Leave Team](#leave-a-team)
		 - [Assign Contact](#assign-a-contact)
		 - [View Team](#view-a-team)
		 - [View Assigned Contacts](#view-assigned-contacts)
		 - [View Unassigned Contacts](#view-unassigned-contacts)
		 - [ View 25 Contacts per page](#view-25-contacts-per-page)
		 - [Search For Contacts](#search-for-contacts)
		 - [Sort Contacts](#sort-contacts)
		 - [Filter Contacts](#filter-contacts)
		 - [Post notes](#post-notes)
	 - [Requirements](#requirements)
		 - [User Registration](#user-registration)
		 - [User Authentication](#user-authentication)
		 - [Team Creation](#team-creation)
		 - [Team Invitation Generation and Delivery](#team-invitation-generation-and-delivery)
		 - [Accepting team invitation](#accepting-team-invitation)
		 - [Addition Of Contacts To Users Contact Page](#addition-of-contacts-to-users-contact-page)
		 - [Addition Of Notes Implementation](#addition-of-notes-implementation)
 - [Design](#design)
	 - [Data Models](#data-models)
		 - [Users](#users)
		 - [Teams](#teams)
		 - [Invites](#invites)
		 - [Contacts](#contacts)
 - [Implementation](#implementation)
	 - [Underlying Technologies](#underlying-technologies)
	 - [App Structure](#app-structure)
	 - [User Registration and Authentication](#user-registration-and-authentication)
	 - [Creating Teams](#creating-teams)
	 - [Sending and Accepting Team Invites](#sending-and-accepting-team-invites)
	 - [Addition Of Contacts To Users Contact Page](#addition-of-contacts-to-users-contact-page)
	 - [Addition Of Notes](#addition-of-notes)
- [Testing](#testing)
	- [ Test Landing Page](#test-landing-page)
	- [ Test User](#test-user)
	- [ Test Invites](#test-invites)
	- [ Test Contacts](#test-contacts)
	- [  Test Teams](#test-teams)
## Introduction
This document outlines the design and implementation of Sherpa, a free and open-source Customer Relationship Management System (CRMS). A CRMS helps businesses drive sales, track customer interactions, and provide quality service. This is achieved by storing the data of existing and potential customers in a central database that can be accessed and managed by anyone within the organization with appropriate permissions.

This implementation can be used by multiple businesses i.e. users create "teams" and invite other users to join their team. However, it could easily be modified to be used by a single business by removing the team creation endpoint.
## Project Specification
### User Stories
####  Team Invitation Creation
*User Story ID: 1*<br>
As a business owner / manager, I want to invite other users to join my Sherpa team so that they can get access to our CRM resources.
#### Team Invitation Acceptance
*User Story ID: 2*<br>
As a business employee, I want to accept an invitation to join my employer's Sherpa team to get access to their CRM resources.

#### View Contacts
*User Story ID: 3*<br>
As a Sherpa user, I want to view all my team's contacts.
#### Add Contacts
*User Story ID: 4*<br>
As a Sherpa user, I want to add contacts to my contact list.
#### Edit Contacts
*User Story ID: 5*<br>
As a Sherpa user, I want to edit one of my team's contacts i.e. change various details like a phone number.
#### Remove Contacts
*User Story ID: 6*<br>
As a Sherpa user, I want to remove one of my team's contacts.
#### User Logout
*User Story ID: 7*<br>
As a Sherpa user, I want to log out of my account.
#### View User Profile
*User Story ID: 8*<br>
As a Sherpa user, I want to view my personal profile.
#### Leave Team
*User Story ID:  9*<br>
As a Sherpa user, I want to leave my team.
#### Assign Contact
*User Story ID:  10*<br>
As a Sherpa team owner/admin I want to assign a contact to a member of my team.
#### View Team
*User Story ID:  11*<br>
As a Sherpa user I want to view my team i.e. the list of team members.
#### View Assigned Contacts
*User Story ID:  12*<br>
As a Sherpa user I want to view the contacts that have been assigned to me.
#### View Unassigned Contacts
*User Story ID:  13*<br>
As a Sherpa user I want to view the contacts that have yet to be assigned to a member of my team.
#### Search For Contacts
*User Story ID:  14*<br>
As a Sherpa user I want to search for a specific contact using a search bar.
#### Sort Contacts 
*User Story ID:  15*<br>
As a Sherpa user I want to sort my team's contacts by email, phone number, etc.
#### Post Notes
*User Story ID:  16*<br>
As a Sherpa user, I want to add a note to a contact's page.
#### Remove notes
*User Story ID:  17*<br>
As a Sherpa user, I want to remove a note on a contact's page.
### Requirements
#### User Registration
*Requirement ID: 1*<br>  
*Satisfies User Story: 1, 2, 7

A user must be able to register an account with Sherpa's database by providing a valid email and password combination. This will then enable them to authenticate themselves. 
####  User Authentication
*Requirement ID: 2*<br>  
*Satisfies User Story: 1, 2*

Before accessing Sherpa services, a user must prove who they are. They can do this by providing the email and password they previously used to register. This will then be compared to Sherpa's database, if they provide matching credentials they will be considered authenticated for all subsequent requests for their session.
#### Team Creation
*Requirement ID: 3*<br>  
*Satisfies User Story: 1, 2*

In order to do anything meaningful with Sherpa (beyond creating an account and proving their identity) a user must be a member of a team. In order for there to be teams to join, users must be able to create them. If a user is not already a member of a team they can register one with Sherpa's database by providing the name of their organization. 
####  Team Invitation Generation and Delivery
*Requirement ID: 4*<br>  
*Satisfies User Story: 1, 2*

An owner or administrator of a team must be able to invite another user to join their team. This can be achieved by providing the email of the person they wish to invite and Sherpa will send them an invitation link on their behalf via email.
####  Accepting Team Invitation
*Requirement ID: 5*<br>  
*Satisfies User Story: 2*
A user must be able to accept an invitation to a team. They can achieve this by clicking the invitation link they received in their email and then logging in. A user may only accept the invitation if they're not already a member of a team and log in using the same email the invitation was sent to.
#### Addition Of Contacts
*Requirement ID: 6*<br>  
*Satisfies User Story: 4, 5, 6, 12, 13, 14, 15, 16, 17, 18*
A user must be able to add contacts to their contact list. This is completed by logging in and navigating to the home page.  On the home page go to your contacts page. Then click on the add contact button. Once you have added a contact you can remove a contact, send a contact, or edit a contact. Once you have added a contact you can search contacts, filter, and sort them. If no contacts are present the above user stories cannot take place. Posting notes can only be achieved after adding a contact.
#### Addition Of Notes 
*Requirement ID: 7*<br>
A User must have previously added a post to be able to view and remove previous notes. This can be completed by adding a contact. Once a contact has been added it is possible for you to post notes that your assigned contacts can view. Adding this allows you to remove notes as well as view them.

*Satisfies User Story: *
## Design
### Data Models
#### Users
The following table describes the data model used for "user" entities i.e. user accounts.

*Table:  1*
| email | password_hash |team_id|owner_status|admin_status
|:--:|:--:|:--:|:--:|:--:|
| Primary Key, String |String  |Integer|Boolean|Boolean

Users use a unique email along with a password to authenticate themselves. The team_id is the team whose CRM resources the user has access to (if any), and the two boolean values indicate whether they're an owner and/or admin.
#### Teams
The following table describes the data model used for "team" entities i.e. groups of users with access to the same CRM resources.

*Table:  2*
| team_id | name |
|:--:|:--:|
| Primary Key, Integer, Auto Increment |String|

The team_id is unique to each team and auto increments from 0. The name is the name decided by the team owner upon creation.
#### Invites
The following table describes the data model used for "invite" entities i.e. invitations to users to join a given team.

*Table:  3*
| invite_id | team_id |
|:--:|:--:|
| Primary Key, String |Integer|

The invite_id consists of the email being invited, the team_id the invitation is for. Along with some strong pseudo random numbers for security. The team_id is the id of the team the user is being invited to.
#### Contacts
The following table describes the data structure of the contacts page. Each contact has a name, email, phone number, contact owner, company, and status.
*Table: 4*
| contact_id | team_id | name | email | phone number | contact owner | company | status |
 :--------------: | :--: | :--: | :--: | :------: | :------: | :--: | :--: |
| Primary Key, String | Integer | String | String | Integer | String | String | String |

The contact_id is the primary key for this table, Each parameter needs to pass before a contact. 
Along with the contact_id each user will have a tema_id that associates them with a team. They will also have their name, email, phone number, contact owner, company, and status.

## Implementation
### Underlying Technologies
The following details our team's technology stack and gives context to the implementation chapter i.e. please assume that all implementation details rely on the use of the relevant technologies listed here.

 - **Programming Language:** Python
 - **Database Management System:** MySQL
 - **Web Framework:** Flask
 - **Virtual Environments:** Python-dotenv
 - **Object-Relational Mapper (ORM):** Flask-SQLAlchemy
 - **SMTP Library:** Flask-Mail
 - **Form Rendering & Validation:** WTForms
 - **User Authentication:** Werkzeug
 - **URL Token Generation:**  Python's Secrets module
 - **Cloud Orchestration**: Amazon Web Services (AWS) Elastic Beanstalk
 - **Application Server Hosting**: AWS EC2
 - **Database Server Hosting**: AWS RDS

### App Structure

 - Sherpa is a Flask application and is made up of various "endpoints" / routes that users can send  requests to. 
 - All Sherpa endpoints (except /login and /signup) are protected by an "@login_required" wrapper. This is just a Python decorator that calls a function to reject the user's request if they haven't been authenticated. They're redirected to the login page and once they're authenticated they're redirected back to the protected endpoint.
 - Database and SMTP access is facilitated by environment variables specified in a .env file. 
 - All database interactions occur through the use of SQLAlchemy data "models". These are outlined in the Design chapter and are essentially Pythonic descriptions of MySQL tables.

### User Registration and Authentication

*Implementation of requirements: 1, 2*

The following flow chart details the sign up process flow for a new Sherpa user. 


![Flow chart detailing the signup process flow for a new user.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Sign%20Up.png)
<br>*Figure: 1*

*Endpoint: /signup*

 - The user must submit a valid response to the signup form i.e. valid email, password confirmation etc. 
 - The user's email must also not be already registered (SQL query for submitted email). 
 - If either of the above checks fail the user is returned to the form and informed of the issue. 
 - Once the user submits a valid form response with a unique email, the back-end will generate a hashed version of their plain text password. Werkzeug uses pbkdf2 to generate a SHA-256 hash along with a salt unique to each user, thus preventing the passwords from being brute forced. 
 - Finally, the users details and the hashed version of their password are added to an instance of the Users data model and this is inserted into the database.

The following flow chart details the login process flow for an existing Sherpa user.

![Flow chart detailing the signup process flow for a new user.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Log%20In.png)
<br>*Figure: 2*

*Endpoint: /login*

 - The user must submit a valid response to the signup form i.e. required inputs etc. 
 - The user's email must exist in the database i.e. they're registered and they must authenticate themselves. This is achieved by generating a hash using the salt specific to the user and the plain-text password they provided as form input. If it matches the password hash for that email in the database the user is then authenticated.
 - If either of the above checks fail the user is returned to the form and informed of the issue. 
 - So that the user does not need to use password authenticated for every request a cookie is generated that they can present in lieu of a password for the remainder of the session. This cookie is signed using a strong pseudo random secret key to prevent cookie theft and forgery.
 - Then the user is redirected to the home page or to the endpoint they had attempted to visit prior to authentication.
### Creating Teams

*Implementation of requirement: 3*

The following flow chart details the process flow for creating a Sherpa team.

![Flow chart detailing the team creation process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Team%20Creation.png)
<br>*Figure: 3*

*Endpoint: /create_team*

 - The user must submit a valid response to the signup form i.e. include a team name.
 - The user can't be a member of a team (SQL query to check that their team_id is NULL).
 - If either of the above checks fail the user is returned to the form and informed of the issue. 
 - If the endpoint gets a valid response, the form data is added to an instance of the Teams data model and this is inserted into the database. This team will be assigned a unique id as the team_id column is an auto incrementing primary key.
 - The user's team_id is then updated based on the team_id returned from the database commit and this update is committed to the database as well.
 - Then the user is redirected to the home page.
 
### Sending and Accepting Team Invites

*Implementation of requirement: 4, 5*

The following flow chart details the process flow for inviting another user to a Sherpa team.
![Flow chart detailing the team invitation process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Invite.png)
<br>*Figure: 4*

*Endpoint: /invite*

 - The user must submit a valid response to the invite form i.e. valid email, required input etc.
 - The user issuing the invite must be a member of a team and one of that team's admins.
 - The invitee must not be a member of that team already. 
- If the endpoint receives a valid response, an invite_id is generated. The format is as follows: *[invitee_email]_[team_id]__[secure_token]*.  The secure token consists of 16 cryptographically secure characters and is generated using the token_urlsafe method of the secrets module and is necessary to prevent fraudulent invitation generation.
- Once the invite_id is generated it is added to an instance of the Invites data model along with the team_id the invitation is for. This is then inserted into the invites table in the database.
- The user is then returned to the form and informed of the successful invitation.

The following flow chart details the process flow for accepting a Sherpa invitation. It is a modified version of the login flow: see Figure 2.

![Flow chart detailing the team invitation acceptance process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Invite%20Accept.png)
<br>*Figure: 5*

*Endpoint: /invite/<invite_id>*

 - User must submit a valid form submission and be authenticated (as per the normal login flow).
 - If the user doesn't pass an invite_id to the endpoint, the normal login flow resumes and concludes.
 - If an invite_id is passed, it must be validated. First a lookup is done on the invites table to see if that invitation exists, if it does then the user's data is checked to see if they're in fact not a member of a team (a user can't accept an invitation until they've left their current team). Finally, the login email is compared to the email specified in the id, the user can't accept an invitation unless they authenticate themselves using the email specified.
 - If the invitation and user details are validated as above, the user's team id is set to the team_id specified in the invitation and the invitation is removed from the table. Then the normal login flow resumes and concludes.
 
### Addition Of Contacts To Users Contact Page
*Implementation of requirement: 6*
The following flow chart details the process for adding contacts to a Sherpa users contact list.
- The user must submit a valid form for login and be authenticated. As seen above the same process applies to the validation of users. Once a Sherpa user is logged in and authenticated they must click on the contacts button. This will take them to the contacts page where they can add a contact. Once all necessary parameters have been passed a contact is created and multiple user stories can now occur. Such as 4, 5, 6, 12, 13, 14, 15, 16, and 17. All these stories require contacts to exist within the database for them to be feasible.
- 
*Implementation of requirement: 6*
![Flow chart detailing the adding of contacts](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/contacts_page.JPG)
 <br>*Figure: 6*
 
*Endpoint: /contacts*

- You input contact details, If the form validates then the database is queried to see if there is an existing contact, otherwise the details are discarded and the form is reloaded. If not then the contact is added to the database and added to the Sherpa user's contact list. Once the contact has been added then the form is reloaded allowing you to execute a range of operations of your contact list. Such as deleting, filtering, and viewing assigned and unassigned contacts,  
### Addition Of Notes Implementation
- *Implementation of requirement: 18*
*Endpoint: /contacts*
The following flow chart details the process of adding a note on the contacts page. 
![Flow chart detailing the addition of notes](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/adding_note.PNG)
<br>*Figure: 7*

*Endpoints: contact/101010010%40mail.com_123/activity*

- Once a user has navigated to the contacts page. Add a contact if one does not exist. Once one exists click on the edit button. This will take you to a different endpoint "contact/101010010%40mail.com_123/notes" where you can see previous notes as well as add a note. Once a note is written and the add button is pressed. It is timestamped and then committed.   
Using turbo that specific section of the page is updated ( the activity box on the page ).

## Testing 
### Test Landing Page
*Test case: 1*<br>

- Using Pytest the landing page was tested. Using client make a get request to the url of the page, "/login".  Store the recieved data from that get request in the html variable. Using pytest "assert" statement, assert that the landing status of the page is "200". It means the page was served without issues.
### Test User
*Test case: 2*<br>

- Using Pytest a fake instance of a user and dummy information was passed into it. Then using assert statements check that the passed information was correctly received by the Users class.
### Test Invites
*Test case: 3*<br>
- Using pytest a fake invite was created by calling the invite class and using the assert statement we can find out whether the class behaves as it should.
### Test Contacts
*Test case: 4*<br>

- Using Pytest create a fake instance of a contact being added. Check that all contact details are received properly. 
### Test Teams 
*Test case: 5*<br>
-  Using Pytest a fake instance of  a team was created using the Teams class. Parameters for a team creation were passed and the behavior was checked using an assert statement. 
