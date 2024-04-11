import pyodbc
from functools import partial
from tenacity import retry, stop_after_delay, wait_fixed, retry_if_exception_type
import sqlite3


def create_connection(server, database, username, password):
    try:
        connection = pyodbc.connect(f"Driver={{SQL Server}};Server={server};Database={database};Uid={username};Pwd={password};Trusted_Connection=yes;")
        print("Connection established")
        return connection    
    except pyodbc.Error as e:
        print(f"Error connecting to {server}/{database}: {e}")
    return None
        
def getinvoicesummary_data(invoicenumber):
    import json
    print(invoicenumber)
    conn = create_connection("XXX", "XXX", "XXX", "XXX$")
    selectquery = "select i.AccountNumber,i.PeriodStartDate, i.PeriodEndDate, i.BillDate, i.DueDate, i.BillPreviousBalance, i.BillPastDueBalance, i.BillPaymentReceived, i.BillBalance, i.Id from dbo.Invoices i where i.InvoiceNumber = '"+ invoicenumber +"'"
    cursor = conn.cursor()
    cursor.execute(selectquery)
    record = cursor.fetchone()
    invoicerec = {}
    listrec = []
    invoicerec['AccountNumber'] = str(record[0])
    invoicerec['PeriodStartDate'] = str(record[1])
    invoicerec['PeriodEndDate'] = str(record[2])
    invoicerec['BillDate'] = str(record[3])
    invoicerec['DueDate'] = str(record[4])
    invoicerec['BillPreviousBalance'] = str(record[5])
    invoicerec['BillPastDueBalance'] = str(record[6])
    invoicerec['BillPaymentReceived'] = str(record[7])
    invoicerec['BillBalance'] = str(record[8])
    invoicerec['InvoiceId'] = str(record[9])

    listrec.append(invoicerec)
    print('invoice id : ' + invoicerec['InvoiceId'])
    conn.close()
    jsonString = json.dumps(listrec)
    return jsonString

# Custom error type for this example
class CommunicationError(Exception):
    pass

# Define shorthand decorator for the used settings.
retry_on_communication_error = partial(
    retry,
    stop=stop_after_delay(10),  # max. 10 seconds wait.
    wait=wait_fixed(0.4),  # wait 400ms 
    retry=retry_if_exception_type(CommunicationError),
)()

@retry_on_communication_error
def getinvoicesline_data(invoicenumber, linenum):
    import json
    print(invoicenumber)
    print(linenum)
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    invoicelinequery = "select il.CapturePrimaryPlanName, il.TotalCharges, il.PrimaryPlanMRC, il.DataUsageMB,il.TaxesSurchargeCharges, il.EquipmentCharges from dbo.InvoiceLines il join dbo.Invoices i on i.id = il.InvoiceId where i.InvoiceNumber = '"+ invoicenumber +"' and il.CaptureWirelessNumber = '"+ linenum +"'"
    lineinvoice = {}
    listrec = []
    cursor = conn.cursor()
    cursor.execute(invoicelinequery)
    invoicelinerecord = cursor.fetchone()
    print("for invoiceline")
    try:
        print(invoicelinerecord)
        lineinvoice['CapturePrimaryPlanName'] = str(invoicelinerecord[0])
        lineinvoice['TotalCharges'] = str(invoicelinerecord[1])
        lineinvoice['PrimaryPlanMRC'] = str(invoicelinerecord[2])
        lineinvoice['DataUsageMB'] = str(invoicelinerecord[3])
        lineinvoice['TaxesSurchargeCharges'] = str(invoicelinerecord[4])
        lineinvoice['EquipmentCharges'] = str(invoicelinerecord[5])
        listrec.append(lineinvoice)
        conn.close()
        jsonString = json.dumps(listrec)
    except:
        print('Error occured - unable to construct json data from query - probably empty or no rows returned. Retrying.')
        raise CommunicationError
    return jsonString

@retry_on_communication_error
def getinvoicesline_count(invoiceId):
    import json
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    invoicelinequery = "select COUNT(*) from dbo.InvoiceLines where InvoiceId = '"+ invoiceId +"'"
    lineinvoice = {}
    listrec = []
    cursor = conn.cursor()
    cursor.execute(invoicelinequery)
    invoicelinerecord = cursor.fetchone()
    print("for invoiceline")
    try:
        print(invoicelinerecord)
        lineinvoice['totalcount'] = str(invoicelinerecord[0])
        listrec.append(lineinvoice)
        conn.close()
        jsonString = json.dumps(listrec)
    except:
        print('Error occured - unable to construct json data from query - probably empty or no rows returned. Retrying.')
        raise CommunicationError
    return jsonString

def check_if_invoice_exist(invoicenumber):
    print("checking ",invoicenumber)
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    cursor = conn.cursor()
    cursor.execute("select InvoiceNumber from dbo.Invoices where InvoiceNumber = '"+ invoicenumber +"'")
    try:    
        rec = cursor.fetchall()
        if len(rec)!=0:
            print("has record!")
            print(rec)
            return True
        return False
    except err:
        print(err)
    conn.close()
    return False

def check_job_is_done(ssqagent, utctime):
    conn = None
    cursor = None
    print('carrier ' + ssqagent)
    print('utc: ' + utctime)
    try:

        conn = create_connection("uat-sql.ad.mobilesolutions.net", "msdb", "AD\gaucho.agregado", "vEJD10hQDU4$")
        cursor = conn.cursor()
        ssqjob = None
        if ssqagent == 'att':
            ssqjob = 'InvoiceProcessingAttIIQ'
        elif ssqagent == 'verizon':
            ssqjob = 'InvoiceProcessingVerizonIIQ'
        elif ssqagent == 'tmobile':
            ssqjob = 'InvoiceProcessingTMobileIIQ'
        print("select j.name as 'JobName', run_date,run_time, msdb.dbo.agent_datetime(run_date, run_time) as 'RunDateTime', h.step_name, h.message From msdb.dbo.sysjobs j INNER JOIN msdb.dbo.sysjobhistory h ON j.job_id = h.job_id where j.name = '"+ssqjob+"' and msdb.dbo.agent_datetime(run_date, run_time) > '"+ utctime +"'")
        cursor.execute("select j.name as 'JobName', run_date,run_time, msdb.dbo.agent_datetime(run_date, run_time) as 'RunDateTime', h.step_name, h.message From msdb.dbo.sysjobs j INNER JOIN msdb.dbo.sysjobhistory h ON j.job_id = h.job_id where j.name = '"+ssqjob+"' and msdb.dbo.agent_datetime(run_date, run_time) > '"+ utctime +"'")
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        if len(records) > 1:
            return True
        
        # print("Printing each row")
        # for row in records:
        #     print("step name: ", row[4])
        #     print("message: ", row[5])
        #     print("\n")
        #     if row[5] in 'The job succeeded':
        #         return True

        return False
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print("The sql connection is closed")

def getUTCnow():
    import datetime

    #newutc = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    t = datetime.datetime.utcnow()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return str(s[:-3])


def check_sysjob_status():
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "msdb", "AD\gaucho.agregado", "vEJD10hQDU4$")
    cursor = conn.cursor()
    cursor.execute("select h.* from dbo.sysjobhistory h inner join dbo.sysjobs j on h.job_id = j.job_id where j.name = 'InvoiceProcessingAttIIQ'")
    try:
        record = cursor.fetchone()
        if len(record)!=0:
            print("Name: ", record[3])
            print("Status of Run", record[7])
            if record[7] == 1:
                print("Job is done!")
                conn.close()
                return True
        else:
            print("no job found")
    except Exception as e:
        print('error',e)
    conn.close()
    return False

def delete_invoice(invoicenumber):
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    cursor = conn.cursor()
    print("invoice is:",invoicenumber)
    val = "'" + invoicenumber + "'"
    storedProc = "exec Invoices_DeleteInvoiceFromMax @InvoiceNumber = ?"
    params = (val)
    cursor.execute(storedProc, invoicenumber)
    # Call commit() method to save changes to the database
    conn.commit() 
    conn.close()
   
def callsqlserveragentjob(carrier):
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "msdb", "AD\gaucho.agregado", "vEJD10hQDU4$")
    conn.autocommit = True
    cursor = conn.cursor()
    if carrier == 'att':
        print('its at&t')
        cursor.execute("exec dbo.sp_start_job N'InvoiceProcessingAttIIQ';")
    elif carrier =='verizon':
        print('its verizon')
        cursor.execute("exec dbo.sp_start_job N'InvoiceProcessingVerizonIIQ';")
    elif carrier =='tmobile':
        print('its verizon')
        cursor.execute("exec dbo.sp_start_job N'InvoiceProcessingTMobileIIQ';")
    conn.close()

def callsqlserveragentjobM2M(carrier):
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "msdb", "AD\gaucho.agregado", "vEJD10hQDU4$")
    conn.autocommit = True
    cursor = conn.cursor()
    if carrier == 'att':
        print('its at&t')
        cursor.execute("exec dbo.sp_start_job N'InvoiceProcessingAttM2M';")
    elif carrier =='verizon':
        print('its verizon')
        cursor.execute("exec dbo.sp_start_job N'InvoiceProcessingVerizonM2M';")
    conn.close()
     
def checkinvoiceprocessinglog(invoicenumber, utctime):
    conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    cursor = conn.cursor()
    query = "SELECT * FROM Integration.dbo.InvoiceProcessingLog where InvoiceNumber = '" + invoicenumber +"' and CreatedDate > '"+ utctime +"'"
    cursor.execute(query)
    rec = cursor.fetchone()

    try:
        if len(rec)!=0:
            conn.close()
            return True
    except Exception as e:
        conn.close()
        return False

    

def checkinvoiceindoesnotreconcile(invoicenumber):
    try:
        conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
        cursor = conn.cursor()
        query = "select * from Integration.dbo.InvoiceProcessingDoesNotReconcileLog where IgnoreInd != 1 and InvoiceNumber = '"+ invoicenumber +"'"
        cursor.execute(query)
        rec = cursor.fetchone()
        if len(rec)!=0:
            conn.close()
            return True
    except Exception as e:
        print('error',e)
        conn.close()
        return False

def checkinvoiceindoesnotreconcileandmanualadjustment(invoicenumber,manual):
    try:
        conn = create_connection("uat-sql.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
        cursor = conn.cursor()
        query = "select * from Integration.dbo.InvoiceProcessingDoesNotReconcileLog where IgnoreInd != 1 and InvoiceNumber = '"+ invoicenumber +"'"
        cursor.execute(query)
        rec = cursor.fetchone()
        if len(rec)!=0:
            print('its in does not reconcile')
            if int(rec[15]) == int(manual):
                conn.close()
                return True
            else:
                print('manual adjustment value is incorrect')
                        
        return False
    except Exception as e:
        print('error',e)
        conn.close()
        return False 


def check_error_folder(zipfilename, carrier):
    import glob
    import os
    error_folder = None
    if carrier == 'att':
        error_folder = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Att\\error\\"
    elif carrier == 'verizon':
        error_folder = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Verizon\\error\\"
    elif carrier == 'tmobile':
        error_folder = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\TMobile\\error\\"

    zip_files = glob.glob(os.path.join(error_folder, "*.zip"))
    for zip_file in zip_files:
        print('comparing: ' + os.path.basename(zip_file) + " and " + zipfilename)
        if os.path.basename(zip_file) == zipfilename:
            return True

    return False  




def move_zipfile_to_ssis(carrier):
    from pathlib import Path
    import shutil
    import os
    dest_temp = None
    if carrier == 'att':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Att\\in"
    elif carrier == 'verizon':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Verizon\\in"
    elif carrier == 'tmobile':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\TMobile\\in"

    source_dir = "D:\\File\\OutPut\\"
    files = os.listdir(source_dir)
    for q in files:
        shutil.move(source_dir + q, dest_temp)

def move_zipfile_to_m2mINFolder(carrier):
    from pathlib import Path
    import shutil
    import os
    dest_temp = None
    if carrier == 'att':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Att\\m2m\\in"
    elif carrier == 'verizon':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Verizon\\m2m\\in"
    source_dir = "D:\\File\\OutPut\\m2mzip\\"
    files = os.listdir(source_dir)
    for q in files:
        shutil.move(source_dir + q, dest_temp)

def move_usagefile_to_m2mUsageFolder(carrier):
    from pathlib import Path
    import shutil
    import os
    dest_temp = None
    if carrier == 'att':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Att\\m2m\\m2musage"
    elif carrier == 'verizon':
        dest_temp = r"\\uat-sql.ad.mobilesolutions.net\\messagehub\\SSIS\\Invoices\\InvoiceIQ\\Verizon\\m2m\\m2musage"
    source_dir = "D:\\File\\OutPut\\usagefile\\"
    files = os.listdir(source_dir)
    for q in files:
        shutil.move(source_dir + q, dest_temp)
   


def generateInvoiceSummaryData(invoicenumber):
    import csv
    conn = create_connection("SQLAGL01.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    selectquery = "select i.InvoiceNumber ,i.AccountNumber,i.PeriodStartDate, i.PeriodEndDate, i.BillDate, i.DueDate, i.BillPreviousBalance, i.BillPastDueBalance, i.BillPaymentReceived, i.BillBalance ,  (select c.Name from dbo.Carriers c where id = i.CarrierId) As 'carrier' from dbo.Invoices i where i.InvoiceNumber = '"+ invoicenumber +"'"
    cursor = conn.cursor()
    cursor.execute(selectquery)
    rows = cursor.fetchall()
    csv_file = "generatedInvoiceSummaryData.csv"
    headers = ["filename","invoicenumber","AccountNumber","PeriodStartDate","PeriodEndDate","BillDate","DueDate","BillPreviousBalance","BillPastDueBalance","BillPaymentReceived","BillBalance","carrier"]
    # Write the data to a CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(headers)
        # Write the data rows
        for row in rows:
            writer.writerow(row)


def generateInvoiceLineData(invoicenumber):
    import csv
    conn = create_connection("SQLAGL01.ad.mobilesolutions.net", "Max", "AD\gaucho.agregado", "vEJD10hQDU4$")
    selectquery = "select i.InvoiceNumber ,i.AccountNumber,i.PeriodStartDate, i.PeriodEndDate, i.BillDate, i.DueDate, i.BillPreviousBalance, i.BillPastDueBalance, i.BillPaymentReceived, i.BillBalance ,  (select c.Name from dbo.Carriers c where id = i.CarrierId) As 'carrier' from dbo.Invoices i where i.InvoiceNumber = '"+ invoicenumber +"'"
    cursor = conn.cursor()
    cursor.execute(selectquery)
    rows = cursor.fetchall()
    csv_file = "generatedInvoiceSummaryData.csv"
    headers = ["filename","invoicenumber","AccountNumber","PeriodStartDate","PeriodEndDate","BillDate","DueDate","BillPreviousBalance","BillPastDueBalance","BillPaymentReceived","BillBalance","carrier"]
    # Write the data to a CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(headers)
        # Write the data rows
        for row in rows:
            writer.writerow(row)
