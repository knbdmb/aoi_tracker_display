# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def create_monthly_display():
    print('trying to print out monthly display')  # Press ⌘F8 to toggle the breakpoint.
    # get data, filter and sort data
    # get list of existing files into dictionary
    # for each month not yet written (current month is always genterated) create chart
    # set up frame of chart
    # step through data and create chart
    # finish chart and start on next one

    #import pandas as pd
    from pandas_ods_reader import read_ods
    #import numpy as np

    #import matplotlib as mpl

    #import matplotlib.pyplot as plt

    #import seaborn as sns
    from calendar import monthrange
    import datetime
    def week_number_of_month(date_value):
        return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)
    import drawSvg as draw
    import time

    today_date = datetime.date.today()
    today_day_of_month = today_date.day
    today_yyyy_mm = str(today_date.year) + "_" + str(today_date.month).zfill(2)

    # get data from spreadsheet
    path = "../aoi_tracker.ods"
    sheet_name = "actions"
    df = read_ods(path, sheet_name)

    path_output = "./aoi_month_rpt"
    file_output = "yyyy_mm_rpt.svg"

    # filter rows without dates and prep data
    df = df[df['date'].notna()]
    df = df[df['date'] >= "2020-01-01"]
    df["tot_proj"] = df["types_of_thought"] + "_-_" + df["project"]
    df["yyyy_mm"] = df['date'].str[0:4] \
                    + "_" \
                    + df['date'].str[5:7]
    df["project_date"] = df["project"] + df['date']

    # Using the sorting function
    df.sort_values(by=["yyyy_mm", "types_of_thought", "project_date"],
                   axis=0, ascending=[True, True, True],
                   inplace=True)

    # Set up required variables before the for loop
    current_month = "yyyy_mm"
    current_project = "xxxxxxxxxx"
    starting_day_number    = 0
    month_number_of_days   = 0
    available_hours        = [0]*32
    available_cumulative_hours = [0]*32
    available_hours_logged = [0]*32
    focus_hours            = [0]*32
    focus_cumulative_hours = [0] * 32
    focus_hours_logged     =  [0]*32

    current_number_of_projects = 0
    number_of_projects_per_month = 0
    number_of_projects_per_month_max = 0

    print("start through dataframe to determine max projects in a month")
    # Step through dataframe and calculate hours arrays and totals
    for ind in df.index:
        if current_month != df['yyyy_mm'][ind]:
            current_month = df['yyyy_mm'][ind]
            if (number_of_projects_per_month > number_of_projects_per_month_max):
                number_of_projects_per_month_max = number_of_projects_per_month
            number_of_projects_per_month = 0
        if current_project != df['project'][ind]:
            current_project = df['project'][ind]
            number_of_projects_per_month += 1
            #print(df['date'][ind], number_of_projects_per_month, ", ", number_of_projects_per_month_max)

    number_of_tot_proj_min = 25
    if number_of_projects_per_month_max > number_of_tot_proj_min:
        number_of_tot_proj = number_of_projects_per_month_max
    else:
        number_of_tot_proj = number_of_tot_proj_min

    #time.sleep(10)

    default_gap = 50
    task_width = 100
    task_height = 8
    cal_details_offset_x = 2
    cal_details_offset_y = 10
    balances_height = 300
    available_hours_width = 200
    available_hours_height = 3000  # 31 days * task_height * 12 h/day rounded up
    month_chart_height = available_hours_height
    month_chart_label_height = 100
    title_height = 200
    current_available_offset_y = 0
    starting_day_number = 0
    month_number_of_days = 0

    paper_to_border_offset_x = default_gap
    available_hours_offset_x = paper_to_border_offset_x + default_gap
    month_chart_offset_x     = available_hours_offset_x + available_hours_width + default_gap
    month_chart_width        = task_width * number_of_tot_proj
    balances_offset_x        = paper_to_border_offset_x + default_gap
    balances_width           = available_hours_width + default_gap + month_chart_width
    cal_offset_x             = paper_to_border_offset_x + default_gap + cal_details_offset_x
    title_offset_x           = month_chart_offset_x
    title_width              = month_chart_width
    border_width             = balances_offset_x + balances_width + default_gap
    drawing_width            = paper_to_border_offset_x + border_width
    avail_hrs_charts_offset_x = available_hours_offset_x - default_gap / 2
    avail_hrs_charts_width    = available_hours_width + default_gap

    paper_to_border_offset_y = default_gap
    balances_offset_y        = paper_to_border_offset_y + default_gap
    available_hours_offset_y = balances_offset_y + balances_height + month_chart_label_height + default_gap
    avail_hrs_zero_height  = 500
    avail_hrs_diff_height = 10
    cal_offset_y             = available_hours_offset_y + available_hours_height + default_gap + cal_details_offset_y
    month_chart_offset_y     = available_hours_offset_y
    title_offset_y           = available_hours_offset_y + available_hours_height + default_gap
    border_height            = title_offset_y + title_height + default_gap
    drawing_height           = border_height + default_gap



    dow_month_offset_x = 0
    month_offset_y = 0
    #current_day_postion_x = paper_to_border_offset_x + border_to_chart_offset_x + dow_month_offset_x
    #current_day_postion_y = paper_to_border_offset_y + border_to_chart_offset_y + month_offset_y
    current_task_offset_y = 0

    f6text_offset_x = 1
    f6text_offset_y = 2
    day_display_height = 0
    hour_height = 0
    day_display_width = 0
    date_offset_x = 0
    date_offset_y = 0

    task_offset_y = day_display_height - hour_height + f6text_offset_y
    task_offset_x = f6text_offset_x
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
                      "5": "#6C0BA9",
                      "4": "red",
                      "3": "orange",
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

    first_record_of_df = False
    drawing_obj_flag = False
    current_month = "yyyy_mm"
    current_project = "xxxxxxxxxx"
    print("start through dataframe to plot tasks")
    # Step through dataframe and generate charts
    for ind in df.index:
        df_date = datetime.date.fromisoformat(df['date'][ind])
        print("this is the next row to be processed: ", df_date)
        if current_month != df['yyyy_mm'][ind]:
            if drawing_obj_flag:
                # totals found from previous months
                # fill in available hours stats
                # fill in calender hours and focus hours stats

                #date_given = datetime.datetime(year=2019, month=7, day=30).date()
                print("\nNumber of weeks the month: ", week_number_of_month(df_date), "\n")
                #time.sleep(1)
                # fill in balance focus details
                # save drawing obj to file
                file_output = current_month + "_rpt.svg"
                d.saveSvg(path_output + "/" + file_output)
                # del drawing_object
                del d
                drawing_obj_flag = False

            # establish drawing object and set flag
            d = draw.Drawing(drawing_width, drawing_height, origin=(0, 0))
            drawing_obj_flag = True

            current_number_of_projects = 0

            # print out statistis from last month before resetting arrays

            current_month = df['yyyy_mm'][ind]
            # start new month
            #df_date = datetime.date.fromisoformat(df['date'][ind])
            (starting_day_number, month_number_of_days) = monthrange(int(df_date.strftime("%y")),
                                                                     int(df_date.strftime("%m")))
            print(df_date,starting_day_number, month_number_of_days)
            print(current_month)
            available_hours[0] = 0
            available_cumulative_hours[0] = 0
            available_hours_logged[0] = 0
            focus_hours[0] = 0
            focus_cumulative_hours[0] = 0
            focus_hours_logged[0] = 0
            for i in range(1, month_number_of_days + 1):
                cm_date = datetime.date.fromisoformat(str(df_date.year)
                                              + "-" + str(df_date.month).zfill(2)
                                              + "-" + str(i).zfill(2))
                #print(i,cm_date)
                if cm_date.weekday() == 6:
                    available_hours[i] = 8
                    available_cumulative_hours[i] = available_hours[i] + available_cumulative_hours[i-1]
                    focus_hours[i] = 3
                    focus_cumulative_hours[i] = focus_hours[i] + focus_cumulative_hours[i-1]

                else:
                    available_hours[i] = 10
                    available_cumulative_hours[i] = available_hours[i] + available_cumulative_hours[i - 1]
                    focus_hours[i] = 5
                    focus_cumulative_hours[i] = focus_hours[i] + focus_cumulative_hours[i - 1]

                available_hours_logged[i] = 0
                focus_hours_logged[i] = 0
            #print(available_hours)

            #print(available_cumulative_hours)

            #print(focus_hours)

            #print(focus_cumulative_hours)

            #time.sleep(2)

            # clean previous month info and chart
            current_month_x_offset = month_chart_offset_x
            current_month_y_offset = month_chart_offset_y
            current_task_offset_y = 0
            current_available_offset_y = available_hours_offset_y \
                                         + avail_hrs_zero_height \
                                         + available_cumulative_hours[month_number_of_days] * task_height
            # set up drawing size object

            # Draw an irregular polygon for border
            d.append(draw.Lines(paper_to_border_offset_x,
                                paper_to_border_offset_y,

                                paper_to_border_offset_x,
                                border_height,

                                border_width,
                                border_height,

                                border_width,
                                paper_to_border_offset_y,

                                paper_to_border_offset_x,
                                paper_to_border_offset_y,
                                close=False,
                                fill=color_border,
                                stroke='black'))
            # month chart
            d.append(draw.Rectangle(month_chart_offset_x,
                                    month_chart_offset_y,
                                    month_chart_width, month_chart_height,
                                    fill=day_color))
            # give month chart horizontal hour lines
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 10 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("10 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 10 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 20 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("20 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 20 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 40 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("40 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 40 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 60 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("60 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 60 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 80 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("80 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 80 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 100 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("100 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 100 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 200 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("200 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 200 * task_height + 12,
                               fill='black'))
            d.append(draw.Rectangle(month_chart_offset_x, month_chart_offset_y + 300 * task_height,
                                    month_chart_width, task_height, fill="#555555"))
            d.append(draw.Text("300 hours", 20, month_chart_offset_x + 5, month_chart_offset_y + 300 * task_height + 12,
                               fill='black'))

            # determine available hours and focus hours and plot
            # Available hours
            d.append(draw.Rectangle(available_hours_offset_x,
                                    available_hours_offset_y,
                                    available_hours_width, available_hours_height,
                                    fill=day_color))
            # fill in available hours chart area
            # draw total available hours line
            d.append(draw.Rectangle(avail_hrs_charts_offset_x,
                                    current_available_offset_y,
                                    avail_hrs_charts_width, task_height,
                                    fill="#555555"))
            # draw zero offset area
            d.append(draw.Rectangle(avail_hrs_charts_offset_x,
                                    available_hours_offset_y,
                                    avail_hrs_charts_width, avail_hrs_zero_height,
                                    fill="#555555"))
            # draw available hours and focus hours
            if today_yyyy_mm == current_month:
                d.append(draw.Rectangle(avail_hrs_charts_offset_x,
                                        available_hours_offset_y + avail_hrs_zero_height,
                                        avail_hrs_charts_width,
                                        focus_cumulative_hours[month_number_of_days - today_day_of_month] * task_height,
                                        fill="#00C0F0")) # #FFC0CB

                avail_hrs_diff_height = available_cumulative_hours[month_number_of_days - today_day_of_month] \
                                        - focus_cumulative_hours[month_number_of_days - today_day_of_month]

                d.append(draw.Rectangle(avail_hrs_charts_offset_x,
                                        available_hours_offset_y 
                                        + avail_hrs_zero_height 
                                        + focus_cumulative_hours[month_number_of_days - today_day_of_month] * task_height,
                                        avail_hrs_charts_width,
                                        avail_hrs_diff_height * task_height,
                                        fill="#32CD32"))


            # determine calendar shape and plot
            # calendar
            d.append(draw.Rectangle(cal_offset_x,
                                    cal_offset_y,
                                    196, 168,
                                    fill=day_color))

            # title
            d.append(draw.Rectangle(title_offset_x,
                                    title_offset_y,
                                    title_width, title_height,
                                    fill=day_color))
            # fill in title area
            d.append(draw.Text(current_month, 50, title_offset_x + title_width/2, title_offset_y + title_height/2,
                               fill='black'))
            today_date_label = "Created on: " + str(today_date)
            d.append(draw.Text(today_date_label, 50, title_offset_x, title_offset_y,
                               fill='black'))
            # Balances
            d.append(draw.Rectangle(balances_offset_x,
                                    balances_offset_x,
                                    balances_width, balances_height,
                                    fill=day_color))
            # fill in Balance area
            d.append(draw.Text("project 1.3t", 30, balances_offset_x + 5,
                               balances_offset_y + 40, fill='black'))
            d.append(draw.Text("project 1.3d", 30, balances_offset_x + 5,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Text("project 1.2t", 30, balances_offset_x + 5,
                               balances_offset_y + balances_height/3 + 40, fill='black'))
            d.append(draw.Text("project 1.2d", 30, balances_offset_x + 5,
                               balances_offset_y + balances_height/3 + 5, fill='black'))
            d.append(draw.Text("project 1.1t", 30, balances_offset_x + 5,
                               balances_offset_y + 2 * balances_height/3 + 40, fill='black'))
            d.append(draw.Text("project 1.1d", 30, balances_offset_x + 5,
                               balances_offset_y + 2 * balances_height/3 + 5, fill='black'))

            d.append(draw.Text("project 2.3", 30, balances_offset_x + balances_width/4 + 5,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Text("project 2.2", 30, balances_offset_x + balances_width/4 + 5,
                               balances_offset_y + balances_height/3 + 5, fill='black'))
            d.append(draw.Text("project 2.1", 30, balances_offset_x + balances_width/4 + 5,
                               balances_offset_y + 2 * balances_height/3 + 5, fill='black'))

            d.append(draw.Text("project 3.3", 30, balances_offset_x + balances_width/2,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Text("project 3.2", 30, balances_offset_x + balances_width/2,
                               balances_offset_y + balances_height/3 + 5, fill='black'))
            d.append(draw.Text("project 3.1", 30, balances_offset_x + balances_width/2,
                               balances_offset_y + 2 * balances_height/3, fill='black'))

            d.append(draw.Text("project 4.3", 30, balances_offset_x + balances_width*3/4,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Text("project 4.2", 30, balances_offset_x + balances_width*3/4,
                               balances_offset_y + balances_height/3 + 5, fill='black'))
            d.append(draw.Text("project 4.1", 30, balances_offset_x + balances_width*3/4,
                               balances_offset_y + 2 * balances_height/3, fill='black'))


            # date created label
            d.append(draw.Rectangle(200, 75, 200, 8, fill='#ffffff'))
            today_date_label = "Created on: " + str(today_date)
            d.append(draw.Text(today_date_label, 6, 201, 77,
                               fill='black'))  # Text with font size 6
            # set column x offset for task plotting to first column
            current_month_x_offset = month_chart_offset_x
            # set column y offset to start position
            current_month_y_offset = month_chart_offset_y
            current_number_of_projects = 0
            # fill in tot and project labels
            current_project = df['project'][ind]
            if first_record_of_df:
                d.append(draw.Text(df['project'][ind][0:13], 12,
                                   current_month_x_offset,
                                   current_month_y_offset - 50,
                                   fill='black'))
                d.append(draw.Text(df['types_of_thought'][ind][0:13], 12,
                                   current_month_x_offset,
                                   current_month_y_offset - 100,
                                   fill='black'))


        if current_project != df['project'][ind]:
            current_project = df['project'][ind]
            # move to new column for task ploting
            # set column y offset to start position
            if first_record_of_df:
                current_number_of_projects += 1
            first_record_of_df = True # fix better name

            current_month_x_offset = month_chart_offset_x + current_number_of_projects * task_width
            current_month_y_offset = month_chart_offset_y
            # plot out tot and project labels

            d.append(draw.Text(df['project'][ind][0:13], 12,
                               current_month_x_offset,
                               current_month_y_offset - 50,
                               fill='black'))
            d.append(draw.Text(df['types_of_thought'][ind][0:13], 12,
                               current_month_x_offset,
                               current_month_y_offset - 100,
                               fill='black'))

        # jjj
        # for current row of df
        # plot task box and description in the month chart
        d.append(draw.Rectangle(current_month_x_offset,
                                current_month_y_offset,
                                task_width,
                                task_height * df['amount'][ind],
                                stroke='black',
                                fill=tot_color_array[df['types_of_thought'][ind][0]]))
        d.append(draw.Text(df['task'][ind][0:32], 6,
                           current_month_x_offset,
                           current_month_y_offset,
                           fill='black'))
        # increment y offset
        current_month_y_offset = current_month_y_offset + task_height * df['amount'][ind]
        # update hours to totals arrays
        # track hours per day
        df_date = datetime.date.fromisoformat(df['date'][ind])
        # plot task box and description in the available hours chart
        #print("before avail: ",current_available_offset_y)
        current_available_offset_y = current_available_offset_y - task_height * df['amount'][ind]
        #print("just after: ",current_available_offset_y)
        d.append(draw.Rectangle(available_hours_offset_x,
                                current_available_offset_y,
                                available_hours_width,
                                task_height * df['amount'][ind],
                                stroke='black',
                                fill=tot_color_array[df['types_of_thought'][ind][0]]))
        d.append(draw.Text(df['task'][ind][0:32], 6,
                           available_hours_offset_x,
                           current_available_offset_y,
                           fill='black'))
        #print(df['yyyy_mm'][ind], " _-_ ", df['project'][ind], " _-_ ", df['task'][ind])

    if drawing_obj_flag:
        file_output = current_month + "_rpt.svg"
        d.saveSvg(path_output + "/" + file_output)
        d.saveSvg(path_output + "/current_month_rpt.svg")
    print("done with monthly display")

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

    # Using the sorting function
    df.sort_values(by=["date", "types_of_thought", "project"],
                   axis=0, ascending=[True, True, True],
                   inplace=True)

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
                      "5": "#6C0BA9",
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
    today_date_label = "Created on: " + str(datetime.date.today())
    d.append(draw.Text(today_date_label, 6, 201, 77,
                       fill='black'))  # Text with font size 6



    d.saveSvg('yearsdisp.svg')



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
    df.sort_values(by=["date", "types_of_thought", "project"],
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
    #create_years_display()
    #create_heatmap()
    #import_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
