from peewee import *

myDB = MySQLDatabase('terminal',host="127.0.0.1",port=3306,user="root",passwd="root")


class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB



class File_ORM(MySQLModel):
    id=PrimaryKeyField()
    work_id=IntegerField()
    path=CharField()
    name=CharField()


class File_History(MySQLModel):
    id=PrimaryKeyField()
    parent_id=IntegerField()
    path=CharField()
    work_id=IntegerField()


class Resource_ORM(MySQLModel):
    id=PrimaryKeyField()
    resource=CharField()


class Format_ORM(MySQLModel):
    id=PrimaryKeyField()
    format=CharField()


class Work_Type_ORM(MySQLModel):
    id=PrimaryKeyField()
    work_type=CharField()




class Work_ORM(MySQLModel):
    id=PrimaryKeyField()
    request_id=IntegerField( null = True)
    work_type_id=IntegerField( null = True)


    start_date =  DateTimeField( null = True)
    stop_date =  DateTimeField( null = True)
    colvo = CharField( null = True)
    atrib = CharField( null = True)
    sub_atrib = CharField( null = True)
    status = CharField( null = True)
    coments = CharField( null = True)

    fact_start= DateTimeField( null = True)
    fact_stop= DateTimeField( null = True)


class Request_ORM(MySQLModel):
    id=PrimaryKeyField()
    tvc_id=CharField( null = True)
    date= DateTimeField( null = True)
    resource_id=IntegerField( null = True)
    start= DateTimeField( null = True)
    stop= DateTimeField( null = True)

    fact_start= DateTimeField( null = True)
    fact_stop= DateTimeField( null = True)

    ViPlanner=CharField( null = True)
    program_name=CharField( null = True)

    in_format_id=IntegerField( null = True)
    out_format_id=IntegerField( null = True)

    redaction_comment=CharField( null = True)
    video_comment=CharField( null = True)
    audio_comment=CharField( null = True)
    work_comment=CharField( null = True)

    project_start=CharField( null = True)# = Point(1, 1)  #

    orderer =CharField( null = True)#= Point(1, 1)  #
    theme =CharField( null = True)#= Point(1, 1)  #


class Request():
    request=None
    resource=None
    in_format=None
    out_format=None
    work_set=[]
    def save(self):

        self.resource.save() # nado li ?!?!?!?!?
        self.request.resource_id = self.resource.id
        self.request.save()

        for work in self.work_set:
            work.request_id=self.request.id
            work.save()




class Work():
    work=None # Work_Orm
    work_type=None # Work_Type_orm

    def save(self):
        self.work.work_type_id=self.work_type.id
        self.work_type.save()
        self.work.save()
    @staticmethod
    def get_work_type_id(str):
        try:
            return Work_Type_ORM.get(work_type=str)
        except Exception as e:
            print(e)
            return None




def init_db():
    if False:

        myDB.connect()
        #for i in range(20):
        Request_ORM.drop_table()
        Resource_ORM.drop_table()
        Work_Type_ORM.drop_table()
        Work_ORM.drop_table()
        Format_ORM.drop_table()
        File_ORM.drop_table()
        File_History.drop_table()
        Request_ORM.create_table()
        Resource_ORM.create_table()
        Work_Type_ORM.create_table()
        Work_ORM.create_table()
        Format_ORM.create_table()
        File_ORM.create_table()
        File_History.create_table()

        wt=Work_Type_ORM()
        wt.id=1
        wt.work_type='wt1'
        wt.save()
        wt.id=2
        wt.work_type='wt2'
        wt.save()

        r=Resource_ORM()
        r.id=1
        r.resource='АСМ-9'
        r.save()




        myDB.close()
init_db()