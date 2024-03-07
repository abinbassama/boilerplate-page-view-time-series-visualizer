import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('./fcc-forum-pageviews.csv', index_col='date')

# Clean data
print(df['value'].quantile(0.800), df['value'].quantile(0.025))
df = df[(df['value'] < df['value'].quantile(0.975)) & (df['value'] > df['value'].quantile(0.025))]

###month dict
month_dict = {1: 'January',
              2: 'Feb',
              3: 'March',
              4: 'April',
              5: 'May',
              6: 'June',
              7: 'July',
              8: 'August',
              9: 'September',
              10: 'October',
              11: 'November',
              12: 'December'}
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.plot(df.index, df['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 150))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


# draw_line_plot()


def draw_bar_plot():
    df_bar = df.copy()
    df_bar['date'] = pd.to_datetime(df_bar.index)
    df_bar['month'] = df_bar['date'].dt.month
    df_bar['year'] = df_bar['date'].dt.year
    df_bar = df_bar[['month', 'year', 'value']]
    df_bar = df_bar.groupby(['year', 'month'])['value'].sum().reset_index()

    # df_bar['month'] = df_bar['month'].apply(lambda x : month_dict[x])
    print(df_bar.head())
    # Draw bar plot
    plt.subplots(figsize=(8, 8))
    pal = sns.color_palette("Paired")
    fig = sns.barplot(x="year",
                      y="value",
                      hue="month",
                      data=df_bar,
                      palette=pal)

    fig.set_xlabel('Years')
    fig.set_ylabel('Average Page Views')

    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles=handles, labels=month_names, title='Months', loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()

    df_box.reset_index(inplace=True)
    df_box['date']=pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20, 8))
    sns.boxplot(x='year',
                y='value',
                hue='year',
                data=df_box,
                ax=ax[0],
                palette='Set2',
                legend=False
                )  # Adjust palette for year-wise plot
    ax[0].set_ylabel("Page Views", size=14)
    ax[0].set_xlabel("Year", size=14)
    ax[0].set_title("Year-Wise Box Plot (Trend)", size=18)

    sns.boxplot(x='month',
                y='value',
                hue='month',
                data=df_box,
                ax=ax[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
               )  # Adjust palette for month-wise plot
    ax[1].set_ylabel("Page Views", size=14)
    ax[1].set_xlabel("Month", size=14)
    ax[1].set_title("Month-Wise Box Plot (Seasonality)", size=18)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
