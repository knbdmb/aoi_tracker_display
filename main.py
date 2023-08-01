# This is processes the aoi tracking spreadsheet in to various reports

def create_monthly_display():
    print('trying to print out monthly display')  # Press ⌘F8 to toggle the breakpoint.
    # get data, filter and sort data
    # get list of existing files into dictionary
    # for each month not yet written (current month is always genterated) create chart
    # set up frame of chart
    # step through data and create chart
    # finish chart and start on next one

    import pandas as pd
    from pandas_ods_reader import read_ods
    #import numpy as np

    #import matplotlib as mpl

    #import matplotlib.pyplot as plt

    #import seaborn as sns
    from calendar import monthrange
    import datetime
    def week_number_of_month(date_value):
        #return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1])
        week = date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1]
        if week < 0:
            week = week + 52
        return week
    import drawsvg as draw
    import time

    import mixbox

    today_date = datetime.date.today()
    today_day_of_month = today_date.day
    today_yyyy_mm = str(today_date.year) + "-" + str(today_date.month).zfill(2)

    # get data from spreadsheet
    path = "../aoi_tracker.ods"
    sheet_name = "actions"
    df = read_ods(path, sheet_name)

    sheet_name = "month_plans"
    dfmp = read_ods(path, sheet_name)

    path_output = "./aoi_month_rpt"
    path_output_web = "/Library/WebServer/Documents/aoi_month_rpt_web"
    file_output = "yyyy_mm_rpt.svg"

    # filter rows without dates and prep data
    df = df[df['date'].notna()]
    df = df[df['date'] >= "2020-01-01"]
    df["tot_proj"] = df["types_of_thought"] + "_-_" + df["project"]
    df["yyyy_mm"] = df['date'].str[0:4] \
                    + "-" \
                    + df['date'].str[5:7]
    df["project_date"] = df["project"] + df['date']

    dfmp = dfmp[dfmp["yyyy_mm"].notna()]


    # Using the sorting function
    df.sort_values(by=["yyyy_mm", "types_of_thought", "project_date"],
                   axis=0, ascending=[True, True, True],
                   inplace=True)

    dfmp.sort_values(by=["yyyy_mm", "task"],
                   axis=0, ascending=[True, True],
                   inplace=True)


    # Set up required variables before the for loop
    current_month = "yyyy_mm"
    current_project = "xxxxxxxxxx"
    starting_day_number    = 0
    month_number_of_days   = 0
    available_hours            = [0]*32
    available_cumulative_hours = [0]*32
    available_hours_logged     = [0]*32
    focus_hours                = [0]*32
    focus_cumulative_hours     = [0]*32
    focus_hours_logged         = [0]*32
    planned_hours              = [0]*32
    planned_cumulative_hours   = [0]*32
    planned_hours_logged       = [0]*32

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
    # the following values must match the tot_color_array values
    tot_rgb5 = (108, 11, 169)
    tot_rgb4 = (255, 0, 0)
    tot_rgb3 = (255, 165, 0)
    tot_rgb2 = (0, 255, 0)
    tot_rgb1 = (65, 65, 255)
    day_gray_level = 210 # sets the default level of gray of a calendar day
    z5 = mixbox.rgb_to_latent(tot_rgb5)
    z4 = mixbox.rgb_to_latent(tot_rgb4)
    z3 = mixbox.rgb_to_latent(tot_rgb3)
    z2 = mixbox.rgb_to_latent(tot_rgb2)
    z1 = mixbox.rgb_to_latent(tot_rgb1)
    z_mix = [0] * mixbox.LATENT_SIZE

    tot_totals_rows = 6
    tot_totals_cols = 32
    tot_totals_arr = [[0 for j in range(tot_totals_cols)] for i in range(tot_totals_rows)]
    tot_percents_arr = [[0 for j in range(tot_totals_cols)] for i in range(tot_totals_rows)]
    tot_color_rows_rgb = 3 # 0 = red, 1 = green, 2 = blue
    # the following sets the default color to gray
    tot_color_arr = [[day_gray_level for j in range(tot_totals_cols)] for i in range(tot_color_rows_rgb)]
    #print(tot_color_arr)
    #time.sleep(5)

    def fill_in_calendar_area(previous_month, tot_totals_arr):
        print("got to calendar filling functinn")

        # this is where the calendar day is drawing for current month data ......
        # fill out percentages array
        # use the filled out type of task array to determine percentages per month and day
        #print("totals just before cal percents: ", tot_totals_arr)
        #print("percents just before cal percents: ", tot_percents_arr)

        for i in range(0, tot_totals_cols):
            if tot_totals_arr[0][i] > 0:
                tot_percents_arr[0][i] = 1
                for j in range(1, tot_totals_rows):
                    tot_percents_arr[j][i] = tot_totals_arr[j][i] / tot_totals_arr[0][i]
                    # print(tot_totals_arr[j][i]," divide by ",tot_totals_arr[0][i])
        #print("totals just after cal percents: ", tot_totals_arr)
        #print("percents just after cal percents: ", tot_percents_arr)
        # time.sleep(1)
        # fill out color array
        # use the type of task percentages array to determine color per month and day
        # tot_color_arr = [[63 for j in range(tot_totals_cols)] for i in range(tot_color_rows)]
        for i in range(0, tot_totals_cols):  # then range has to be adjusted per month
            if tot_percents_arr[0][i] == 1:
                # for j in range(1, tot_totals_rows):
                #    print(tot_percents_arr[j][i])
                for k in range(len(z_mix)):  # mix together:
                    z_mix[k] = (tot_percents_arr[1][i] * z1[k] +
                                tot_percents_arr[2][i] * z2[k] +
                                tot_percents_arr[3][i] * z3[k] +
                                tot_percents_arr[4][i] * z4[k] +
                                tot_percents_arr[5][i] * z5[k])
                # print(i)
                rgb_mix = mixbox.latent_to_rgb(z_mix)
                # print(rgb_mix)
                # print(rgb_mix[0])
                tot_color_arr[0][i] = rgb_mix[0]
                # print(rgb_mix[1])
                tot_color_arr[1][i] = rgb_mix[1]
                # print(rgb_mix[2])
                tot_color_arr[2][i] = rgb_mix[2]
        #print("number of columns in tot_color_arr, ", i)
        #print(tot_color_arr)
        # time.sleep(3)

        # draw each day with color, high light border of today in green
        # by stepping through tot_color_arr[][] up to month_number_of_days
        print(previous_month)
        for i in range(1, month_number_of_days + 1):  # need to add 1 to get full month

            day_to_process = previous_month + "-" + str(i).zfill(2)
            date_to_process = datetime.date.fromisoformat(day_to_process)
            #print(day_to_process)
            #print(str(date_to_process))
            dtp_day_index = pd.Timestamp(day_to_process).weekday()
            dtp_week_index = 5 - week_number_of_month(date_to_process)
            (pm_starting_day_number, pm_month_number_of_days) = monthrange(int(date_to_process.strftime("%y")),
                                                                     int(date_to_process.strftime("%m")))

            #print("day to process day index: ", dtp_day_index)
            #print("day to process week index: ", dtp_week_index)
            #print("number of days in month: ", pm_month_number_of_days)

            dtp_day_offset_x = cal_offset_x + dtp_day_index * cal_day_width
            dtp_week_offset_y = cal_offset_y + dtp_week_index * cal_day_height
            dtp_color = "rgb(" + str(tot_color_arr[0][i]) + "," + str(tot_color_arr[1][i]) + "," + str(tot_color_arr[2][i]) + ")"
            #print(dtp_color)
            if date_to_process == today_date:
                today_color = 'green'
                today_size = 10
            else:
                today_color = 'black'
                today_size = 1
            d.append(draw.Rectangle(dtp_day_offset_x, dtp_week_offset_y,
                                    cal_day_width, cal_day_height,
                                    fill=dtp_color, stroke=today_color, stroke_width=today_size))
            d.append(draw.Text(str(i), 50, dtp_day_offset_x + 5, dtp_week_offset_y + 12,
                               fill=today_color))
            d.append(draw.Text(pd.to_datetime(date_to_process).day_name(), 18, dtp_day_offset_x + 5,
                               dtp_week_offset_y + 90, fill=today_color))

            tot_percent_amount = "%.1f" % (tot_percents_arr[1][i] * 100)
            tot_info = "A: " + str(tot_totals_arr[1][i]) + " hrs, " + str(tot_percent_amount) + " %"
            d.append(draw.Text(tot_info, 5, dtp_day_offset_x + 62, dtp_week_offset_y + 52,
                               fill='black'))

            tot_percent_amount = "%.1f" % (tot_percents_arr[2][i] * 100)
            tot_info = "I: " + str(tot_totals_arr[2][i]) + " hrs, " + str(tot_percent_amount) + " %"
            d.append(draw.Text(tot_info, 5, dtp_day_offset_x + 62, dtp_week_offset_y + 42,
                               fill='black'))

            tot_percent_amount = "%.1f" % (tot_percents_arr[3][i] * 100)
            tot_info = "P: " + str(tot_totals_arr[3][i]) + " hrs, " + str(tot_percent_amount) + " %"
            d.append(draw.Text(tot_info, 5, dtp_day_offset_x + 62, dtp_week_offset_y + 32,
                               fill='black'))

            tot_percent_amount = "%.1f" % (tot_percents_arr[4][i] * 100)
            tot_info = "E: " + str(tot_totals_arr[4][i]) + " hrs, " + str(tot_percent_amount) + " %"
            d.append(draw.Text(tot_info, 5, dtp_day_offset_x + 62, dtp_week_offset_y + 22,
                               fill='black'))

            tot_percent_amount = "%.1f" % (tot_percents_arr[5][i] * 100)
            tot_info = "M: " + str(tot_totals_arr[5][i]) + " hrs, " + str(tot_percent_amount) + " %"
            d.append(draw.Text(tot_info, 5, dtp_day_offset_x + 62, dtp_week_offset_y + 12,
                               fill='black'))


            #print(previous_month)
            #print(i, end=" ")

        # print box in title area showing color of the month
        dtp_color = "rgb(" + str(tot_color_arr[0][0]) + "," + str(tot_color_arr[1][0]) + "," + str(tot_color_arr[2][0]) + ")"
        # print(dtp_color)
        d.append(draw.Rectangle(title_offset_x, title_offset_y + title_height - 600,
                                    600, 180,
                                    fill=dtp_color, stroke='black'))
        d.append(draw.Text("Color of Month: ", 50,
                           title_offset_x, title_offset_y + title_height - 480,
                           fill='black'))

        # Details on types of thoughts statistics
        d.append(draw.Rectangle(title_offset_x + 600, title_offset_y + title_height - 600 + 5 * 30,
                                    30, 30,
                                    fill=tot_color_array["1"], stroke='black'))
        tot_percent_amount = "%.1f" % (tot_percents_arr[1][0] * 100)
        tot_info = "Active: " + str(tot_totals_arr[1][0]) + " hrs, " + str(tot_percent_amount) + " %"
        d.append(draw.Text(tot_info, 30,
                           title_offset_x + 635, title_offset_y + title_height - 600 + 5 * 30,
                           fill='black'))

        d.append(draw.Rectangle(title_offset_x + 600, title_offset_y + title_height - 600 + 4 * 30,
                                    30, 30,
                                    fill=tot_color_array["2"], stroke='black'))
        tot_percent_amount = "%.1f" % (tot_percents_arr[2][0] * 100)
        tot_info = "Interactive: " + str(tot_totals_arr[2][0]) + " hrs, " + str(tot_percent_amount) + " %"
        d.append(draw.Text(tot_info, 30,
                           title_offset_x + 635, title_offset_y + title_height - 600 + 4 * 30,
                           fill='black'))

        d.append(draw.Rectangle(title_offset_x + 600, title_offset_y + title_height - 600 + 3 * 30,
                                    30, 30,
                                    fill=tot_color_array["3"], stroke='black'))
        tot_percent_amount = "%.1f" % (tot_percents_arr[3][0] * 100)
        tot_info = "Passive: " + str(tot_totals_arr[3][0]) + " hrs, " + str(tot_percent_amount) + " %"
        d.append(draw.Text(tot_info, 30,
                           title_offset_x + 635, title_offset_y + title_height - 600 + 3 * 30,
                           fill='black'))

        d.append(draw.Rectangle(title_offset_x + 600, title_offset_y + title_height - 600 + 2 * 30,
                                    30, 30,
                                    fill=tot_color_array["4"], stroke='black'))
        tot_percent_amount = "%.1f" % (tot_percents_arr[4][0] * 100)
        tot_info = "Exercise: " + str(tot_totals_arr[4][0]) + " hrs, " + str(tot_percent_amount) + " %"
        d.append(draw.Text(tot_info, 30,
                           title_offset_x + 635, title_offset_y + title_height - 600 + 2 * 30,
                           fill='black'))

        d.append(draw.Rectangle(title_offset_x + 600, title_offset_y + title_height - 600 + 1 * 30,
                                    30, 30,
                                    fill=tot_color_array["5"], stroke='black'))
        tot_percent_amount = "%.1f" % (tot_percents_arr[5][0] * 100)
        tot_info = "Maintenance: " + str(tot_totals_arr[5][0]) + " hrs, " + str(tot_percent_amount) + " %"
        d.append(draw.Text(tot_info, 30,
                           title_offset_x + 635, title_offset_y + title_height - 600 + 1 * 30,
                           fill='black'))
        tot_info = "Total Logged for Month: " + str(tot_totals_arr[0][0]) + " hrs, "
        d.append(draw.Text(tot_info, 30,
                           title_offset_x + 635, title_offset_y + title_height - 600 + 0 * 30,
                           fill='black'))
        print("on to next month")


    current_number_of_projects = 0
    number_of_projects_per_month = 0
    number_of_projects_per_month_max = 0

    # Set up the month_task dictionaries for use going through the action df
    task_list = {}
    month_task_plan = {}
    month_task_actual = {}
    month_task_total_actual_hours = {}
    for ind in dfmp.index:
        month_task_plan[(dfmp['yyyy_mm'][ind], dfmp['task'][ind])] = dfmp['planned_hours'][ind]
        month_task_actual[(dfmp['yyyy_mm'][ind], dfmp['task'][ind])] = 0
        month_task_total_actual_hours[dfmp['yyyy_mm'][ind]] = 0
        if ((dfmp['task'][ind]) in task_list.keys()):
            task_list[dfmp['task'][ind]] = 1 + task_list[dfmp['task'][ind]]
        else:
            task_list[dfmp['task'][ind]] = 1
    task_list_keys = list(sorted(task_list.keys()))

    #print(task_list)
    #print("list of keys: ",task_list_keys)
    #for i in task_list_keys:
    #    print(i)

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

        if ((df['yyyy_mm'][ind], df['task'][ind]) in month_task_actual):
            month_task_actual[(df['yyyy_mm'][ind], df['task'][ind])] = df['amount'][ind] \
                                                + month_task_actual[(df['yyyy_mm'][ind], df['task'][ind])]
            month_task_total_actual_hours[df['yyyy_mm'][ind]] = df['amount'][ind] \
                                                + month_task_total_actual_hours[df['yyyy_mm'][ind]]

    number_of_tot_proj_min = 25
    if number_of_projects_per_month_max > number_of_tot_proj_min:
        number_of_tot_proj = number_of_projects_per_month_max
    else:
        number_of_tot_proj = number_of_tot_proj_min

    #print('plan=> ',month_task_plan)
    #print('actual=> ',month_task_actual)
    #time.sleep(10)

    #initialize the task display array
    task_display = [[0 for x in range(3)] for y in range(16)]
    for y in range(16):
        task_display[y][0] = "-"
        task_display[y][1] = "-"
        task_display[y][2] = "#AAAAAA"
        #print(task_display)
    #time.sleep(10)

    task_width = 100
    task_height = 8
    default_gap = 50
    paper_to_border_offset_x = default_gap
    paper_to_border_offset_y = default_gap

    available_hours_width = 200
    available_hours_height = 3000  # 31 days * task_height * 12 h/day rounded up
    avail_hrs_zero_height = 500  # allows for more time logged than normal
    available_hours_offset_x = paper_to_border_offset_x
    available_hours_offset_y = paper_to_border_offset_y + available_hours_height + avail_hrs_zero_height

    cal_day_width = 110
    cal_day_height = 110
    cal_total_width = cal_day_width * 7
    cal_total_height = cal_day_height * 6
    cal_offset_x = available_hours_offset_x
    cal_offset_y = available_hours_offset_y + cal_total_height + default_gap



    avail_hrs_charts_width    = available_hours_width + default_gap
    current_available_offset_y = 0
    avail_hrs_charts_offset_x = available_hours_offset_x - default_gap / 2


    balances_width = task_width * number_of_tot_proj
    balances_height = 350
    balances_offset_x = available_hours_offset_x + available_hours_width + default_gap
    balances_offset_y = available_hours_offset_y


    # the month chart label positions are calculated while the month chart is generated
    month_chart_label_height = 100  # this provides the gap where the labels are printed
    # the month chart label x offsets are calculated while the month chart is generated
    # the month chart label y offsets are calculated while the month chart is generated

    month_chart_offset_x = balances_offset_x
    month_chart_offset_y = balances_offset_y + balances_height + default_gap + month_chart_label_height
    month_chart_width = task_width * number_of_tot_proj
    month_chart_height = available_hours_height - avail_hrs_zero_height

    title_offset_x = cal_offset_x + cal_total_width + default_gap
    title_offset_y = cal_offset_y
    title_width = balances_offset_x + balances_width - title_offset_x
    title_height = cal_total_height

    border_width             = balances_offset_x + balances_width + default_gap
    border_height            = available_hours_offset_y + available_hours_height + default_gap

    drawing_width            = border_width + paper_to_border_offset_x
    drawing_height           = border_height + paper_to_border_offset_y


    starting_day_number = 0
    month_number_of_days = 0
    avail_hrs_diff_height = 10

    #start changing chart

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

    # In this for loop, as the dataframe is stepped through,
    # there is a check for if yyyy-mm has changed.
    # If it has then the calendar area is filled in and arrays reset,
    # previous month's report is saved to file.
    # the report page is setup for the new yyyy-mm
    # else the step through the dataframe continues.
    for ind in df.index:
        df_date = datetime.date.fromisoformat(df['date'][ind])
        #print("this is the next row to be processed: ", df_date)

        if current_month != df['yyyy_mm'][ind]:
            previous_month = current_month
            if drawing_obj_flag:
                # totals found from previous months
                # fill in available hours stats
                # fill in calendar hours by calling  function
                fill_in_calendar_area(previous_month, tot_totals_arr)

                #date_given = datetime.datetime(year=2019, month=7, day=30).date()
                print("\nNumber of week in the month: ", week_number_of_month(df_date), "\n")
                #if week_number_of_month(df_date) == 6:
                    #time.sleep(1)
                # fill in balance focus details
                # save drawing obj to file
                file_output = current_month + "_rpt.svg"
                d.save_svg(path_output + "/" + file_output)
                d.save_svg(path_output_web + "/" + file_output)
                # del drawing_object
                del d
                drawing_obj_flag = False

            # establish drawing object and set flag
            d = draw.Drawing(drawing_width, drawing_height, origin=(0, 0), id='map-svg')
            drawing_obj_flag = True

            current_number_of_projects = 0

            # print out statistis from last month before resetting arrays

            current_month = df['yyyy_mm'][ind]
            # start new month
            df_date = datetime.date.fromisoformat(df['date'][ind])
            (starting_day_number, month_number_of_days) = monthrange(int(df_date.strftime("%y")),
                                                                     int(df_date.strftime("%m")))
            print(df_date,starting_day_number, month_number_of_days)
            print(current_month)
            #time.sleep(5)
            available_hours[0] = 0
            available_cumulative_hours[0] = 0
            available_hours_logged[0] = 0
            focus_hours[0] = 0
            focus_cumulative_hours[0] = 0
            focus_hours_logged[0] = 0
            planned_hours[0] = 0
            planned_cumulative_hours[0] = 0
            planned_hours_logged[0] = 0
            for i in range(1, month_number_of_days + 1):  # need to add 1 to get full month
                cm_date = datetime.date.fromisoformat(str(df_date.year)
                                              + "-" + str(df_date.month).zfill(2)
                                              + "-" + str(i).zfill(2))
                #print(i,cm_date)
                if cm_date.weekday() == 6:
                    available_hours[i] = 8
                    available_cumulative_hours[i] = available_hours[i] + available_cumulative_hours[i-1]
                    focus_hours[i] = 3
                    focus_cumulative_hours[i] = focus_hours[i] + focus_cumulative_hours[i-1]
                    planned_hours[i] = 2
                    planned_cumulative_hours[i] = planned_hours[i] + planned_cumulative_hours[i-1]

                else:
                    available_hours[i] = 10
                    available_cumulative_hours[i] = available_hours[i] + available_cumulative_hours[i - 1]
                    focus_hours[i] = 5
                    focus_cumulative_hours[i] = focus_hours[i] + focus_cumulative_hours[i - 1]
                    planned_hours[i] = 2.5
                    planned_cumulative_hours[i] = planned_hours[i] + planned_cumulative_hours[i-1]

                available_hours_logged[i] = 0
                focus_hours_logged[i] = 0
                planned_hours_logged[i] = 0

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

            #start the grouping of the chart
            #group = draw.Group()

            # end the grouping of the chart
            #d.append(group)


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
            # jjj working on this area
            d.append(draw.Text("Month Chart: " + current_month, 120, month_chart_offset_x + month_chart_width/2 - 620,
                               month_chart_offset_y + 280 * task_height + 12, fill='black'))


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
            d.append(draw.Text("TLA: " + str(available_cumulative_hours[month_number_of_days]), 25,
                               available_hours_offset_x,
                               current_available_offset_y + 2 * task_height,
                               fill='black'))
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
                                fill="#00C0F0"))  # light blue
                d.append(draw.Text("CFA: " + str(focus_cumulative_hours[month_number_of_days - today_day_of_month]),
                                25,
                                avail_hrs_charts_offset_x,
                                available_hours_offset_y + avail_hrs_zero_height + \
                                focus_cumulative_hours[month_number_of_days - today_day_of_month] * task_height - 30,
                                fill='black'))


                avail_hrs_diff_height = available_cumulative_hours[month_number_of_days - today_day_of_month] \
                                        - focus_cumulative_hours[month_number_of_days - today_day_of_month]

                d.append(draw.Rectangle(avail_hrs_charts_offset_x,
                                available_hours_offset_y
                                + avail_hrs_zero_height
                                + focus_cumulative_hours[month_number_of_days - today_day_of_month] * task_height,
                                avail_hrs_charts_width,
                                avail_hrs_diff_height * task_height,
                                fill="#32CD32"))  # light green
                d.append(draw.Text("CLA: " + str(available_cumulative_hours[month_number_of_days - today_day_of_month]),
                                25,
                                avail_hrs_charts_offset_x,
                                available_hours_offset_y
                                + avail_hrs_zero_height
                                + focus_cumulative_hours[month_number_of_days - today_day_of_month] * task_height
                                + avail_hrs_diff_height * task_height
                                - 30,
                                fill='black'))

            # determine calendar shape and plot, calendar area is filled out
            # using the fill_in_calendar_area(tot_totals_arr) function just
            # before the previous month report is saved to file.
            d.append(draw.Rectangle(cal_offset_x, cal_offset_y,
                                    cal_total_width, cal_total_height,
                                    fill=day_color))



            # draw title area
            d.append(draw.Rectangle(title_offset_x, title_offset_y,
                                    title_width, title_height,
                                    fill=day_color))
            # fill in title area
            today_date_label = "Date created: " + str(today_date)
            d.append(draw.Text(today_date_label, 50,
                               title_offset_x, title_offset_y,
                               fill='black'))
            d.append(draw.Text("Month Chart:" + current_month, 50,
                               title_offset_x, title_offset_y + title_height - 50,
                               fill='black'))
            d.append(draw.Text("Total Loggable Hours Available (TLA): "
                               + str(available_cumulative_hours[month_number_of_days]), 50,
                               title_offset_x, title_offset_y + title_height - 100,
                               fill='black'))

            if today_yyyy_mm == current_month:
                d.append(draw.Text("Current Loggable Hours Available (CLA): "
                                   + str(available_cumulative_hours[month_number_of_days - today_day_of_month]), 50,
                                   title_offset_x, title_offset_y + title_height - 150,
                                   fill='black'))
                d.append(draw.Text("Current Focus Hours Available (CFA): "
                                   + str(focus_cumulative_hours[month_number_of_days - today_day_of_month]), 50,
                                   title_offset_x, title_offset_y + title_height - 200,
                                   fill='black'))

            # Balances
            d.append(draw.Rectangle(balances_offset_x, balances_offset_y,
                                    balances_width, balances_height,
                                    fill=day_color))

            ###month_task_actual[(df['yyyy_mm'][ind], df['task'][ind])]
            ###month_task_plan[(dfmp['yyyy_mm'][ind], dfmp['task'][ind])]
            ###task_list[dfmp['task'][ind]]
            ###    #for i in task_list_keys:
            ###    #    print(i)

            tdindex = 0
            month_task_pa_total_balance = 0
            current_mp_y_offset = available_hours_offset_y + avail_hrs_zero_height
            for i in task_list_keys:
                if ((current_month, i) in month_task_plan):
                    task_balance = month_task_plan[(current_month, i)] - \
                                   month_task_actual[(current_month, i)]
                    task_display[tdindex][0] = i
                    task_display[tdindex][1] = str(month_task_plan[(current_month, i)]) + \
                                                " - " + \
                                               str(month_task_actual[(current_month, i)]) + \
                                                " = " + str(task_balance)
                    month_task_pa_ratio = month_task_actual[(current_month, i)] / month_task_plan[(current_month, i)]

                    if month_task_pa_ratio > 1.3:
                        task_display[tdindex][2] = '#FFB6C1'  # light red
                    elif month_task_pa_ratio > 1.0:
                        task_display[tdindex][2] = '#FFFDD0'  # light yellow
                    elif month_task_pa_ratio == 1.0:
                        task_display[tdindex][2] = '#00FF00'  # green
                    elif month_task_pa_ratio >= .6:
                        task_display[tdindex][2] = '#C7F6B6'  # light green
                    elif month_task_pa_ratio == 0:
                        task_display[tdindex][2] = '#9292D3'  # darker blue
                    else:
                        task_display[tdindex][2] = '#CCCCEA'  # light blue

                    if month_task_pa_ratio < 1.0:  # completed tasks are not shown needing more time on graph
                        month_task_pa_total_balance = task_balance + month_task_pa_total_balance
                        #print("draw amount: ", task_display[tdindex][0])
                        d.append(draw.Rectangle(available_hours_offset_x - 15,
                                            current_mp_y_offset,
                                            task_width,
                                            task_balance * task_height,
                                            stroke="black", fill=task_display[tdindex][2]))
                        d.append(draw.Text(task_display[tdindex][0], 6, available_hours_offset_x - 15,
                                           current_mp_y_offset, fill='black'))

                        current_mp_y_offset = task_balance * task_height + current_mp_y_offset

                    tdindex = tdindex + 1

                #print("mnod= ", month_number_of_days)
                #print("tdom= ",today_day_of_month)
                #print("pch=", planned_cumulative_hours)
                #print("pch2=", planned_cumulative_hours[2])
                #print("pch1=", planned_cumulative_hours[1])
                #print("pch0=", planned_cumulative_hours[0])

                month_task_pa_total_diff = month_task_pa_total_balance \
                                            - planned_cumulative_hours[(month_number_of_days - today_day_of_month)]

                if month_number_of_days >  today_day_of_month:
                    month_task_pa_total_ratio = month_task_pa_total_balance \
                                            / planned_cumulative_hours[(month_number_of_days - today_day_of_month)]
                else:
                    month_task_pa_total_ratio = 1

                if month_task_pa_total_ratio > 1.3:
                    month_task_pa_total_ratio_color = '#FFB6C1'  # light red
                elif month_task_pa_total_ratio > 1.0:
                    month_task_pa_total_ratio_color = '#FFFDD0'  # light yellow
                elif month_task_pa_total_ratio == 1.0:
                    month_task_pa_total_ratio_color = '#00FF00'  # green
                elif month_task_pa_total_ratio >= .6:
                    month_task_pa_total_ratio_color = '#C7F6B6'  # light green
                elif month_task_pa_total_ratio == 0:
                    month_task_pa_total_ratio_color = '#9292D3'  # darker blue
                else:
                    month_task_pa_total_ratio_color = '#CCCCEA'  # light blue

            # draw planned cumulative hours box and label
            d.append(draw.Rectangle(available_hours_offset_x + 115,
                                available_hours_offset_y + avail_hrs_zero_height,
                                100,
                                planned_cumulative_hours[month_number_of_days - today_day_of_month] * task_height,
                                stroke = "black", fill=month_task_pa_total_ratio_color))  # light red
            d.append(draw.Text("ATP: " + str(planned_cumulative_hours[month_number_of_days - today_day_of_month]), 20,
                                available_hours_offset_x + 115, available_hours_offset_y + avail_hrs_zero_height -30,
                                fill='black'))
            d.append(draw.Text("APR: " + '{0:.2f}'.format(month_task_pa_total_ratio), 20,
                                available_hours_offset_x + 115, available_hours_offset_y + avail_hrs_zero_height -60,
                                fill='black'))
            d.append(draw.Text("Hours Available For Planned Tasks (APT): "
                               + str(planned_cumulative_hours[month_number_of_days - today_day_of_month]), 50,
                               title_offset_x, title_offset_y + title_height - 250,
                               fill='black'))
            # label current month task pa total balance
            d.append(draw.Text("BAT: " + str(month_task_pa_total_balance), 20,
                                available_hours_offset_x - 15, available_hours_offset_y + avail_hrs_zero_height -30,
                                fill='black'))
            d.append(draw.Text("APD: " + str(month_task_pa_total_diff), 20,
                                available_hours_offset_x - 15, available_hours_offset_y + avail_hrs_zero_height -60,
                                fill='black'))
            d.append(draw.Text("Balance of Actual Task Hours (BAT): "
                               + str(month_task_pa_total_balance), 50,
                               title_offset_x, title_offset_y + title_height - 300,
                               fill='black'))
            d.append(draw.Text("Actual to Planned Ratio (APR): "
                               + '{0:.2f}'.format(month_task_pa_total_ratio), 50,
                               title_offset_x, title_offset_y + title_height - 350,
                               fill='black'))
            d.append(draw.Text("Actual to Planned Difference (APD): "
                               + '{0:.2f}'.format(month_task_pa_total_diff), 50,
                               title_offset_x, title_offset_y + title_height - 400,
                               fill='black'))


            # fill in Balance area
            d.append(draw.Text(task_display[0][0], 25, balances_offset_x + 50,
                               balances_offset_y + 3 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[0][1], 25, balances_offset_x + 50,
                               balances_offset_y + 3 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x,
                                    balances_offset_y + 3 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[0][2]))

            d.append(draw.Text(task_display[1][0], 25, balances_offset_x + 50,
                               balances_offset_y + 2 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[1][1], 25, balances_offset_x + 50,
                               balances_offset_y + 2 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x,
                                    balances_offset_y + 2 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[1][2]))

            d.append(draw.Text(task_display[2][0], 25, balances_offset_x + 50,
                               balances_offset_y + balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[2][1], 25, balances_offset_x + 50,
                               balances_offset_y + balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x,
                                    balances_offset_y + balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[2][2]))

            d.append(draw.Text(task_display[3][0], 25, balances_offset_x + 50,
                               balances_offset_y + 40, fill='black'))
            d.append(draw.Text(task_display[3][1], 25, balances_offset_x + 50,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x,
                                    balances_offset_y,
                                    45, 55, stroke = "black", fill=task_display[3][2]))

            d.append(draw.Text(task_display[4][0], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + 3 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[4][1], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + 3 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/4,
                                    balances_offset_y + 3 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[4][2]))

            d.append(draw.Text(task_display[5][0], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + 2 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[5][1], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + 2 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/4,
                                    balances_offset_y + 2 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[5][2]))

            d.append(draw.Text(task_display[6][0], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[6][1], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/4,
                                    balances_offset_y + balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[6][2]))

            d.append(draw.Text(task_display[7][0], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + 40, fill='black'))
            d.append(draw.Text(task_display[7][1], 25, balances_offset_x + balances_width/4 + 50,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/4,
                                    balances_offset_y + 5,
                                    45, 55, stroke = "black", fill=task_display[7][2]))

            d.append(draw.Text(task_display[8][0], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + 3 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[8][1], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + 3 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/2,
                                    balances_offset_y + 3 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[8][2]))

            d.append(draw.Text(task_display[9][0], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + 2 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[9][1], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + 2 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/2,
                                    balances_offset_y + 2 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[9][2]))

            d.append(draw.Text(task_display[10][0], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[10][1], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/2,
                                    balances_offset_y + balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[10][2]))

            d.append(draw.Text(task_display[11][0], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + 40, fill='black'))
            d.append(draw.Text(task_display[11][1], 25, balances_offset_x + balances_width/2 + 50,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width/2,
                                    balances_offset_y + 5,
                                    45, 55, stroke = "black", fill=task_display[11][2]))

            d.append(draw.Text(task_display[12][0], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + 3 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[12][1], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + 3 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width*3/4,
                                    balances_offset_y + 3 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[12][2]))

            d.append(draw.Text(task_display[13][0], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + 2 * balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[13][1], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + 2 * balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width*3/4,
                                    balances_offset_y + 2 * balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[13][2]))

            d.append(draw.Text(task_display[14][0], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + balances_height/4 + 40, fill='black'))
            d.append(draw.Text(task_display[14][1], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + balances_height/4 + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width*3/4,
                                    balances_offset_y + balances_height/4 + 5,
                                    45, 55, stroke = "black", fill=task_display[14][2]))

            d.append(draw.Text(task_display[15][0], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + 40, fill='black'))
            d.append(draw.Text(task_display[15][1], 25, balances_offset_x + balances_width*3/4 + 50,
                               balances_offset_y + 5, fill='black'))
            d.append(draw.Rectangle(balances_offset_x + balances_width*3/4,
                                    balances_offset_y + 5,
                                    45, 55, stroke = "black", fill=task_display[15][2]))

            # reinitialize the various variables to start new month after they have been used.

            # reinitialize the task display array
            for y in range(16):
                task_display[y][0] = "-"
                task_display[y][1] = "-"
                task_display[y][2] = "#AAAAAA"
                #print(task_display)

            # reset tot_totals_arr, percentages array and color array after use in cal and title areas
            tot_totals_rows = 6  # 1 for month and 5 for each type of thought
            tot_totals_cols = 32
            tot_totals_arr = [[0 for j in range(tot_totals_cols)] for i in range(tot_totals_rows)]
            tot_percents_arr = [[0 for j in range(tot_totals_cols)] for i in range(tot_totals_rows)]
            tot_totals_rows_rgb = 3 # 3 for each rgb value
            tot_color_arr = [[day_gray_level for j in range(tot_totals_cols)] for i in range(tot_color_rows_rgb)]
            #print("print totals arr after reinilize: ", tot_totals_arr)
            #print("print percents arr after reinilize: ", tot_percents_arr)
            #print("print color arr after reinilize: ", tot_color_arr)

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

        # for current row of df

        # This is where the calendar day tot totals array are accumulated ......
        # this happens after the previous month's data is output.
        index_of_tot = int(df['types_of_thought'][ind][0:1]) # this pulls first char from types of thought
        #print(index_of_tot)
        day_of_month = datetime.date.fromisoformat(df['date'][ind]).day
        #print("day of the month"+str(day_of_month))
        tot_totals_arr[index_of_tot][day_of_month] = tot_totals_arr[index_of_tot][day_of_month] + df['amount'][ind]
        tot_totals_arr[0][day_of_month] = tot_totals_arr[0][day_of_month] + df['amount'][ind]
        tot_totals_arr[index_of_tot][0] = tot_totals_arr[index_of_tot][0] + df['amount'][ind]
        tot_totals_arr[0][0] = tot_totals_arr[0][0] + df['amount'][ind]
        #print(tot_totals_arr)
        #time.sleep(1)

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
        fill_in_calendar_area(current_month, tot_totals_arr)

        file_output = current_month + "_rpt.svg"
        d.save_svg(path_output + "/" + file_output)
        d.save_svg(path_output + "/current_month_rpt.svg")
        d.save_svg(path_output_web + "/" + file_output)
        d.save_svg(path_output_web + "/current_month_rpt.svg")
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
    import drawsvg as draw

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

    #print("start through dataframe")
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







        """
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
        """

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



    d.save_svg('yearsdisp.svg')



    #print("done with years display")



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
    print_hi('PyCharm')
    create_monthly_display()
    create_years_display()
    create_heatmap()
    import_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
