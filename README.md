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
