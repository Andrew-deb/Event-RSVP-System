# Event-RSVP-System

## Core backend Knowledge showing how the data flows through the system

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────┐
│  🔵 REQUEST     │    │  📋 INPUT        │    │  🗄️ ORM         │    │  🐘 DATABASE │
│                 │    │    SCHEMA        │    │  (SQLAlchemy)   │    │  (Postgres)  │
│ Raw HTTP Data   │───→│ Validation &     │───→│ Python Objects  │───→│ SQL Storage  │
│ (JSON/Form)     │    │ Deserialization  │    │ (Model Instance)│    │ & Queries    │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────┘
                                                                              │
                                                                              │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐         │
│  🟢 RESPONSE    │    │  📋 OUTPUT       │    │  🗄️ ORM         │         │
│                 │    │    SCHEMA        │    │  (SQLAlchemy)   │    ┌────┘
│ Formatted JSON  │←───│ Serialization &  │←───│ Records →       │←───┘
│ To Client       │    │ JSON Formatting  │    │ Python Objects  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```


### Component Breakdown

**🔵 Request** - The incoming HTTP request from the client containing raw JSON or form data.

**📋 Schema (API Input)** - Pydantic schema that validates and deserializes the request data, ensuring it matches expected types and constraints.

**🗄️ ORM (SQLAlchemy)** - The Python object-relational mapper that converts validated data into SQLAlchemy model instances before persisting to the database.

**🐘 Database (Postgres)** - The PostgreSQL database where data is stored, retrieved, and managed with SQL transactions.

**🗄️ ORM (SQLAlchemy)** - Converts raw database records back into Python model instances so the application can work with objects instead of raw SQL rows.

**📋 Schema (API Output)** - Pydantic schema that serializes the ORM model objects into JSON-compatible format, filtering/formatting data for the response.

**🟢 Response** - The final HTTP response sent back to the client with properly formatted JSON data.


### File Layers and their responsibility
| Layer    | Responsibility         |
| -------- | ---------------------- |
| Pydantic | Validate input         |
| Route    | Enforce business rules |
| DB       | Persist valid data     |



## Core Business Logic for the Event RSVP System

### User

A User represents a person who interacts with the RSVP system. Each user has a unique identity, can RSVP to events, and is tracked in the database with essential details.

| Column | Purpose |
|--------|---------|
| id | Identify the user uniquely |
| name | Display name of the user |
| email | Contact and login identifier |
| password | Secure authentication |
| role | Defines permissions (organizer, attendee, admin) |

**Roles:**
- **Organizer** - Creates and manages events
- **Attendee** - RSVPs to events

### Events

An event is created by a User (Organizer).

| Column | Purpose |
|--------|---------|
| id | Identify the event uniquely |
| name | Display name of the event |
| date | Event date and time |
| location | Event location |
| organizer_id | Reference to organizing user |


### RSVP

This is how the suer responds to an Event. Core Logic here is that we create a many-to-many relationship using the user.id and the event.id as a composite key to uniquely identify, who RSVP the event and what event was RSVPed.

**Rules:**

- A user can respond to an event only once
- An event can have many RSVPs
- If an event has a capacity, "going" RSVPs must not exceed capacity

| Field    | Why                       |
| -------- | ------------------------- |
| id       | Identify RSVP             |
| user_id  | Who is responding         |
| event_id | Which event               |
| status   | going / maybe / not_going |


**Logic:**

***RSVP POST Logic***
- The exact resource been acted upon is the Event while RSVP is action being carried out on this event.
- Since Event is the resource acted upon, event_id would be included in the path URL which is now used in identifying a particular event the RSVP belongs to.
- We did not include the event_id in the RSVP request body (which is simply the RSVPCreate pydantic model) because the event is the resource being acted on. The path /events/{event_id}/rsvp already tells the server which event the RSVP belongs to. Putting event_id in the body would duplicate that information and risk mismatches between path and body.
- **Why the route is prefixed as /events instead of /rsvp**: This is because RSVPs are not independent resources. They only exist because of an event and inside the context of an event following REST Hierarchy
- **Note:** 

    ❗Path parameters identify the resource (the event)

    ❗ Request body describes the action on that resource (the RSVP details)

***Capacity Logic***
- Only RSVPs with status "going" count toward event capacity.
- If the number of “going” RSVPs equals the event’s capacity, no more “going” RSVPs should be allowed.

Note:
- "maybe" ❌ does NOT count
- "not_going" ❌ does NOT count