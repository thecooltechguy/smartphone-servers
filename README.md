## smartphone-servers
This is the landing page for the Cell Phone Data Center project. The structure of this GitHub repo is as follows:

### I. Project Overview
**Motivation** Our project is motivated by the excess of smartphone E-waste. 150 million phones discarded each year in the US alone, many before they need to be; despite their nominal 10-year lifespan, most phones are discarded within a year or two. This is especially problematic because these devices are difficult to recycle. Because of their specialized construction (and classification as hazardous waste) they can't simply be thrown into a traditional recycling bin. And even when smartphones do make their way to an E-waste recycling facility, these are oftentimes unregulated, employing child labor and exposing workers to hazardous chemicals.

For our 237D final project, we take an alternate approach: Expanding the lifetime of discarded smartphones by reusing them for general computational tasks. Previous work has indicated the feasibility of this approach, but many systems challenges remain. For our 237D class project, we explore these challenges by designing and constructing our own cell phone data center. Our overall goal is to evaluate the feasibility of reusing smartphones as general-purpose cloud servers.

**Overview** Our cell phone data center consists of three main components: the phone bank itself, a collection of used cell phones; a smartplug-enabled power strip, which allows power to the phones to be toggled on and off remotely; and a central management device, which is responsible for managing power and distributing tasks among the phones. 

The management device receives incoming job submissions, and distributes them amongst the phones. The actual computations themselves are performed on the phones themselves. To evaluate our system, we test it on a variety of common computational tasks, such as factoring large prime numbers. We package all of these components together into a 3D-printed chassis, the designs for which we also make public.

### II. Team Members
**Subhash Ramesh**
**Eric Siu**
**Emanoel Zadorian**
**Ruohan Hu**
**Jennifer Switzer**

### III. 237D Class Materials
Reports and presentations can be found in the `reports` folder.

Our mid-semester demo videos can be found here:
1. Overall demo -- https://youtu.be/TaK98wkG5LY
2. Power management demo -- https://youtu.be/Mx6LJpP9_fM

### IV. Documentation
Documentation, including guidelines for reproducing our work, can be found in the wiki.
