import psycopg2, json



class DB:

    def __init__(self):

        self.conn = None
        self.cursor = None

    @classmethod
    def connect(self, type_connection:str,  con_dict:dict):
        # connect to the DB
        
        try:

            # creation of connection to DB local or remote.

            if type_connection == "local":
                self.conn = psycopg2.connect(
                    host = con_dict['host'],
                    database = con_dict['database'],
                    user = con_dict['user'],
                    password = con_dict['password']
                )
            elif type_connection == "remote":
                self.conn = psycopg2.connect(
                    host = con_dict['host'],
                    database = con_dict['database'],
                    user = con_dict['user'],
                    password = con_dict['password'],
                    port = con_dict['port']
                )
            else:
                raise ValueError("wrong type of connection was provided")

            # create cursor for future use
            self.cursor = self.conn.cursor()

        except psycopg2.InternalError:
            raise psycopg2.InternalError("Connection to DB failed")
        except KeyError:
            raise KeyError("Not all needed data was provided")
        except ValueError:
            raise ValueError("wrong type of connection was provided")
        except Exception as e:
            raise Exception(e)

    @classmethod
    def check_table(self, table_name:str) -> bool:
        # check if table exists
        
        self.cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
        exist = self.cursor.fetchone()[0]
        return False if not exist else True
    
    @classmethod
    def execute_change(self, sql:str, values:tuple = None):
        # execute sql query
        
        if values is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, values)
        self.conn.commit()

    @classmethod
    def check_create_table(self, table_name:str, sql:str):
        # check if table exists if not than create one

        if not self.check_table(table_name):
            self.execute_change(sql.replace('||', table_name))

    @classmethod
    def get_one_cell_record(self, config:dict) -> str:
        # get specific value from record based on filter 
        
        q = f"""SELECT ({config['return']}) FROM {config['table_name']} WHERE {config['filter']} = %s"""
        self.cursor.execute(q, (config['filter_value'], ))
        ret = self.cursor.fetchone()
        if ret:
            return ret[0]
        else:
            return None

    @classmethod
    def close(self):
        # close connection
        
        self.cursor.close()
        self.conn.close()


def read_config() -> list:
    # return json config
    
    with open("config.json", "r") as f:
        config = json.load(f)
    return [config['db_config'], config["job_config"]]

def input(path_to_file:str, path_to_data:str) -> list:
    # return input data
    
    with open(path_to_file, "r") as f:
        data = json.load(f)
    try:
        for key in path_to_data.split('/'):
            if key.isdigit():
                data = data[int(key)]
            else:
                data = data[key]
        return data
    except KeyError:
        raise KeyError("path for input data is incorect")
    except Exception as e:
        raise Exception(e)

def data_in(data:dict, config:list, pgAdmin:complex, table_name:str):
    # go through records and add them to DB
    
    for index in range(1, len(config) + 1):
        current_config = config[str(index)]
        for interface in data[current_config['name']]:
            name = f"{current_config['name']}{interface['name']}"

            try: description = interface["description"]
            except: description = ""

            try: max_frame_size = int(interface["mtu"])
            except: max_frame_size = None

            portchannel_id = None
            if 'connect' in current_config.keys() and current_config['connect']['is_required']:
                if current_config['connect']['json_key'] in interface.keys():
                    name_conn = f"{current_config['connect']['connect_name']}{interface[current_config['connect']['json_key']]['number']}"
                    reply =  pgAdmin.get_one_cell_record({"return": "id", "filter": "name", "filter_value": name_conn, "table_name": table_name})
                    if reply is not None:
                        portchannel_id = int(reply)
            sql = f"INSERT INTO table_name (name, description, max_frame_size, config, port_channel_id) VALUES (%s, %s, %s, %s, %s);"
            pgAdmin.execute_change(sql, (name, description, max_frame_size, json.dumps(interface), portchannel_id, ))
            print(f'Record {name} added to the DB')

def main():
    # main code

    [conn_list, config] = read_config()

    pgAdmin = DB
    pgAdmin.connect(config["db"]["type_connection"], conn_list)

    pgAdmin.check_create_table(config["db"]["table_name"], config["db"]["table_sql"])



    data = input(config["input"]["path_to_file"], config["input"]["path_to_data"])

    data_in(data, config["data_in_config"], pgAdmin, config["db"]["table_name"])

    pgAdmin.close()


if __name__ == "__main__":
    main()
