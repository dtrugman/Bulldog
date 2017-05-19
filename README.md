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

The configuration file is a single JSON object.
This root JSON object shoud contain exactly two keys:

- log: Holds the log infrastructure configuration
- watchdogs: Holds the configuration for the different watchdogs

```
{
    "log": {
        // REQUIRED: log infrastrucure configuration, see log section
    },
    "watchdogs": {
        // REQUIRED: configuration for the diffent watchdogs 
    }
}
```

## Log

The log infrastructure requires the following values:

- dir: The directory to write the log files to
- level: A numeric values specifying the threshold of the logger (See following list)

Example:

```
"log": {
    "dir": "/var/log/bulldog/",
    "level": 20
}
```

### Log dir

Just specify an absolute or relative path.

If you wish to write the log files to the same dir as the binary, just use "."

### Log level

The supported log levels are:

- 10 = DEBUG
- 20 = INFO
- 30 = WARNING
- 40 = ERROR
- 50 = CRITICAL

**The recommended value is 20 = INFO.**

## Watchdog

The watchdog configuration may contain multiple keys, each is a custom name for an application we want to watch,
and their respectful values are the configurations we should use for watching these applications.

The keys have no formatting restrictions.

```
watchdogs: {
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
"appN": {
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

See the following section to understand each component configuration.


### Handler

The handler is the internal component that handles the actual actions taken, e.g. stop/start the target application.
The amount of actions is unlimited, and each is fully configurable by the user.
Every action should have a unique name that identifies it.
Every action merely a command line that consists of a command and an array of arguments.

The only pre-programmed command is the 'stop' command. See the 'stop action' for more information.

#### Custom actions

Every action specified under the handler should have the following configuration:

```
"handler": {
    "command-name": {
        "cmd": "/path/to/exec",
        "args": [ "arg1", ... ]
    }
}
```

After defining a command, we can use it as an action in our different manifests.
For more info, see the cycler manifest section for more info.

#### Stop action

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

#### Restart action

Since a restart is merely a stop -> start sequence, there is no specific configuration for the restart command.

### Inspector

This module is responsible for spotting any active targets running on the system,
and analyzing the amount of resources these applications are using.
The inspector can perform multiple checks, each configured seperately:

```
"inspector": {
    "target": {
        // REQUIRED: target spotter configuration, see relevant section
    },
    "memory" {
        // OPTIONAL: memory probe configuration, see relevant section
    },
    "cpu": {
        // OPTIONAL: CPU probe configuration, see relevant section
    }
}
```

The target configuration is always required, because otherwise the watchdog will be oblivious to the target.
On the other hand, the different probes are optional, and don't require configuration if you don't use them.

#### Target spotter

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

#### Memory probe

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

#### CPU probe

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

### Cycler

The cycler is a basic time-based trigger.
Every time the cycler fires, the watchdog starts running checks and reacts according to the results.

The cycler has the following configurations:

- frequency: How often should the cycler fire a trigger (in seconds)
- manifest: How should the watchdog behave when an event is triggered, see the manifest section for more details

Example:

```
"cycler": {
    "freq": <value>,
    "manifest": {
        // The cycler event manifest
    }
}
```

#### Manifest

The manifest is an array of pairs.
Each pair consists of a array of checks and an array of reactions.

Example:

```
"manifest": [
    {
        "check": [ "check1", "check2" ],
        "reaction: [ "reaction1" ]
    },
    {
        "check": [ "check1", "check3" ],
        "reaction: [ "reaction9" ]
    },
    {
        "check": [ "check2" ],
        "reaction": [ "reaction2", "reaction17" ]
    }
]
```

Every check triggers an action from the Inspector (see the Inspector chapter for more information).
Currently, the supported checks are:

- running: Checks if the target is running, and if not, triggers the specified reactions
- memory: Checks the target's memory according to the memory probe's constrains. If the target misbehaves, triggers the specified reactions
- cpu: Checks the target's CPU usage according to the CPU probe's constrains. If the target misbehaves, triggers the specified reactions

The reaction on the other hand are very customizable, and may vary according to your needs.
Every Handler action defined may be used as a reaction (see the Handler chapter for more information).