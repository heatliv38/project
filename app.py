from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from util import *
from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from util import *
from hashlib import md5
from random import *
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta




app = Flask(__name__)
app.secret_key = '2y14ZhoB0P'

conn = pymysql.connect(host='localhost',
                user='root',
                password='0123',
                db='capstone',
                charset='utf8mb4',
                port = 3306,
                cursorclass=pymysql.cursors.DictCursor)



def match(weights):
    all_fields=list(weights.keys()) #get all keys
    protocol_fields=all_fields[1:]  #get keys protocol related keys
    patient_id=weights['index']  #get patient index
    query1="SELECT * FROM protocols"
    query2="SELECT * FROM patients WHERE patients.index={}".format(patient_id)
    patient_data=query_fetchall(query2, conn)[0] #dict object
    protocol_data=query_fetchall(query1, conn)  #list of dicts
    
    #matching
    score={}
    matched_fields={}
    for i in range(len(protocol_data)):
        cur_protocol=protocol_data[i]
        score[cur_protocol['name']]=0 #set initial score to 0
        matched_fields[cur_protocol['name']]=[]
        for x in protocol_fields:
            if patient_data[x]==cur_protocol[x]:
                score[cur_protocol['name']]+=int(weights[x]) #add score
                matched_fields[cur_protocol['name']].append(x)  #append matched fields
    score={k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}

    return score, matched_fields


@app.route('/', methods=['GET'])
def home_page_get():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def home_page_post():
    return render_template("index.html")

@app.route('/protocol_data', methods=['GET'])
def protocol_data_get():
    query = "SELECT * from protocols"
    protocol_data=query_fetchall(query, conn)
    return render_template("protocol_data.html", data=protocol_data)

@app.route('/protocol_data', methods=['POST'])
def protocol_data_post():
    query = "SELECT * from protocols"
    protocol_data=query_fetchall(query, conn)
    return render_template("protocol_data.html", data=protocol_data)

@app.route('/patient_data', methods=['GET'])
def patient_data_get():
    query = "SELECT * from patients"
    patient_data=query_fetchall(query, conn)
    return render_template("patient_data.html", data=patient_data)

@app.route('/patient_data', methods=['POST'])
def patient_data_post():
    query = "SELECT * from patients"
    patient_data=query_fetchall(query, conn)
    return render_template("patient_data.html", data=patient_data)

@app.route('/matching_criterion', methods=['GET'])
def matching_criteria_get():
	return render_template('matching_criterion.html')

@app.route('/matching_criterion', methods=['POST'])
def matching_criteria_post():
##    p_index = request.form['index']
##    treatment_site=request.form['treatment_site']
##    T=request.form['T']
##    N=request.form['N']
##    M=request.form['M']
##    risk_group=request.form['risk_group']
##    primary_site=request.form['primary_site']
##    metastasis=request.form['metastasis']
##    nodes_num=request.form['node_num']
##    histology=request.form['histology']
##    margin=request.form['margin']
##    PSA=request.form['PSA']
##    gleason=request.form['gleason']
##    recurrence=request.form['recurrence']
##    performance_status=request.form['performance_status']
##    age=request.form['age']
##    treatment_intent=request.form['treatment_intent']
##    retreat=request.form['retreat']
##    prior_RT=request.form['prior_RT']
##    surgery=request.form['surgery']
##    other_therapies=request.form['other_therapies']
    print([request.form.keys()])
    score, matched_fields=match(request.form)
    print(score)
    print(matched_fields)
    query = "SELECT MRN from patients where patients.index={}".format(p_index)
    print(query)
    patient_MRN=query_fetchone(query, conn)['MRN']
    print(patient_MRN)
    session['MRN'] = patient_MRN
    return redirect('/matching_result')

@app.route('/matching_result', methods=['GET'])
def matching_result_get():
    return render_template('matching_result.html')

@app.route('/matching_result', methods=['POST'])
def matching_result_post():
    #query = "SELECT * from patients"
    #patient_data=query_fetchall(query, conn)
    return render_template("matching_result.html")


@app.route('/patient_input', methods=['GET'])
def patient_input_get():
	return render_template('patient_input.html')

@app.route('/patient_input', methods=['POST'])
def patient_input_post():
    name=request.form['name']
    MRN=request.form['MRN']
    DOB=request.form['DOB']
    age=request.form['age']
    weight=request.form['weight']
    height=request.form['height']
    gender=request.form['gender']
    race=request.form['race']
    performance_status=request.form['performance_status']
    #join values for multiple selection for treatment site
    treatment_site=";".join(request.form.to_dict(flat=False)['treatment_site'])
    T=request.form['T']
    N=request.form['N']
    M=request.form['M']
    risk_group=request.form['risk_group']
    primary_site=request.form['primary_site']
    metastasis=request.form['metastasis']
    nodes_num=request.form['nodes_num']
    staging_system=request.form['staging_system']
    histology=request.form['histology']
    margin=request.form['margin']
    PSA=request.form['PSA']
    gleason=request.form['gleason']
    recurrence=request.form['recurrence']
    volume_size=request.form['volume_size']
    dimension_size=request.form['dimension_size']
    location=request.form['location']
    clinical_risk=request.form['clinical_risk_factors']
    treatment_intent=request.form['treatment_intent']
    retreat=request.form['retreat']
    prior_RT=request.form['prior_RT']
    surgery=request.form['surgery']
    chemtherapy=request.form['chemtherapy']
    hormone=request.form['hormone']
    immunotherapy=request.form['immunotherapy']
    ADT=request.form['ADT']

    query ="""INSERT INTO patients(name,MRN,DOB,age,weight,height,gender,race,performance_status,
                         treatment_site,T,N,M,risk_group,primary_site,metastasis,nodes_num,
                         staging_system,histology,margin,PSA,gleason,recurrence,volume_size,
                         dimension_size,location,clinical_risk,treatment_intent,retreat,prior_RT,
                         surgery,chemtherapy,hormone,immunotherapy,ADT)
              VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",
                     "{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",
                     "{}")""".format(name,MRN,DOB,age,weight,height,gender,race,                                                                                                      performance_status,
                         treatment_site,T,N,M,risk_group,primary_site,metastasis,nodes_num,
                         staging_system,histology,margin,PSA,gleason,recurrence,volume_size,
                         dimension_size,location,clinical_risk,treatment_intent,retreat,prior_RT,
                         surgery,chemtherapy,hormone,immunotherapy,ADT)

    result = query_insert(query, conn)
    if result == 0:
        flash("Request denied, please try one more time!")
    return redirect('/')

@app.route('/protocol_input', methods=['GET'])
def protocol_input_get():
	return render_template('protocol_input.html')

@app.route('/protocol_input', methods=['POST'])
def protocol_input_post():
    d=request.form.to_dict(flat=False)
    study_name=d['study_name'][0]
    description=d['description'][0]
    source=d['source'][0]
    PMID=d['PMID'][0]
    publish_date=d['publish_date'][0]
    size=d['size'][0]
    study_type=d['study_type'][0]
    analysis_type=';'.join(d['analysis_type'])
    country=';'.join(d['country'])
    DOI=d['DOI'][0]
    treatment_site=';'.join(d['treatment_site'])
    T=';'.join(d['T'])
    N=';'.join(d['N'])
    M=';'.join(d['M'])
    risk_group=';'.join(d['risk_group'])
    primary_site=d['primary_site'][0]
    metastasis=d['metastasis'][0]
    nodes_num=d['nodes_num'][0]
    staging_system=';'.join(d['staging_system'])
    histology=d['histology'][0]
    margin=d['margin'][0]
    PSA=d['PSA'][0]
    gleason=d['gleason'][0]
    recurrence=d['recurrence'][0]
    volume_size=d['volume_size'][0]
    dimension_size=d['dimension_size'][0]
    location=d['location'][0]
    clinical_risk=d['clinical_risk_factors'][0]
    performance_status=';'.join(d['performance_status'])
    age=d['age'][0]
    weight=d['weight'][0]
    height=d['height'][0]
    gender=d['gender'][0]
    race=';'.join(d['race'])
    treatment_intent=d['treatment_intent'][0]
    retreat=d['retreat'][0]
    prior_RT=d['prior_RT'][0]
    surgery=d['surgery'][0]
    chemtherapy=d['chemtherapy'][0]
    hormone=d['hormone'][0]
    immunotherapy=d['immunotherapy'][0]
    ADT=d['ADT'][0]   
    regimen_I=d['regimen_I'][0]
    RI_base_dose_fraction=d['RI_base_dose_fraction'][0]
    RI_boost_dose_modality=d['RI_boost_dose_modality'][0]
    RI_other_therapies=d['RI_other_therapies'][0]
    RI_TCP_median_follow_up=d['RI_TCP_median_follow_up'][0]
    RI_LC=d['RI_LC'][0]
    RI_OS=d['RI_OS'][0]
    RI_PFS=d['RI_PFS'][0]
    RI_bPFS=d['RI_bPFS'][0]
    RI_DFS=d['RI_DFS'][0]
    RI_FFS=d['RI_FFS'][0]
    RI_MFS=d['RI_MFS'][0]
    RI_CSS=d['RI_CSS'][0]
    RI_DMFS=d['RI_DMFS'][0]
    RI_BCR=d['RI_BCR'][0]
    RI_NTCP_median_follow_up=d['RI_NTCP_median_follow_up'][0]
    RI_toxicity_system=d['RI_toxicity_system'][0]
    RI_acute=d['RI_acute'][0]
    RI_G1=d['RI_G1'][0]
    RI_G2=d['RI_G2'][0]
    RI_G3=d['RI_G3'][0]
    RI_G4=d['RI_G4'][0]
    RI_G5=d['RI_G5'][0]
    regimen_II=d['regimen_II'][0]
    RII_base_dose_fraction=d['RII_base_dose_fraction'][0]
    RII_boost_dose_modality=d['RII_boost_dose_modality'][0]
    RII_other_therapies=d['RII_other_therapies'][0]
    RII_TCP_median_follow_up=d['RII_TCP_median_follow_up'][0]
    RII_LC=d['RII_LC'][0]
    RII_OS=d['RII_OS'][0]
    RII_PFS=d['RII_PFS'][0]
    RII_bPFS=d['RII_bPFS'][0]
    RII_DFS=d['RII_DFS'][0]
    RII_FFS=d['RII_FFS'][0]
    RII_MFS=d['RII_MFS'][0]
    RII_CSS=d['RI_CSS'][0]
    RII_DMFS=d['RI_DMFS'][0]
    RII_NTCP_median_follow_up=d['RII_NTCP_median_follow_up'][0]
    RII_toxicity_system=d['RII_toxicity_system'][0]
    RII_acute=d['RII_acute'][0]
    RII_G1=d['RII_G1'][0]
    RII_G2=d['RII_G2'][0]
    RII_G3=d['RII_G3'][0]
    RII_G4=d['RII_G4'][0]
    RII_G5=d['RII_G5'][0]
    modality=d['modality'][0]
    planning=d['planning'][0]
    delivery=d['delivery'][0]
    imaging=d['imaging'][0]
    setup=d['setup'][0]
    key_conclusion=d['key_conclusion'][0]
    target_dose_constraints=d['target_dose_constraints'][0]
    OAR_constraints=d['OAR_constraints'][0]
    
    query ="""INSERT INTO protocols(name,description,source,PMID,date,study_size,study_type,analysis_type,country,DOI,treatment_site,
    T,N,M,risk_group,primary_site,metastasis,nodes_num,staging_system,histology,margin,PSA,gleason,recurrence,volume_size,dimension_size,
    location,clinical_risk,performance_status,age,weight,height,gender_ratio,race,treatment_intent,retreat,prior_RT,surgery,chemtherapy,
    hormone,immunotherapy,ADT,Regimen_I,RI_base_dose_fractions,RI_boost_dose_modality,RI_other_therapies,RI_TCP_median_follow_up,
    RI_local_control,RI_overall_survival,RI_PFS,RI_bPFS,RI_DFS,RI_FFS,RI_MFS,RI_CSS,RI_DMFS,RI_BCR,RI_NTCP_median_follow_up,RI_toxicity_system,
    RI_acute,RI_G1,RI_G2,RI_G3,RI_G4,RI_G5,Regimen_II,RII_base_dose_fractions,RII_boost_dose_modality,RII_other_therapies,RII_TCP_median_follow_up,
    RII_local_control,RII_overall_survival,RII_PFS,RII_bPFS,RII_DFS,RII_FFS,RII_MFS,RII_CSS,RII_DMFS,RII_NTCP_median_follow_up,RII_toxicity_system,
    RII_acute,RII_G1,RII_G2,RII_G3,RII_G4,RII_G5,modality,planning,delivery,imaging,setup,key_conclusion,target_dose_constraints,
    OAR_constraints) VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",
    "{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",
    "{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",
    "{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")""".format(
    study_name,description,source,PMID,publish_date,size,study_type,analysis_type,country,DOI,treatment_site,
    T,N,M,risk_group,primary_site,metastasis,nodes_num,staging_system,histology,margin,PSA,gleason,recurrence,volume_size,dimension_size,
    location,clinical_risk,performance_status,age,weight,height,gender,race,treatment_intent,retreat,prior_RT,surgery,chemtherapy,
    hormone,immunotherapy,ADT,regimen_I,RI_base_dose_fraction,RI_boost_dose_modality,RI_other_therapies,RI_TCP_median_follow_up,
    RI_LC,RI_OS,RI_PFS,RI_bPFS,RI_DFS,RI_FFS,RI_MFS,RI_CSS,RI_DMFS,RI_BCR,RI_NTCP_median_follow_up,RI_toxicity_system,
    RI_acute,RI_G1,RI_G2,RI_G3,RI_G4,RI_G5,regimen_II,RII_base_dose_fraction,RII_boost_dose_modality,RII_other_therapies,RII_TCP_median_follow_up,
    RII_LC,RII_OS,RII_PFS,RII_bPFS,RII_DFS,RII_FFS,RII_MFS,RII_CSS,RII_DMFS,RII_NTCP_median_follow_up,RII_toxicity_system,
    RII_acute,RII_G1,RII_G2,RII_G3,RII_G4,RII_G5,modality,planning,delivery,imaging,setup,key_conclusion,target_dose_constraints,
    OAR_constraints)

    result = query_insert(query, conn)
    if result == 0:
        flash("Request denied, please try one more time!")
    print('result:',result)
    return redirect('/')

############### Code from previous project, kept for reference ######################
@app.route('/register_agent', methods=['GET'])
def register_agent_get():
    return render_template('register_agent.html')

@app.route('/register_agent', methods=['POST'])
def register_agent():
    email = request.form['email']
    # password = request.form['password']
    # confirm_password = request.form['confirm_password']
    # Password encoded with utf-8 first then encoded with md5
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    confirm_password = md5(request.form['confirm_password'].encode('utf-8')).hexdigest()
    if password != confirm_password:
        err = "The confirmed password should match the password you input before!"
        flash(err)
        return render_template("register_agent.html")

    booking_agent_ID = request.form['booking_agent_ID']

    query = 'SELECT * FROM Booking_agent WHERE email="%s"' % (email)
    print(query)
    data = query_fetchone(query, conn)

    if data is not None:
        err = "User already exists!"
        flash(err)
        return redirect('/register_agent')
    else:
        query = 'INSERT INTO Booking_agent VALUES("{}", "{}", "{}")'.format(email, password, booking_agent_ID)
        result = query_insert(query, conn)
        if result == 0:
            flash("Request denied, please try one more time!")
        session['email'] = email
        session['role'] = "agent"
        notification = "Successfully signed up! Please sign in again!"
        return redirect('/login_agent')

@app.route('/register_staff', methods=['GET'])
def register_staff_get():
    return render_template('register_staff.html')

@app.route('/register_staff', methods=['POST'])
def register_staff():
    user_name = request.form['user_name']
    # password = request.form['password']
    # confirm_password = request.form['confirm_password']
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    confirm_password = md5(request.form['confirm_password'].encode('utf-8')).hexdigest()
    
    if password != confirm_password:
        err = "The confirmed password should match the password you input before!"
        flash(err)
        return render_template("register_staff.html")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    airline_name = request.form['airline_name']
    phone_number = request.form['phone_number']
    
    query = 'SELECT * FROM Airline_staff WHERE user_name="%s"' % (user_name)
    print(query)
    data = query_fetchone(query, conn)

    if data is not None:
        err = "User already exists!"
        flash(err)
        return redirect('/register_staff')
    else:
        query = 'INSERT INTO Airline_staff VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format\
            (user_name, password, first_name, last_name, dob, airline_name)
        result = query_insert(query, conn)
        if result == 0:
            flash("Request denied, please try one more time!")

        query2 = 'INSERT INTO Phone_number VALUES("{}", "{}")'.format\
                (user_name, phone_number)
        result2 = query_insert(query2, conn)
        if result2 == 0:
                flash("Request denied, please try one more time!")
        session['user_name'] = user_name
        session['role'] = "staff"
        return redirect('/login_staff')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login_customer', methods=['GET'])
def login_customer_get():
	return render_template('login_customer.html')

@app.route('/login_customer', methods=['POST'])
def login_customer():
    email = request.form['email']
    # password = request.form['password']
    password = md5(request.form['password'].encode('utf-8')).hexdigest()

    query = 'SELECT * FROM Customer WHERE email="%s" and password="%s"' % (email, password)
    print(query)
    data = query_fetchone(query, conn)

    if (data):
        session['email'] = email
        session['role'] = "customer"
        return redirect('/home_customer')
    else:
        err = "Email or password error!"
        flash(err)
        return redirect('/login_customer')

@app.route('/login_agent', methods=['GET'])
def login_agent_get():
	return render_template('login_agent.html')

@app.route('/login_agent', methods=['POST'])
def login_agent():
    email = request.form['email']
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    # password = request.form['password']
    query = 'SELECT * FROM Booking_agent WHERE email="%s" and password="%s"' % (email, password)
    print(query)
    data = query_fetchone(query, conn)

    if (data):
        session['email'] = email
        session['role'] = "agent"
        return redirect('/home_agent')
    else:
        err = "Email or password error!"
        flash(err)
        return redirect('/login_agent')

@app.route('/login_staff', methods=['GET'])
def login_staff_get():
	return render_template('login_staff.html')

@app.route('/login_staff', methods=['POST'])
def login_staff():
    email = request.form['email']
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    # password = request.form['password']

    query = 'SELECT * FROM Airline_staff WHERE user_name ="%s" and password="%s"' % (email, password)
    print(query)
    data = query_fetchone(query, conn)

    if (data):
        session['email'] = email
        session['role'] = "staff"
        return redirect('/home_staff')
    else:
        err = "Email or password error!"
        flash(err)
        return redirect('/login_staff')

@app.route('/home_customer', methods=['GET'])
def customer_page_get():
	return render_template('home_customer.html')

@app.route('/home_customer', methods=['POST'])
def customer_page():
    print(session['email'])
    print(session['role'])            
    return render_template("home_customer.html", username=session['email'])

@app.route('/myflight', methods=['GET'])
def myflight_get():
    # Show my flights
    print(session['email'])
    query = "SELECT airline_name, flight_num, depart_date_time, arrive_date_time, status, sold_price, Airplane_ID, Airport_depart_name, Airport_arrive_name  FROM Cust_buy, Ticket natural join Flight WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' ".format(session['email'])
    query2 = "SELECT airline_name, flight_num, depart_date_time, arrive_date_time, status, sold_price, Airplane_ID, Airport_depart_name, Airport_arrive_name    FROM Agent_buy, Ticket natural join Flight WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' ".format(session['email'])
    print('my_flights SQL: ', query+query2)
    my_flights_customer = query_fetchall(query, conn)
    my_flights_agent = query_fetchall(query2, conn)
    print(my_flights_customer)
    print(my_flights_agent)
    if len(my_flights_customer)>0:
        if len(my_flights_agent)>0:
            for item in my_flights_agent:
                my_flights_customer.append(item)
        my_flights =my_flights_customer
    else:
        if len(my_flights_agent)>0:
            my_flights =my_flights_agent
    print('my_flights response: ', my_flights)
    return render_template("myflight.html", flights=my_flights, username = session['email'])

@app.route('/myflight', methods=['POST'])
def myflight_post():
    # Show my flights
    query = "SELECT * FROM Cust_buy, Ticket natural join Flight WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' ".format(session['email'])
    query2 = "SELECT airline_name, flight_num, depart_date_time, arrive_date_time, status, sold_price, Airplane_ID, Airport_depart_name, Airport_arrive_name    FROM Agent_buy, Ticket natural join Flight WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' ".format(session['email'])
    print('my_flights SQL: ', query+query2)
    my_flights_cusomer = query_fetchall(query, conn)
    my_flights_agent = query_fetchall(query2, conn)
    my_flights = my_flights_cusomer+my_flights_agent
    print('my_flights response: ', my_flights)
    return render_template("myflight.html", flights=my_flights, username = session['email'])

@app.route('/myspending', methods=['GET'])
def myspending_get():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_year_ago = date.today() + relativedelta(months=-12)
    six_months_ago = date.today() + relativedelta(months=-6)
    # six months spending graph
    query = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Cust_buy,Ticket " \
            "WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
            "(purchase_date_time)".format(session['email'], six_months_ago)
            
    query2 = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Agent_buy,Ticket " \
    "WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
    "(purchase_date_time)".format(session['email'], six_months_ago)
    
    # print('six month spending SQL: ', query+query2)
    six_months_customer = query_fetchall(query, conn)
    six_months_agent = query_fetchall(query2, conn)
        
    if len(six_months_customer)>0:
        if len(six_months_agent)>0:
            for item in six_months_agent:
                six_months_customer.append(item)
        six_months =six_months_customer
    else:
        if len(six_months_agent)>0:
            six_months =six_months_agent
    # one year spending        
    query = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Cust_buy,Ticket " \
    "WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
    "(purchase_date_time)".format(session['email'], one_year_ago)
            
    query2 = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Agent_buy,Ticket " \
    "WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
    "(purchase_date_time)".format(session['email'], one_year_ago)
    print('one_year spending SQL: ', query+query2)
    one_year_customer = query_fetchall(query, conn)
    one_year_agent = query_fetchall(query2, conn)
    if len(one_year_customer)>0:
        if len(one_year_agent)>0:
            for item in one_year_agent:
                one_year_customer.append(item)
        one_year =one_year_customer
    else:
        if len(one_year_agent)>0:
            one_year =one_year_agent
    print('one_year', one_year)
    one_year_sum = 0
    for i in range(len(one_year)):
        one_year_sum += float(one_year[i]["total"])
    return render_template("myspending.html", username=session['email'],six_month_spending=six_months, one_year_spending=one_year_sum)


@app.route('/myspending', methods=['POST'])
def myspending_post():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_year_ago = date.today() + relativedelta(months=-12)
    six_months_ago = date.today() + relativedelta(months=-6)
    # six months spending graph
    query = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Cust_buy,Ticket " \
            "WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
            "(purchase_date_time)".format(session['email'], six_months_ago)
            
    query2 = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Agent_buy,Ticket " \
    "WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
    "(purchase_date_time)".format(session['email'], six_months_ago)
    six_months_customer = query_fetchall(query, conn)
    six_months_agent = query_fetchall(query2, conn)
        
    if len(six_months_customer)>0:
        if len(six_months_agent)>0:
            for item in six_months_agent:
                six_months_customer.append(item)
        six_months =six_months_customer
    else:
        if len(six_months_agent)>0:
            six_months =six_months_agent
    # one year spending        
    query = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Cust_buy,Ticket " \
    "WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
    "(purchase_date_time)".format(session['email'], one_year_ago)
            
    query2 = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Agent_buy,Ticket " \
    "WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' AND Ticket.purchase_date_time >= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
    "(purchase_date_time)".format(session['email'], one_year_ago)
    print('one_year spending SQL: ', query+query2)
    one_year_customer = query_fetchall(query, conn)
    one_year_agent = query_fetchall(query2, conn)
    if len(one_year_customer)>0:
        if len(one_year_agent)>0:
            for item in one_year_agent:
                one_year_customer.append(item)
        one_year =one_year_customer
    else:
        if len(one_year_agent)>0:
            one_year =one_year_agent
    print('one_year', one_year)
    one_year_sum = 0
    for i in range(len(one_year)):
        one_year_sum += float(one_year[i]["total"])
        
    if from_date:
        query = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Cust_buy,Ticket " \
            "WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' AND Ticket.purchase_date_time >= '{}' AND Ticket.purchase_date_time <= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
            "(purchase_date_time)".format(session['email'], from_date,to_date)
            
        query2 = "SELECT SUM(sold_price) AS total, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Agent_buy,Ticket " \
            "WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' AND Ticket.purchase_date_time >= '{}' AND Ticket.purchase_date_time <= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
            "(purchase_date_time)".format(session['email'], from_date,to_date)
    
        range_customer = query_fetchall(query, conn)
        range_agent = query_fetchall(query2, conn)

        if len(range_customer)>0:
            if len(range_agent)>0:
                for item in range_agent:
                    range_customer.append(item)
            range_spending =range_customer
        else:
            if len(range_agent)>0:
                range_spending =range_agent
                
        range_sum = 0
        for i in range(len(range_spending)):
            range_sum += float(range_spending[i]["total"])
        return render_template("myspending.html", username=session['email'],six_month_spending=six_months, one_year_spending=one_year_sum,range_spending = range_spending, range_sum = range_sum)
        
    return render_template("myspending.html", username=session['email'],six_month_spending=six_months, one_year_spending=one_year_sum)

@app.route('/myrating', methods=['GET'])
def myrating_get():
    # Show my flights
    print(session['email'])
    query = "SELECT airline_name, flight_num, depart_date_time, arrive_date_time, status, sold_price, Airplane_ID, Airport_depart_name, Airport_arrive_name  FROM Cust_buy, Ticket natural join Flight WHERE ticket.ID = Cust_buy.ticket_ID and Cust_buy.email = '{}' ".format(session['email'])
    query2 = "SELECT airline_name, flight_num, depart_date_time, arrive_date_time, status, sold_price, Airplane_ID, Airport_depart_name, Airport_arrive_name    FROM Agent_buy, Ticket natural join Flight WHERE ticket.ID = Agent_buy.ticket_ID and Agent_buy.customer_email = '{}' ".format(session['email'])
    print('my_flights SQL: ', query+query2)
    my_flights_customer = query_fetchall(query, conn)
    my_flights_agent = query_fetchall(query2, conn)
    print(my_flights_customer)
    print(my_flights_agent)
    if len(my_flights_customer)>0:
        if len(my_flights_agent)>0:
            for item in my_flights_agent:
                my_flights_customer.append(item)
        my_flights =my_flights_customer
    else:
        if len(my_flights_agent)>0:
            my_flights =my_flights_agent
    # print('my_flights response: ', my_flights)
    print(" ")
    print(" ")
    print("my flights",my_flights)
    return render_template("myrating.html", flights=my_flights, username = session['email'])

@app.route('/myrating', methods=['POST'])
def myrating_post():
    airline_name = request.form.get('airline_name')
    flight_number = request.form.get('flight_number')
    depart_date_time = request.form.get('depart_date_time')
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    query = 'SELECT * FROM Flight WHERE airline_name="%s" AND flight_num = "%s" AND depart_date_time = "%s"' % (airline_name,flight_number,depart_date_time)
    data = query_fetchone(query, conn)
    print("data",data)
    if data is None:
        err = "No Flight exists for this information!"
        flash(err)
        return redirect('/myrating')
    else:
        query = 'SELECT * FROM Rate WHERE airline_name="%s" AND flight_num = "%s" AND DATE(depart_date_time) = "%s"' % (airline_name,flight_number,depart_date_time)
        data = query_fetchone(query, conn)
        if data is None:
            query = 'INSERT INTO Rate VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format\
                (airline_name, flight_number, depart_date_time, session["email"], rating, comment)
            print(" ")
            print("insert query",query)
            result = query_insert(query, conn)
            print("inserting!",result)
            if result == 0:
                flash("Request denied, please try one more time!")
        else:
            query = 'UPDATE Rate SET points = "{}", flight_comment = "{}" WHERE airline_name= "{}" AND flight_num = "{}" AND DATE(depart_date_time) = "{}" AND email = "{}")'.format\
                (rating, comment, airline_name, flight_number, depart_date_time, session["email"])
            result = query_insert(query, conn)
    rate = True
    print("here", rate)
    return render_template("myrating.html", username = session['email'],rate = rate, comment = comment)

@app.route('/search_flights', methods=['GET'])
def search_flights_get():
    return render_template("search_flights.html")

@app.route('/search_flights', methods=['POST'])
def search_flights_post():
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')
    if airport_depart_name:
        query = "SELECT * FROM flight WHERE airport_depart_name = '{}' AND airport_arrive_name = '{}' \
            AND DATE(depart_date_time) = '{}'".format(airport_depart_name, airport_arrive_name, airport_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('search_flights.html', flights1 = response)

    elif depart_city:
        query = "SELECT * FROM flight WHERE airport_depart_name = (SELECT name FROM Airport WHERE city = '{}') \
            AND airport_arrive_name = (SELECT name FROM Airport WHERE city = '{}') \
            AND DATE(depart_date_time) = '{}'".format(depart_city, arrive_city, city_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('search_flights.html', flights1 = response)

    elif flight_num:
        query = "SELECT * FROM flight WHERE flight_num = '{}' AND DATE(arrive_date_time) = '{}'\
            AND DATE(depart_date_time) = '{}'".format(flight_num, arrive_date, depart_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('search_flights.html', flights2 = response)
    
@app.route('/purchasing', methods=['GET'])
def purchasing_get():
    return render_template("purchasing.html",username=session['email'])

@app.route('/purchasing', methods=['POST'])
def purchasing_post():
    airline_name = request.form.get('airline_name')
    flight_number = request.form.get('flight_number')
    depart_date_time = request.form.get('depart_date_time')
    expiration_date = request.form.get('expiration_dare')
    expiration_date = expiration_date + "-01"
    card_type = request.form.get('card_type')
    name_on_card = request.form.get('name_on_card')
    card_num = request.form.get('card_num')
    ID = randint(1, 99999)
    purchase_date_time = date.today()
    #calculate sold price
    #get passenger number
    if airline_name:
        query = "SELECT count(*) as total FROM Ticket WHERE flight_num = '{}' AND DATE(depart_date_time) = '{}'\
        AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        result = query_fetchone(query, conn)
        print(result)
        passenger_num = int(result["total"])
        print("passenger_num", passenger_num)

        query_seat = "SELECT num_of_seats,base_price,depart_date_time as depart_time FROM Airplane natural join Flight WHERE Flight.airplane_id = Airplane.ID AND flight_num = '{}' AND DATE(depart_date_time) = '{}'\
        AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        seat_query = query_fetchone(query_seat, conn)
        print(query_seat)
        print(seat_query)
        print("seat_query",seat_query)
        seat_num = int(seat_query["num_of_seats"])
        print("seat_num",seat_num)


        print("seat number:", seat_num)
        print("passenger number:", passenger_num)
        if seat_num <= passenger_num:
            flash("The flight is already full!")
            return render_template("purchasing.html",username=session['email'])
        
        if seat_num*0.7<passenger_num:
            sold_price = 1.2*int(seat_query["base_price"])
        else:
            sold_price = int(seat_query["base_price"])
        print("sold_price",sold_price)
        
        query = "INSERT INTO Ticket VALUES ('{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}')".format(ID, sold_price, card_type, card_num, name_on_card, str(expiration_date), str(purchase_date_time), airline_name, flight_number, seat_query['depart_time'])
        result = query_fetchall(query, conn)
        
        query2 = "INSERT INTO Cust_buy VALUES ('{}', '{}')".format(session['email'],ID)
        result = query_fetchall(query2, conn)
        return render_template("purchasing.html",username=session['email'], purchase =True )
    return render_template("purchasing.html",username=session['email'])

@app.route('/home_agent', methods=['GET'])
def agent_page_get():
    return render_template('home_agent.html',username=session['email'])

@app.route('/home_agent', methods=['POST'])
def agent_page():
    print(session['email'])
    print(session['role'])
    if session['role'] =="agent":
        return render_template("home_agent.html", username=session['email'])

    return redirect('/login')

@app.route('/agent_topcustomers', methods=['GET', 'POST'])
def agent_topcustomers():
    six_month_ago = date.today() + relativedelta(months=-6)
    one_year_ago = date.today() + relativedelta(months=-12)

    # Top 5 customers based on number of tickets bought in past 6 months
    query = "SELECT distinct name, COUNT(*) AS num_of_tickets FROM Customer, Agent_buy NATURAL JOIN Ticket\
        WHERE Customer.email=Agent_buy.customer_email AND booking_agent_email='{}' AND DATE(purchase_date_time)>='{}'\
        AND ID=ticket_ID GROUP BY name ORDER BY num_of_tickets DESC".format(session['email'], six_month_ago)
    print(query)
    six_month_top = query_fetchall(query, conn)
    #print(six_month_top)
    for c in six_month_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(six_month_top) < 5:
        top_customer_tkts = six_month_top
    else:
        top_customer_tkts = six_month_top[0:5]
    print(top_customer_tkts)

    # Top 5 customers based on amount of commission received in the last year
    query = "SELECT name, SUM(commission) AS sum_commission FROM Customer, Agent_buy NATURAL JOIN Ticket\
        WHERE Customer.email=Agent_buy.customer_email AND booking_agent_email='{}' AND DATE(purchase_date_time)>='{}'\
        AND ID=ticket_ID GROUP BY name ORDER BY sum_commission DESC".format(session['email'], one_year_ago)
    print(query)
    one_year_top = query_fetchall(query, conn)
    for c in one_year_top:
        c["sum_commission"] = float(c["sum_commission"])
    #print(one_year_top)
    if len(one_year_top) < 5:
        top_customer_comm = one_year_top
    else:
        top_customer_comm = one_year_top[0:5]
    print(top_customer_comm)

    labels = [ item['name'] for item in top_customer_tkts]
    datas = [ item['num_of_tickets'] for item in top_customer_tkts]
    print(labels)
    print(datas)
    return render_template("agent_topcustomers.html", username=session['email'], top_customer_tkts=top_customer_tkts,\
        top_customer_comm=top_customer_comm,label_chart = labels,data = datas)

@app.route('/agent_myflight', methods=['GET'])
def agent_myflight_get():
    print(session['email'])
    today = date.today()
    query = "SELECT DISTINCT * FROM Agent_buy, Ticket NATURAL JOIN Flight WHERE ticket.ID = Agent_buy.ticket_ID \
        AND Agent_buy.booking_agent_email = '{}' AND depart_date_time>'{}'".format(session['email'], today)
    my_flights = query_fetchall(query, conn)
    print("my_flights response: ", my_flights)
    return render_template("agent_myflight.html", flights=my_flights, username=session['email'])

@app.route('/agent_mycommission', methods=['GET','POST'])
def agent_mycommission():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_month_ago = date.today() + relativedelta(days=-30)

    # total amount of commission in the past 30 days
    query = "SELECT SUM(commission) AS total FROM Agent_buy NATURAL JOIN Ticket WHERE booking_agent_email='{}' \
        AND DATE(purchase_date_time)>='{}' AND ID=ticket_ID".format(session['email'], one_month_ago)
    print(query)
    # total = float(query_fetchall(query, conn)[0]["total"])
    if query_fetchall(query, conn)[0]["total"] is None:
        total = 0
    else:
        total = float(query_fetchall(query, conn)[0]["total"])
    print("30 days commission:", total)

    # average commission
    query2 = "SELECT COUNT(*) AS num FROM Agent_buy NATURAL JOIN Ticket WHERE booking_agent_email='{}' \
        AND DATE(purchase_date_time)>='{}'AND ID=ticket_ID".format(session['email'], one_month_ago)
    print(query2)
    if query_fetchall(query, conn)[0]["total"] is None:
        num_of_tickets = 0
    else:
        num_of_tickets = query_fetchall(query2, conn)[0]["num"]
    # num_of_tickets = query_fetchall(query2, conn)[0]["num"]
    print("30 days number of tickets bought:", num_of_tickets)
    average = total/num_of_tickets
    print("30 days average commission received:", average)

    # specift a range
    if from_date:
        query = "SELECT SUM(commission) AS total FROM Agent_buy NATURAL JOIN Ticket WHERE booking_agent_email='{}' \
        AND DATE(purchase_date_time) between '{}' and '{}'AND ID=ticket_ID".format(session['email'], from_date, to_date)
        print(query)
        if query_fetchall(query, conn)[0]["total"] is None:
            range_total = 0.0
        else:
            range_total = float(query_fetchall(query, conn)[0]["total"])
        print("Total commission:", range_total)
        if range_total ==None:
            no_comm=True
        else:
            no_comm=False
        query2 = "SELECT COUNT(*) AS num FROM Agent_buy NATURAL JOIN Ticket WHERE booking_agent_email='{}' \
        AND DATE(purchase_date_time) between '{}' and '{}'AND ID=ticket_ID".format(session['email'], from_date, to_date)
        print(query2)
        if query_fetchall(query2, conn)[0]["num"] is None:
            range_num_tkts = 0.0
        else:
            range_num_tkts = query_fetchall(query2, conn)[0]["num"]
        # range_num_tkts = query_fetchall(query2, conn)[0]["num"]
        print("Number of tickets:", range_num_tkts)

        return render_template("agent_mycommission.html", username=session['email'], total=total, \
            num_of_tickets=num_of_tickets, average=average, range_total=range_total, range_num_tkts=range_num_tkts, show = True,no_comm = no_comm)
    return render_template("agent_mycommission.html", username=session['email'], total=total, \
            num_of_tickets=num_of_tickets, average=average)

@app.route('/agent_search', methods=['GET'])
def agent_search_get():
    return render_template("agent_search.html", username=session['email'])

@app.route('/agent_search', methods=['POST'])
def agent_search_post():
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')
    if airport_depart_name:
        query = "SELECT * FROM flight NATURAL JOIN ticket WHERE airport_depart_name = '{}' AND airport_arrive_name = '{}' \
            AND DATE(depart_date_time) = '{}'".format(airport_depart_name, airport_arrive_name, airport_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('agent_search.html', flights1 = response, username=session['email'])

    elif depart_city:
        query = "SELECT * FROM flight NATURAL JOIN ticket WHERE airport_depart_name = (SELECT name FROM Airport WHERE city = '{}') \
            AND airport_arrive_name = (SELECT name FROM Airport WHERE city = '{}') \
            AND DATE(depart_date_time) = '{}'".format(depart_city, arrive_city, city_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('agent_search.html', flights1 = response, username=session['email'])

    elif flight_num:
        query = "SELECT * FROM flight NATURAL JOIN ticket WHERE flight_num = '{}' AND DATE(arrive_date_time) = '{}'\
            AND DATE(depart_date_time) = '{}'".format(flight_num, arrive_date, depart_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('agent_search.html', flights2 = response, username=session['email'])

@app.route('/agent_purchasing', methods=['GET'])
def agent_purchasing_get():
    return render_template("agent_purchasing.html", username=session['email'])

@app.route('/agent_purchasing', methods=['POST'])
def agent_purchasing_post():
    customer_email = request.form.get('customer_email')
    airline_name = request.form.get('airline_name')
    flight_number = request.form.get('flight_number')
    depart_date_time = request.form.get('depart_date_time')
    expiration_date = request.form.get('expiration_dare')
    card_type = request.form.get('card_type')
    name_on_card = request.form.get('name_on_card')
    card_num = request.form.get('card_num')
    ID = randint(1, 99999)
    purchase_date_time = date.today()

    #calculate sold price
    #get passenger number
    if airline_name:
        query = "SELECT count(*) as total FROM Ticket WHERE flight_num = '{}' AND DATE(depart_date_time) = '{}'\
            AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        result = query_fetchone(query, conn)
        print(result)
        passenger_num = int(result["total"])
        print("passenger_num", passenger_num)

        query_seat = "SELECT num_of_seats,base_price,depart_date_time as depart_time FROM Airplane natural join Flight \
            WHERE Flight.airplane_id = Airplane.ID AND flight_num = '{}' AND DATE(depart_date_time) = '{}'\
            AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        print(query_seat)
        seat_query = query_fetchone(query_seat, conn)
        print(seat_query)
        print("seat_query",seat_query)
        if seat_query is None:
            seat_num = 0
        else:
            seat_num = int(seat_query["num_of_seats"])
        print("seat_num",seat_num)

        if seat_num <= passenger_num:
            flash("The flight is already full!")
            return render_template("agent_purchasing.html", username=session['email'])
        
        if seat_num*0.7<passenger_num:
            sold_price = 1.2*int(seat_query["base_price"])
        else:
            sold_price = int(seat_query["base_price"])
        print("sold_price",sold_price)
        
        query = "INSERT INTO Ticket VALUES ('{}', '{}', '{}','{}', '{}', '{}',\
            '{}', '{}', '{}','{}')".format(ID, sold_price, card_type, card_num, name_on_card, \
            str(expiration_date), str(purchase_date_time), airline_name, flight_number, seat_query['depart_time'])
        print(query)
        result = query_fetchall(query, conn)

        commission = 0.1*sold_price
        query2 = "INSERT INTO Agent_buy VALUES ('{}', '{}', '{}', '{}')".format(session['email'], customer_email, ID, commission)
        print(query2)
        result = query_fetchall(query2, conn)

        return render_template("agent_purchasing.html", username=session['email'], purchase=True)
    return render_template("agent_purchasing.html", username=session['email'])


@app.route('/home_staff', methods=['GET'])
def staff_page_get():
	return render_template('home_staff.html', username=session['email'])

@app.route('/home_staff', methods=['POST'])
def staff_page():
    print(session['email'])
    print(session['role'])            
    return render_template("home_staff.html", username=session['email'])


@app.route('/staff_search_flight', methods=['GET'])
def staff_search_flight_get():
    one_months_next = date.today() + relativedelta(months=+1)
    date_today = date.today()
    # Show airline flights
    print(session['email'])
    query = "SELECT * FROM Flight natural join Airline_staff WHERE user_name = '{}'and depart_date_time>'{}' and depart_date_time<'{}'".format(session['email'],date_today, one_months_next)
    airline_flights = query_fetchall(query, conn)
    print(airline_flights)
    return render_template("staff_search_flight.html", flights=airline_flights, username = session['email'])

@app.route('/staff_search_flight', methods=['POST'])
def staff_search_flight_post():
    # Show airline flights
    print(session['email'])
    query = "SELECT * FROM Flight natural join Airline_staff WHERE user_name = '{}' ".format(session['email'])
    airline_flights = query_fetchall(query, conn)
    print(airline_flights)
    #search flights
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')
    
    customer_depart_date_time = request.form.get('customer_depart_date_time')
    customer_flight_num = request.form.get('customer_flight_number')
    customer_airline_name = request.form.get('customer_airline_name')
    
    status_depart_date_time = request.form.get('status_depart_date_time')
    status_flight_num = request.form.get('status_flight_number')
    status_airline_name = request.form.get('status_airline_name')
    
    if airport_depart_name:
        query = "SELECT * FROM flight natural join Airline_staff WHERE airport_depart_name = '{}' AND airport_arrive_name = '{}' \
            AND DATE(depart_date_time) = '{}' AND user_name = '{}'".format(airport_depart_name, airport_arrive_name, airport_date,session['email'])
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html',  flights=airline_flights, flights1 = response,username = session['email'])
    elif depart_city:
        query = "SELECT * FROM flight natural join Airline_staff WHERE airport_depart_name = (SELECT name FROM Airport WHERE city = '{}') \
            AND airport_arrive_name = (SELECT name FROM Airport WHERE city = '{}') \
            AND DATE(depart_date_time) = '{}' AND user_name = '{}'".format(depart_city, arrive_city, city_date,session['email'])
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html', flights=airline_flights,  flights1 = response,username = session['email'])
    elif flight_num:
        query = "SELECT * FROM flight natural join Airline_staff WHERE flight_num = '{}' AND DATE(arrive_date_time) = '{}'\
            AND DATE(depart_date_time) = '{}' AND user_name = '{}'".format(flight_num, arrive_date, depart_date,session['email'])
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html',  flights=airline_flights, flights2 = response,username = session['email'])
    # search for status
    elif status_flight_num:
        query = "SELECT status FROM flight WHERE flight_num = '{}' AND DATE(depart_date_time) = '{}' AND airline_name = '{}'".format(status_flight_num, status_depart_date_time, status_airline_name)
        print(query)
        response = query_fetchall(query, conn)
        print(response[0]["status"])
        return render_template('staff_search_flight.html',  flights=airline_flights, flights_status = response[0]["status"],username = session['email'])
    # search for customer number
    elif customer_flight_num:
        query = "SELECT count(*) as num FROM flight natural join ticket WHERE flight_num = '{}' AND DATE(depart_date_time) = '{}' AND airline_name = '{}'".format(customer_flight_num, customer_depart_date_time, customer_airline_name)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html',  flights=airline_flights, flight_customer = response[0]["num"], username = session['email'])
    return render_template('staff_search_flight.html')

@app.route('/staff_rating', methods=['GET'])
def staff_rating_get():
    print(session['email'])
    #get airline name of the staff
    query_airline = "SELECT airline_name FROM Airline_staff WHERE user_name = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    print("staff_airline_name",staff_airline_name)
    # get average rating
    query = "SELECT airline_name, flight_num, depart_date_time, avg(points) as avg FROM Flight natural join Rate where airline_name = '{}' group by flight_num, airline_name, depart_date_time".format(staff_airline_name)
    avg_rating_response = query_fetchall(query, conn)
    print("avg_rating_response",avg_rating_response)
    if len(avg_rating_response)==0:
        print("len ==0")
        no_rate = True
        return render_template("staff_rating.html", staff_airline_name = staff_airline_name, username = session['email'], no_rate = no_rate)
    # get rating from each customer 
    query = "SELECT * FROM Rate where airline_name = '{}'".format(staff_airline_name)
    all_rating = query_fetchall(query, conn)
    no_rate = False
    print(all_rating)
    return render_template("staff_rating.html", staff_airline_name = staff_airline_name, avg_rating = avg_rating_response, all_rating=all_rating, username = session['email'], no_rate=no_rate)

@app.route('/staff_rating', methods=['POST'])
def staff_rating_post():
    #get airline name of the staff
    query_airline = "SELECT airline_name FROM Airline_staff WHERE user_name = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    print("staff_airline_name",staff_airline_name)
    
    return render_template("staff_rating.html", staff_airline_name = staff_airline_name, username = session['email'])

@app.route('/staff_update_flights', methods=['GET'])
def staff_update_flights_get():
    if session['role'] != 'staff':
        err = "You are not a staff!"
        print( session['role'])
        flash(err)
        return redirect('/login_staff')
    else:
        #get airline name of the staff
        query_airline = "SELECT airline_name FROM Airline_staff WHERE user_name = '{}' ".format(session['email'])
        staff_airline =  query_fetchone(query_airline, conn)
        staff_airline_name = staff_airline["airline_name"]
        print("staff_airline_name",staff_airline_name)
        #get airplane of the airline
        query = "SELECT * FROM Flight where airline_name = '{}'".format(staff_airline_name)
        all_airplane = query_fetchall(query, conn)
        print("all airplane",all_airplane)
        return render_template("staff_update_flights.html", all_airplane = all_airplane, staff_airline_name = staff_airline_name, username = session['email'])

@app.route('/staff_update_flights', methods=['POST'])
def staff_update_flights_post():
    #get airline name of the staff
    query_airline = "SELECT airline_name FROM Airline_staff WHERE user_name = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    print("staff_airline_name",staff_airline_name)
    #create flights
    create_airline_name = request.form.get('create_airline_name')
    create_flight_number = request.form.get('create_flight_number')
    create_airline_id = request.form.get('create_airline_id')
    create_depart_date_time = request.form.get('create_depart_date_time')
    create_arrival_date_time = request.form.get('create_arrival_date_time')
    create_airport_depart_name = request.form.get('create_airport_depart_name')
    create_airport_arrival_name = request.form.get('create_airport_arrival_name')
    create_status = request.form.get('create_status')
    create_base_price = request.form.get('create_base_price')
    #change flight status
    status_depart_date_time = request.form.get('status_depart_date_time')
    status_flight_num = request.form.get('status_flight_number')
    status_airline_name = request.form.get('status_airline_name')
    status_status = request.form.get('status_status')   
    #add airplane
    add_airplane_id = request.form.get('add_airplane_id')
    add_num_of_seats = request.form.get('add_num_of_seats')
    add_airline_name = request.form.get('add_airline_name')
    #add airport
    airport_name = request.form.get('airport_name')
    airport_city = request.form.get('airport_city')
    
    if session['role'] != 'staff':
        err = "You are not a staff!"
        print( session['role'])
        flash(err)
        return redirect('/login_staff')
    else:
        if create_airline_name:
        #insert new flight
            query = 'INSERT INTO Flight VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format\
                (create_airline_name, create_flight_number, create_depart_date_time, create_arrival_date_time, create_status, create_base_price,create_airline_id,create_airport_depart_name,create_airport_arrival_name)
            result = query_insert(query, conn)
            if result == 0:
                flash("Request denied, please try one more time!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        elif status_flight_num:
            query = 'UPDATE Flight SET status = "{}" WHERE airline_name= "{}" AND flight_num = "{}" AND DATE(depart_date_time) = "{}" '.format\
                (status_status, status_airline_name, status_flight_num, status_depart_date_time)
            result = query_insert(query, conn)
            print("change status",query)
            print(result)
            if result == 0:
                flash("No flight exists!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        elif add_airplane_id:
            query = 'INSERT INTO Airplane VALUES("{}", "{}", "{}")'.format(add_airline_name, add_airplane_id, add_num_of_seats)
            result = query_insert(query, conn)
            print("add airplane",query)
            print(result)
            if result == 0:
                flash("Unable to add flight!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        elif airport_city:
            query = 'INSERT INTO Airport VALUES("{}", "{}")'.format(airport_name, airport_city)
            result = query_insert(query, conn)
            print("add airport",query)
            print(result)
            if result == 0:
                flash("Unable to add airport!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        else:
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = False)

@app.route('/staff_revenue', methods=['GET'])
def staff_revenue_get():
    query_airline = "SELECT airline_name FROM Airline_staff WHERE user_name = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    labels = []
    today = date.today()
    one_month_ago = today + relativedelta(months=-1)
    one_year_ago = today + relativedelta(years=-1)
    # Direct sales in the last month
    query1 = "SELECT SUM(sold_price) AS v FROM Ticket NATURAL JOIN Cust_buy WHERE ID=ticket_ID AND airline_name = '{}' \
        AND purchase_date_time BETWEEN '{}' AND '{}'".format(staff_airline_name, one_month_ago, today)
    print(query1)
    result = query_fetchall(query1, conn)
    print(result)
    print(result[0]['v'])
    if result[0]['v'] == None:
        result[0]['v']  =0
    labels.extend(result)
    
    # Indirect sales in the last month
    query2 = "SELECT SUM(sold_price) AS v FROM Ticket NATURAL JOIN Agent_buy WHERE ID=ticket_ID AND airline_name = '{}' \
        AND purchase_date_time BETWEEN '{}' AND '{}'".format(staff_airline_name, one_month_ago, today)
    print(query2)
    result = query_fetchall(query2, conn)
    if result[0]['v']   == None:
        result[0]['v']  =0
    labels.extend(result)
        
    # Direct sales in the last year
    query3 = "SELECT SUM(sold_price) AS v FROM Ticket NATURAL JOIN Cust_buy WHERE ID=ticket_ID AND airline_name = '{}' \
        AND purchase_date_time BETWEEN '{}' AND '{}'".format(staff_airline_name, one_year_ago, today)
    print(query3)
    result = query_fetchall(query3, conn)
    if result[0]['v']  == None:
        result[0]['v']  =0
    labels.extend(result)
    
    # Indirect sales in the last year
    query4 = "SELECT SUM(sold_price) AS v FROM Ticket NATURAL JOIN Agent_buy WHERE ID=ticket_ID AND airline_name = '{}' \
        AND purchase_date_time BETWEEN '{}' AND '{}'".format(staff_airline_name, one_year_ago, today)
    print(query4)
    result = query_fetchall(query4, conn)
    if result[0]['v']   == None:
        result[0]['v']  =0
    labels.extend(result)
    
    for value in labels:
        value['v'] = float(value['v'])
    print(labels)
    
    return render_template("staff_revenue.html", staff_airline_name = staff_airline_name, username = session['email'], labels = labels)

@app.route('/staff_allagents', methods=['GET'])
def staff_allagents_get():
    one_month_ago = date.today() + relativedelta(months=-1)
    one_year_ago = date.today() + relativedelta(months=-12)

    # Top 5 agents based on the number of tickets sales for the past month
    query = "SELECT booking_agent_email, COUNT(*) AS num_of_tickets FROM Agent_buy NATURAL JOIN Ticket\
        WHERE ID=ticket_ID AND DATE(purchase_date_time)>='{}' GROUP BY booking_agent_email ORDER BY num_of_tickets DESC".format(one_month_ago)
    print(query)
    one_month_top = query_fetchall(query, conn)
    for c in one_month_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(one_month_top) < 5:
        top_agent_tkts = one_month_top
    else:
        top_agent_tkts = one_month_top[0:5]
    print(top_agent_tkts)

    # Top 5 agents based on the number of tickets sales for the past year
    query = "SELECT booking_agent_email, COUNT(*) AS num_of_tickets FROM Agent_buy NATURAL JOIN Ticket\
        WHERE ID=ticket_ID AND DATE(purchase_date_time)>='{}' GROUP BY booking_agent_email ORDER BY num_of_tickets DESC".format(one_year_ago)
    print(query)
    tkts_one_year_top = query_fetchall(query, conn)
    for c in tkts_one_year_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(tkts_one_year_top) < 5:
        top_agent_tkts_year = tkts_one_year_top
    else:
        top_agent_tkts_year = tkts_one_year_top[0:5]
    print(top_agent_tkts_year)

    # Top 5 agents based on the amount of commission received for the last year
    query = "SELECT booking_agent_email, SUM(commission) AS sum_commission FROM Agent_buy NATURAL JOIN Ticket\
        WHERE ID=ticket_ID AND DATE(purchase_date_time)>='{}' GROUP BY booking_agent_email ORDER BY sum_commission DESC".format(one_year_ago)
    print(query)
    one_year_top = query_fetchall(query, conn)
    for c in one_year_top:
        c["sum_commission"] = float(c["sum_commission"])
    #print(one_year_top)
    if len(one_year_top) < 5:
        top_agent_comm = one_year_top
    else:
        top_agent_comm = one_year_top[0:5]
    print(top_agent_comm)

    return render_template("staff_allagents.html", username=session['email'], top_agent_tkts=top_agent_tkts, \
        top_agent_tkts_year=top_agent_tkts_year, top_agent_comm=top_agent_comm)

@app.route('/staff_destination', methods=['GET'])
def staff_destination_get():
    three_month_ago = date.today() + relativedelta(months=-3)
    one_year_ago = date.today() + relativedelta(months=-12)
    today_date = date.today()
    # Top 3 popular destination in past 3 months (based on number of tickets bought)
    query = "SELECT distinct city, COUNT(*) AS num_of_tickets FROM Airport, Flight NATURAL JOIN Ticket\
        WHERE airport_arrive_name = Airport.name AND DATE(depart_date_time)>='{}' AND DATE(purchase_date_time)<='{}' GROUP BY name ORDER BY num_of_tickets DESC".format(three_month_ago,today_date)
    print(query)
    three_month_top = query_fetchall(query, conn)
    #print(six_month_top)
    for c in three_month_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(three_month_top) < 5:
        top_destination_three_month = three_month_top
    else:
        top_destination_three_month = three_month_top[0:5]
    print(top_destination_three_month)

    # Top 3 popular destination in last year (based on number of tickets bought)
    query = "SELECT distinct city, COUNT(*) AS num_of_tickets FROM Airport, Flight NATURAL JOIN Ticket\
        WHERE airport_arrive_name = Airport.name AND DATE(depart_date_time)>='{}' AND DATE(purchase_date_time)<='{}' GROUP BY name ORDER BY num_of_tickets DESC".format(one_year_ago,today_date)
    one_year_top = query_fetchall(query, conn)
    for c in one_year_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(one_year_top) < 5:
        top_destination_one_year = one_year_top
    else:
        top_destination_one_year = one_year_top[0:5]
    
    return render_template("staff_destination.html", username=session['email'], top_destination_one_year=top_destination_one_year,\
        top_destination_three_month=top_destination_three_month)

@app.route('/staff_destination', methods=['POST'])
def staff_destination_post():
    return render_template("staff_destination.html",username=session['email'])

@app.route('/staff_view_report', methods=['GET'])
def sstaff_view_report_get():
    one_year_ago = date.today() + relativedelta(months=-12)
    today_date = date.today()
    # report in past year
    query = "SELECT COUNT(*) AS num_of_tickets, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Ticket " \
        "WHERE purchase_date_time >= '{}' AND purchase_date_time <= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
        "(purchase_date_time)".format(one_year_ago,today_date)
    print(query)
    one_year_tkt = query_fetchall(query, conn)
    for c in one_year_tkt:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    print(one_year_tkt)

    return render_template("staff_view_report.html", username=session['email'], one_year_tkt=one_year_tkt)

@app.route('/staff_view_report', methods=['POST'])
def staff_view_report_post():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_year_ago = date.today() + relativedelta(months=-12)
    today_date = date.today()
    # report in past year
    query = "SELECT COUNT(*) AS num_of_tickets, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Ticket " \
        "WHERE purchase_date_time >= '{}' AND purchase_date_time <= '{}' GROUP BY YEAR(purchase_date_time), MONTH" \
        "(purchase_date_time)".format(one_year_ago,today_date)
    print(query)
    one_year_tkt = query_fetchall(query, conn)
    for c in one_year_tkt:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    print(one_year_tkt)

    # report in a specified range
    if from_date:
        query = "SELECT COUNT(*) AS num_of_tickets, YEAR(purchase_date_time) AS y, MONTH(purchase_date_time) AS m FROM Ticket \
        WHERE purchase_date_time >= '{}' AND purchase_date_time <= '{}' GROUP BY YEAR(purchase_date_time), MONTH \
        (purchase_date_time)".format(from_date,to_date)
        print(query)
        range_tkt = query_fetchall(query, conn)
        for c in range_tkt:
            c["num_of_tickets"] = int(c["num_of_tickets"])
        print(one_year_tkt)

    return render_template("staff_view_report.html",username=session['email'], one_year_tkt=one_year_tkt, range_tkt=range_tkt)


@app.route('/staff_frequent_customer', methods=['GET'])
def staff_frequent_customer_get():
    #most frequent customer
    one_year_ago = date.today() + relativedelta(months=-12)
    print(session['email'])
    query = "SELECT email, count(*) as num_of_tickets FROM Cust_buy, Ticket WHERE Cust_buy.ticket_ID = Ticket.ID AND purchase_date_time>='{}' GROUP BY email".format(one_year_ago)
    cust_buy_tkt = query_fetchall(query, conn)
    print(cust_buy_tkt)
    
    query = "SELECT customer_email, count(*) as num_of_tickets FROM Agent_buy, Ticket WHERE Agent_buy.ticket_ID = Ticket.ID AND purchase_date_time>='{}' GROUP BY customer_email".format(one_year_ago)
    agent_buy_tkt = query_fetchall(query, conn)
    print(agent_buy_tkt)   
    
    email_list = []
    for item in cust_buy_tkt:
        email_list.append(item['email'])
    print(" ")
    print(email_list)
    
    
    
    for item in agent_buy_tkt:
        if item['customer_email'] in email_list:
            for item2 in cust_buy_tkt:
                if item2['email'] == item['customer_email']:
                    item2['num_of_tickets'] += item['num_of_tickets']
        else:    
            cust_buy_tkt.append(item)
                    
    max_cust = cust_buy_tkt[0]
    for item in cust_buy_tkt:
        if item['num_of_tickets']>=max_cust['num_of_tickets']:
            max_cust = item
            
    #see flights of a particular customer on particular airline
    query_airline = "SELECT airline_name FROM Airline_staff WHERE user_name = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    
    query = "SELECT * FROM Cust_buy, Ticket natural join Flight WHERE ticket.ID = Cust_buy.ticket_ID and airline_name = '{}' ".format(staff_airline_name)
    query2 = "SELECT * FROM Agent_buy, Ticket natural join Flight WHERE ticket.ID = Agent_buy.ticket_ID and airline_name = '{}' ".format(staff_airline_name)
    print('my_flights SQL: ', query+query2)
    cust_flights_customer = query_fetchall(query, conn)
    cust_flights_agent = query_fetchall(query2, conn)
    if len(cust_flights_customer)>0:
        if len(cust_flights_agent)>0:
            cust_flights_customer+=cust_flights_agent
        cust_flights =cust_flights_customer
    else:
        if len(cust_flights_agent)>0:
            cust_flights =cust_flights_agent
    print('cust_flights response: ', cust_flights)
    
    return render_template("/staff_frequent_customer.html", flights=cust_flights,staff_airline_name = staff_airline_name,  max_cust = max_cust, username = session['email'])

@app.route('/staff_frequent_customer', methods=['POST'])
def staff_frequent_customer_post():
    return render_template('/staff_frequent_customer.html', username = session['email'])

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect("/login")


if __name__ == "__main__":
    app.run('127.0.0.1', 5000)
    

    
    # w={'index':1, 'treatment_site':10, 'T':10}
    # s, ml=match(w)
    # print(s)
    # print(ml)
