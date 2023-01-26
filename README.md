# Sherpa: A Free and Open-Source CRM
![Sherpa logo: a picture of a Yak beneath a mountain range with the text "Sherpa".`enter code here](https://raw.githubusercontent.com/mattmallencode/crm/main/static/sherpa_logo.png)
<br>  
Oliver Linger, 120444372
<br>  
Matt Mallen, 120355103
<br>  
Eimantas Pusinskas, 120312336
<br>  
Aria Shahi, 119522223
## Table of Contents
 - [Table of Contents](#specification) 
 - [Introduction](#introduction)  
 - [Project Specification](#project-specification)
	 - [User Stories](#user-stories) 
		 - [Team Invitation Creation](#team-invitation-creation)
		 - [Team Invitation Acceptance](#team-invitation-acceptance)
	 - [Requirements](#requirements)
		 - [User Registration](#user-registration)
		 - [User Authentication](#user-authentication)
		 - [Team Creation](#team-creation)
		 - [Team Invitation Generation and Delivery](#team-invitation-generation-and-delivery)
		 - [Team Invitation Acceptance](#team-invitation-acceptance)
 - [Design](#design)
	 - [Data Models](#data-models)
		 - [Users](#users)
		 - [Teams](#teams)
		 - [Invites](#invites)
 - [Implementation](#implementation)
	 - [Underlying Technologies](#underlying-technologies)
	 - [App Structure](#app-structure)
	 - [User Registration and Authentication](#user-registration-and-authentication)
	 - [Creating Teams](#creating-teams)
	 - [Sending and Accepting Team Invites](#sending-and-accepting-team-invites)
## Introduction
This document outlines the design and implementation of Sherpa, a free and open-source Customer Relationship Management System (CRMS). A CRMS helps businesses drive sales, track customer interactions, and provide quality service. This is achieved by storing the data of existing and potential customers in a central database that can be accessed and managed by anyone within the organisation with appropriate permissions.

This implementation can be used by multiple businesses i.e. users create "teams" and invite other users to join their team. However, it could easily be modified to be used by a single business by removing the team creation endpoint.
## Project Specification
### User Stories
####  Team Invitation Creation
*User Story ID: 1*

As a business owner / manager I want to invite other users to join my Sherpa team so that they can get access to our CRM resources.
#### Team Invitation Acceptance
*User Story ID: 2*

As a business employee I want to accept an invitation to join my employer's Sherpa team to get access to their CRM resources.
### Requirements
#### User Registration
*Requirement ID: 1*
*Satisfies User Story: 1, 2*

A user must be able to register an account with Sherpa's database by providing a valid email and password combination. This will then enable them to authenticate themselves.
####  User Authentication
*Requirement ID: 2*
*Satisfies User Story: 1, 2*

Before accessing Sherpa services, a user must prove who they are. They can do this by providing the email and password they previously used to register. This will then be compared to Sherpa's database, if they provide matching credentials they will be considered authenticated for all subsequent requests for their session.
#### Team Creation
*Requirement ID: 3*
*Satisfies User Story: 1, 2*

In order to do anything meaningful with Sherpa (beyond creating an account and proving their identity) a user must be a member of a team. In order for there to be teams to join, users must be able to create them. If a user is not already a member of a team they can register one with Sherpa's database by providing the name of their organisation. 
####  Team Invitation Generation and Delivery
*Requirement ID: 4*
*Satisfies User Story: 1, 2*

An owner or administrator of a team must be able to invite another user to join their team. This can be achieved by providing the email of the person they wish to invite and Sherpa will send them an invitation link on their behalf via email.
####  Team Invitation Acceptance
*Requirement ID: 5*
*Satisfies User Story: 2*

A user must be able to accept an invitation to a team. They can achieve this by clicking the invitation link they received in their email and then logging in. A user may only accept the invitation if they're not already a member of a team and log in using the same email the invitation was sent to.

## Design
### Data Models
#### Users
The following table describes the data model used for "user" entities i.e. user accounts.

*Table:  1*
| email | password_hash |team_id|owner_status|admin_status
|:--:|:--:|:--:|:--:|:--:|
| Primary Key, String |String  |Integer|Boolean|Boolean

Users use a unique email along with a password to authenticate themselves. The team_id is the team whose CRM resources the user has access to (if any), and the two boolean values indicates whether they're an owner and/or admin 
#### Teams
The following table describes the data model used for "team" entities i.e. groups of users with access to the same CRM resources

*Table:  2*
| team_id | name |
|:--:|:--:|
| Primary Key, Integer, Auto Increment |String|

The team_id is unique to each team and auto increments from 0. The name is the the name decided by the team owner upon creation.
#### Invites
The following table describes the data model used for "invite" entities i.e. invitations to users to join a given team.

*Table:  3*
| invite_id | team_id |
|:--:|:--:|
| Primary Key, String |Integer|

The invite_id consists of the email being invited, the team_id the invitation is for along with some strong pseudo random numbers for security. The team_id is the id of the team the user is being invited to.
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
 - Database and SMTP access is facilitated by environment variables specified in a .env file. 
 - All database interactions occur through the use of SQLAlchemy data "models". These are outlined in the Design chapter and are essentially Pythonic descriptions of MySQL tables.

### User Registration and Authentication

*Implementation of requirements: 1, 2*

The following flow chart details the sign up process flow for a new Sherpa user. 


![Flow chart detailing the signup process flow for a new user.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Sign%20Up.png)
*Figure: 1*

*Endpoint: /signup*

 - The user must submit a valid response to the signup form i.e. valid email, password confirmation etc. 
 - The user's email must also not be already registered (SQL query for submitted email). 
 - If either of the above checks fail the user is returned to the form and informed of the issue. 
 - Once the user submits a valid form response with a unique email, the back-end will generate a hashed version of their plain text password. Werkzeug uses pbkdf2 to generate a SHA-256 hash along with a salt unique to each user, thus preventing the passwords from being brute forced. 
 - Finally, the users details and the hashed version of their password are added to an instance of the Users data model and this is inserted into the database.

The following flow chart details the login process flow for an existing Sherpa user.

![Flow chart detailing the signup process flow for a new user.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Log%20In.png)
*Figure: 2*

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
*Figure: 3*

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
*Figure: 4*

*Endpoint: /invite*

 - The user must submit a valid response to the invite form i.e. valid email, required input etc.
 - The user issuing the invite must be a member of a team and one of that team's admins.
 - The invitee must not be a member of that team already. 
- If the endpoint receives a valid response, an invite_id is generated. The format is as follows: *[invitee_email]_[team_id]__[secure_token]*.  The secure token consists of 16 cryptographically secure characters and is generated using the token_urlsafe method of the secrets module and is necessary to prevent fraudulent invitation generation.
- Once the invite_id is generated it is added to an instance of the Invites data model along with the team_id the invitation is for. This is then inserted into the invites table in the database.
- The user is then returned to the form and informed of the successful invitation.

The following flow chart details the process flow for accepting a Sherpa invitation. It is a modified version of the login flow: see Figure 2.

![Flow chart detailing the team invitation acceptance process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Invite%20Accept.png)

*Endpoint: /invite/<invite_id>*

 - User must submit a valid form submission and be authenticated (as per the normal login flow).
 - If the user doesn't pass an invite_id to the endpoint, the normal login flow resumes and concludes.
 - If an invite_id is passed, it must be validated. First a lookup is done on the invites table to see if that invitation exists, if it does then the user's data is checked to see if they're in fact not a member of a team (a user can't accept an invitation until they've left their current team). Finally, the login email is compared to the email specified in the id, the user can't accept an invitation unless they authenticate themselves using the email specified.
 - If the invitation and user details are validated as above, the user's team id is set to the team_id specified in the invitation and the invitation is removed from the table. Then the normal login flow resumes and concludes.
