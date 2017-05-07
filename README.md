# WatchDog

A powerful generic watchdog
Currently it's still a Work In Progress - First version will be released soon enough

# Motivation

Almost every application nowdays requires an external watchdog to monitor its activity.

As most of these watchdogs share the same common architecture and functionality,
it was natural to write a single configurable application that will might spare some developers time and effort in the future.

# Design

This WatchDog application is written in Python 2.*
It will support running in the background as a Windows Service or a Unix Daemon.
Every once an in a while (configurable period of time) it will perform the following steps:

- Check if the target (watched) application is alive. If not, it will handle it
- Check if the target uses too much memory (configurable). If it is, it will handle it
- Check if the target is using too much CPU (configurable). If it is, it will handle it

Handle it means that you can configure the WatchDog to do a certain configurable set of options, e.g. stop/start/restart/alert

# Configuration

The application requires a single configuration file in JSON format to operate.
The JSON is split into segments according to the internal modules of the app.

## Investigator configuration

This module is responsible for spotting any active targets running on the system,
and analyzing the amount of resources these applications are using.

### Target spotter configuration

The target spotter can identify running targets using multiple parameters.
Its configuration is the value of the "target" key.
Just specify any of the following keys and the desired values to filter according
to that parameter.
A process is considered our target if it matches all the specified filters.

- name: The process' name
- exe: The process' executable absolute path
- cmdline: The process' command line arguments (Array).
             Note: If the process has no arguments except for argv0, you should 
             specify an additional empty string arg
- cwd: The process' current working directory
- username: The process' real owner uid

### Memory probe configuration

The memory probe examines the target's memory usage.
Its configuration is the value of the "memory" key.
The examination is configured using these parameters:

- threshold: The maximal amount of memory (in bytes) the target is allowed to use
             DEFAULT: 500000000 (500MB)
- period: The sampling period. Use 0 to sample once.
          A value of 'n' stands for 'n+1' samples, 1 second apart from each other.
          DEFAULT: 0
- set: The memory set to examine, supported values are: rss, vms, uss, pss
       DEFAULT: uss

### CPU probe configuration

The CPU probe examines the target's CPU usage.
Its configuration is the value of the "CPU" key.
The examination is configured using these parameters:

- threshold: The maximal amount of CPU the target is allowed to use.
             Note: On a machine with 4 CPUs an app can reach 400% CPU usage.
             DEFAULT: 95%
- period: The sampling period. Use 0 to sample once.
          A value of 'n' stands for 'n+1' samples, 1 second apart from each other.
          DEFAULT: 4 (5 sampling points, 1 second apart)