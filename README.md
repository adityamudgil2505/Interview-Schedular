# Interview-Schedular
A simple application where we can create interview by entering participant emails (for interview and candidate), interview start time, and duration in minutes.

## Criteria
- Throw message when 
  - any participant is not available during schedule time (that is has another interview)
  - Number of participant less than 2
  - Any email not present in user database

## Features
- Admin can see schedule of all interviews.
- Admin can add and can also edit any interview.

## Database Schema
- Table 1 user
  - user_id: int
  - email_id: text
- Table 2 interview
  - interview_id: int
  - start_time: int
  - end_time: int
  - interviewer_id: text
- Table 3 candidates
  - interview_id: int
  - candidate_id: text

## Skills used
- HTML
- Flask
- Sqlite

## Screenshots
### Home Screen
![alt Home Screen](/ScreenShots/1.png)
### Add Interview Screen
![alt Add Interview Screen](/ScreenShots/2.png)
### View all Interview Schedule Screen
![alt View all Interview Schedule Screen](/ScreenShots/3.png)
### Edit Interview Screen
![alt Edit Interview Screen](/ScreenShots/4.png)
### Message Screen
![alt Message Screen](/ScreenShots/5.png)
