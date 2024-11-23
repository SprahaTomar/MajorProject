from flask import current_app
from app import db, app
import matplotlib.pyplot as plt
import pandas as pd

def load_data():
    with app.app_context():
        projects_data = pd.read_sql("SELECT project_name, investment_goal, current_investment FROM projects", db.engine)
        investments_data = pd.read_sql("SELECT projects.project_name, investments.investor, SUM(investments.amount) AS total_investment "
                               "FROM investments "
                               "JOIN projects ON investments.project_id = projects.id "
                               "GROUP BY projects.project_name, investments.investor", db.engine)


        project_names = projects_data['project_name']
        investment_goals = projects_data['investment_goal']
        current_investments = projects_data['current_investment']

        investors = ['Investor1', 'Investor2', 'Investor3']  
        investors_investment = []  
        for investor in investors:
            investments_per_investor = investments_data[investments_data['investor'] == investor]
            investor_total_investment = investments_per_investor['total_investment']
            investors_investment.append(investor_total_investment)

        investment_dates = investments_data['investment_date']
        roi_values = investments_data['ROI']

        create_bar_chart(project_names, investment_goals)
        create_line_chart(project_names, current_investments, investment_goals)
        create_stacked_bar_chart(project_names, investors_investment, investors)
        #create_roi_line_chart(investment_dates, roi_values)

def create_bar_chart(project_names, investment_goals):
    plt.figure(figsize=(10, 6))
    plt.bar(project_names, investment_goals, color='blue')
    plt.xlabel('Project Name')
    plt.ylabel('Investment Goal')
    plt.title('Bar Chart of Investment Goals')
    plt.xticks(rotation=45)
    plt.savefig('bar_chart.png')
    plt.show()

def create_line_chart(project_names, current_investments, investment_goals):
    plt.figure(figsize=(10, 6))
    plt.plot(project_names, current_investments, label='Current Investment', marker='o')
    plt.plot(project_names, investment_goals, label='Investment Goal', marker='x')
    plt.xlabel('Project Name')
    plt.ylabel('Amount')
    plt.title('Line Chart of Project Progress')
    plt.xticks(rotation=45)
    plt.savefig('line_chart.png')
    plt.show()

def create_stacked_bar_chart(project_names, investors_investment, investors):
    plt.figure(figsize=(10, 6))
    bottom = [0] * len(project_names)
    for investor_investment, investor in zip(investors_investment, investors):
        plt.bar(project_names, investor_investment, bottom=bottom, label=investor)
        bottom = [sum(x) for x in zip(bottom, investor_investment)]
    plt.xlabel('Project Name')
    plt.ylabel('Total Investment')
    plt.title('Stacked Bar Chart of Investments per Project')
    plt.xticks(rotation=45)
    plt.savefig('stacked_bar_chart.png')
    plt.show()

'''def create_roi_line_chart(investment_dates, roi_values):
    plt.figure(figsize=(10, 6))
    plt.plot(investment_dates, roi_values, marker='o')
    plt.xlabel('Investment Date')
    plt.ylabel('ROI')
    plt.title('Line Chart of ROI Over Time')
    plt.xticks(rotation=45)
    plt.savefig('roi_line_chart.png')
    plt.show()'''

# Call the load_data function to execute the chart creation
load_data()
