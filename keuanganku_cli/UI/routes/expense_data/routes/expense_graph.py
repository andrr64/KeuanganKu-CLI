import matplotlib.pyplot as plt

from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprint, kprintInfo, kline

from database.db import KDatabase
from database.helper.sql_expense import SQLExpense, ModelExpense
import random

def s_generateRandomHexColor() -> str:
    """Generate a random hexadecimal color code."""
    # Menghasilkan 6 digit hex color code secara acak
    return '#' + ''.join(random.choices('0123456789ABCDEF', k=6))

def dyn_generateChartData(expense_distribution: dict):
    data_length = len(expense_distribution)
    color = [s_generateRandomHexColor() for _ in range(data_length)]
    explosion = [0.05 for _ in range(data_length)]

    pie_data = list(expense_distribution.values())
    pie_labels = [f'{key}\n({value:,.0f})' for key, value in expense_distribution.items()]

    return pie_data, pie_labels, color, explosion

def UI_distribution_graph(db: KDatabase, title: str, distribution_func):
    expense_distribution = distribution_func(db.connection)

    if expense_distribution is None:
        clrscreen()
        kprintInfo('Something wrong...')
        return

    pie_data, pie_labels, color, explosion = dyn_generateChartData(expense_distribution)

    plt.pie(
        pie_data,
        colors=color,
        labels=pie_labels,
        autopct='%1.1f%%', pctdistance=0.80,
        explode=explosion,
        textprops={'fontsize': 10}
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    # Adding Title of chart
    total = sum(pie_data)
    plt.title(f'{title}\nTotal: {total:,.0f}')

    # Displaying Chart
    plt.show()

def UI_weeklyDistributionGraph(db: KDatabase):
    UI_distribution_graph(db, 'Weekly Expense Distribution', SQLExpense().readWeeklyDistribution)

def UI_monthlyDistributionGraph(db: KDatabase):
    UI_distribution_graph(db, 'Monthly Expense Distribution', SQLExpense().readMonthlyDistribution)

def UI_yearlyDistributionGraph(db: KDatabase):
    UI_distribution_graph(db, 'Yearly Expense Distribution', SQLExpense().readYearlyDistribution)