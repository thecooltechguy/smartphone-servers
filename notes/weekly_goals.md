## Week 9 : May 22 -- First half (e.g. todos for Wednesday)
Jen: Finish landing page, clean up wiki \
Subhash/Eric: Add Quickstart + Wyze pages, Subhash add new test files \
Emmanuel: Upload stl files/instructions for box, add page to Wiki \
Ruohan: Change some phone logic to match the task team 
## Week 8 : May 15
All: Work on written report \
Jen: Record the smartplug functionality, set up 1-2 new phones, clean up the ut documentation, meet w/Ruohan to benchmark, print labels for phones \
Ruohan: Repartition phone, meet w/Jen to benchmark, add logic to check exit code, implement time out \
Ruohan/Jen: Send heartbeats more often (every 3s), fill in the information for heartbeats, try docker again, unique identifiers \
Emmanuel: Print the box, try Android rooting \
Subhash (Normal Process):
- Use only phones that are 'healthy', prioritize phone with lowest cpu use
- Have a 'cancel process' message type
- Have unique identifiers for phones 

Eric (Abnormal Process):
- Be able to reschedule a job if it expires/implement time out
- Have logic for cutting power to phone that's misbehaving
## Week 6 : May 1
### Mobile team
Ruohan: Receiving and running tasks (coordinate with task management team) \
Jen: Figure out apt-get cache issue; determine if we can do docker/sysbench; fill in battery status, cpu use, disk use for heartbeats; add SD to phone.
### Task Management team
Subhash: Finish end points for updating job status, integrate with socket-io \
Eric: Integrating with socket-io
### Benchmarking
Emmanuel: Make example git or docker images, get/set up phone from Jen, [optionally] build the box
## Week 5 : April 24
Overall goal: Implement and test job submission, job delegation, and job acknowledgment functionality
### Mobile team
0. Set up our workflow for the phones
1. Figure out the ut api for battery level, etc. and add it to heartbeats (with hardcoded ip)
2. Implement tasks
3. Determine if phone can accept push notifications/otherwise how to manage communications instantiated by the raspberry pi (websockets potentially)
### Task management team
1. Integrate Smart Plug code into existing server code
2. Implement sending tasks to phones
3. Implement receiving a response from one of the phones and updating the state of each phone on a local database on the Pi
4. Figure out and implement algorithms to distribute jobs based on phone states (for now it will be simple, will add more in later weeks)
### Benchmarking team a.k.a. Emmanuel
1. ...
### Integration (Jen)
1. Set up the testbench

## Week 4 : April 17 
Overall goal: Have heartbeats implemented, determine if we can run docker on ubuntu touch, pick 3-4 example applications
### Mobile team
1. Determine if Docker will work on Ubuntu Touch (or another type of container) 
2. Implement the sending of heartbeats
### Task management team
1. Implement the receiving of heartbeats 
2. Connect to the smartplugs to turn them ON/OFF
### Benchmarking team a.k.a. Emmanuel
1. Come up with a list of 4 example applications (don't need code yet, can be conceptual) 
