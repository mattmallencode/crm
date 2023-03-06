# Sherpa: A Free and Open-Source CRM
﻿
![Sherpa logo: a picture of a Yak beneath a mountain range with the text "Sherpa"](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/sherpa_logo.png)
<br>
Oliver Linger, 120444372

Matt Mallen, 120355103

Eimantas Pusinskas, 120312336

Aria Shahi, 119522223

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Some CRM Terms](#some-crm-terms)
- [What Sherpa Can Do](#what-sherpa-can-do)
- [How Sherpa Adds Value](#how-sherpa-adds-value)
- [Project Specification](#project-specification)
  - [User Stories](#user-stories)
    - [Team Invitation Creation](#team-invitation-creation)
    - [Team Invitation Acceptance](#team-invitation-acceptance)
    - [View Contacts](#view-contacts)
    - [Add Contacts](#add-contacts)
    - [Edit Contacts](#edit-contacts)
    - [Remove Contacts](#remove-contacts)
    - [View User Profile](#view-user-profile)
    - [User Logout](#user-logout)
    - [View Team](#view-team)
    - [Leave Team](#leave-team)
    - [Assign Contact](#assign-contact)
    - [View Assigned Contacts](#view-assigned-contacts)
    - [View Unassigned Contacts](#view-unassigned-contacts)
    - [ View Contacts In Pages](#view-contacts-in-pages)
    - [Search For Contacts](#search-for-contacts)
    - [Sort Contacts](#sort-contacts)
    - [View Contact Activity](#view-contact-activity)
    - [Post Notes](#post-notes)
    - [Remove Notes](#remove-notes)
    - [Send Email](#send-email)
    - [View Emails](#view-emails)
    - [Reply to Email](#reply-to-email)
    - [Set a Task](#set-a-task)
    - [View Tasks](#view-tasks)
    - [Schedule Meeting](#schedule-meeting)
    - [View Meetings](#view-meetings)
    - [Create Deal](#create-deal)
    - [View Deals](#view-deals)
    - [Edit Deal](#edit-deal)
    - [Close Deal](#close-deal)
    - [Search Deals](#search-deals)
    - [Sort Deals](#sort-deals)
     - [Assign Deal](#assign-deal)
    - [View Assigned Deals](#view-assigned-deals)
  - [Requirements](#requirements)
    - [User Registration](#user-registration)
    - [User Authentication](#user-authentication)
    - [Team Creation](#team-creation)
    - [Team Invitation Generation and Delivery](#team-invitation-generation-and-delivery)
    - [Accepting Team Invitation](#accepting-team-invitation)
    - [Database Create Read Update and Delete CRUD](#database-create-read-update-and-delete-crud)
    - [User Profile and Logout](#user-profile-and-logout)
    - [Database Viewing](#database-viewing)
    - [Database Filtering](#database-filtering)
    - [Database Searching](#database-searching)
    - [Database Sorting](#database-sorting)
- [Design](#design)
  - [Data Models](#data-models)
    - [Users](#users)
    - [Teams](#teams)
    - [Invites](#invites)
    - [Contacts](#contacts)
    - [Notes](#notes)
- [Implementation](#implementation)
  - [Underlying Technologies](#underlying-technologies)
  - [App Structure](#app-structure)
  - [User Registration and Authentication](#user-registration-and-authentication)
  - [Creating Teams](#creating-teams)
  - [Sending and Accepting Team Invites](#sending-and-accepting-team-invites)
  - [Contact Information Management](#contact-information-management)
  - [Google Account Integration](#google-account-integration)
  - [Contact Relationship Management](#contact-relationship-management)
  - [Deal Management](#deal-management)
- [Testing](#testing)
  - [Test Landing Page](#test-landing-page)
  - [Test User](#test-user)
  - [Test Invites](#test-invites)
  - [Test Contacts](#test-contacts)
  - [Test Teams](#test-teams)
 - [Project Reflection](#project-reflection)
	 - [Diffculties](#difficulties)
	 - [Engineering Tradeoffs](#engineering-tradeoffs)

## Introduction

This document outlines the design and implementation of Sherpa, a free and open-source Customer Relationship Management System (CRMS). A CRMS helps businesses drive sales, track customer interactions, and provide quality service. This is achieved by storing the data of existing and potential customers in a central database that can be accessed and managed by anyone within the organization with appropriate permissions.

This implementation can be used by multiple businesses i.e. users create "teams" and invite other users to join their team. However, it could easily be modified to be used by a single business by removing the team creation endpoint.

## Some CRM Terms

The following are definitions of important terms in CRM software. Please familiarise yourself with them to ease your understanding of this document.

+ __Contacts__: are potential or existing customers of a business.
+ __Deals__: are potential or existing sales contract between a business and  a customer. Deals can be:
	+  **open** i.e. no contract has been signed / no money has been exchanged, or
	+ **closed** i.e. the business has made the sale / money has been credited to it.
+ **Deal Goal**: The amount of money a business aims to earn when initially pursuing a deal with a customer.
+ **Deal Closed Amount**: The actual amount of money a business earned after closing a deal with a customer.

## What Sherpa Can Do

Sherpa has the following features:

+ __User-Friendly Interface__ - Sherpa has friendly and accessible interface, meaning any member of an organisation can quickly pick up Sherpa in their daily workflow, leading to increased productivity and enhanced client satisfaction.
+ __Contact Information Management__ - Sherpa provides an easy to use dashboard for managing contact information where team members can add, view, and edit information e.g. email addresses, phone numbers, statuses etc. Contact information can also be searched, sorted, and filtered so that one can easily find data of interest.
+ __Contact Relationship Management__ - Users can communicate with contacts using our integrated Google API features where you may send/receive emails, set tasks in your calendar, and schedule online meetings with your contacts all from within the application. Tasks and meetings also appear in your Google calendar as well as that of the contact's. Furthermore, Sherpa allows one to leave "notes" for colleagues and informs one of the "activity" between team members and contacts to facilitate collaboration.
+ __Deal Management__ - Sherpa provides an easy to use dashboard for managing deal information where team members can add, view and edit deals e.g. marking them as closed, setting the goal of the deal, etc. Deal information can also be searched, sorted, and filtered so that one can easily find data of interest.
+ __Data Analysis__ - Sherpa provides an analytics dashboard where you can get an insight into your organisation's sale performance. Analytics regarding your companies recent open/closed deals are displayed, along with a forecast for future deals and other data.

## How Sherpa Adds Value

One may wonder if rather than using a CRM like Sherpa if they could instead manage their relationships with customers in a more ad hoc manner e.g. just use an email service like Google on its own in conjunction with conferencing software.  However, the real value in a system like this is how all of the pieces link up together. 

Firstly, with Sherpa, **your sales team always has a cohesive view**. For example, if contact's email changes, it changes for everyone on your team.
    
Secondly, Sherpa **makes management easier**. A manager can assign a member of their sales team to chase down a specific customer, and that sales person knows immediately after logging into the application which contacts they are supposed to be handling (rather than having to keep up with endless Email/MS Teams / Slack threads to keep pace with management).
    

Lastly, **everything is traceable** with Sherpa. Not just in terms of analytics but also in terms of customer interactions. Everyone on a team can see which customers have been “left on the back burner” so to speak based on when the last time they were emailed for example.

To put it simply, it would be very painful to set up a cohesive flow in terms of managing your relationship with customers if you were to bootstrap this yourself with several unconnected applications. Sherpa makes it easy.

## Project Specification

### User Stories

#### Team Invitation Creation

*User Story ID: 1*

As a business owner / manager, I want to invite other users to join my Sherpa team so that they can get access to our CRM resources.

#### Team Invitation Acceptance

*User Story ID: 2*

As a business employee, I want to accept an invitation to join my employer's Sherpa team to get access to their CRM resources.

#### View Contacts

*User Story ID: 3*

As a Sherpa user, I want to view all my team's contacts.

#### Add Contacts

*User Story ID: 4*

As a Sherpa user, I want to add a contact to my team's contacts list.

#### Edit Contacts

*User Story ID: 5*

As a Sherpa user, I want to edit one of my team's contacts i.e. change various details like a phone number.

#### Remove Contacts

*User Story ID: 6*

As a Sherpa user, I want to remove one of my team's contacts.

#### View User Profile

*User Story ID: 7*

As a Sherpa user, I want to view my profile.

#### User Logout

*User Story ID: 8*

As a Sherpa user, I want to log out of my account.

#### View Team

*User Story ID:  9*

As a Sherpa user I want to view my team i.e. the list of team members.

#### Leave Team

*User Story ID:  10*

As a Sherpa user, I want to leave my team.

#### View Contacts

*User Story ID:  11*

As a Sherpa user I want to view my team's contacts.

#### Assign Contact

*User Story ID:  12

As a Sherpa team owner/admin I want to assign a contact to a member of my team.

#### View Assigned Contacts

*User Story ID:  13*

As a Sherpa user I want to view the contacts that have been assigned to me.

#### View Unassigned Contacts

*User Story ID:  14*

As a Sherpa user I want to view the contacts that have yet to be assigned to a member of my team.

#### Search For Contacts

*User Story ID:  15*

As a Sherpa user I want to search for a specific contact(s) using a search bar.

#### Sort Contacts

*User Story ID:  16*

As a Sherpa user I want to sort my team's contacts by email, phone number, etc.

#### View Contact Activity

*User Story ID:  17*

As a Sherpa user I want to view all team activity for a contact e.g. notes, emails, meetings etc.

#### Post Notes

*User Story ID:  18*

As a Sherpa user, I want to add a note to a contact's page.

#### Remove notes

*User Story ID:  19*

As a Sherpa user, I want to remove a note on a contact's page.

#### Send Email 

*User Story ID: 20*

As a Sherpa user, I want to send an email to a contact.

#### View Emails 

*User Story ID: 21*

As a Sherpa user, I want to view my emails sent and received to/from a contact.

#### Reply to Email 

*User Story ID: 22*

As a Sherpa user, I want to reply to an email from a contact.

#### Set a Task

*User Story ID: 23*

As a Sherpa user, I want to create a task in relation to a contact.

#### View Tasks
*User Story ID: 24*

As a Sherpa user, I want to view all tasks in relation to a contact.

#### Schedule Meeting
*User Story ID: 25*

As a Sherpa user, I want to schedule a meeting with a contact which is integrated with my Google calendar.

#### View Meetings
*User Story ID: 26*

As a Sherpa user, I want to view my scheduled meetings with a contact.

#### Create Deal
*User Story ID: 27*

As a Sherpa user, I want to create a deal .

#### View Deals
*User Story ID: 28*

As a Sherpa user, I want to view my team's deals.

#### Edit Deal
*User Story ID: 29*

As a Sherpa user, I want to edit a deal.

#### Close Deal
*User Story ID: 30*

As a Sherpa user, I want to close a deal.

#### Search Deals
*User Story ID: 31*

As a Sherpa user, I want to search my team's deals.

#### Sort Deals
*User Story ID: 32*

As a Sherpa user, I want to sort my team's deals.

#### Assign Deal

*User Story ID:  33

As a Sherpa team owner/admin I want to assign a deal to a member of my team.

#### View Assigned Deals

*User Story ID:  34*

As a Sherpa user I want to view the deals that have been assigned to me.

### Requirements

#### User Registration

*Requirement ID: 1*

*Satisfies User Stories: 1, 2, 7

A user must be able to register an account with Sherpa's database by providing a valid email and password combination. This will then enable them to authenticate themselves.

#### User Authentication

*Requirement ID: 2*

*Satisfies User Stories: 1, 2*

Before accessing Sherpa services, a user must prove who they are. They can do this by providing the email and password they previously used to register. This will then be compared to Sherpa's database, if they provide matching credentials they will be considered authenticated for all subsequent requests for their session.

#### Team Creation

*Requirement ID: 3*

*Satisfies User Stories: 1, 2*

In order to do anything meaningful with Sherpa (beyond creating an account and proving their identity) a user must be a member of a team. In order for there to be teams to join, users must be able to create them. If a user is not already a member of a team they can register one with Sherpa's database by providing the name of their organization.

#### Team Invitation Generation and Delivery

*Requirement ID: 4*

*Satisfies User Stories: 1, 2*

An owner or administrator of a team must be able to invite another user to join their team. This can be achieved by providing the email of the person they wish to invite and Sherpa will send them an invitation link on their behalf via email.

#### Accepting Team Invitation

*Requirement ID: 5*

*Satisfies User Story: 2*

A user must be able to accept an invitation to a team. They can achieve this by clicking the invitation link they received in their email and then logging in. A user may only accept the invitation if they're not already a member of a team and log in using the same email the invitation was sent to.

#### Database Create, Read, Update, and Delete (CRUD)

*Requirement ID: 6*

*Satisfies User Stories: 3 - 6

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

A user must be able to interface with their team's databases and achieve all of the basic CRUD operations with their team's records by interacting with the web app i.e. forms and buttons, not SQL.

**For Contacts**

For create operations users must provide at least an email for the new contact (all other data is optional). For create and update operations user must provide a unique email address i.e. they can not update the email of an existing contact to match the email of another contact.

**For Deals**

For create operations users must provide at least a name and goal for the new deal (all other data is optional). For update operations, a user can not update a goal of a deal. If the user changes the deal stage to "closed" they must provide a closed amount, thereafter the deal stage and closed amount will not be able to be updated for that record.

#### User Profile and Logout

*Requirement ID: 7*

*Satisfies User Story: 7, 8*

A user must be able to view a profile page with their account information. Furthermore, they must be able to logout of their account, meaning their session (authentication cookies etc) will be cleared and they will have to use their username and password again if they wish to resume using the application.

#### View and Leave Teams

*Requirement ID: 7*

*Satisfies User Story: 9, 10*

A user must be able to view a page that lists all of the members of their team. On this page, they will be given the option to leave their team (this will also feature a "are you sure?" (or similar) checkbox.

#### Database Viewing

*Requirement ID: 8*

*Satisfies User Story: 11, 28*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Users must be able to view their team's contacts or deals. Since a business may have an enumerable number of customers and sales contracts, Sherpa can not serve all records on one page without hindering the user experience therefore records must be "chunked up" into "pages" (each page being a group of 25 records), with the user able to navigate records using the "next page" and "previous page" buttons.

#### Database Filtering

*Requirement ID: 9*

*Satisfies User Story: 12 - 14, 33-34*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Admins of a team must be able to assign a member of their team as an "owner" of a contact or deal. This will update the record's owner_id to the email of the new contact owner.

Users must then be able to filter for "my contacts", "my deals" etc, i.e. just display the records that have an owner_id equal to the user's email. Users should also be able to view "unassigned contacts" i.e. the contacts that have a NULL owner_id. There won't be an "unassigned deals" view.

#### Database Searching

*Requirement ID: 10*

*Satisfies User Story: 15, 31*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Users must be able to search their team's contacts or deals. Users should be able to search for a specific name, email, phone number etc and be served the records that match their search term.

#### Database Sorting

*Requirement ID: 11, 32*

*Satisfies User Story: 16*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

User must be able to sort their team's contacts or deals by email, phone number, etc. The app must support both ascending and descending sorting and for improved user experience this should behave as a "toggle" feature i.e. click a column header once and it'll be sorted in ascending order, click that same column header again and the order will be flipped.

## Design

### Data Models

This section describes the app's "data models". These represent the relational data of various entities in Sherpa e.g. users, and can ultimately be viewed as descriptions of SQL tables.

#### Users

The following table describes the data model used for "user" entities i.e. user accounts.

*Table 1: Users Data Model*
| email | password_hash | team_id | owner_status | admin_status | name |
| :-: | :-: | :-: | :-: | :-: | :-: |
| Primary Key, String | String | Integer | Boolean | Boolean | String |

+ email - email address of the user
+ password_hash - the users password stored as a hash value
+ team_id - the team associated with the user to which the user will have CRM access to
+ owner_status - indicates if user is an owner of their team
+ admin_status - indicates if user is an admin within their team
+ name - the real name of the user


#### Teams

The following table describes the data model used for "team" entities i.e. groups of users with access to the same CRM resources.

*Table 2: Teams Data Model*

| team_id | name |
| :-: | :-: |
| Primary Key, Integer | String |

+ team_id - auto-incremented integer which is used as the primary key to uniquely identify a team
+ name - name of the team


#### Invites
The following table describes the data model used for "invite" entities i.e. invitations to users to join a given team.

*Table 3: Invites Data Model*

| invite_id | team_id |
| :-: | :-: |
| Primary Key, String | Integer |

+ invite_id - "{invitee_email}_{team_id}_{secure_token}", used to uniquely identify invite.
+ team_id - the team to which the invitation applies for


#### Contacts
The following table describes the data model used for "contact" entities i.e. a contact of a given team.

*Table 4: Contacts Data Model*

| contact_id | team_id | name | email | phone number | contact owner | company | status |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Primary Key, String | Integer | String | String | Integer | String | String | String |

+ contact_id - "{email}_{team_id}", used to uniquely identify contact
+ team_id - secondary key used to associate a contact with a team
+ name - name of the contact
+ email - email address of the contact
+ phone_number - phone number of the contact
+ contact_owner - owner (team member) assigned to the contact
+ company - the company associated with the contact
+ status - the status of the relationship with the contact e.g. "New"


#### Notes

The following table describes the data model used for "note" objects i.e. notes added to a specific contact by a Sherpa user.

*Table 5: Notes Data Model*

| note_id | contact_id | note | author | date |
| :-: | :-: | :-: | :-: | :-: |
| Primary Key, Integer | String | String | String | String |

+ note_id - auto-incremented integer which is used as the primary key to uniquely identify a note
+ contact_id - secondary key which is used to correlate a note with a specific contact
+ note - the actual content of the note
+ author - author of the note
+ date - the date the note was written


#### Deals
The following table describes the data model used for "deal" objects i.e. deals with a contact which are assigned to a user.

*Table 6 : Deals Data Model*

| deal_id | team_id | name | stage | close_date | owner | amount | associated_contact | associated_company
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|Primary Key, Integer | Integer | String | String | Datetime | String | Integer | String | String |

+ deal_id - auto-incremented integer which is used as the primary key to uniquely identify a deal
+ team_id - secondary key which is used to correlate a deal with a specific team
+ name - the name given to the deal 
+ stage - the deal stage, used to track the progression of the deal 
+ close_date - the date the deal was closed, if it was closed. [Optional]
+ owner - the owner of the deal [Optional]
+ amount - value of the deal [Optional]
+ associated_contact - contact associated with this deal
+ associated_company - company associated with this deal

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

#### Operation of AWS Server

The diagram below depicts the operation of the application with the AWS server

![Chart detailing the operation of the application with AWS ](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/aws.png)

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

### Contact Information Management

*Implementation of requirement: 6*

*Endpoint: /contacts*
The following details the implementation of the contacts page where users are served with a dashboard from which they can manage all of their teams contacts. The contacts page serves two primary purposes; management and organization.

#### Management
+ Create Contact
	+ Users are served with a form to create a contact containing information regarding name, email, phone number, contact owner, company and status. Once the form is submitted a contact is created
+ View Contacts
	+ If there are existing contacts, all existing contacts with their respective information are displayed to the user as an interactive table
+ Edit Contacts
	+ Contacts are displayed as an interactive table where users can click on current contact information and replace with new information. Once "Edit" is clicked for a specific contact, then the edited info is updated in the database and the table is refreshed for the user to see the new updated version of their contacts list
+ Remove Contacts
	+ Users can remove a specific contact by clicking on "Remove" which will remove the contact from the team's database and update the users view of the contacts list

#### Organization
+ Search
	+ Users can use the search bar to search for a contact or specific data of a contact
+ Sort 
	+ Users can click on the column heading to sort the contacts according to the column heading e.g. sort by Company
+ Filter
	+ Users can filter the view of contacts using the filter tabs. e.g. user can filter view to only see the user's assigned contacts 


### Google Account Integration

*Implementation of requirement: 7*

Users must integrate their Google accounts with Sherpa to obtain a Google session token in order to avail of Sherpa's Google services such as Emails, Tasks and Meetings.
The following diagram details the process of integrating Google with a Sherpa account.

![Diagram detailing the retrieval of a Google session token. Image is sourced from  "https://developers.google.com/identity/protocols/oauth2"](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/google_auth.png)

Google accounts are authenticated using OAuth 2.0. More information about OAuth 2.0 can be found [here](https://developers.google.com/identity/protocols/oauth2).

###  Contact Relationship Management
*Implementation of Requirement: 8*

The following details the operation and implementation of the features that allow teams to manage relationships with their contacts within Sherpa. 

*Endpoint: /contact/\<contact_id>/\<activity>*

The parameters passed to the endpoint above determine the view of the contact page where a singular contact can be managed directly by a team member

- contact_id - the ID of the contact requested to be viewed more in depth
- activity - the feature requested e.g. emails, meetings. The default activity is a summary of all previous interactions with the contact in recent history   

If the activity requested is the Email, Meetings or Tasks features, then the user must have a Google session token in order to avail of these services. The following flowchart depicts the logic-flow of rendering these services

![Flow Chart detailing the flow of rendering activities on the contact page](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/crm_contact_activity.png)
<br>

*Endpoint: /contact/\<contact_id\>/__activity__*

- View Activity Log
	-  The user is presented with a log of previous interactions with the contact specified in the contact_id parameter. In this log, a brief overview of all Notes, Emails, Tasks and Meetings that have occurred with this contact is displayed ranging from most recent to oldest.


*Endpoint: /contact/\<contact_id\>/__notes__*

- Create Note
	- User is presented with a form containing a text box for a note. Once the form is submitted, this note is added to the database uniquely correlating the note to the contact specified in the contact_id parameter.
- View Notes
	- User is presented with a table of all notes added to the contact's record by the user and any members of the user's team
- Remove Note
	- User is able to click "Remove" on any note in order to remove this note from the contact's record


*Endpoint: /contact/\<contact_id\>/__emails__*

 - Sending Emails
	 - The user is presented with a form containing text boxes for the email subject and the main contents of the email. If the form is submitted and validated, the email is sent to the Sherpa Inbox of the contact specified in the contact_id parameter.
 - Viewing Emails
	 - A table of previous emails between the user and the contact specified in the contact_id parameter is displayed to the user.
 - Replying to Emails
	 - User has an option to reply to an email or to the most recent email in a thread of emails from the contact specified in contact_id by clicking on the "Reply" button, which pre-populates the Send Email Form with the subject as the subject of the thread. Once the user submits the form a reply is sent back to the contact in this selected thread.


*Endpoint: /contact/\<contact_id\>/__tasks__*

[To be completed once tasks feature is implemented]


*Endpoint: /contact/\<contact_id\>/__meetings__*

- Schedule a Meeting 
	- User is presented a form to schedule a Google meeting with the contact specified in the contact_id parameter. User can input a meeting title, description and start/end date of the meeting. Once the form is submitted, the meeting is scheduled and a meeting event is added to the Google Calendar's of both the user and the contact.
- View Meetings
	- User is presented with a table containing all scheduled meetings with the contact.


### Deal Management
*Implementation of Requirement: 9*

*Endpoint: /deals*
The following details the implementation of the deals page where users are served with a dashboard from which they can manage all of their teams deals. The deals page serves two primary purposes; management and organization.

#### Management
+ Create Deal
	+ Users are served with a form to create a deal containing information regarding deal name, stage, owner, close date, amount, associated contacts and associated companies. Once the form is submitted a deal is created
+ View Deals
	+ If there are existing deals, all existing deals with their respective information are displayed to the user as an interactive table
+ Edit Deals
	+ Deals are displayed as an interactive table where users can click on current deal information and replace with new information. Once "Edit" is clicked for a specific deal, then the edited info is updated in the database and the table is refreshed for the user to see the new updated version of the deals table
+ Close Deals
	+ Users using the "Deal Stage" dropdown menu can close a deal and also select a date for when the deal was closed using the "Close Date" dropdown calendar feature

#### Organization
+ Search
	+ Users can use the search bar to search for a deal or specific data within a deal
+ Sort 
	+ Users can click on the column heading to sort the deals according to the column heading e.g. sort by Deal Amount
+ Filter
	+ Users can filter the view of deals using the filter tabs. e.g. user can filter view to only see the user's deals

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

- Using Pytest a fake instance of  a team was created using the Teams class. Parameters for a team creation were passed and the behavior was checked using an assert statement.

## Project Reflection

This chapter will serve as a reflection on the 12 weeks we as a team spent working on our project, highlighting the difficulties we experienced and the engineering trade offs we had to consider while developing Sherpa.

### Difficulties

This section outlines the difficulties and challenges we individually and as a team encountered in the process of developing Sherpa.  

+ __Turbo__
	+ Implementing Turbo in our application proved to be difficult. Our goal was to have our whole application using Turbo to increase the performance of our web application and to ensure a smooth user experience while using Sherpa. Due to a lack of documentation online regarding Turbo, we had to go through a lot of trial and error when implementing Turbo. Therefore, this was time consuming and proved frustrating at times when encountering unexpected behaviours. But once completed the benefit of Turbo was evident with the smooth performance of our web application.
+ __Modularization__
	+ 
+ __Google Feature Integration__
	+ 
+ __Testing__
	+ Writing the test cases for our code was challenging initially due to having little experience with testing web application. Also, the structure of our code caused problems with writing test cases. But once modularization was implemented within our code then test cases were much easier to write.
+ __Security__
Security was something that was of utmost importance for our application in order to ensure the security of user data and preventing any potential threats. 
	+ _Hashing_ -  We managed to implement security features where user data is stored securely by hashing is before storing it in the database.
	+ _Cross-Site Scripting_ - Our use of Flask SQL Alchemy as an ORM made sure to prevent any potential XSS attacks
	+ _Session Cookies_ - Our implementation of session cookies within our application ensured that users are authenticated when making requests and prevent unauthorized users accessing forbidden data.



### Engineering Tradeoffs
This section lays out the engineering trade


