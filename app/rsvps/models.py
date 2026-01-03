# from pydantic import BaseModel
# from enum import Enum

# # Define RSVP status options
# class RSVPStatus(str, Enum):
#     going = "going"
#     not_going = "not_going"
#     maybe = "maybe"

# class RSVPCreate(BaseModel):
#     user_id: int
#     event_id: int
#     status: RSVPStatus   # client must send one of the allowed statuses

# class RSVPResponse(BaseModel):
#     id: int
#     user_id: int
#     event_id: int
#     status: RSVPStatus   # response will show the chosen status
