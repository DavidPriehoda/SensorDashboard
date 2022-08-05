import mysql.connector, json, os
counter = 0
username = '' # studentnum
password = '' # database password (NOT LearningCentral Password)

#must be connected to cardiff VPN
#make sure table name is "data" for consistency
#make sure in same dir as unzipped sensor_data folder

mydb = mysql.connector.connect(
    host="csmysql.cs.cf.ac.uk",
    user=username,
    password=password
)

for filename in os.listdir("sensor_data"):
    with open("sensor_data/" + filename, "r") as read_file:
        data = json.load(read_file)

    mycursor = mydb.cursor()

    for d in data:
        sql = f"INSERT INTO {username}_homesensors.data ("
        sql2 = " VALUES ("
        for key in d:
            sql = sql + key + ", "
            value = d[key]
            #clean data
            if value == "": value = "null"  # must provide val
            elif value[len(value) - 1] == ".": value = value[0:len(value) - 1]  # remove trailing full stops

            # strings got to be in ''
            try:
                float(value)
                sql2 = sql2 + value + ", "  # appends keys to values line
            except ValueError:  # not a float
                if value != "null":
                    sql2 = sql2 + "'" + value + "'" + ", "  # appends keys to values line
                else:
                    sql2 = sql2 + value + ", "  # appends keys to values line

        sql = ")".join(sql.rsplit(", ", 1))  # replace trailing commas with );
        sql2 = ");".join(sql2.rsplit(", ", 1))  # replace trailing commas with );
        statement = sql + sql2
        counter += 1
        print("Executing statement " + str(counter) + ":" + statement)
        mycursor.execute(statement)

    print(mycursor.rowcount, "record inserted.")

mydb.commit()
