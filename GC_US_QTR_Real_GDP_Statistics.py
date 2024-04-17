#Get US QTR Real GDP data
#Compute the QoQ Real GDP Growth (between 2 quarters, 1 quarter apart)
#Compute the QoQ Real GDP Growth ANNUALISED (between 2 quarters, 1 quarter apart)
#Plot the US Real GDP QoQ Growth ANNUALISED
#Plot the US Real GDP QoQ Growth ANNUALISED Bar Plot
#Generate Statistics for the US Real GDP QoQ Growth ANNUALISED
#Plot the US Real GDP QoQ Growth ANNUALISED Histogram
import GC_Image_Handler
import argparse
from fredapi import Fred
import matplotlib.pyplot as plt
import pandas as pd

###################################################################################################
def Fred_Get_Real_GDP_Data(filenameStr = "US_Real_GDP.csv"):
    #Read file
    fred_key_filename = "C:\\WQ_Fred_Key.txt"
    with open(fred_key_filename, 'r') as file:
        FRED_API_KEY = file.read().replace('\n', '')
        fred = Fred(api_key=FRED_API_KEY)

    setSeries = "GDPC1"
    fred_data = fred.get_series(setSeries)

    # print("US Real GDP (Quarterly)")
    print("https://fred.stlouisfed.org/series/GDPC1")

    #Convert to DataFrame
    fred_data = pd.DataFrame(fred_data)

    #Set index to Date
    fred_data.index.names = ["Date"]
 
    #Rename column to US Real GDP
    fred_data.columns = ["US Real GDP"]

    # print(fred_data.info())
    # print(fred_data.head(3))
    # print(fred_data.tail(3))
    # input("==========================================")

    return fred_data

###################################################################################################
def Fred_Real_GDP_QoQ_Growth_Annualised(fred_data):
    #Compute %QoQ Growth
    #Values are computed to PERCENTAGE values  
    fred_data['QoQ_Growth_pct'] = (fred_data['US Real GDP'].pct_change() * 100).round(3)
    fred_data['Annualised_Growth_pct'] = (((1 + fred_data['QoQ_Growth_pct'] / 100)**4 - 1) * 100).round(3)

    #Remove NaN values
    fred_data = fred_data.dropna()

    # print(fred_data.info())
    # print(fred_data.head(3))
    # print(fred_data.tail(3))
    # input("==========================================")

    return fred_data

###################################################################################################
def Fred_Save_Real_GDP_Data(fred_data, filenameStr = "US_Real_GDP.csv"):
    #Save to csv
    fred_data.to_csv(filenameStr)

def Fred_Read_Real_GDP_Data(filenameStr = "US_Real_GDP.csv"):
    fred_data = pd.read_csv(args.csv)

    #Set index to Date
    fred_data.set_index("Date", inplace=True)

    #Parse Date string into datetime exclude time
    fred_data.index = pd.to_datetime(fred_data.index).date

    fred_data.index.names = ["Date"]

    # print(fred_data.info())
    # print(fred_data.head(3))
    # print(fred_data.tail(3))
    # print(fred_data.index[0])
    # print(type(fred_data.index[0]))
    # input("==========================================")
    return fred_data

###################################################################################################
def Plot_US_Real_GDP_QoQ_Annualised(fred_data, setName = "Annualised_Growth_pct", plot_type = "AREA_PLOT", lastN = -1):
    mean = fred_data[setName].mean()
    sd = fred_data[setName].std()

    if lastN > 0:
        fred_data = fred_data[-lastN:]

    plt.figure(figsize=(20, 10))
    if plot_type == "AREA_PLOT":
        #Compute monthly returns mean
        #Plot Date,M2_Monthly and reduce frequency of x-axis
        #Fill above mean with green, below mean with red
        plt.fill_between(fred_data.index, fred_data[setName], mean, where = fred_data[setName] > mean, facecolor = "green", interpolate = True)
        plt.fill_between(fred_data.index, fred_data[setName], mean, where = fred_data[setName] < mean, facecolor = "red", interpolate = True)

    else:
        #Column plot, green for above mean, red for below mean
        #Adjust sizing if less than 30 data points
        if len(fred_data.index) < 30:
            setWidth = len(fred_data.index) / 30 * 20
        else: 
            setWidth = len(fred_data.index) / 30 * 5

        #Plot bar chart
        plt.bar(fred_data.index, fred_data[setName], color = ['red' if x < mean else 'green' for x in fred_data[setName]], width = setWidth)

    #Remove empty space on x-axis
    plt.xlim(fred_data.index[0], fred_data.index[-1])

    #Plot SD
    Plot_Standard_Deviation_Lines(mean, sd)

    #Label y-axis text for each SD
    Plot_Standard_Deviation_Text(mean, sd, fred_data)

    Plot_Text_Last_Entry(fred_data, setName)

    if lastN < 0:
        title = "US Real GDP Growth %QoQ Annualised "
    else:
        title = "US Real GDP Growth %QoQ Annualised " + str(lastN) + " Quarters"
    plt.title(title, fontsize=15, fontweight = 'bold')
    plt.xlabel("Date", fontsize=15, fontweight = 'bold')
    plt.ylabel(title, fontsize=15, fontweight = 'bold')
    plt.grid(True)

    #y-axis on Right side
    plt.gca().yaxis.tick_right()
    # plt.gca().yaxis.set_label_position("right")

    #Set y-axis limits to between 4SD
    plt.ylim(mean - 4 * sd, mean + 4 * sd)

    #add space right of y-axis
    plt.subplots_adjust(right=0.8)  # Adjust the value as needed
    
    #Decrease space left of y-axis
    plt.subplots_adjust(left=0.1)  # Adjust the value as needed

    #x-axis 45 degree rotation
    plt.xticks(rotation=45)

    title = title.replace(" ", "_")[len("US_Real_GDP_"):]
    GC_Image_Handler.Save_Plot_to_Folder("US_Real_GDP", title + ".png", openFile = True)

    # print(fred_data.head(3))
    # print(fred_data.tail(3))
    # input("==========================================")

###################################################################################################
def Plot_Standard_Deviation_Lines(mean, sd):
    one_sd = sd
    two_sd = sd * 2
    three_sd = sd * 3
    plt.axhline(mean, color='black', linewidth=3, linestyle='--')
    plt.axhline(mean - one_sd, color='blue', linewidth=1)
    plt.axhline(mean + one_sd, color='blue', linewidth=1)
    plt.axhline(mean - two_sd, color='orange', linewidth=1)
    plt.axhline(mean + two_sd, color='orange', linewidth=1)
    plt.axhline(mean - three_sd, color='red', linewidth=1)
    plt.axhline(mean + three_sd, color='red', linewidth=1)

###################################################################################################
def Plot_Standard_Deviation_Text(mean, sd, fred_data):
    one_sd = sd
    two_sd = sd * 2
    three_sd = sd * 3
    
    number_of_months = len(fred_data.index) 
    factor = 0.3
   
    #Set SD_OFFSET to be right of +y-axis by total number of months in the data + 3 months
    SD_OFFSET = fred_data.index[-1] + pd.DateOffset(months= int(number_of_months * factor))

    plt.text(SD_OFFSET, mean + three_sd, "+3SD: {:7.3f} %".format(mean + three_sd), fontsize=12, color = 'red', fontweight = 'bold')
    plt.text(SD_OFFSET, mean + two_sd,   "+2SD: {:7.3f} %".format(mean + two_sd), fontsize=12, color = 'orange', fontweight = 'bold')
    plt.text(SD_OFFSET, mean + one_sd,   "+1SD: {:7.3f} %".format(mean + one_sd), fontsize=12, color = 'blue', fontweight = 'bold')
    plt.text(SD_OFFSET, mean, "mean: {:7.3f} %".format(mean), fontsize=12, color = 'black', fontweight = 'bold')
    plt.text(SD_OFFSET, mean - one_sd,   "-1SD: {:7.3f} %".format(mean - one_sd), fontsize=12, color = 'blue', fontweight = 'bold')
    plt.text(SD_OFFSET, mean - two_sd,   "-2SD: {:7.3f} %".format(mean - two_sd), fontsize=12, color = 'orange', fontweight = 'bold')
    plt.text(SD_OFFSET, mean - three_sd, "-3SD: {:7.3f} %".format(mean - three_sd), fontsize=12, color = 'red', fontweight = 'bold')

###################################################################################################
def Plot_Text_Last_Entry(fred_data, setName):
    #Plot text last value with box
    lastDataStr = "   {:3.3f} %".format(fred_data[setName].iloc[-1])

    number_of_months = len(fred_data.index) 
    factor = 0.05
    current_offset = pd.DateOffset(months= int(number_of_months * factor))

    plt.text(fred_data.index[-1] + current_offset, fred_data[setName].iloc[-1], lastDataStr, 
             fontsize=12, color = 'black', fontweight = 'bold',
             bbox=dict(facecolor='white', edgecolor='red', pad=2))

###################################################################################################
def Compute_Statistics(in_data, colName = "Return", pct = True):
    #Find Descriptive Statistics of the Returns data
    #Mean, Standard Deviation, Skewness, Kurtosis
    mean   = (in_data[colName].mean()).round(3)
    sd     = (in_data[colName].std()).round(3)
    #Compute 1,2 and 3 standard deviation values round 2 decimal places
    sd1_pos = (mean + sd).round(3)
    sd2_pos = (mean + 2 * sd).round(3)
    sd3_pos = (mean + 3 * sd).round(3)
    sd1_neg = (mean - sd).round(3)
    sd2_neg = (mean - 2 * sd).round(3)
    sd3_neg = (mean - 3 * sd).round(3)
    skewness = in_data[colName].skew().round(3)
    kurtosis = in_data[colName].kurtosis().round(3)

    print()
    print("Descriptive Statistics:")
    if pct == True:
        print("Count :",len(in_data))
        print("Mean  :", mean.round(3), "%")
        print("SD    :", sd, "%")
        print("1SD   : [", sd1_neg, "% : ", sd1_pos, "%]")
        print("2SD   : [", sd2_neg, "% : ", sd2_pos, "%]")
        print("3SD   : [", sd3_neg, "% : ", sd3_pos, "%]")
    else:
        print("Count :",len(in_data))
        print("Mean  :", mean.round(3))
        print("StdDev:", sd)
        print("1SD   : [", sd1_neg, " : ", sd1_pos, "]")
        print("2SD   : [", sd2_neg, " : ", sd2_pos, "]")
        print("3SD   : [", sd3_neg, " : ", sd3_pos, "]")

    print("Skew  :", in_data[colName].skew().round(3))
    print("Kurt  :",in_data[colName].kurtosis().round(3))

    #Combine all the statistics into a tuple
    return mean, sd1_pos, sd1_neg, sd2_pos, sd2_neg, sd3_pos, sd3_neg, skewness, kurtosis

###################################################################################################
def Plot_Returns_Histogram(in_data, colName = "Return", stat = None, pct = True):
    #Plot all the Returns data into a histogram
    BIN_SIZE = 100

    # plt.rcParams['font.family'] = 'Lucida Console' #Set Font to Lucida Console
    plt.figure(figsize=(20, 12))
    plt.hist(in_data[colName], bins=BIN_SIZE, edgecolor='black')

    #Append % sign for x-axis
    if pct == True:
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
    else:
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

    plt.grid(axis='y')

    #Unpack the tuple
    mean_pct, sd1_pos, sd1_neg, sd2_pos, sd2_neg, sd3_pos, sd3_neg, skewness, kurtosis = stat
    
    #Display the mean and standard deviation lines
    plt.axvline(mean_pct, color='black', linestyle='--', lw=3)
    plt.axvline(sd1_pos, color='blue', linestyle='--', lw=1)
    plt.axvline(sd1_neg, color='blue', linestyle='--', lw=1)
    plt.axvline(sd2_pos, color='orange', linestyle='--', lw=2)
    plt.axvline(sd2_neg, color='orange', linestyle='--', lw=2)
    plt.axvline(sd3_pos, color='red', linestyle='--', lw=3)
    plt.axvline(sd3_neg, color='red', linestyle='--', lw=3)

    #Reduce the intervals to within 3 standard deviation
    x_lower = 1.2 * (sd3_neg)
    x_higher = 1.2 * (sd3_pos)
    plt.xlim(x_lower, x_higher)

    plt.title(colName + " Histogram", fontsize=20, fontweight = 'bold')
    plt.xlabel("Date", fontsize=20, fontweight = 'bold')
    plt.ylabel("Frequency", fontsize=20, fontweight = 'bold')
    plt.grid(True)    
    plt.subplots_adjust(bottom=0.30)  # Increase the bottom margin

    Plot_Text_Statistics(all_stat, BIN_SIZE, in_data, colName, pct = True)
    Plot_Text_Statistics_on_Axis(all_stat, BIN_SIZE, in_data, colName, pct = True)

    colNameStr = colName.replace(" ", "_")
    GC_Image_Handler.Save_Plot_to_Folder("US_Real_GDP", colNameStr + "_Histogram.png", openFile = True)

###################################################################################################
def Plot_Text_Statistics(all_stat, binSize, in_data, colName, pct = True):
    counts, bin_edges = pd.cut(in_data[colName], bins=binSize, retbins=True)
    #Display the counts for each bin on a table
    # print(pd.DataFrame({'Counts': counts.value_counts()})
    #         .sort_index(ascending=True)
    #         .reset_index()
    #         .rename(columns={'index': 'Bin'})
    #         .to_string(index=False))

    mean, sd1_pos, sd1_neg, sd2_pos, sd2_neg, sd3_pos, sd3_neg, skewness, kurtosis = all_stat

    #Count the number of returns within 1SD, 2SD and 3SD
    sd1_count = in_data[colName].apply(lambda x: x > sd1_neg and x < sd1_pos).sum()
    sd2_count = in_data[colName].apply(lambda x: x > sd2_neg and x < sd2_pos).sum()
    sd3_count = in_data[colName].apply(lambda x: x > sd3_neg and x < sd3_pos).sum()

    plt.rcParams['font.family'] = 'Lucida Console' #Set Font to Lucida Console

    #Print Statistics onto plot below x-axis on the left, black background
    OFFSET_TEXT = -0.15
    if pct == True:
        plt.text(0, OFFSET_TEXT - 0.05, f'Count : {len(in_data)}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.10, f'Mean  : {mean:.3f}%', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.15, f'1SD   : [{sd1_neg:7.3f}% : {sd1_pos:7.3f}%]   count: {sd1_count:4}   prob: {sd1_count/len(in_data):.3%}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.20, f'2SD   : [{sd2_neg:7.3f}% : {sd2_pos:7.3f}%]   count: {sd2_count:4}   prob: {sd2_count/len(in_data):.3%}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.25, f'3SD   : [{sd3_neg:7.3f}% : {sd3_pos:7.3f}%]   count: {sd3_count:4}   prob: {sd3_count/len(in_data):.3%}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
    else:
        plt.text(0, OFFSET_TEXT - 0.05, f'Count : {len(in_data)}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.10, f'Mean  : {mean:.3f}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.15, f'1SD   : [{sd1_neg:7.3f} : {sd1_pos:7.3f}]   count: {sd1_count:4}   prob: {sd1_count/len(in_data):.3%}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.20, f'2SD   : [{sd2_neg:7.3f} : {sd2_pos:7.3f}]   count: {sd2_count:4}   prob: {sd2_count/len(in_data):.3%}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
        plt.text(0, OFFSET_TEXT - 0.25, f'3SD   : [{sd3_neg:7.3f} : {sd3_pos:7.3f}]   count: {sd3_count:4}   prob: {sd3_count/len(in_data):.3%}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)

    plt.text(0, OFFSET_TEXT - 0.30, f'Skew  : {skewness:5.3f}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)
    plt.text(0, OFFSET_TEXT - 0.35, f'Kurt  : {kurtosis:5.3f}', ha='left', transform=plt.gca().transAxes, fontweight = 'bold', fontsize = 15)

###################################################################################################
def Plot_Text_Statistics_on_Axis(all_stat, binSize, in_data, colName, pct = True):
    mean, sd1_pos, sd1_neg, sd2_pos, sd2_neg, sd3_pos, sd3_neg, skewness, kurtosis = all_stat

    #set default font
    plt.rcParams['font.family'] = 'Courier New'

    #Plot SD text on Histogram x-axis
    #centralize the text offset below the x-axis
    OFFSET = -4
    if pct == True:
        plt.text(mean, OFFSET, "{:3.3f}%".format(mean), fontsize=20, color = 'black', fontweight = 'bold', ha='center')
        plt.text(sd1_pos, OFFSET, "{:3.3f}%".format(sd1_pos), fontsize=20, color = 'blue', fontweight = 'bold', ha='center')
        plt.text(sd1_neg, OFFSET, "{:3.3f}%".format(sd1_neg), fontsize=20, color = 'blue', fontweight = 'bold', ha='center')
        plt.text(sd2_pos, OFFSET, "{:3.3f}%".format(sd2_pos), fontsize=20, color = 'orange', fontweight = 'bold', ha='center')
        plt.text(sd2_neg, OFFSET, "{:3.3f}%".format(sd2_neg), fontsize=20, color = 'orange', fontweight = 'bold', ha='center')
        plt.text(sd3_pos, OFFSET, "{:3.3f}%".format(sd3_pos), fontsize=20, color = 'red', fontweight = 'bold', ha='center')
        plt.text(sd3_neg, OFFSET, "{:3.3f}%".format(sd3_neg), fontsize=20, color = 'red', fontweight = 'bold', ha='center')
    else:
        plt.text(mean, OFFSET, "{:3.3f}".format(mean), fontsize=20, color = 'black', fontweight = 'bold', ha='center')
        plt.text(sd1_pos, OFFSET, "{:3.3f}".format(sd1_pos), fontsize=20, color = 'blue', fontweight = 'bold', ha='center')
        plt.text(sd1_neg, OFFSET, "{:3.3f}".format(sd1_neg), fontsize=20, color = 'blue', fontweight = 'bold', ha='center')
        plt.text(sd2_pos, OFFSET, "{:3.3f}".format(sd2_pos), fontsize=20, color = 'orange', fontweight = 'bold', ha='center')
        plt.text(sd2_neg, OFFSET, "{:3.3f}".format(sd2_neg), fontsize=20, color = 'orange', fontweight = 'bold', ha='center')
        plt.text(sd3_pos, OFFSET, "{:3.3f}".format(sd3_pos), fontsize=20, color = 'red', fontweight = 'bold', ha='center')
        plt.text(sd3_neg, OFFSET, "{:3.3f}".format(sd3_neg), fontsize=20, color = 'red', fontweight = 'bold', ha='center')


    lastDataStr = "{:3.3f} %".format(in_data[colName].iloc[-1])
    #draw an arrow on the last data point
    #offset below the x-axis
    plt.annotate(lastDataStr, 
                xy=(in_data[colName].iloc[-1], 0), 
                xytext=(in_data[colName].iloc[-1], -6), 
                arrowprops=dict(facecolor='red', shrink=4),
                fontweight='bold', size=20, color='red')

###################################################################################################
###################################################################################################
if __name__ == "__main__":
    GC_Image_Handler.Close_Existing_Image() #Close existing .png file

    parser = argparse.ArgumentParser(description='Description of your script')
    # Add optional argument
    parser.add_argument('-csv', type=str, help='.csv filename')
    # Parse command-line arguments
    args = parser.parse_args()
    # print(args.csv)
    if args.csv is None:
        args.csv = "US_Real_GDP.csv"

    fred_data = Fred_Get_Real_GDP_Data(args.csv)

    #Compute Real GDP %QoQ Growth
    Fred_Real_GDP_QoQ_Growth_Annualised(fred_data)

    Fred_Save_Real_GDP_Data(fred_data, args.csv)

    fred_data = Fred_Read_Real_GDP_Data(args.csv)

    #Plot US Real GDP QoQ Annualised for 
    # Plot_US_Real_GDP_QoQ_Annualised(fred_data, lastN=20)#last 5 years = =5 * 4 = 20 quarters
    Plot_US_Real_GDP_QoQ_Annualised(fred_data, plot_type = "BAR_PLOT", lastN=20)#last 5 years = =5 * 4 = 20 quarters
    Plot_US_Real_GDP_QoQ_Annualised(fred_data, plot_type= "BAR_PLOT")#Full Set

    all_stat = Compute_Statistics(fred_data, colName="Annualised_Growth_pct", pct = True)
    Plot_Returns_Histogram(fred_data, colName = "Annualised_Growth_pct", stat = all_stat, pct = True)
