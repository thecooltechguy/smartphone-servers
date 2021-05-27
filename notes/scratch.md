Place to put internal notes / scratch to be cleaned up before webpresence deadline

# 5-4 Milestone report
A place to organize our thoughts for the meeting with Ryan.

# Current state
## Phones
## Task Management

- Power plugs have been fully integrated into the codebase (setup instructions in README.md)
- Phone to Server communication implemented via SocketIO
- Simple random task assignment implemented for MVP

## Benchmarking
## Construction
## Integration

# Left to do for MVP

## Meeting outline

### MVP
Send a sample job from the raspberry pi to a phone, which the phone will download and execute. The sample job will be a simple python script that adds two numbers.

### Milestones
- Raspberry pi controlling the smart plugs for managing device power - DONE
- Phones sending heartbeats to the Raspberry Pi - DONE
- Phones running code from a URL - DONE
- Raspberry pi sending a job to a phone - IN PROGRESS
- User interface for submitting jobs to the Raspberry PI - IN PROGRESS
- Getting benchmark results with `sysbench` - IN PROGRESS
- Get benchmark results from running specific, standardized testing programs on the phones - IN PROGRESS
- Constructing a physical prototype where the Raspberry pi is connected to multiple phones - NOT STARTED
- Constructing the actual physical case housing the phones and the Raspberry Pi - NOT STARTED

### Deliverables
- Raspberry pi server (which handles device communication and task management/distribution among the devices)
- Client software running on the phones that communicates with the Pi server and runs submitted jobs
- Physical case to house the phones and Pi
- A benchmarking suite to test the performance & efficiency of our setup

### Schedule
- Original schedule estimated MVP by end of week 7, but we'll have it done by end of this week.
- In the next 2-3 weeks following that, we aim to finish our benchmarking suite and our physical case.
- If further time allows, we also aim to add fault-tolerance to the job scheduling, so that important jobs can run on multiple phones in case of device failure, support job retrying, etc.

# Links
## Put all relevant links 

### Course materials
Project specifications: https://www.overleaf.com/3254262872kdykmhqwkcbw

### Google drive
Google drive folder: https://drive.google.com/drive/folders/1seUEuyJ0AYfaMmjsHsWMcX0Nxt-EvhUo?usp=sharing

# Relevant Papers
https://journals.sagepub.com/doi/full/10.1177/0361198119845654

https://www.sciencedirect.com/science/article/pii/S2590116819300347

place to put ideas for use-cases

- http://www.ramanujanmachine.com/ (code that runs to auto discover new math discoveries, etc.). there is something similar for generic science i think but i forgot its name.
