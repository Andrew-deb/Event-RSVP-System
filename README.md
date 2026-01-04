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

### Component Breakdown

**🔵 Request** - The incoming HTTP request from the client containing raw JSON or form data.

**📋 Schema (API Input)** - Pydantic schema that validates and deserializes the request data, ensuring it matches expected types and constraints.

**🗄️ ORM (SQLAlchemy)** - The Python object-relational mapper that converts validated data into SQLAlchemy model instances before persisting to the database.

**🐘 Database (Postgres)** - The PostgreSQL database where data is stored, retrieved, and managed with SQL transactions.

**🗄️ ORM (SQLAlchemy)** - Converts raw database records back into Python model instances so the application can work with objects instead of raw SQL rows.

**📋 Schema (API Output)** - Pydantic schema that serializes the ORM model objects into JSON-compatible format, filtering/formatting data for the response.

**🟢 Response** - The final HTTP response sent back to the client with properly formatted JSON data.