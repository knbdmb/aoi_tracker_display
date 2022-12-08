# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def create_monthly_display()
    print('trying to print out month display')  # Press ⌘F8 to toggle the breakpoint.

def create_years_display():
    # Use a breakpoint in the code line below to debug your script.
    print('trying to print out years display')  # Press ⌘F8 to toggle the breakpoint.

    import pandas as pd
    from pandas_ods_reader import read_ods
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns
    import datetime
    import drawSvg as draw

    # get data from spreadsheet
    path = "../aoi_tracker.ods"
    sheet_name = "actions"
    df = read_ods(path, sheet_name)

    # filter rows without dates and prep data
    df = df[df['date'].notna()]
    df = df[df['date'] >= "2020-01-01"]
    df["tot_proj"] = df["types_of_thought"] + "_-_" + df["project"]






    paper_to_border_offset_x = 50
    paper_to_border_offset_y = 50
    border_to_chart_offset_x = 50
    border_to_chart_offset_y = 50

    day_display_width = 200
    day_display_height = 200
    hour_height = 8
    hour_width = day_display_width

    number_of_months = 3 * 12 # this determined later
    dow_month_offset_x = 0
    month_offset_y = 0
    current_day_postion_x = paper_to_border_offset_x + border_to_chart_offset_x + dow_month_offset_x
    current_day_postion_y = paper_to_border_offset_y + border_to_chart_offset_y + month_offset_y
    current_task_offset_y = 0

    f6text_offset_x = 1
    f6text_offset_y = 2
    date_offset_y = day_display_height - hour_height + f6text_offset_y
    date_offset_x = f6text_offset_x
    day_number_offset_x = day_display_width / 2
    day_number_offset_y = 100
    year_month_offset_x = 10
    year_month_offset_y = 200

    color_border    = "#999999"
    color_even_year = "#CCCCCC"
    color_odd_year  = "#DDDDDD"
    color_weekday   = "#FFFFFF"
    color_weekend   = "#EEEEEE"
    day_color       = "#EEEEEE" # this set to highlight weekends
    year_color      = "#EEEEEE" # this set to highlight years
    task_color      = "gray"    # this is set for each task
    day_number_color = "#B9B9B9"
    year_month_color = "#696969"
    tot_color_array = {
                      "5": "cyan",
                      "4": "red",
                      "3":  "orange",
                      "2": "green",
                      "1": "#4141FF",
                      "x": "gray"
                      }

    max_char = 53
    tot_max = 14
    proj_max = 14
    task_max = 33
    tot_offset_x = 0
    proj_offset_x = 54
    task_offset_x = 110

    # number_of_months = 3 * 12 # this would be 3 years of months
    number_of_months = 0
    current_month = "x"
    for ind in df.index:
        df_date = datetime.date.fromisoformat(df['date'][ind])
        if current_month != df_date.strftime("%m"):
            number_of_months += 1
            print(number_of_months)
            current_month = df_date.strftime("%m")

    chart_width = (7 - 1 + 31) * day_display_width
    # 7 = days in week, 1 day less of offset, 31 max days in month
    chart_height = ( number_of_months ) * day_display_height
    # 3 years, 12 months per year

    drawing_width =(chart_width + 2*paper_to_border_offset_x + 2*border_to_chart_offset_x)
    drawing_height =(chart_height + 2*paper_to_border_offset_y + 2*border_to_chart_offset_y)

    d = draw.Drawing(drawing_width, drawing_height, origin=(0,0))


    # Draw an irregular polygon for border
    d.append(draw.Lines(paper_to_border_offset_x,
                        paper_to_border_offset_y,

                        paper_to_border_offset_x,
                        paper_to_border_offset_y + chart_height + 2*border_to_chart_offset_y,

                        paper_to_border_offset_x + chart_width + 2*border_to_chart_offset_x,
                        paper_to_border_offset_y + chart_height + 2*border_to_chart_offset_y,

                        paper_to_border_offset_x + chart_width + 2*border_to_chart_offset_x,
                        paper_to_border_offset_y,

                        paper_to_border_offset_x,
                        paper_to_border_offset_y,
                        close = False,
                        fill = color_border,
                        stroke='black'))


    # Set up required variables before the for loop
    current_year = 9999
    current_month = "99"
    current_day = 99
    number_of_months = 0

    print("start through dataframe")
    # Step through dataframe and generate chart
    for ind in df.index:
        df_date = datetime.date.fromisoformat(df['date'][ind])

        if current_day != df_date.day:
            current_day = df_date.day
            current_task_offset_y = 0
            # process new month
            if current_month != df_date.strftime("%m"):
                current_month = df_date.strftime("%m")
                first_of_month_offset_x = datetime.datetime(df_date.year, int(df_date.strftime("%m")), 1).weekday()
                if (df_date.year % 2) == 0:
                    year_color = color_even_year
                else:
                    year_color = color_odd_year

                # draw month box in right color
                d.append(draw.Rectangle(current_day_postion_x,
                                        current_day_postion_y + int(number_of_months) * day_display_height,
                                        37 * day_display_width, day_display_height,
                                        fill=year_color))
                year_month_colected = str(df_date.year) + "-" + df_date.strftime("%m")
                d.append(draw.Text(year_month_colected, 90,
                                   current_day_postion_x + year_month_offset_x,
                                   current_day_postion_y + year_month_offset_y +\
                                   int( number_of_months - 1) * day_display_height,
                                   fill=year_month_color))
                number_of_months += 1

            dow_month_offset_x = first_of_month_offset_x + df_date.day - 1 # fix off by one in x

            #day_number_offset_x
            #day_number_offset_y
            #day_number_color = "#B9B9B9"


            # draw day box
            if df_date.weekday() < 5:
                day_color = color_weekday
            else:
                day_color = color_weekend
            d.append(draw.Rectangle(current_day_postion_x + dow_month_offset_x * day_display_width,
                                    current_day_postion_y + int(number_of_months -1 ) * day_display_height,
                                    day_display_width, day_display_height,
                                    fill=day_color))
            d.append(draw.Text(df['date'][ind], 6,
                               current_day_postion_x + dow_month_offset_x * day_display_width + date_offset_x,
                               current_day_postion_y + int(number_of_months - 1) * day_display_height + date_offset_y,
                               fill='black'))
            d.append(draw.Text(str(df_date.day), 100,
                               current_day_postion_x + dow_month_offset_x * day_display_width + day_number_offset_x,
                               current_day_postion_y + int(number_of_months - 1) * day_display_height + day_number_offset_y,
                               text_anchor="middle",
                               fill=day_number_color))

        # draw task
        d.append(draw.Rectangle(current_day_postion_x + dow_month_offset_x * day_display_width,
                                current_day_postion_y + int(number_of_months - 1) * day_display_height + current_task_offset_y,
                                day_display_width, hour_height * df['amount'][ind],
                                stroke='black',
                                fill=tot_color_array[df['types_of_thought'][ind][0]]))
        d.append(draw.Text(df['types_of_thought'][ind][0:13], 6,
                           current_day_postion_x + dow_month_offset_x * day_display_width + f6text_offset_x + tot_offset_x,
                           current_day_postion_y + int(number_of_months - 1) * day_display_height + f6text_offset_y + current_task_offset_y,
                           fill='black'))
        d.append(draw.Text(df['project'][ind][0:13], 6,
                           current_day_postion_x + dow_month_offset_x * day_display_width + f6text_offset_x + proj_offset_x,
                           current_day_postion_y + int(
                               number_of_months - 1) * day_display_height + f6text_offset_y + current_task_offset_y,
                           fill='black'))
        d.append(draw.Text(df['task'][ind][0:32], 6,
                           current_day_postion_x + dow_month_offset_x * day_display_width + f6text_offset_x + task_offset_x,
                           current_day_postion_y + int(
                               number_of_months - 1) * day_display_height + f6text_offset_y + current_task_offset_y,
                           fill='black'))


        current_task_offset_y = current_task_offset_y + hour_height * df['amount'][ind]







        #"""
        print(dow_month_offset_x)
        print(df['date'][ind],
              df_date.year,
              df_date.strftime("%m"),
              df_date.day,
              df_date.weekday(),
              df['types_of_thought'][ind],
              df['project'][ind],
              df['task'][ind],
              df['amount'][ind])
        #"""

    """
    # the following rectangles are used for testing
    d.append(draw.Rectangle(current_day_postion_x,
                            current_day_postion_y,
                            day_display_width, day_display_height,
                            fill='#1248ff'))
    d.append(draw.Text('2022-12-03', 6,
                       current_day_postion_x + date_offset_x,
                       current_day_postion_y + date_offset_y,
                       fill='black'))

    d.append(draw.Rectangle(current_day_postion_x + day_display_width,
                            current_day_postion_y + day_display_height,
                            day_display_width, day_display_height,
                            fill='#1248ff'))

    d.append(draw.Rectangle(current_day_postion_x + 36 * day_display_width,
                            current_day_postion_y + (number_of_months -1) * day_display_height,
                            day_display_width, day_display_height,
                            fill='#124800'))
    d.append(draw.Text('2022-12-04', 6,
                       current_day_postion_x + 36 * day_display_width + date_offset_x,
                       current_day_postion_y + (number_of_months -1) * day_display_height + date_offset_y,
                       fill='black'))

    d.append(draw.Rectangle(current_day_postion_x + 36 * day_display_width,
                            current_day_postion_y,
                            day_display_width, day_display_height,
                            fill='#1200ff'))

    d.append(draw.Rectangle(current_day_postion_x,
                            current_day_postion_y + (number_of_months -1) * day_display_height,
                            day_display_width, day_display_height,
                            fill='#0048ff'))

    d.append(draw.Rectangle(200, 75, 200, 8, fill='#1248ff'))
    d.append(draw.Text('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789', 6, 201, 77,
                       fill='black'))  # Text with font size 6
    """

    d.append(draw.Rectangle(200, 75, 200, 8, fill='#ffffff'))
    today_date = "Created on: " + str(datetime.date.today())
    d.append(draw.Text(today_date, 6, 201, 77,
                       fill='black'))  # Text with font size 6



    d.saveSvg('monthsdisp.svg')



    print("done with years display")



def create_heatmap():
    # Use a breakpoint in the code line below to debug your script.
    print('trying to print out the heat map')  # Press ⌘F8 to toggle the breakpoint.

    import pandas as pd
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns

    from pandas_ods_reader import read_ods

    path = "../aoi_tracker.ods"
    sheet_name = "actions"
    df = read_ods(path, sheet_name)

    # remove rows without dates
    df = df[df['date'].notna()]
    # remove rows before 2020-01-01
    df = df[df['date'] >= "2020-01-01"]
    df["tot_proj"] = df["types_of_thought"] + "_-_" + df["project"]

    pt_tot_proj_yyyy_mm_h = np.round(pd.pivot_table(df, values='amount',
                                            index='tot_proj',
                                            columns='yyyy-mm',
                                            aggfunc=np.sum), 2)

    plt.figure(figsize=(23, 20))
    pt_plot_h = sns.heatmap(pt_tot_proj_yyyy_mm_h )
    fig_h = pt_plot_h.get_figure()
    fig_h.savefig("pt_tot_proj_yyyy_mm_h.png")

    print("done with heat map")



def import_data():
    # Use a breakpoint in the code line below to debug your script.
    print('got to starting importing data')  # Press ⌘F8 to toggle the breakpoint.

    import pandas as pd
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns

    from pandas_ods_reader import read_ods

    path = "../aoi_tracker.ods"
    #path = "../ooo_shiny_urls.ods"

    # by default the first sheet is imported
    #df = read_ods(path)

    # load a sheet based on its index (1 based)
    #sheet_idx = 2
    #df = read_ods(path, sheet_idx)

    # load a sheet based on its name
    #sheet_name = "urls"
    sheet_name = "actions"
    df = read_ods(path, sheet_name)

    #print(df.columns)

    # remove rows without dates
    df = df[df['date'].notna()]
    # remove rows before 2020-01-01
    df = df[df['date'] >= "2020-01-01"]
    df["tot_proj"] = df["types_of_thought"] + "_-_" + df["project"]

    # Using the sorting function
    df.sort_values(["date", "types_of_thought", "project"],
                   axis=0, ascending=[True, True, True],
                   inplace=True)

    pd.set_option('display.max_columns', 10)
    #print(df)
    #print(df.head(10))
    #print(df.tail(10))



    # pt_project total for each of the projects
    pt_tot_proj = np.round(pd.pivot_table(df, values='amount',
                                    index='tot_proj',
                                    aggfunc=np.sum), 2)

    html = pt_tot_proj.to_html(classes='table table-stripped')
    text_file = open("pt_tot_proj.html", "w")
    text_file.write(html)
    text_file.close()

    pt_plot = pt_tot_proj.plot.barh(figsize=(15,16))
    fig = pt_plot.get_figure()
    fig.savefig("pt_tot_proj.png")





    # pt_type_yyyy-mm vert bar chart of total for all catagories
    pt_yyyy_type = np.round(pd.pivot_table(df, values='amount',
                                    index='yyyy-mm',
                                    columns='types_of_thought',
                                    aggfunc=np.sum), 2)

    html = pt_yyyy_type.to_html(classes='table table-stripped')
    text_file = open("pt_yyyy_type.html", "w")
    text_file.write(html)
    text_file.close()

    pt_plot = pt_yyyy_type.plot.barh(figsize=(15,16), stacked=True)
    fig = pt_plot.get_figure()
    fig.savefig("pt_yyyy_type.png")

    # pt_project_yyyy-mm
    pt_tot_proj_yyyy = np.round(pd.pivot_table(df, values='amount',
                                    index='tot_proj',
                                    columns='yyyy-mm',
                                    aggfunc=np.sum), 2)

    html = pt_tot_proj_yyyy.to_html(classes='table table-stripped')
    text_file = open("pt_tot_proj_yyyy.html", "w")
    text_file.write(html)
    text_file.close()

    pt_plot = pt_tot_proj_yyyy.plot.barh(figsize=(15,16), stacked=True)
    fig = pt_plot.get_figure()
    fig.savefig("pt_tot_proj_yyyy.png")

    # pt_task_yyyy-mm stacked vertial bar chart
    pt_task_yyyy_mm = np.round(pd.pivot_table(df, values='amount',
                                               index='task',
                                               columns='yyyy-mm',
                                               aggfunc=np.sum), 2)

    html = pt_task_yyyy_mm.to_html(classes='table table-stripped')
    text_file = open("pt_task_yyyy_mm.html", "w")
    text_file.write(html)
    text_file.close()

    #pt_plot = pt_task_yyyy_mm.plot.barh(figsize=(60,100), stacked=True)
    #fig = pt_plot.get_figure()
    #fig.savefig("pt_task_yyyy_mm.png")

    #pt_plot = plt.plot(pt_task_yyyy_m,figsize=(60,100))
    #pt_plot = sns.heatmap(pt_task_yyyy_mm, square=True)

    #pt_task_yyyy_mm_h = np.round(pd.pivot_table(df, values='amount',
    #                                          index='task',
    #                                          columns='yyyy-mm',
    #                                          aggfunc=np.sum), 2)
    #pt_plot_h = sns.heatmap(pt_task_yyyy_mm_h)
    #fig_h = pt_plot_h.get_figure()
    #fig_h.savefig("pt_task_yyyy_mm_h.png")

    print("got to here")

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    create_monthly_display()
    create_years_display()
    #create_heatmap()
    #import_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
