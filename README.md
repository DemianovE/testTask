# Test task

## Overview

This project is created to fulfill the test python task. The solution contains python code and json configuration file.

## PYTHON

Python code represents class/function implementation. Class is used for connection and manipulation with DB and functions are used for data manipulations and main algorithm. The code is made as such so it in combination with configuration can be versatile and does not depend on hardcoded structure.

## Configuration

- `db_config`: configurations for the DB manipulations
  - `host`: DB host 
  - `database`: DB name
  - `user`: DB user
  - `password`: DB password
  - `port`: DB port
- `job_config`: configuration for this run
  - `db`: all db-related run configurations
    - `type_connection`: can be local or remote
    - `table_sql`: SQL to create a table if it is not already in DB
    - `table_name`: DB table which will be used
  - `input`: input data configurations
    - `path_to_file`: path to the json file
    - `path_to_data`: path to the data we need inside of the json (an example is below)
  - `data_in_config`: main config for data manipulations
    - `1`: the number represents the priority in which code will work with this type
      - `name`: name of the interface
      - `connect`: optional DICT which is used to configure getting IDs for port_channel_id in this task
        - `is_required`: can be true or false
        - `connect_name`: name of the interface to which this interface is connected (example below)
        - `json_key`: path in the json to the value of the interface name

To customize the behavior of the code and add new interfaces to the process you can modify the values in the `config.json` file. Here's an example of how the `config.json` file might look:
```json
{
    "db_config": {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "1234",
        "port": "5432"
    },
    "job_config": {
        "db": {
            "type_connection": "local",
            "table_sql": "CREATE TABLE || (id SERIAL PRIMARY KEY,connection INTEGER, name VARCHAR(255) NOT NULL,description VARCHAR(255),config json, type VARCHAR(50), infra_type VARCHAR(50), port_channel_id INTEGER,max_frame_size INTEGER)",
            "table_name": "table_name"
        },
        "input": {
            "path_to_file": "C:/pathconfigClear_v2.json",
            "path_to_data": "frinx-uniconfig-topology:configuration/Cisco-IOS-XE-native:native/interface"
        },
        "data_in_config": {
            "1": {
                "name": "Port-channel"
            },
            "2": {
                "name": "TenGigabitEthernet",
                "connect":{
                  "is_required": true,
                  "connect_name": "Port-channel",
                  "json_key": "Cisco-IOS-XE-ethernet:channel-group"
                }
            },
            "3": {
                "name": "GigabitEthernet"
            }
        }
    }
}
