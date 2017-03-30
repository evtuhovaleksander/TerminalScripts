from xls_importer import confg
from xls_importer.confg import Point
from sql import Request,Resource_ORM,Request_ORM,Work_Type_ORM,Work_ORM,Work
import xlrd
import datetime
import funcs

class xlsReader:
    work_book=None
    sheet=None

    def __init__(self,path,index):
        self.work_book=xlrd.open_workbook(path)
        self.sheet = self.work_book.sheet_by_index(index)

    def open_book(self,path):
        self.work_book=xlrd.open_workbook(path)

    def open_sheet(self,index):
        self.sheet = self.work_book.sheet_by_index(0)

    def get_element(self,point):
        return self.sheet.cell(point.y, point.x).value


    def get_request(self):
        request=Request()
        request.request=Request_ORM()
        request.request.tvc_id=self.get_element(confg.tvc_id)
                            #datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")      24.03.2017 15:00


        print(self.get_element(confg.date))

        #dateoffset = 693594
        #print(datetime.datetime.fromordinal(dateoffset + self.get_element(confg.date)))


        request.request.date=datetime.datetime.strptime(self.get_element(confg.date), "%d.%m.%Y")#self.get_element(confg.date)

        request.request.project_start=datetime.datetime.strptime(self.get_element(confg.project_start), "%d.%m.%Y %H:%M")#self.get_element(confg.project_start)
        request.request.orderer=self.get_element(confg.orderer)
        request.request.theme=self.get_element(confg.theme)



        request.request.efir_date=funcs.get_date(self.get_element(confg.efir_date))


        request.request.program_name=self.get_element(confg.program_name)
        r=self.get_element(confg.resource)
        request.resource = Resource_ORM.get_or_create(resource=r)[0]
        request.work_set=[]
        request.work_set=self.atach_works_to_request()

        request.request.start=request.work_set[0].work.start_date
        request.request.stop=request.work_set[0].work.stop_date

        return request

    def atach_works_to_request(self):
        start_index=confg.start_row_index
        stop_index=start_index
        while Work.get_work_type_id(self.get_element(Point(confg.work_type_column,stop_index))):
            stop_index+=1
        #stop_index+=1
        if confg.debug: print(start_index)
        if confg.debug: print(stop_index)

        works=[]
        for row_index in range(start_index,stop_index):
            tmp_work=self.get_work(row_index)
            print(row_index)
            #tmp_work.request_id=request_id
            works.append(tmp_work)
        return works






    def get_work(self,row_id):
        work=Work()
        work.work=Work_ORM()
        #work.work_type=Work_Type_ORM.get(work_type=self.get_element(Point(confg.work_type_column,row_id)))
        work.work_type = Work.get_work_type_id(self.get_element(Point(confg.work_type_column, row_id)))
        work.work.start_date = funcs.get_date(self.get_element(Point(confg.start_date_column,row_id)))
        work.work.stop_date = funcs.get_date(self.get_element(Point(confg.stop_date_column,row_id)))
        work.work.colvo = self.get_element(Point(confg.colvo_column,row_id))
        work.work.atrib = self.get_element(Point(confg.atrib_column,row_id))
        work.work.sub_atrib = self.get_element(Point(confg.sub_atrib_column,row_id))
        work.work.status = self.get_element(Point(confg.status_column,row_id))
        work.work.coments = self.get_element(Point(confg.coments_column,row_id))
        return work









rd=xlsReader('/home/alexdark/tr1.xlsx',0)
req=rd.get_request()
req=req
req.save()
