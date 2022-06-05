# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 11:59:43 2022

@author: JIAN
"""
def upload ():
    
    '''#configuration values
    endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
    username = 'JZNYC'
    password = '58290273'
    database_name = 'buildingInfo' '''



    import pymysql

    #configuration values
    endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
    database_name = 'buildingInfo'
    username = str(input('PLEASE INPUT USERNAME: '))
    password = str(input('PLEASE INPUT PASSWORD: '))

    #S3 configuration values
    aws_access_key_id = 'Look in AWS'
    aws_secret_access_key = 'Look in AWS'


    #connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)


    #insert info
    cursor = connection.cursor()

    print('writing to the S3')
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    s3 = session.resource('s3')
    # Filename - File to upload
    # Bucket - Bucket to upload to (the top level directory under AWS S3)
    # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
    s3.meta.client.upload_file(Filename='input_file_path', Bucket='bucket_name', Key='s3_output_key')
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=s3_bucket_name)
    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location['LocationConstraint'],
        s3_bucket_name,
        key_name)
    print('wrote to the S3')
    
    print('writing to the database')
    cursor.execute("INSERT INTO HouseInfo (houseID, zipcode, bedroom, bathroom, floor, parkingspot, area, cost, photoUrl) VALUES('00003', 10010, 3, 3.00, 1, 2, 1500.00, 600000.00, {object_url})")
    connection.commit()
    print('wrote to the database')


# def select ():
    '''#configuration values
    endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
    username = 'JZNYC'
    password = '58290273'
    database_name = 'buildingInfo' '''    

    import pymysql

    #configuration values
    endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
    database_name = 'buildingInfo'
    username = str(input('PLEASE INPUT USERNAME: '))
    password = str(input('PLEASE INPUT PASSWORD: '))


    #connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)

    #S3 connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)

    def handler():
        cursor = connection.cursor()
        cursor.execute('SELECT * from HouseInfo')
    
        rows = cursor.fetchall()
    
        for row in rows:
            print('{0} {1}'.format(row[0], row[1]))
       

    # handler()
    
    
    
    
def select ():
    '''#configuration values
    endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
    username = 'JZNYC'
    password = '58290273'
    database_name = 'buildingInfo' '''    

    import pymysql

    #configuration values
    endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
    database_name = 'buildingInfo'
    username = str(input('PLEASE INPUT USERNAME: '))
    password = str(input('PLEASE INPUT PASSWORD: '))


    #connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)

    def handler():
        cursor = connection.cursor()
        cursor.execute('SELECT houseID from HouseInfo')
    
        rows = cursor.fetchall()
    
        for row in rows:
            print('{0}'.format(row[0]))
       
        
        
        
    handler()
        
    
    
select()