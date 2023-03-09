﻿# Sherpa: A Free and Open-Source CRM
﻿
![Sherpa logo: a picture of a Yak beneath a mountain range with the text "Sherpa"](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/sherpa_logo.png)
<br>
Oliver Linger, 120444372

Matt Mallen, 120355103

Eimantas Pusinskas, 120312336

Aria Shahi, 119522223

## Table of Contents

TODO: TABLE OF CONTENTS AT END (PLUS NEED TO CHECK).

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
    - [Complete Tasks](#complete-tasks)
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
    - [View Assigned Deals](#view-assigned-deals) 
    - [Close Deal](#close-deal)
    - [Closed Vs Goal](#closed-vs-goal)
    - [Forecast](#forecast)
    - [Deal Stage Funnel](#deal-stage-funnel)
    - [Activity Statistics](#activity-statistics)
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

TODO: GITHUB LINK

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

TODO: bit of an intro to the user stories. Also need do add the "in order" part to every user story.

The following user stories describe various tasks that a user might want to accomplish while using a CRM system. User stories are short descriptions of a user's goals or desires, which are used to guide the development of software applications. In this case, the user stories are focused on the functions of a CRM (Customer Relationship Management) system called Sherpa. The stories cover tasks such as inviting team members, adding and editing customer contacts, creating and viewing deals, scheduling meetings, and more. Each story is identified by a unique ID number, which can be used to track its progress during development. By focusing on the user's needs and objectives, these stories help ensure that the CRM system is designed to be efficient, effective, and easy to use.

#### Team Invitation Creation

*User Story ID: 1*

As a business owner / manager, I want to invite other users to join my Sherpa team so that they can get access to our CRM resources.

#### Team Invitation Acceptance

*User Story ID: 2*

As a business employee, I want to accept an invitation to join my employer's Sherpa team to get access to their CRM resources.

#### View Contacts

*User Story ID: 3*

As a Sherpa user, I want to view all my team's contacts so that I can view the contact information of our customers.

#### Add Contacts

*User Story ID: 4*

As a Sherpa user, I want to add a contact to my team's contacts list so I can record the contact information of a new customer.

#### Edit Contacts

*User Story ID: 5*

As a Sherpa user, I want to edit one of my team's contacts i.e. change various details like a phone number so I can correct mistakes or update stale information.

#### Remove Contacts

*User Story ID: 6*

As a Sherpa user, I want to remove one of my team's contacts so I can delete a record for a person who is no longer a customer or delete an erroneous record.

#### View User Profile

*User Story ID: 7*

As a Sherpa user, I want to view my profile so I can see the information associated with my Sherpa account.

#### User Logout

*User Story ID: 8*

As a Sherpa user, I want to log out of my account so that I need to log in, in order to use Sherpa again.

#### View Team

*User Story ID:  9*

As a Sherpa user I want to view my team so that I can see the list of the members of my team.

#### Leave Team

*User Story ID:  10*

As a Sherpa user, I want to leave my team so that I no longer have access to the team's CRM resources and I am free to create / join another team.

#### Assign Contact

*User Story ID:  11

As a Sherpa team owner/admin I want to assign a contact to a member of my team they understand who they have to communicate with to try generate a sale.

#### View Assigned Contacts

*User Story ID:  12*

As a Sherpa user I want to view the contacts that have been assigned to me so I can see what data they have to help me generate a sale.

#### View Unassigned Contacts

*User Story ID:  13*

As a Sherpa user I want to view the contacts that have yet to be assigned to a member of my team so they dont get left unattend.

#### Search For Contacts

*User Story ID:  14*

As a Sherpa user I want to search for a specific contact(s) using a search bar to speed up the time it takes to find a contact.

#### Sort Contacts

*User Story ID:  15*

As a Sherpa user I want to sort my team's contacts by email, phone number, etc.

#### View Contact Activity

*User Story ID:  16*

As a Sherpa user I want to view all team activity for a contact e.g. notes, emails, meetings etc so I understand to a greater extend to what way a deals heading.

#### Post Notes

*User Story ID:  17*

As a Sherpa user, I want to add a note to a contact's page to notify my colleges of anything significant thats happening to that specific contact.

#### Remove notes

*User Story ID:  18*

As a Sherpa user, I want to remove a note on a contact's page if it isnt applicable to that contact anymore.

#### Send Email 

*User Story ID: 19*

As a Sherpa user, I want to send an email to a contact so I can communicate with them.

#### View Emails 

*User Story ID: 20*

As a Sherpa user, I want to view my emails sent and received to/from a contact to keep track of our conversations.

#### Reply to Email 

*User Story ID: 21*

As a Sherpa user, I want to reply to an email from a contact to allow for me to exchange information with them.

#### Set a Task

*User Story ID: 22*

As a Sherpa user, I want to create a task in relation to a contact to remind myself of anything that needs to be done in relation to that customer.

#### View Tasks
*User Story ID: 23*

As a Sherpa user, I want to view all tasks in relation to a contact so I can understand the jobs that need to be done as a whole.

#### Complete Task
*User Story ID: 24*

As a Sherpa user, I want to mark a task as complete to notify myself that it has been completed.

#### Schedule Meeting
*User Story ID: 25*

As a Sherpa user, I want to schedule a meeting with a contact which is integrated with my Google calendar so I can notify the contact when we are scheduled to talk.

#### View Meetings
*User Story ID: 26*

As a Sherpa user, I want to view my scheduled meetings with a contact so I can join the meetings.

#### Create Deal
*User Story ID: 27*

As a Sherpa user, I want to create a deal to allow for a new sales contract to be made.

#### View Deals
*User Story ID: 28*

As a Sherpa user, I want to view my team's deals to help me understand what direction my teams deals are going.

#### Edit Deal
*User Story ID: 29*

As a Sherpa user, I want to edit a deal to match the deals current situation.

#### Close Deal
*User Story ID: 30*

As a Sherpa user, I want to close a deal to update the status of a deal to reflect the fact that the sale has be finalized.

#### Search Deals
*User Story ID: 31*

As a Sherpa user, I want to search my team's deals to check my team's activity.

#### Sort Deals
*User Story ID: 32*

As a Sherpa user, I want to sort my team's deals to make it quicker for me to find a deal.

#### Assign Deal

*User Story ID:  33*

As a Sherpa team owner/admin I want to assign a deal to a member of my team to let them know what contacts they have to persue.

#### View Assigned Deals

*User Story ID:  34*

As a Sherpa user I want to view the deals that have been assigned to me so I know what I must do to do my job.

#### Closed Vs Goal

*User Story ID:  36*

As a Sherpa user I want to view a graph illustrating how my team is performing in terms of the "goals" of our deals and how much they are actually "closed" for.

#### Forecast

*User Story ID:  37*

As a Sherpa user I want to view a graph illustrating my team's forecasted deal  earnings for the month to help me get a greater understanding of where my deals are heading.

#### Deal Stage Funnel

*User Story ID:  38*

As a Sherpa user I want to view a graph illustrating the how successful my team is at progressing deals from stage to stage to help me make data driven decisions.

#### Activity Statistics

*User Story ID:  39*

As a Sherpa user I want to view a graph illustrating the breakdown of customer interaction statistics of the top 5 sales people on my team (top being the team members with the most interactions e.g. emails, meetings etc).

### Requirements

TODO: an intro to the requirements.

The success of any software project is dependent on the ability to understand, document, and implement the requirements of the system. In this section, we will outline the requirements for the Sherpa web application, a CRM tool for managing contacts and deals. These requirements have been defined through the use cases of the system, and they serve as a roadmap for our team to ensure that the final product meets the needs and expectations of its users. The requirements are organized into functional areas, such as user registration and authentication, team creation and management, database CRUD operations, and user profile management, among others. By following these requirements, the Sherpa development team was able to deliver a reliable and user-friendly application that fulfills its intended purpose.

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

*Satisfies User Stories: 3 - 6, 28-30

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

*Requirement ID: 8*

*Satisfies User Story: 9, 10*

A user must be able to view a page that lists all of the members of their team. On this page, they will be given the option to leave their team (this will also feature a "are you sure?" (or similar) checkbox.

#### Database Viewing in Pages

*Requirement ID: 9*

*Satisfies User Story: 3, 27*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Users must be able to view their team's contacts or deals. Since a business may have an enumerable number of customers and sales contracts, Sherpa can not serve all records on one page without hindering the user experience therefore records must be "chunked up" into "pages" (each page being a group of 25 records), with the user able to navigate records using the "next page" and #### Closing Deals"previous page" buttons.

#### Database Filtering

*Requirement ID: 10*

*Satisfies User Story: 11 - 13, 33-34*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Admins of a team must be able to assign a member of their team as an "owner" of a contact or deal. This will update the record's owner_id to the email of the new contact owner.

Users must then be able to filter for "my contacts", "my deals" etc, i.e. just display the records that have an owner_id equal to the user's email. Users should also be able to view "unassigned contacts" i.e. the contacts that have a NULL owner_id. There won't be an "unassigned deals" view.

#### Database Searching

*Requirement ID: 11*

*Satisfies User Story: 14, 31*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Users must be able to search their team's contacts or deals. Users should be able to search for a specific name, email, phone number etc and be served the records that match their search term.

#### Database Sorting

*Requirement ID: 12*

*Satisfies User Story: 15, 32*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

User must be able to sort their team's contacts or deals by email, phone number, etc. The app must support both ascending and descending sorting and for improved user experience this should behave as a "toggle" feature i.e. click a column header once and it'll be sorted in ascending order, click that same column header again and the order will be flipped.

#### Activity Logging and Viewing

*Requirement ID:  13*

*Satisfies User Story:  16*

Users must be able to view a log of all contact activity for all emails, tasks, meetings and notes related to the contact. Every time an activity occurs, this event must be logged detailing the activity type and the datetime it occurred. If activities have been logged then the user must be able to view this log.

#### Note Management

*Requirement ID:  14*

*Satisfies User Story:  17, 18*

A user must be able to manage their notes on a contact by being able to view notes, add new notes and remove notes. A form must be presented for every contact where users are able to create a note. A table must also be presented where users can view every note for a contact with the option to remove the note

#### Google OAuth (Open Authorisation)

*Requirement ID:  15*

*Satisfies User Story:  20-26*

A user must be able to authenticate their Google Account with OAuth in order to be able to use Sherpa's Google features.

#### Email Management

*Requirement ID: 16*

*Satisfies User Story: 20 - 22*

A user must be able to manage their emails with a contact. A user must be presented with a form for sending an email to a contact containing fields for the email subject and the email body. The user must also be able to view all email threads with the contact and be able to reply to the most recent email in a thread.

#### Task Management

*Requirement ID: 17*

*Satisfies User Story: 23 - 25*

A user must be able to manage their tasks for a customer. A form must be presented where users can set a task in relation to a customer. A table must also be presented displaying all tasks for a given customer.


#### Meeting Management

*Requirement ID: 18*

*Satisfies User Story: 25 26*

A user must be able to manage their meetings with a customer. A form must be presented where users can schedule a meeting with a customer. A table must also be displayed where users can view all their scheduled meetings with a customer.

#### Closing Deals

*Requirement ID: 19*

*Satisfies User Story: 30*


A user when presented with the forms for adding/editing deals must have the option to alter the deal "stage" to Closed. When closing a deal the user must provide the "closed amount".

#### Closed Vs Goal Plot Generation

*Requirement ID: 20*

*Satisfies User Story: 37*

TODO

#### Deal Forecast Plot Generation

*Requirement ID: 21*

*Satisfies User Story: 38*

TODO

#### Deal Conversion Tracking

*Requirement ID: 22*

*Satisfies User Story: 39*

TODO

#### Deal Stage Funnel Plot Generation

*Requirement ID: 23*

*Satisfies User Story: 39*

TODO

#### Activity Plot Generation

*Requirement ID: 24*

*Satisfies User Story: 40*

TODO: EIMANTAS

#### Serving Plots

*Requirement ID: 25*

*Satisfies User Story: 37-40*

TODO: EIMANTAS

## Data Models

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

+ invite_id - "{invitee_email}\_{team_id}\_{secure_token}", used to uniquely identify invite.
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
The following table describes the data model used for "deal" objects i.e. a deal of a given team.

*Table 6 : Deals Data Model*

| deal_id | team_id | name | stage | close_date | owner | amount | associated_contact | associated_company
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|Primary Key, Integer | Integer | String | String | Datetime | String | Integer | String | String |

+ deal_id - auto-incremented integer which is used as the primary key to uniquely identify a deal
+ team_id - secondary key which is used to correlate a deal with a specific team
+ name - the name given to the deal 
+ stage - the deal stage, used to track the progression of the deal 
+ close_date - the date the deal was closed, if it was closed
+ owner - the owner of the deal
+ amount - value of the deal
+ associated_contact - contact associated with this deal
+ associated_company - company associated with this deal

#### Activity Log
The following table describes the data model used for "activity log" objects i.e. recordings of the metadata of interactions with customers i.e. emails, meetings, tasks, etc.

*Table 7 : Activity Log Data Model*

| activity_id | activity_type | actor | timestamp | contact_id | team_id | description |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|Primary Key, Integer | String | String | Datetime | String | Integer | String |

+ activity_id - auto-incremented integer which is used as the primary key to uniquely identify an activity
+ activity_type - the type of activity, can be "note", "email", "task", "complete_task", and "meeting
+ actor - the "doer" of the activity i.e. the team member who created the note, sent the email etc
+ timestamp - the date and time at which this activity was logged
+ contact_id - the id of the contact associated with this activity e.g. the recipient of the email, the subject of the note, etc.
+ team_id - secondary key which is used to correlate an activity with a specific team.
+ description - a short string describing the activity e.g. "{actor} created a note on {timestamp}.

#### Deal Stage Conversion
TODO: EIMANTAS

## Implementation

This chapter outlines the implementation of Sherpa. It outlines the technology stack as well as the structure of the application overall. It then details the implementation of Sherpa's requirements, some of these requirement implementations are accompanied by flow charts which are an abstraction of the underlying logic - some requirements not as we did not believe they necessitated a visual aid.

### Underlying Technologies

The following details our team's technology stack and gives context to the implementation chapter i.e. please assume that all implementation details rely on the use of the relevant technologies listed here.

- **Programming Language:** Python
- **Database Management System:** MySQL
- **Web Framework:** Flask
- **Virtual Environments:** Python-dotenv
- **Object-Relational Mapper (ORM):** Flask-SQLAlchemy
- **SMTP Library:** Flask-Mail
- **JavaScript WebSocket Library**: Flask-Turbo
- **Form Rendering & Validation:** WTForms
- **User Authentication:** Werkzeug
- **URL Token Generation:**  Python's Secrets module
- **Plotting Library**: Matplotlib
- **OAuth Library**: Flask-OAuthlib
- **Cloud Orchestration**: Amazon Web Services (AWS) Elastic Beanstalk
- **Application Server Hosting**: AWS EC2
- **Database Server Hosting**: AWS RDS

### App Structure

- Sherpa is a Flask application and is made up of various "endpoints" / routes that users can send  requests to.
- All Sherpa endpoints (except /login and /signup) are protected by an "@login_required" wrapper. This is just a Python decorator that calls a function to reject the user's request if they haven't been authenticated. They're redirected to the login page and once they're authenticated they're redirected back to the protected endpoint.
- Most Sherpa endpoints (except for example / and /login) are protected by a "@team_required" wrapper. This is another decorator that calls a function to reject the user's request if they are not a member of a team. The user is redirected to the "create_team" endpoint.
- Database and SMTP access is facilitated by environment variables specified in a .env file.
- All database interactions occur through the use of SQLAlchemy data "models". These are outlined in the Data Models chapter and are essentially Pythonic descriptions of MySQL tables.
- Sherpa has a monolithic database but each team has two - what we have come to call - "virtual" databases; one for contacts and one for deals. The databases are "virtual" because in reality they're part of a single structure but to prevent teams from being able to access or edit each other's records, data is segregated using team_ids i.e. anytime we issue a query for "team sensitive" data that only members of your team ought to have permissions for, we limit the query to just read, update or delete records that have a "team_id" matching that of your team.

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

### Basic Database Operations (CRUD)

*Implementation of requirement: 6*

"Database" in this context refers to the set of records belonging to a team, either its contacts or deals. 

Since the CRUD operations for both contacts and deals are very similar, their implementation is described in one section. For additional brevity some disparities in form validation etc between contacts and deals are not detailed but one should be able to gather how we interface the user with the MySQL database from what follows.

Each database's "read" operation displays a series of "live" forms i.e. HTML input elements that have been prepopulated with the records from the database. 

Each form represents a record and each form comprises a row in a larger table representing the database. This allows the user to view and edit records using the same elements - they then can save any changes by clicking the appropriate button or remove a specific record by clicking its individual remove button.

#### Create
*Endpoints: /add_contact and /add_deal*

* Initialise an instance of the Contacts or Deals data models.
* Set the instance variables to the values fetched from the add record form.
* Commit the new record to MySQL after some validation checks e.g. "does this contact already exist in this team's records?".

#### Read
*Endpoints: /contacts and /deals*

* Fetch relevant records from the database i.e. all contacts or deals with the correct team_id. 
* Then iterate over the list of records, making each record into a HTML form.
* Each form is then added to a list of forms that is iterated over when templating using Jinja2, associated each form with an "edit" button in the HTML that has its href attribute set to the appropriate edit endpoint with the relevant id (see update for more).
* This results in all contacts or deals being rendered as an "editable" table that the user can now read.
* Each form is also associated with its own "remove" button in the HTML that has its href attribute set to the appropriate remove endpoint with the relevant id (see delete for more).


#### Update

*Endpoints: /edit_contact/<contact_id> and /edit_deal/<deal_id>*

* As described in read, each record in the contacts or deals database is rendered as an individual editable HTML form element and associated with its own edit button. 
* When a user clicks this button, the form is submitted to the relevant edit endpoint and crucially includes the relevant id for example the href attribute might be "/edit_contact/X" with X being the ID of the contact the user wishes to edit.
* This way the back end can update the relevant record that matches that ID with the data POSTed by the form (after validation) and commit these changes to MySQL.

#### Delete

*Endpoints: /remove_contact/<contact_id> and /remove_deal/<deal_id>*

* As described in read, each record in contacts or deals database is rendered as an individual row of a HTML table (inside this row is an editable form but this is more relevant to the edit section).
* Each row is associated with its own "remove" button.
* When a user clicks this button, the form is submitted to the relevant remove endpoint and crucially includes the relevant id for example the href attribute might be "/remove_contact/X" with X being the ID of the contact the user wishes to remove.
* This way the back end can remove the relevant record that matches that ID and commit these changes to MySQL.

### Reseting a User's Authenticated Session

*Implementation of requirement: 7*

*endpoint: /profile*

* If a user sends a GET request to this endpoint they will be served a page with basic account information, email address etc.
* If however, they submit a POST request, their flask session will be cleared this means they will be redirected to the login page for all subsequent requests by the *@login_required* decorator since they no longer have a signed login cookie in their session.

### Viewing Teams and Leaving Them

*Implementation of requirement: 8*

TODO

### Viewing Databases in Pages

*Implementation of requirement: 9*

When the user visits the webpage, the server-side code retrieves all records from the database using a SQL query. The records are then stored in a list.

Next, the code determines which page the user is currently viewing. By tracking the current page number in a session variable.

Once the current page is determined, the code calculates the starting and ending indexes of the records to display on that page. For example, if each page displays 25 records and the user is on page 3, the starting index would be 50 (2 * 25) and the ending index would be 74 (50 + 24).

The code then selects the records between the starting and ending indexes and formats them into HTML table rows. These rows are concatenated together to form the HTML table body.

Additionally, the code generates HTML links for each page number. These links allow the user to navigate between pages. The links are displayed as arrows on the webpage.

Finally, the code combines the HTML table and paging links into a single HTML page and sends it to the user's browser for display.

Overall, this approach is relatively efficient because it only retrieves the records needed for the current page, rather than retrieving all records at once. It also allows for easy paging and navigation between pages

TODO (FLOW)

### Showing the User the Records they Own

*Implementation of requirement: 10*

TODO

### Searching a Database

*Implementation of requirement: 11*

The search bar allows the user to search through the database based on certain criteria. The user can search for deals by entering a search term in the search bar and selecting a filter. The search bar is defined using a Flask form such as DealsSearchForm. When the user enters a search term and submits the form, the search term is extracted from the form and used to search for relevant deals in the database.

First, the search term is optimized for searching by calling a function like optimize_deals_search depending on the page. This function checks whether the search term looks like an email address or not, and returns "email" if it does and "name/company/email" otherwise.

Next, the .query object is filtered based on the user's search criteria. The variable for this example we'll say 'deals' is set to the Deals.query object at the start of the function. Then, the results of this query are filtered based on the user's search term. If the search term is an email, then only the associated_contact column is searched. If the search term is not an email, then all relevant columns are searched.

Finally, the results of the search are returned to the user in the deals variable. The deals variable is a query object, which means that it represents a set of results from the database. The results are not actually fetched from the database until the query is executed (in this case, by calling .limit() and .offset()).


TODO (FLOW)


### Sorting a Database

*Implementation of requirement: 12*

Our code allows the user to sort a list of contacts/deals in a database based on different columns such as name, email, or phone number. The sorting is handled by a function such as order_contacts(), which takes three parameters: sort, order, and contacts.

The sort parameter indicates the column to sort by, and it can have values such as "name", "email", or "phone_number". The order parameter indicates whether to sort in ascending or descending order and can have values of "ASC" or "DESC". Finally a parameter, for this we'll say contacts, is the query object returned by the database that contains the contacts to sort.

The function first checks which column the user wants to sort by and then sorts the contacts accordingly using the order_by() method. If the order parameter is "ASC", the contacts/deals are sorted in ascending order. If it is "DESC", they are sorted in descending order.

The sorting is triggered by the contacts()/deals() function, which sets the values of sort and order parameters based on the user's selection. The sort parameter is changed if the user is sorting a different column than the previous sort, and the order parameter is changed if the user is toggling the sort of the same column.

Overall, this code allows users to sort a list of contacts/deals in a database based on different columns and in ascending or descending order.

TODO (FLOW)

### Activity Feature

*Implementation of requirement: 13*

TODO

### Notes Feature

*Implementation of requirement: 14*

TODO

### Integrating Google Accounts

*Implementation of requirement: 15*

Users must integrate their Google accounts with Sherpa to obtain a Google session token in order to avail of Sherpa's Google services such as Emails, Tasks and Meetings.

The following diagram details the process of integrating Google with a Sherpa account.

![Diagram detailing the retrieval of a Google session token. Image is sourced from  "https://developers.google.com/identity/protocols/oauth2"](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/google_auth.png)
<br>*TODO: FIGURE*

Google accounts are authenticated using OAuth 2.0. For brevity, we won't go into more detail than this over concerns over word count. If you'd like to learn more about OAuth 2.0 please click [here](https://developers.google.com/identity/protocols/oauth2).

### Parsing API Responses

*Implementation of requirements: 16-18*

TODO (FLOW)

### Sending and Receiving Emails

*Implementation of requirement: 16*

TODO

### Creating, Viewing, and Completing Tasks

*Implementation of requirement: 17*

TODO

### Scheduling and Joining Meetings

*Implementation of requirement: 18*

TODO

### Closing Deals

*Implementation of requirement: 19*

TODO

### Tracking Deal Conversions

*Implementation of requirement: 22*

TODO

### Creating Data Analytics Plots

*Implementation of requirement: 20, 21, 23, 24*

TODO (FLOW)

### Serving Plots

*Implementation of requirement: 25*

* When a plot is ready to be served to the user as part of HTTP response, Sherpa first initialises an in-memory bytes buffer.
* Then the plot figure is saved as a PNG in this new buffer.
* Then the data in the buffer is encoding using base64 encoding.
* This encoded data is then included in the HTTP response as part of an "img" element.


## Testing

TODO

## Project Reflection

This chapter will serve as a reflection on the 12 weeks we as a team spent working on our project, highlighting how we worked together and the challenges we faced while developing Sherpa.

### The Team's Process

Our team's process for completing tasks was highly organized and effective, despite being a small team. With daily three-hour work sessions, we ensured that we were all working together and making progress on the project at hand. This approach helped our team stay on track and remain focused on important tasks.

In addition, our team had a weekly whiteboarding session where we planned user stories. This collaborative approach to task management ensures that everyone was aligned on the project's goals and objectives. By breaking down tasks into user stories, our team prioritized work and ensured that we were working on the most critical tasks.

Our team's approach also included a "polishing" week every second week. This was an excellent practice as it allowed our team to review completed work and make necessary improvements. This approach helped to ensure that the final product was of a high quality.

Overall, our team's process was highly effective, and our approach to task management was highly structured, ensuring that everyone was working together towards a common goal. This collaborative approach allowed our team to remain focused and prioritize work, resulting in high-quality work that was completed efficiently.


### What Went Well

#### Collaborative approach:

Our team's approach to task management was highly collaborative, with daily work sessions and weekly whiteboarding sessions. This allowed everyone to work together towards a common goal and ensured that everyone was aligned on the project's goals and objectives.

  

#### Prioritization:

By breaking down tasks into user stories, Our team was able to prioritize work and ensure that we were working on the most critical tasks. This helped us stay focused and make progress on the most important parts of the project.

  

#### Quality control:

Our team's approach included a "polishing" week every second week, which allowed us to review completed work and make necessary improvements. This helped ensure that the final product was of a high quality.

#### Efficiency:

Our team was able to complete high-quality work efficiently, thanks to our structured and collaborative approach to task management. This allowed us to make progress on the project and meet our goals within our timeframe.

### Mistakes To Learn From

During the course of our project, we made some mistakes and learned some valuable lessons. One mistake we made was not standardizing our HTML, which led to some inconsistencies in our code. To avoid this in the future, we learned to standardize our HTML and use best practices to ensure consistency throughout our project.

Another mistake we made was not using Flask blueprints, which made it more difficult to manage our code as the project grew. We realized the importance of using blueprints to organize our code and make it easier to maintain and update.

Additionally, we initially did not use Bootstrap for our CSS, which resulted in some inconsistencies in the visual design of our project. To address this, we learned the importance of using a CSS framework like Bootstrap, which helped us to ensure consistency and improve the overall visual design of our project.

Overall, we learned that standardizing our code, using frameworks and best practices, and prioritizing consistency were essential to the success of our project. These lessons helped us to improve our processes and achieve better results in future projects.

### What Went Well

### Mistakes To Learn From

### What Was Technically Challenging

This section outlines the difficulties and challenges we individually and as a team encountered in the process of developing Sherpa.  

+ __Turbo__
	+ Implementing Turbo in our application proved to be difficult. Our goal was to have our whole application using Turbo to increase the performance of our web application and to ensure a smooth user experience while using Sherpa. Due to a lack of documentation online regarding Turbo, we had to go through a lot of trial and error when implementing Turbo. Therefore, this was time consuming and proved frustrating at times when encountering unexpected behaviours. But once completed the benefit of Turbo was evident with the smooth performance of our web application.
+ __Modularization__
	+ TODO
+ __Google Integration__
	+ TODO
+ __Testing__
	+ Writing the test cases for our code was challenging initially due to having little experience with testing web application. Also, the structure of our code caused problems with writing test cases. But once modularization was implemented within our code then test cases were much easier to write.
+ __Security__
Security was something that was of utmost importance for our application in order to ensure the security of user data and preventing any potential threats. 
	+ _Hashing_ -  We managed to implement security features where user data is stored securely by hashing is before storing it in the database.
	+ _Cross-Site Scripting_ - Our use of Flask SQL Alchemy as an ORM made sure to prevent any potential XSS attacks
	+ _Session Cookies_ - Our implementation of session cookies within our application ensured that users are authenticated when making requests and prevent unauthorized users accessing forbidden data.