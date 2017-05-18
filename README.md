# Bulldog

A powerful & portable generic watchdog application.

Currently it's still a Work In Progress - First version will be released soon enough!

# Motivation

Almost every application nowdays requires an external watchdog to monitor its activity.

As most of these watchdogs share the same common architecture and functionality,
it was natural to write a single configurable application that will might spare some developers time and effort in the future.

# Design

This watchdog application is written in Python 2.*
It will support running in the background as a Windows Service or a Unix Daemon.
Every once an in a while (configurable period of time) it will perform the following steps:

- Check if the target (watched) application is alive. If not, it will handle it
- Check if the target uses too much memory (configurable). If it is, it will handle it
- Check if the target is using too much CPU (configurable). If it is, it will handle it

Handle it means that you can configure the watchdog to do a certain configurable set of options, e.g. stop/start/restart/alert

# Packages

You can choose to use one of the following ways to distribute this application:

- Integrate this code into your existing application
- Create a binary executable by running `generate.sh` from inside the `bin` directory
- Craete *.rpm and *.deb packages by running `pack.sh` from the root directory

# Configuration

The application requires a single configuration file in JSON format to operate.
The JSON is split into segments according to the internal modules of the app.

## Configuration format

The configuration file is a single JSON object.
This root JSON object may contain multiple keys.
Each key is an custom name for an application we want to watch,
and the value for this key, is the configuration we should use for watching this application.
The keys have not formatting requirements whatsoever.

```
{
    "app1": {
        // Here comes the configuration for app1's watchdog
    },
    "app2": {
        // Here comes the configuration for app2's watchdog
    },
    ...
    "appN": {
        // Here comes the configuration for appN's watchdog
    }
}
```

Each of the watchdogs is configured in a modular manner.
The watchdog is comprised of multiple components, each configured seperately:

```
{
    "handler": {
        // Here comes the handler's configuration
    },
    "inspector": {
        // Here comes the inspector's configuration
    },
    "cycler": {
        // Here comes the cycler's configuration
    }
}
```

See the following sub-chapters to understand each component configuration.

## Handler configuration

The handler is the internal component that handles the actual actions taken, e.g. stop/start the target application.
Currently, the handler supports only three actions: stop, start & restart.

### Start action

In order to start the target application, the watchdog must be able to execute it.
To do so, it neets to receive two configuration parameters: cmd and args.
The configuration for the start command is nested under the handler's configuration and looks like this:

```
"handler": {
    "start": {
        "cmd": "/path/to/app/exec",
        "args": [ "arg1", ... ]
    }
}
```

### Stop action

The watchdog can stop the target application using two different ways.

- It can send a kill signal to the process using its pid
- It can execute a specific kill command specified in the configuration

If you do not specify any stop configuration under the handler's configuration, the watchdog will use the first method.
If you wish to specify a custom configuration, just use the following format (which is the same as the one for start):

```
"handler": {
    "start": {
        // Some start configuration
    }, 
    "stop": {
        "cmd": "/path/to/killer/exec",
        "args": [ "arg1", ... ]
    }
}
```

### Restart action

Since a restart is merely a stop -> start sequence, there is no specific configuration for the restart command.

## Inspector configuration

This module is responsible for spotting any active targets running on the system,
and analyzing the amount of resources these applications are using.
The inspector can perform multiple checks, each configured seperately:

```
"inspector": {
    "target": {
        // REQUIRED: target spotter configuration, see relevant sub-chapter
    },
    "memory" {
        // REQUIRED: memory probe configuration, see relevant sub-chapter
    },
    "cpu": {
        // REQUIRED: CPU probe configuration, see relevant sub-chapter
    }
}
```

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

Example:

```
"target": {
    "exe": "/bin/nc",
    "cmdline": ["nc", "-vl", "9000"],
    "username": "root"
}
```

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

Example:

```
"memory": {
    "threshold": 100000000,
    "period": 1,
    "set": "uss"
}
```

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

Example:

```
"cpu": {
    "threshold": 80,
    "period": 2
}
```