
import PySimpleGUI as sg;
import mysql.connector as connector



# from userPageGUI import userPage;

def buyShares(email,password,portfolioCompaniesUser,userQty):

    con = connector.connect(host='localhost',
            port='3306',
            user='root',
            password='mySql@123',
            database='project1');

    cur = con.cursor(buffered = True);

    layout = [
        [sg.Text("----Enter the details of the shares to be bought----")],
        [sg.Text("Company Name: ", size=(20,1)) , sg.Input(key='-company-', size=(20,1))],
        [sg.Text("Qty: ", size=(20,1)) , sg.Input(key='-qty-', size=(20,1))],
        [sg.Text("Password: ", size=(20,1)) , sg.Input(key ='password', size=(20,1))],
        [sg.Button('OK')]
    ];

    window = sg.Window("buyShares" , layout , size = (400,400));

    while True:
        event,values = window.read();
        inputPassword = values['password'];

        if(event == 'OK'):
            if(inputPassword != password):
                window['password'].update('Invalid Password! Access denied!');
                window.close();

                layout1 = [
                    [sg.Text("INVALID PASSWORD!")],
                    [sg.Text("Access denied!")],
                    [sg.Button("OK")]
                ];

                window1 = sg.Window("AccessDenied" , layout1, size= (200,100));

                while True:
                    event,values = window1.read();

                    if(event == sg.WINDOW_CLOSED):
                        break;
                    
                    if(event == 'OK'):
                        window1.close();
                        break;


            else:
                print("Update table");
                company = values['-company-'];
                qty = values['-qty-'];
                print(portfolioCompaniesUser);
                print(userQty);

                if company in portfolioCompaniesUser:
                    #update
                    query = "update portfolio set Qty = Qty + {} where (email = '{}' AND company_name = '{}')".format(qty,email,company);
                else:
                    #insert new company
                    queryForBuyPrice = "select ltp from stock_info where company_name = '{}'".format(company);
                    cur.execute(queryForBuyPrice);
                    buyPriceRecords = cur.fetchall();
                    for row in buyPriceRecords:
                        buyPrice = row[0];


                    query = "insert into portfolio values ('{}' , '{}' , {} , {})".format(email,company,qty,buyPrice);

                cur.execute(query);
                con.commit();
                print("updated");

                layout2 = [
                    [sg.Text("The stocks have been credited to your account")],
                    [sg.Button("OK")]
                ];

                window2 = sg.Window("Credited" , layout2 , size = (400,100));

                while True:
                    event,values = window2.read();
                    if(event == sg.WINDOW_CLOSED):
                        # userPage(email,password);
                        break;

                    if(event == 'OK'):
                        userPage(email,password);
                        window2.close();
                        break;
            
            window.close();





        if(event == sg.WINDOW_CLOSED):
            break;

    window.close();


def userPage(email,password):

    con = connector.connect(host='localhost',
            port='3306',
            user='root',
            password='mySql@123',
            database='project1');

    cur = con.cursor(buffered = True);


    #getting fname and lname corresponding to the email
    query = "select fname,lname from user_info where email = '{}'".format(email);

    cur.execute(query);
    nameRecords = cur.fetchall();


    for name in nameRecords:
        fname = name[0];
        lname = name[1];

    print(fname +" " + lname);

    #getting portfolio companies corresponding to the email
    queryForPortfolioCompanies = "select company_name from portfolio where email = '{}'".format(email);
    cur.execute(queryForPortfolioCompanies);
    portfolioCompaniesRecords = cur.fetchall();

    portfolioCompaniesUser = [];
    for portfollioCompany in portfolioCompaniesRecords:
        company = portfollioCompany[0];
        portfolioCompaniesUser.append(company);
        print(company);

    portfolioCompaniesUserLtp = [];
    for company in portfolioCompaniesUser:
        queryForLtp = "select ltp from stock_info where company_name = '{}'".format(company);
        cur.execute(queryForLtp);
        ltp = cur.fetchall();

        for lastPrice in ltp:
            portfolioCompaniesUserLtp.append(lastPrice[0]);
            print(lastPrice);


    userQty = [] ;
    userBuyPrice = [];
    for company in portfolioCompaniesUser:
        query = "select buy_price , Qty from portfolio where email = '{}' AND company_name = '{}'".format(email,company);
        cur.execute(query);

        infoRecord = cur.fetchall();

        for row in infoRecord:
            userQty.append(row[1]);
            userBuyPrice.append(row[0]);







    #for the message to be displayed on the GUI
    noOfCompaniesInPortfolio = len(portfolioCompaniesRecords);
    if(len(portfolioCompaniesRecords) == 0):
        print("Empty portfolio!");
        message = "EMPTY PORTFOLIO!";
    else:
        message = str(noOfCompaniesInPortfolio) + " companies currently in your portfolio.";

    i = 1;
    totalInvestedAmt = 0;
    currentValue = 0;
    for company in portfolioCompaniesUser:
        print(company);
        print(portfolioCompaniesUserLtp[i - 1]);
        print(userBuyPrice[i - 1]);
        print(userQty[i - 1]);
        totalInvestedAmt += (userBuyPrice[i - 1] * userQty[i - 1]);
        currentValue += (portfolioCompaniesUserLtp[i - 1] *  userQty[i - 1]);
        i+=1;
        print("end");






    length = len(portfolioCompaniesUser);
    layout = [
        [sg.Text("Hello, " + fname + " " + lname)],
        [sg.Text(message)],
        [sg.Text("Total Invested Amount = ") , sg.Text(totalInvestedAmt)],
        [sg.Text("Current Value of investment = ") , sg.Text(currentValue)],
        [sg.Text("                                  ------------------YOUR PORTFOLIO--------------         ")],
        [sg.Text("COMPANY",size = (15,1)) , sg.Text("LTP",size = (10,1)) , sg.Text("BUY_AVG",size = (10,1)) , sg.Text("QTY",size = (10,1)) , sg.Text("MTM",size = (10,1))],
        [[sg.Text(portfolioCompaniesUser[i],size = (15,1)) , sg.Text(portfolioCompaniesUserLtp[i] , size = (10,1)) , sg.Text(userBuyPrice[i] , size = (10,1)) , sg.Text(userQty[i] , size = (10,1)) , sg.Text((portfolioCompaniesUserLtp[i] - userBuyPrice[i]) * userQty[i] , size = (10 , 1))]for i in range(0 , length)],

        [sg.Button("Modify Portfolio")]
       
    ];

    window = sg.Window("User page- Portfolio" , layout , size = (600,600));

    while True:

        event , values = window.read();

        if(event == sg.WINDOW_CLOSED):
            break;

        if(event == 'Modify Portfolio'):
            window.close();
            buyShares(email,password,portfolioCompaniesUser,userQty);
            print("Returns to user page");
            userPage(email,password);


    
    window.close();


