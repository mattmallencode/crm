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
    - [View and Leave Teams](#view-and-leave-teams)
    - [Database Viewing in Pages](#database-viewing-in-pages)
    - [Database Filtering](#database-filtering)
    - [Database Searching](#database-searching)
    - [Database Sorting](#database-sorting)
    - [Activity Logging and Viewing](#activity-logging-and-viewing)
    - [Note Management](#note-management)
    - [Google OAuth (Open Authorisation)](#google-oauth-open-authorisation)
    - [Email Management](#email-management)
    - [Task Management](#task-management)
    - [Meeting Management](#meeting-management)
    - [Closing Deals](#closing-deals)
    - [Closed Vs Goal Plot Generation](#closed-vs-goal-plot-generation)
    - [Deal Forecast Plot Generation](#deal-forecast-plot-generation)
    - [Deal Conversion Tracking](#deal-conversion-tracking)
    - [Deal Stage Funnel Plot Generation](#deal-stage-funnel-plot-generation)
    - [Activity Plot Generation](#activity-plot-generation)
    - [Serving Plots](#serving-plots) 
 - [Data Models](#data-models)
    - [Users](#users)
    - [Teams](#teams)
    - [Invites](#invites)
    - [Contacts](#contacts)
    - [Notes](#notes)
    - [Deals](#deals)
    - [Activity Log](#activity-log)
    - [Deal Stage Conversion](#deal-stage-conversion)
- [Implementation](#implementation)
  - [Underlying Technologies](#underlying-technologies)
  - [App Structure](#app-structure)
  - [User Registration and Authentication](#user-registration-and-authentication)
  - [Creating Teams](#creating-teams)
  - [Sending and Accepting Team Invites](#sending-and-accepting-team-invites)
  - [Basic Database Operations (CRUD)](#basic-database-operations-(CRUD))
  - [Reseting a User's Authentication Session](#reseting-a-user's-authentication-session)
  - [Viewing teams And Leaving Team](#viewing-teams-and-leaving-team)
  - [Viewing Database in Pages](#viewing-database-in-pages)
  - [Showing the User the Records they Own](#showing-the-user-the-records-they-own)
  - [Contact Information Management](#contact-information-management)
  - [Searching a Database](#searching-a-database)
  - [Sorting a Database](#sorting-a-database)
  - [Activity Feature](#activity-feature)
  - [Notes Feature](#notes-feature)
  - [Integrating Google Accounts](#integrating-google-accounts)
  - [Parsing API Responses](#parsing-api-responses)
  - [Sending and Receiving Emails](#sending-and-recieving-emails)
  - [Creating, Viewing, and Completing Tasks](#creating,-viewing,-and-completing-tasks)
  - [Scheduling and Joining Meetings](#scheduling-and-joining-meetings)
  - [Closing Deals](#closing-deals)
  - [Tracking Deal Conversions](#tracking-deal-conversions)
  - [Creating Data Analytics Plots](#creating-data-analytics-plots)
  - [Serving Plots](#serving-plots)
- [Testing](#testing)
  - [Test Client Set Up](#test-client-set-up)
  - [Dealing With User Sessions](#dealing-with-user-sessions)
  - [Simulating API Responses](#simulating-api-responses)
 - [Project Reflection](#project-reflection)
	 - [Process](#process)
	 - [Challenges and Trade-Offs](#challenges-and-trade-offs)
     - [Lessons Learned](#lessons-learned)

## Introduction

This document outlines the design and implementation of Sherpa, a free and open-source Customer Relationship Management (CRM) System. A CRM helps businesses drive sales, track customer interactions and provide quality service. This is achieved by storing the data of existing and potential customers in a central database that can be accessed and managed by anyone within the organisation with appropriate permissions.

Sherpa can be used by multiple businesses i.e. users create "teams" and invite other users to join their team.

Sherpa's GitHub repository is available [here](https://github.com/mattmallencode/crm).

## Some CRM Terms


The following are important terms in CRM software:

+ __Contacts__: potential or existing customers of a business.
+ __Deals__: potential or existing sales contract between a business and  a customer. Deals can be:
  + **open** i.e. no contract has been signed / no money has been exchanged, or
  + **closed** i.e. the business has made the sale / money has been credited to it.
+ **Deal Goal**: The amount of money a business aims to earn when initially pursuing a deal.
+ **Deal Closed Amount**: The actual amount of money a business earned after closing a deal.

## What Sherpa Can Do

Sherpa has the following features:


- Sherpa is a **customer database**. The platform offers a simple user interface to keep track of all customers in one place.
    
- Sherpa allows users to **interact with customers using Google API Integrations**. Users can send and receive emails, schedule meetings with Google Meet, set reminders for Google Calendar, and leave notes about customers for colleagues.

- Sherpa helps users make **data driven decisions**. Sherpa provides an analytics dashboard to help track a team's progress. For example, a user might see from the graph tracking team interactions with customers that their top sales person tends to prefer video calls over emails compared to the rest of the team, they might then decide to do the same to try mimic their success - that's a data driven decision.

## How Sherpa Adds Value

Firstly, with Sherpa, **your sales team always has a cohesive view**. For example, if contact's email changes, it changes for everyone on your team.

Secondly, Sherpa **makes management easier**. A manager can assign a member of their sales team to chase down a specific customer, and that sales person knows immediately after logging into the application which contacts they are supposed to be handling.

Lastly, **everything is traceable** with Sherpa. Not just in terms of analytics but also in terms of customer interactions. Everyone on a team can see which customers have been “left on the back burner” so to speak based on the last time they were emailed for example.

It would be painful to set up a cohesive flow in terms of managing relationship with customers if a business bootstrapped it with several unconnected applications. Sherpa makes it easy.

## Project Specification

### User Stories

The following user stories describe various tasks that a user might want to accomplish while using a CRM system,  which our team used to guide our design and implementation.

#### Team Invitation Creation

*User Story ID: 1*

As a manager, I want to invite other users to join my Sherpa team so they can have access to our CRM resources.

#### Team Invitation Acceptance

*User Story ID: 2*

As an employee, I want to accept an invitation to join my employer's Sherpa team to get access to their CRM resources.

#### View Contacts

*User Story ID: 3*

As a Sherpa user, I want to view my team's contacts to see the contact information of our customers.

#### Add Contacts

*User Story ID: 4*

As a Sherpa user, I want to add a contact to my team's contacts list so I can record the contact information of a new customer.

#### Edit Contacts

*User Story ID: 5*

As a Sherpa user, I want to edit one of my team's contacts so I can correct mistakes or update stale information.

#### Remove Contacts

*User Story ID: 6*

As a Sherpa user, I want to remove one of my team's contacts so I can delete a contact who is no longer a customer or delete an erroneous record.

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

As a Sherpa user, I want to leave my team so that I am free to join another team.

#### Assign Contact

*User Story ID:  11

As a Sherpa team admin I want to assign a contact to a member of my team so they know which customers they should deal with.

#### View Assigned Contacts

*User Story ID:  12*

As a Sherpa user I want to view the contacts that have been assigned to me so I can see which customers my manager wants me to deal with.

#### View Unassigned Contacts

*User Story ID:  13*

As a Sherpa user I want to view the contacts that have yet to be assigned to a member of my team so they are not left unattended.

#### Search For Contacts

*User Story ID:  14*

As a Sherpa user I want to search for a specific contact(s) using a search bar to speed up the time it takes to find a contact.

#### Sort Contacts

*User Story ID:  15*

As a Sherpa user I want to sort my team's contacts by email etc so I can organise the information.

#### View Contact Activity

*User Story ID:  16*

As a Sherpa user I want to view all team activity for a contact e.g. emails, meetings etc so I can track interactions with the customer.

#### Post Notes

*User Story ID:  17*

As a Sherpa user, I want to add a note to a contact's page to notify my colleagues of my dealings with the customer.

#### Remove notes

*User Story ID:  18*

As a Sherpa user, I want to remove a note on a contact's page if it it's erroneous or not applicable anymore.

#### Send Email

*User Story ID: 19*

As a Sherpa user, I want to send an email to a contact so I can communicate with them.

#### View Emails

*User Story ID: 20*

As a Sherpa user, I want to view my emails sent and received to/from a contact to keep track of our conversations.

#### Reply to Email

*User Story ID: 21*

As a Sherpa user, I want to reply to an email from a contact to continue my conversation with them.

#### Set a Task

*User Story ID: 22*

As a Sherpa user, I want to create a task in relation to a contact to remind myself of tasks I must complete in relation to the customer.

#### View Tasks

*User Story ID: 23*

As a Sherpa user, I want to view all tasks in relation to a contact so I can understand the tasks that need to be done as a whole.

#### Complete Task

*User Story ID: 24*

As a Sherpa user, I want to mark a task as complete to "tick" it off my to-do list.

#### Schedule Meeting

*User Story ID: 25*

As a Sherpa user, I want to schedule a meeting with a contact so that I can video conference with them.

#### View Meetings

*User Story ID: 26*

As a Sherpa user, I want to view my scheduled meetings with a contact so I can join the meetings.

#### Create Deal

*User Story ID: 27*

As a Sherpa user, I want to create a deal to allow for a new sales contract to be made.

#### View Deals

*User Story ID: 28*

As a Sherpa user, I want to view my team's deals to view the information associated with the deals.

#### Edit Deal

*User Story ID: 29*

As a Sherpa user, I want to edit a deal to fix erroneous information and update stale data.

#### Close Deal

*User Story ID: 30*

As a Sherpa user, I want to close a deal to update the status of a deal to reflect the fact that the sale has be finalised.

#### Search Deals

*User Story ID: 31*

As a Sherpa user, I want to search my team's deals to make finding a specific deal faster.

#### Sort Deals

*User Story ID: 32*

As a Sherpa user, I want to sort my team's deals to organise the information.

#### Assign Deal

*User Story ID:  33*

As a Sherpa team admin I want to assign a deal to a member of my team to let them know what deals they should take ownership of.

#### View Assigned Deals

*User Story ID:  34*

As a Sherpa user I want to view the deals that have been assigned to me so I know which deals my manager wants me to take ownership of.

#### Closed Vs Goal

*User Story ID:  35*

As a Sherpa user I want to view a graph illustrating how my team is performing in terms of the "goals" of our deals and how much they are actually "closed" for.

#### Forecast

*User Story ID:  36*

As a Sherpa user I want to view a graph illustrating my team's forecasted deal  earnings for the month to help me get a greater understanding of where my deals are heading.

#### Deal Stage Funnel

*User Story ID:  37*

As a Sherpa user I want to view a graph illustrating the how successful my team is at progressing deals from stage to stage to help me make data driven decisions.

#### Activity Statistics

*User Story ID:  38*

As a Sherpa user I want to view a graph illustrating the breakdown of customer interaction statistics of the top 5 sales people on my team (top being the team members with the most interactions e.g. emails, meetings etc).

### Requirements

In this section, we will outline the requirements for Sherpa. Each requirement satisfies one or more user stories.

#### User Registration

*Requirement ID: 1*

*Satisfies User Stories: 1, 2, 7

A user must be able to register an account with Sherpa's database by providing a valid email and password combination, enabling their authentication.

#### User Authentication

*Requirement ID: 2*

*Satisfies User Stories: 1, 2*

Before accessing Sherpa a user must be authenticated. They do this by providing the email and password they used to register. This will then be compared to Sherpa's database, if they provide matching credentials they are authenticated for all subsequent requests.

#### Team Creation

*Requirement ID: 3*

*Satisfies User Stories: 1, 2*

In order to do anything meaningful with Sherpa a user must be a member of a team. Users must be able to create teams. If a user is not already a member of a team they can register one with Sherpa's database.

#### Team Invitation Generation and Delivery

*Requirement ID: 4*

*Satisfies User Stories: 1, 2*

A team administrator must be able to invite another user to join their team. This can be achieved by providing the email of the person they wish to invite and Sherpa will send them an invite link.

#### Accepting Team Invitation


*Requirement ID: 5*

*Satisfies User Story: 2*

A user must be able to accept a team invitation. They can achieve this by clicking the invitation link they received in their email and then logging in.

#### Database Create, Read, Update, and Delete (CRUD)

*Requirement ID: 6*

*Satisfies User Stories: 3 - 6, 28-30

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

A user must be able to interface with their team's databases and achieve all of the basic CRUD operations with their team's records by interacting with the web app i.e. forms and buttons.

#### User Profile and Logout

*Requirement ID: 7*

*Satisfies User Story: 7, 8*

A user must be able to view a profile page with their account information. Furthermore, they must be able to logout of their account, meaning their session will be cleared and they will have to login to be authenticated again.

#### View and Leave Teams

*Requirement ID: 8*

*Satisfies User Story: 9, 10*

A user must be able to view a page that lists all of their teammates. On this page, they have the option to leave their team - validated with an "are you sure?" checkbox.

#### Database Viewing in Pages

*Requirement ID: 9*

*Satisfies User Story: 3, 27*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

Users must be able to view their team's contacts or deals. Since a business may have an enumerable number of customers and records must be split into pages (each page has 25 records), with the user able to navigate pages using the "next" and "previous" page buttons.

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

Users must be able to search their team's contacts or deals. Users should be able to search for a specific name, email etc and be served records matching their search.

#### Database Sorting

*Requirement ID: 12*

*Satisfies User Story: 15, 32*

"Database" in this context refers to the set of records belong to a team, either its contacts or deals.

User must be able to sort their team's contacts or deals by email, phone number, etc. The app must support both ascending and descending sorting and be able to switch between orders using toggle buttons.

#### Activity Logging and Viewing

*Requirement ID:  13*

*Satisfies User Story:  16*

An "activity" is a customer interaction e.g. creating a note, sending an email. Every time an activity occurs, this event must be logged detailing the activity type and the date time it occurred. The user must also be able to view these logs.

#### Note Management

*Requirement ID:  14*

*Satisfies User Story:  17, 18*

A form must be presented for every contact where users are able to create a note. A table must also be presented where users can view every note for a contact with the option to remove the note Users must also be able to remove notes.

#### Google OAuth (Open Authorisation)

*Requirement ID:  15*

*Satisfies User Story:  20-26*

A user must be able to authenticate their Google Account with OAuth in order to be able to use Sherpa's Google features.

#### Email Management

*Requirement ID: 16*

*Satisfies User Story: 20 - 22*

A user must be presented with a form for sending an email to a contact containing fields for the email subject and the email body. The user must also be able to view all email threads with the contact and be able to reply to the most recent email in a thread.

#### Task Management

*Requirement ID: 17*

*Satisfies User Story: 23 - 25*

A form must be presented where users can set a task in relation to a customer. A table must be displayed with the tasks for a given customer.

#### Meeting Management

*Requirement ID: 18*

*Satisfies User Story: 25 26*

A form must be presented where users can schedule a meeting with a customer. A table must be displayed where users can view and join meetings with a customer.

#### Closing Deals

*Requirement ID: 19*

*Satisfies User Story: 30*

A user when presented with the forms for adding/editing deals must have the option to alter the deal "stage" to Closed. When closing a deal, the user must provide the "closed amount".

#### Closed Vs Goal Plot Generation

*Requirement ID: 20*

*Satisfies User Story: 37*

A plot must be generated illustrating how a specific team is performing in terms of their "goals" for deals versus the actual "closed amount".

The plot that is generated has these properties;
+ x-axis : 
	+  Subplot 1: Closed Amount of deal
	+ Subplot 2: Goal of deal
+ y-axis : Close Date of the deal
+ Range: Last 365 days
+ Frequency: Monthly

#### Deal Forecast Plot Generation

*Requirement ID: 21*

*Satisfies User Story: 38*

A  pie chart must be generated illustrating a team's forecasted deal earnings for the current month - it has the these properties:

+ Data:  list of sums of the amounts for the deal stages e.g. Closed Won, Appointment Scheduled etc. Each pie slice is a stage.
+ Range: current month.

The forecasted revenue is the sum of all slices in the pie chart.

#### Deal Conversion Tracking

*Requirement ID: 22*

*Satisfies User Story: 39*

In order to generate the Deal Stage Funnel plot, all changes in deal stage must be tracked.

There must be a table to log deal stage changes which would for every row specify the new deal stage and a timestamp. For a new deal, its stage is logged. If an existing deal changes stage, its logged

#### Deal Stage Funnel Plot Generation

*Requirement ID: 23*

*Satisfies User Story: 39*

A bar chart must be generated to illustrate the progression of a team's deals from stage to stage.

The plot has these properties:

+ x-axis: Number of deals per deal stage
+ y-axis: A bar for each possible deal stage
+ Range: Last Month

Every bar in the chart other than "Closed Won" stage, includes conversion data for Next Step Conversion and Cumulative Conversion. 
 
 + Next Step Conversion - percentage of deals that move from the current stage to the next stage
 + Cumulative Conversion - percentage of deals that move from the first stage to the next stage

The stages follow a hierarchy. 

The hierarchy is laid out as follows; Created -> Qualified To Buy -> Contract Sent -> Appointment Scheduled -> Closed Won. 

This means that deals can move from the Created stage to Qualified To Buy and so on. Deals can skip stages but this must follow the hierarchy e.g. a deal move from "Closed Won" to "Created"

#### Activity Plot Generation

*Requirement ID: 24*

*Satisfies User Story: 40*

A bar chart must be generated to show team performance in relation to "activities" e.g. emails, meetings etc. The top 5 team members are displayed (top being team members with the highest sum of activities each). Each bar represents a team member.

The generated graph must be in the form of a stacked bar chart with every bar detailing the count of an activity type e.g. emails. The chart has these properties:
+ x-axis: names of top 5 members
+ y-axis: activity count
+ Range: last month

#### Serving Plots

*Requirement ID: 25*

*Satisfies User Story: 37-40*

In order to serve plots, they must first be encoded correctly to be included in the HTTP response.

## Data Models

This section describes the app's "data models". These represent the relational data of various entities in Sherpa e.g. users, and can ultimately be viewed as descriptions of SQL tables.

#### Users

The following table describes the data model used for "user" entities i.e. user accounts.


| email | password_hash | team_id | owner_status | admin_status | name |
| :-: | :-: | :-: | :-: | :-: | :-: |
| Primary Key, String | String | Integer | Boolean | Boolean | String |

*Table 1: Users Data Model*

+ email - email address of the user
+ password_hash - the users password stored as a hash value
+ team_id - the team associated with the user to which the user will have CRM access to
+ owner_status - indicates if user is an owner of their team
+ admin_status - indicates if user is an admin within their team
+ name - the real name of the user

#### Teams

The following table describes the data model used for "team" entities i.e. groups of users with access to the same CRM resources.

| team_id | name |
| :-: | :-: |
| Primary Key, Integer | String |

*Table 2: Teams Data Model*

+ team_id - auto-incremented integer which is used as the primary key to uniquely identify a team
+ name - name of the team

#### Invites

The following table describes the data model used for "invite" entities i.e. invitations to users to join a given team.

| invite_id | team_id |
| :-: | :-: |
| Primary Key, String | Integer |


*Table 3: Invites Data Model*

+ invite_id - "{invitee_email}\_{team_id}\_{secure_token}", used to uniquely identify invite.
+ team_id - the team to which the invitation applies for


#### Contacts

The following table describes the data model used for "contact" entities i.e. a contact of a given team.

| contact_id | team_id | name | email | phone number | contact owner | company | status |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Primary Key, String | Integer | String | String | Integer | String | String | String |

*Table 4: Contacts Data Model*

+ contact_id - "{email}_{team_id}", used to uniquely identify contact
+ team_id - secondary key used to associate a contact with a team
+ name - name of the contact
+ email - email address of the contact
+ phone_number - phone number of the contact
+ contact_owner - team member assigned to the contact
+ company - company associated with the contact
+ status - the status of the contact relationship e.g. "New"

#### Notes

The following table describes the data model used for "note" objects i.e. notes added to a specific contact by a Sherpa user.

| note_id | contact_id | note | author | date |
| :-: | :-: | :-: | :-: | :-: |
| Primary Key, Integer | String | String | String | String |


*Table 5: Notes Data Model*

+ note_id - auto-incremented integer which is used as the primary key to uniquely identify a note
+ contact_id - secondary key which is used to correlate a note with a specific contact
+ note - the actual content of the note
+ author - author of the note
+ date - the date the note was written

#### Deals

The following table describes the data model used for "deal" objects i.e. a deal of a given team.

| deal_id | team_id | name | stage | close_date | owner | amount | associated_contact | associated_company |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Primary Key, Integer | Integer | String | String | Datetime | String | Integer | String | String |


*Table 6 : Deals Data Model*

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

| activity_id | activity_type | actor | timestamp | contact_id | team_id | description |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Primary Key, Integer | String | String | Datetime | String | Integer | String |

*Table 7 : Activity Log Data Model*

+ activity_id - auto-incremented integer which is used as the primary key to uniquely identify an activity
+ activity_type - the type of activity, can be "note", "email", "task", "complete_task", and "meeting
+ actor - the "doer" of the activity i.e. the team member who created the note, sent the email etc
+ timestamp - the date and time at which this activity was logged
+ contact_id - the id of the contact associated with this activity e.g. the recipient of the email, the subject of the note, etc.
+ team_id - secondary key which is used to correlate an activity with a specific team.
+ description - a short string describing the activity e.g. "{actor} created a note on {timestamp}.

#### Deal Stage Conversion

The following table describes the data model which is used for calculating deal stage conversion. It is used as a log table where every time a deal transitions to a different stage it is is logged.

| stage_id | team_id | date | stage |
| :-: | :-: | :-: | :-: |
|Primary Key, Integer | Integer | String | String |

*Table 8: Deal Stage Conversion Data Model*

+ stage_id - auto-incremented integer which is used as the primary key to uniquely identify an activity
+ team_id - secondary key which is used to link the deal this stage is associated with to its team 
+ date - the date the deal transitioned to this stage
+ stage - the stage that the deal transitioned to


## Implementation

This chapter outlines the implementation of Sherpa.

### Underlying Technologies

The following details our team's technology stack.

- **Programming Language**: Python
- **Database Management System**: MySQL
- **Web Framework**: Flask
- **Virtual Environments**: Python-dotenv
- **Object-Relational Mapper (ORM)**: Flask-SQLAlchemy
- **SMTP Library**: Flask-Mail
- **JavaScript WebSocket Library**: Flask-Turbo
- **Form Rendering & Validation**: WTForms
- **User Authentication**: Werkzeug
- **Testing Framework**:
- **URL Token Generation**:  Python's Secrets module
- **Plotting Library**: Matplotlib
- **OAuth Library**: Flask-OAuthlib
- **Database Server Hosting**: AWS RDS

### App Structure

- Sherpa is a Flask application and is made up of various "endpoints" users send requests to.
- All Sherpa endpoints (except /login etc) are protected by an "@login_required" wrapper which calls a function to redirect a user if they haven't been authenticated.
- Most Sherpa endpoints (except for example / and /login) are protected by a "@team_required" wrapper which redirects a user if they are not a member of a team. 
- Sherpa is configured with environment variables specified in a .env file.
- All database interactions occur through the SQLAlchemy data models, essentially Pythonic descriptions of MySQL tables.
- Sherpa has a monolithic database but each team has two "virtual" databases for contacts and deals. To prevent teams from accessing each other's records, data is segregated. Anytime we query for "team sensitive"  data, we limit the query to just the records with the correct "team_id".

### User Registration and Authentication

![Picture showing Sherpa's login page](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Sherpa_Login.png)
<br>*Figure 1: Sherpa's login page*

*Implementation of requirements: 1, 2*

The following flow chart details the sign up process flow for a new Sherpa user.

![Flow chart detailing the signup process flow for a new user.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Sign%20Up.png)
<br>*Figure: 2*

*Endpoint: /signup*

- The user must submit a valid response to the signup form.
- The user's email must also not be already registered (SQL query for submitted email).
- If either of the above checks fail the user is returned to the form and informed of the issue.
- Once the user submits a valid request, the back-end will generate a hashed version of their plain text password. Werkzeug uses pbkdf2 to generate a SHA-256 hash along with a salt unique to each user, thus preventing the passwords from being brute forced.
- Finally, the users details are added to an instance of the Users data model and inserted into the database.

The following flow chart details the login process flow for an existing Sherpa user.

![Flow chart detailing the signup process flow for a new user.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Log%20In.png)
<br>*Figure: 3*

*Endpoint: /login*

- The user must submit a valid response to the signup form.
- The user's email must exist in the database.
- The user must authenticate themselves i.e. the password the user provides is hashed and compared to the hashed password on record.
- If either of the above checks fail the user is returned to the form and informed of the issue.
- A cookie is generated that the user presents in lieu of a password for the remainder of the session which is signed using a secret.
- The user is redirected to the home page or to the endpoint they had attempted without authentication.

### Creating Teams

*Implementation of requirement: 3*

The following flow chart details the process flow for creating a Sherpa team.

![Flow chart detailing the team creation process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Team%20Creation.png)
<br>*Figure: 4*

*Endpoint: /create_team*

- The user must submit a valid response to the signup form.
- The user can't be a member of a team i.e. team_id is NULL.
- If either of the above checks fail the user is returned to the form and informed of the issue.
- If the endpoint gets a valid response, the form data is added to an instance of the Teams data model and inserted into the database.
- The user's team_id is then updated based on the team_id returned from the database commit and this update is committed too.
- The user is redirected to the home page.

### Sending and Accepting Team Invites

*Implementation of requirement: 4, 5*

The following flow chart details the process flow for inviting another user to a Sherpa team.
![Flow chart detailing the team invitation process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Invite.png)
<br>*Figure: 5*

*Endpoint: /invite*

![Screenshot of the Sherpa invitation form](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Invite_Form.png)
<br>*Figure 6: Sherpa Team Invitation Form Screenshot*

- The user must submit a valid response to the invite form.
- The user issuing the invite must be a member of a team and one of that team's admins.
- The invitee must not be a member of that team already.
- If the endpoint receives a valid response, an invite_id is generated which includes 16 cryptographically secure characters to prevent fraudulent invitation generation.
- The invite_id is added to an instance of the Invites data model and inserted into the database.
- The user returns to the form and informed of the successful invitation.

The following flow chart details the process flow for accepting a Sherpa invitation. It is a modified version of the login flow: see Figure 2.

![Flow chart detailing the team invitation acceptance process flow.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Invite%20Accept.png)
<br>*Figure: 7*

*Endpoint: /login/<invite_id>*

![Screenshot of a Sherpa team invitation email](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Sherpa_Invite.png)
<br>*Figure 8: Sherpa Team Invitation Email Screenshot*

- User must submit a valid form submission and be authenticated (as per normal login flow).
- If the user doesn't pass an invite_id to the endpoint, the normal login flow resumes.
- If an invite_id is passed, it must be validated. First, the database is checked to see if the invite_id exists. The user also can't accept an invitation unless they authenticate themselves using the email specified.
- If the request is validated, the user's team id is set to the team_id specified in the invitation and the invitation is removed from the table.
- The normal login flow resumes.

### Basic Database Operations (CRUD)
![Screenshot of Sherpa's Contacts page](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Contacts_Screenshot.png)
<br>*Figure 9: Sherpa's Contacts Page*

*Implementation of requirement: 6*

"Database" in this context refers to the set of records belonging to a team, either its contacts or deals.

Each database's "read" operation displays a table of "live" forms i.e. HTML input elements that have been prepopulated with the records from the database, allowing users to view and edit records using the same elements. Each form element represents a record.

![Screenshot of Sherpa's Deals page](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Deals_Screenshot.png)
<br>*Figure 10: Sherpa's Deals Page*



#### Create

*Endpoints: /add_contact and /add_deal*

* Initialise an instance of the Contacts or Deals data models.
* Set the instance variables to the values fetched from the add record form.
* Commit the new record to MySQL after some validation checks e.g. can't create a duplicate record.

#### Read

*Endpoints: /contacts and /deals*

* Fetch relevant records from the database.
* Iterate over list of records; make each record a form.
* Add each form to a list of forms that is iterated over when templating using Jinja2.  Associate each form with an "edit" button.
* All contacts or deals are rendered as an "editable" table.
* Each form has a  "remove" button.

#### Update

*Endpoints: /edit_contact/<contact_id> and /edit_deal/<deal_id>*

* Each record is rendered as a form element and associated with its own edit button.
* When a user clicks this button, the form is submitted to the relevant edit endpoint and includes the relevant record id.
* The record in MySQL that matches that ID is updated with the form data.

#### Delete

*Endpoints: /remove_contact/<contact_id> and /remove_deal/<deal_id>*

* Each record is rendered as a form element and associated with its own remove button.
* Each row is associated with its own "remove" button.
* When a user clicks this button, the form is submitted to the relevant edit endpoint and includes the relevant record id.
* The record in MySQL that matches that ID is deleted.

### Reseting a User's Authenticated Session

*Implementation of requirement: 7*

*endpoint: /profile*

* If a user sends a GET request to this endpoint they are served a page with basic account information.
* If they submit a POST request, their flask session is cleared and they are redirected to the login page for all subsequent requests.

### Viewing Team and Leaving Team

*Implementation of requirement: 8*
*endpoint: /team*

* If a user sends a GET request to the team endpoint. The database is queried to retrieve all User rows with the same team_id as the user. This data is displayed in the HTML to the user.
* A form is on the page, if the user submits the form with a "positive" checkbox, their team_id is set to NULL and these changes are committed to the database.

### Viewing Databases in Pages

*Implementation of requirement: 9*

When the user visits */contacts* or */deals* to view the given virtual database -  Sherpa determines which page the user is currently viewing which is tracked in a session variable (starts off as the first page).

Each page displays 25 records. Once the current page is determined, the code calculates the starting and ending indexes of the records to display on that page.  For example, if the user is on page 3, the starting index would be 50 (2 * 25) and the ending index would be 74 (50 + 24).

Sherpa then selects the records between the starting and ending indexes and serves these as HTML. The HTML also includes "next" and "previous" page buttons that are encoded with the current page number, allowing the user to navigate the pages.

![Flowchart depicting how Sherpa's paging feature works](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/viewing_database_flowchart.jpeg)
<br>*Figure: 11*

### Showing the User the Records they Own

*Implementation of requirement: 10*
*endpoint: /contacts and /deals*

* Team admins can assign users as owners of contacts or deals using the forms.
* If a user clicks "My Contacts" or "My Deals", instead of issuing the normal select query - the /contacts and /deals endpoints modify this query to select for just those records with an "owner_id" equal to the "user_id" of the user making the request.
* The user is then shown all the records they have ownership of.

### Searching a Database

*Implementation of requirement: 11*

* When a user submits a POST request to */contacts* or */deals* using the search button form, their search term is fetched from the form data.
* This search term is then passed to an optimize_search() function that uses regular expressions to determine what the user is likely to be searching for. For example, if "@" is in the search term - the user is likely searching for a particular email. The function then returns the column it recommends to search.
* The contacts returned from the database are filtered for just those that match the user's search term using a "LIKE %{search_term}%" select query. This will be limited to a specific column if optimize_search recommended one, but will otherwise require a full row * column traversal.
* The user is then served the records that match their search term as part of the HTTP response.

![Flowchart representing how Sherpa's search feature looks through the database. ](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/searching_database_flowchart.png)
<br>*Figure: 12*

### Sorting a Database

*Implementation of requirement: 12*

* Sherpa code allows the user to sort a list of contacts/deals in a database based on different columns e.g. name. 
* When a user views a contacts or deals page, each column header in the table they are served is actually a hyperlink which points to */contacts* or */deals*. When a user clicks one of these links, they send a request to the relevant endpoint specifying they wish the data to be returned to them again but sorted by that column.
* Both ascending and descending sorting are supported. This is supported by the "prev_sort" and "sort" parameters which are passed to the hyperlinks, if the endpoint sees "prev_sort" and "sort" both equal "name", it knows the user has toggled the sort direction, and will check the "order" parameter and flip it i.e. if "order" is equal to "ASC" in this event, it will be changed to "DESC".
* The user is then served the data as part of the HTTP response as normal except the select query now includes a "ORDER BY" clause with the appropriate column and order.

![Flowchart representing how Sherpa's sorting feature sorts the database.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/sorting_flowchart.png)
<br>*Figure: 13*

### Activity Feature

*Implementation of requirement: 13*
*endpoint:/contact/<contact_id>/activity*

![Screenshot of Sherpa's Google Meet Integration](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Screenshot%20from%202023-03-10%2012-21-22.png)
<br>*Figure 14: Sherpa's Activity Feature*

* There are several "activity types" in Sherpa e.g. sending an email, marking a task as complete etc. 
* Whenever such a contact interaction occurs a log_activity() function occurs which records the metadata of the activity e.g. the team member responsible, a description, the timestamp etc.
* When a user visits the "activity" section for a particular contact, Sherpa fetches all of the activities associated with that contact and displays them to the user - in the order of most recent activity - as part of the HTML.

### Notes Feature

*Implementation of requirement: 14*
*endpoint:/contact/<contact_id>/notes*

![Screenshot of Sherpa's notes page.](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/notes_screenshot.png)
<br>*Figure 15: Sherpa's Notes Feature*

* When a user submits a POST request to this endpoint using the notes form, Sherpa fetches the contents of the note from the form data and creates and inserts it into a new instance of the notes data model, which is then inserted into the database along with the user's id.
* When a user sends a GET request to this endpoint, all notes associated with the contact are returned as part of the HTTP response.

### Integrating Google Accounts

*Implementation of requirement: 15*

*endpoint: /authorize_email*

The following diagram details the process of integrating Google with a Sherpa account.

![Diagram detailing the retrieval of a Google session token. Image is sourced from  "https://developers.google.com/identity/protocols/oauth2"](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/google_auth.png)
<br>*Figure: 16: Diagram of session token retrieval*

Google accounts are authenticated using OAuth 2.0. If you'd like to learn more about OAuth 2.0 please click [here](https://developers.google.com/identity/protocols/oauth2).

### Parsing API Responses

*Implementation of requirements: 16-18*

Sherpa integrates several Google products, each with their own API. The following is a flow chart detailing the process flow in Sherpa of dealing with an API response from request to return.

![Flowing Chart depicting how Sherpa parses API responses](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Parsing.png)
<br>*Figure: 17:*
 - First a GET request is sent to the relevant Google API endpoint. This request includes a "query" which specifies which data the request is concerned with. For example, the query for getting emails is "from: {contact_email} OR to: {contact_email}" i.e. fetch any email sent to the contact AND any email received from the contact.
 - The server then returns the data as a JSON dump which can be interacted with as a collection of python data structures.
 - Sherpa initialises an empty list to which all the parsed objects will be appended. It then iterates over the JSON dump. Each loop, it initialises an empty dictionary with relevant keys e.g. for an email "subject", etc and maps these keys to the relevant data. This parsed object is then appended to the parsed list.
 - Often timestamps aren't in human readable format so this required working with functions like "strftime" for timestamp conversion.
 - The list is returned to the endpoint that called the given parsing function and is templated as HTML using Jinja2. This is how this templating works for meetings:

```
{% if meetings is not none %}
        {% for meeting in meetings %}
            <section>
                <p><b>Summary:</b> {{ meeting["summary"] }}</p>
                <p><b>Description:</b> {{ meeting["description"] }}</p>
                <p><b>Starts:</b> {{ meeting["starts"] }}</p>
                <p><b>Ends:</b> {{ meeting["ends"] }}</p>
                <a href="{{meeting['link']}}">Join google meet</a>
            </section>
{% endfor %}
{% endif %}
``` 

### Sending and Receiving Emails

*Implementation of requirement: 16*

*endpoint: /contact/<contact_id>/emails*


![Screenshot of Sherpa's Google Gmail Integration](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/gmail_screenshot.png)
<br>*Figure 18: Sherpa's Gmail Integration*

#### Sending Emails

* Sherpa initialises a MIMEText object called "message". 
* The message's subject and body are fetched from the email form. 
* The sender is the user's Gmail. The recipient is the contact's email.
* Sherpa then sends a POST request to the Gmail API with the message encoded as JSON (with their OAuth token).
* The email is then sent from the user's Gmail.

#### Receiving Emails

* Sherpa sends a GET request to the Gmail API to fetch the IDs of all the user's email threads between them and the contact.
* Sherpa then loops through each thread, sending a GET request to fetch the emails for each thread.
* These emails are then parsed and included in the HTTP response.

### Creating, Viewing, and Completing Tasks

*Implementation of requirement: 17*

*endpoint: /contact/<contact_id>/tasks*

![Screenshot of Sherpa's Google Meet Integration](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Task_Screenshot.png)
<br>*Figure 19: Sherpa's Google Tasks Integration*

#### Creating Tasks

* Each task in Google Calendar must be part of a "task list". If its the user's first time creating a task for a contact, Sherpa sends a POST request to the Calendar API to create a task list for the contact.
* Sherpa sends a POST request to the Google Calendar API to create a new task. Due date and title are fetched from the task form data.
* The task then appears in the user's calendar on the due date.

#### Viewing Tasks

* Sherpa sends a GET request to the Google Calendar API to fetch all of the user's task lists. It then iterates over each list until it finds the one specific to this Sherpa contact.
* Sherpa then parses each task in this list.
* The tasks are then split up into "past due", "due", and "completed". Each task (except completed tasks) are templated with a "complete" button.

#### Completing Tasks

* If a user sends a request to the endpoint /contact/<contact_id>/tasks/<complete> then a PUT request is sent to the Google Calendar API to mark the task with the given task_id as completed.
* The task will then appear as "completed" in the user's calendar.

### Scheduling and Joining Meetings

*Implementation of requirement: 18*

*endpoint: /contact/<contact_id>/meetings*

![Screenshot of Sherpa's Google Meet Integration](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Mail_Screenshot.png)
<br>*Figure 20: Sherpa's Google Meet Integration*

* To schedule a meeting, Sherpa fetches the meeting details e.g. start time, from the meeting form data and sends a POST request to the Google Calendar API. The contact's email is an "attendee" for the conference; they receive an email invite and it appears in their calendar.
* Certain parameters must be set in the body of the request to have Google Calendar automatically create a Google Meet Conference e.g. *"conferenceDataVersion": 1*.
* To join meetings, Sherpa fetches all events from the user's calendar that has the contact's email as an "attendee" using a GET request to the Google Calendar API. These events are parsed and returned as part of the HTTP response - each meeting is accompanied by a "join meeting" button with the href set to the google meet link returned in the API response.

### Closing Deals

*Implementation of requirement: 19*

When a user sets the stage of a deal to "closed won", they must specify the closed amount, this is ensured by validating the form data. If no closed amount is included, the user will be informed of their mistake with an error message.

### Tracking Deal Conversions

*Implementation of requirement: 22*

* The Deal Stage Conversion table which logs the transition of deals from stage to stage is used to retrieve all deal stage data from the previous month. 
* This is then used to count the number of deals that were in each stage and stored as a dictionary with the stage as the key and the number of occurrences of the stage in the retrieved data as the value.
* Then for each stage, the conversions are calculated as follows:
	*  Next Step Conversion = Number of deals in next stage / Number of Deals in current stage
	* Cumulative Conversion = Number of deals in next stage / Number of Deals in first stage

### Creating Data Analytics Plots

*Implementation of requirement: 20, 21, 23, 24*


The following chart details the process of creating the plots for the analytics dashboard.

![Diagram the process of create a plot diagram](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/plots.png)
<br>*Figure 21: Diagram detailing the create plot diagram*
### Serving Plots
![Screenshot of Sherpa's analytics dashboard](https://raw.githubusercontent.com/mattmallencode/crm/main/report_images/Analysis.png)
<br>*Figure 22: Sherpa's Data Analytics Dashboard*

*Implementation of requirement: 25*

* When a plot is ready, Sherpa initialises an in-memory bytes buffer.
* Then the plot figure is saved as a PNG in this new buffer.
* Then the data in the buffer is encoding using base64 encoding.
* This encoded data is included in the HTTP response as part of an "img" element.

## Testing

Rather than going through each test case, this section deals with the more interesting aspects of Sherpa's test suite i.e. how it overcomes the challenges unique to testing a web application.

### Test Client Set Up

Flask has a "test_client()" method which simulates requests without needing to run a web server. However, this test client needs access to the "application context" which is a container that holds database connections etc. Before we create a test client, we need to pass the application context to it.

This is achieved with Sherpa's "application factory" which creates an application instance, loads the application's configuration and returns the instance. Sherpa's application factory and test client are both ran as Pytest fixtures. Fixtures are just reusable code that can be passed to test functions and run before each test.

### Simulating API Responses

Third party API integrations are problematic for testing. It is infeasible to send the many "junk" requests to API servers that testing requires. The use of "monkeypatch" proved necessary.  Monkeypatch allows one to force an API endpoint to return a predefined test response. Sherpa patches the "get" response for google oAuth authenticationas follows:

```
user = MockResponse({"google_email": "sherpalecturer@gmail.com"})
monkeypatch.setattr("flask_oauthlib.client.OAuthRemoteApp.get", lambda  self, userinfo: user)
```

## Project Reflection

This chapter will serve as a reflection on how we worked as a team, the challenges we faced, and the lessons we learned.

### Process
- We did all our work together for 3 hours each week day.
- Each week we wrote user stories on a whiteboard, assigned them to members of the team to implement, and took pictures at the end of each session.
- Each second week was “polishing” week. Normally three of us would do back-end work, and one front-end, but during polish week each of us would have a different job: report writing, testing, front-end, or back-end.
- Each polishing week one would have a different role to ensure more even contributions across the project.

### Challenges and Trade-Offs

-   **Turbo**:  Turbo is a JavaScript framework for serving page updates over a web-socket rather than a HTTP request. We wanted to implement this to have native-app-like performance. However Flask-Turbo was poorly documented, so due to time constraints we made the trade-off to only implement it for some pages to deal with other priorities.
-   **Google Integration**: Google integration was challenging as OAuth is a very complicated protocol none of us had experience with. Furthermore, Flask-OAuthlib did not support Gmail out of the box which required us to write code for the module to add support for it.
-   **Testing**: As described in the testing section, testing web applications poses unique challenges and we only had software testing experience with closed systems. A trade-off we had to make here was whether to use unittest or pytest for our testing framework, we all only had experience with unittest but opted for pytest as the documentation for using it with Flask was far more extensive. Despite the greater initial learning curve, this made debugging testing issues far easier.

### Lessons Learned

* We should have wrote more standardised and semantic HTML. This led to consistency issues and made CSS work more difficult, in the future we'd definitely place an emphasis on best-practice, semantic HTML.
* Our application should have been modular from the beginning, the project inevitably grew to large in scope for a single file and it wasted time having to do this mid-development.
* A CSS framework, e.g. Bootstrap, would have made front-end development much faster, having to write all our styles from scratch added an unnecessary technical overhead - one we would avoid if we were to do things over.
