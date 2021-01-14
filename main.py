# Daniel Dupriest
# Data Engineering Winter 2021
# Jan 12 In-class activity

def main():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pylab import rcParams
    import re
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    url = "http://www.hubertiming.com/results/2017GPTR10K"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title
    rows = soup.find_all('tr')
    for row in rows:
        row_td = row.find_all('td')
    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    list_rows = []
    for row in rows:
        cells = row.find_all('td')
        str_cells = str(cells)
        clean = re.compile('(<.*?>|\n|\r)')
        clean2 = (re.sub(clean, '', str_cells))
        list_rows.append(clean2)

    # Create Dataframe
    df = pd.DataFrame(list_rows)
    df1 = df[0].str.split(', ', expand=True)
    df1[0] = df1[0].str.strip('[')

    # Add labels
    col_labels = soup.find_all('th')
    all_header = []
    col_str = str(col_labels)
    cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
    all_header.append(cleantext2)
    df2 = pd.DataFrame(all_header)
    df3 = df2[0].str.split(', ', expand=True)
    frames = [df3, df1]
    df4 = pd.concat(frames)
    df5 = df4.rename(columns=df4.iloc[0])

    # More cleanup
    df6 = df5.dropna(axis=0, how='any')
    df7 = df6.drop(df6.index[0])
    df7.rename(columns={'[Place': 'Place'}, inplace=True)
    df7.rename(columns={'Team]': 'Team'}, inplace=True)
    df7['Team'] = df7['Team'].str.strip(']')
    df7['Name'] = df7['Name'].str.strip()
    names = df7['Name'].tolist()
    fixed_names = [name.strip() for name in names]
    df7['Name'] = fixed_names

    # Compute times
    time_list = df7['Chip Time'].tolist()
    time_mins = []
    for i in time_list:
        num = str.count(i,':')
        if num < 2:
            m, s = i.split(':')
            math = (int(m) * 60 + int(s)) / 60
        else:
            h, m, s = i.split(':')
            math = (int(h) * 3600 + int(m) * 60 + int(s)) / 60
        time_mins.append(math)
    df7['Runner_mins'] = time_mins

    # Analysis
    # print(df7.describe(include=[np.number]))
    # The average time was 60.04

    # rcParams['figure.figsize'] = 15, 5
    # df7.boxplot(column='Runner_mins')
    # plt.grid(True, axis='y')
    # plt.ylabel('Chip Time')
    # plt.xticks([1], ['Runners'])
    # plt.show()
    # The finish times follow a mostly normal distribution with
    # a few outliers taking longer to finish.

    # x = df7['Runner_mins']
    # ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})

    # f_fuko = df7.loc[df7['Gender'] == 'F']['Runner_mins']
    # m_fuko = df7.loc[df7['Gender'] == 'M']['Runner_mins']
    # sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor': 'black'}, label='Female')
    # sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor': 'black'}, label='Male')
    # plt.legend()
    # plt.show()
    # g_stats = df7.groupby("Gender", as_index=True).describe()
    # print(g_stats)
    # There is a clear difference between the genders.

    df7.boxplot(column='Runner_mins', by='Gender')
    plt.ylabel('Chip Time')
    plt.suptitle("")
    plt.show()

if __name__ == '__main__':
    main()


