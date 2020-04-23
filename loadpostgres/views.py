from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import threading
import time
import psycopg2
from datetime import date



def index(request):
    if request.method == 'GET':
        filename = request.GET["filename"]
        t = threading.Thread(target=long_process,
                            args=filename)
        t.setDaemon(True)
        t.start()
        
        
        
        return render(request, 'loaded.html', {})
    else:
        return render(request, 'unload.html', {})

    
def long_process(ins):
    filename = ins
    filelocation='gs://shpgee/'+filename+'.tif'
    download_gs='gsutil cp '+filelocation+'  D:/django/cropcalendar/download/'
    time.sleep(1800)
    stream = os.popen(download_gs)
    local_file=r' D:/django/cropcalendar/download/'+filename+'.tif'
    uploadpostgres='raster2pgsql -s 2037 -c -I  '+ local_file+'  '+filename+' |psql "postgres://postgres:PASS@127.0.0.1:5432/postgres"'
    stream2 = os.popen(uploadpostgres)
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="PASS",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="postgres")
        cursor = connection.cursor()
        today = date.today().strftime("%m-%d-%Y")
        postgres_insert_query = """ INSERT INTO image_record (Time, Name, USER) VALUES (%s,%s,%s)"""
        record_to_insert = (today, filename, 'default')
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        #print (count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")


