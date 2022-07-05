# from email import message
import PySimpleGUI as sg;
import mysql.connector as connector;
from buySharesGUI import buyShares;


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


# userPage('rs123@gmail.com','rs@123');

    

