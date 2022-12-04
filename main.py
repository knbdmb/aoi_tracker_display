# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def create_monthly_display():
    # Use a breakpoint in the code line below to debug your script.
    print('trying to print out month display')  # Press ⌘F8 to toggle the breakpoint.

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

    dow_month_offset_x = 0
    current_day_postion_x = paper_to_border_offset_x + border_to_chart_offset_x
    current_day_postion_y = paper_to_border_offset_y + border_to_chart_offset_y

    f6text_offset_x = 1
    f6text_offset_y = 2
    date_offset_y = day_display_height - hour_height + f6text_offset_y
    date_offset_x = f6text_offset_x

    max_char = 53
    tot_max = 14
    proj_max = 14
    task_max = 33

    chart_width = (7 - 1 + 31) * day_display_width
    # 7 = days in week, 1 day less of offset, 31 max days in month
    chart_height = ( 3 * 12 ) * day_display_height
    # 3 years, 12 months per year

    drawing_width =(chart_width + 2*paper_to_border_offset_x + 2*border_to_chart_offset_x)
    drawing_height =(chart_height + 2*paper_to_border_offset_y + 2*border_to_chart_offset_y)

    import datetime
    import drawSvg as draw

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
                        fill = '#999999',
                        stroke='black'))

    # Draw an irregular polygon for chart border
    d.append(draw.Lines(paper_to_border_offset_x + border_to_chart_offset_x,
                        paper_to_border_offset_y + border_to_chart_offset_y,

                        paper_to_border_offset_x + border_to_chart_offset_x,
                        paper_to_border_offset_y + chart_height + border_to_chart_offset_y,

                        paper_to_border_offset_x + chart_width + border_to_chart_offset_x,
                        paper_to_border_offset_y + chart_height + border_to_chart_offset_y,

                        paper_to_border_offset_x + chart_width + border_to_chart_offset_x,
                        paper_to_border_offset_y + border_to_chart_offset_y,

                        paper_to_border_offset_x + border_to_chart_offset_x,
                        paper_to_border_offset_y + border_to_chart_offset_y,
                        close = False,
                        fill = '#eeeeee',
                        stroke='black'))



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
                            current_day_postion_y + 35 * day_display_height,
                            day_display_width, day_display_height,
                            fill='#124800'))
    d.append(draw.Text('2022-12-04', 6,
                       current_day_postion_x + 36 * day_display_width + date_offset_x,
                       current_day_postion_y + 35 * day_display_height + date_offset_y,
                       fill='black'))

    d.append(draw.Rectangle(current_day_postion_x + 36 * day_display_width,
                            current_day_postion_y,
                            day_display_width, day_display_height,
                            fill='#1200ff'))

    d.append(draw.Rectangle(current_day_postion_x,
                            current_day_postion_y + 35 * day_display_height,
                            day_display_width, day_display_height,
                            fill='#0048ff'))

    d.append(draw.Rectangle(200, 75, 200, 8, fill='#1248ff'))
    d.append(draw.Text('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789', 6, 201, 77,
                       fill='black'))  # Text with font size 6

    for ind in df.index:
        df_date = datetime.date.fromisoformat(df['date'][ind])
        #first_of_month = datetime.datetime(df_date.year, df_date.strftime("%m"), 1).weekday()
        #print(first_of_month)
        #dow_month_offset_x = datetime.date.fromisoformat(df_date.year, df_date.strftime("%m"), "1").weekday()
        #print(dow_month_offset_x)
        print(df['date'][ind],
              df_date.year,
              df_date.strftime("%m"),
              df_date.weekday(),
              df['types_of_thought'][ind],
              df['project'][ind],
              df['task'][ind])



    d.saveSvg('monthsdisp.svg')



    print("done with month display")



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
    #create_heatmap()
    #import_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
