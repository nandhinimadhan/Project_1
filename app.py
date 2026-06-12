import streamlit as st
import pandas as pd
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password@05",
    database="Project_1"
)

cursor_mysql = connection.cursor()

st.sidebar.title("Traffic Crash Analytics & Safety Intelligence Platform")

st.set_page_config(page_title="Traffic Crash Dashboard", layout="wide")

st.title("🚦Traffic Crash Analysis Dashboard📊")

def run_query(query):
    return pd.read_sql(query, connection)


st.sidebar.title("Analysis Menu")

option = st.sidebar.selectbox(
    "Select Analysis",
    [
        "1. Dangerous Weather-Crash Combinations",
        "2. Streets with Highest Injury Crashes",
        "3. Injury Percentage by Crash Type",
        "4. Peak Crash Hour Per Month",
        "5. Top Night Time Crash Causes",
        "6. Daylight vs Darkness Injuries",
        "7. Traffic Control Device Analysis",
        "8. Crash Hotspots",
        "9. Streets with Highest Injury Rate",
        "10. Most Common Crash Type Per Year",
        "11. Highest Average Crashes Day",
        "12. High Risk Time Buckets",
        "13. Top Causes per Crash Type",
        "14. Year Over Year Growth",
        "15. Hotspot Zones"
    ]
)


if option == "1. Dangerous Weather-Crash Combinations":

    query = """
    SELECT WEATHER_CONDITION,
           CRASH_TYPE,
           COUNT(*) AS TOTAL_CRASHES
    FROM trafficcrashesdata
    GROUP BY WEATHER_CONDITION, CRASH_TYPE
    ORDER BY TOTAL_CRASHES DESC
    LIMIT 5;
    """

    df = run_query(query)

    st.subheader("Top 5 Dangerous Weather-Crash Combinations")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: These weather conditions and crash types contribute to the largest number of accidents."
    )

elif option == "2. Streets with Highest Injury Crashes":

    query = """
    SELECT STREET_NAME,
           COUNT(*) AS INJURY_CRASHES
    FROM trafficcrashesdata
    WHERE INJURIES_TOTAL > 0
    GROUP BY STREET_NAME
    ORDER BY INJURY_CRASHES DESC
    LIMIT 10;
    """

    df = run_query(query)

    st.subheader("Top 10 Streets with Injury Crashes")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: These streets should be prioritized for safety improvements."
    )


elif option == "3. Injury Percentage by Crash Type":

    query = """
    SELECT CRASH_TYPE,

    ROUND(
        SUM(CASE
            WHEN INJURIES_TOTAL > 0 THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),2
    ) AS INJURY_PERCENTAGE

    FROM trafficcrashesdata

    GROUP BY CRASH_TYPE

    ORDER BY INJURY_PERCENTAGE DESC;
    """

    df = run_query(query)

    st.subheader("Injury Percentage by Crash Type")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Higher percentages indicate crash types more likely to result in injuries."
    )

elif option == "4. Peak Crash Hour Per Month":

    query = """
    WITH MonthlyHour AS
    (
        SELECT
        MONTH(CRASH_DATE) AS MONTH_NO,
        CRASH_HOUR,
        COUNT(*) AS TOTAL_CRASHES,

        RANK() OVER(
            PARTITION BY MONTH(CRASH_DATE)
            ORDER BY COUNT(*) DESC
        ) AS RNK

        FROM trafficcrashesdata

        GROUP BY MONTH(CRASH_DATE),
                 CRASH_HOUR
    )

    SELECT *
    FROM MonthlyHour
    WHERE RNK = 1;
    """

    df = run_query(query)

    st.subheader("Peak Crash Hour for Each Month")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Helps identify peak accident hours month-wise."
    )

elif option == "5. Top Night Time Crash Causes":

    query = """
    SELECT PRIM_CONTRIBUTORY_CAUSE,
           COUNT(*) AS TOTAL_CRASHES

    FROM trafficcrashesdata

    WHERE CRASH_HOUR >= 18

    GROUP BY PRIM_CONTRIBUTORY_CAUSE

    ORDER BY TOTAL_CRASHES DESC

    LIMIT 5;
    """

    df = run_query(query)

    st.subheader("Top 5 Night Time Crash Causes")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: These causes dominate accidents after 6 PM."
    )

# ---------------------------------------------------
# 6
# ---------------------------------------------------

elif option == "6. Daylight vs Darkness Injuries":

    query = """
    SELECT LIGHTING_CONDITION,

           ROUND(
           AVG(INJURIES_TOTAL),2
           ) AS AVG_INJURIES

    FROM trafficcrashesdata

    WHERE LIGHTING_CONDITION IN
    ('DAYLIGHT','DARKNESS')

    GROUP BY LIGHTING_CONDITION;
    """

    df = run_query(query)

    st.subheader("Daylight vs Darkness Injury Comparison")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Compares injury severity under different lighting conditions."
    )

elif option == "7. Traffic Control Device Analysis":

    query = """
    SELECT TRAFFIC_CONTROL_DEVICE,

           ROUND(
           AVG(INJURIES_TOTAL),2
           ) AS AVG_INJURIES

    FROM trafficcrashesdata

    GROUP BY TRAFFIC_CONTROL_DEVICE

    ORDER BY AVG_INJURIES DESC

    LIMIT 1;
    """

    df = run_query(query)

    st.subheader("Traffic Control Device with Highest Average Injuries")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Indicates which traffic control setup is linked to severe crashes."
    )

elif option == "8. Crash Hotspots":

    query = """
    SELECT LATITUDE,
           LONGITUDE,
           COUNT(*) AS TOTAL_CRASHES

    FROM trafficcrashesdata

    GROUP BY LATITUDE, LONGITUDE

    ORDER BY TOTAL_CRASHES DESC

    LIMIT 5;
    """

    df = run_query(query)

    st.subheader("Top Crash Hotspots")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: These coordinates experience the highest crash frequency."
    )

elif option == "9. Streets with Highest Injury Rate":

    query = """
    SELECT STREET_NAME,

           COUNT(*) AS TOTAL_CRASHES,

           ROUND(
           SUM(
           CASE
           WHEN INJURIES_TOTAL > 0
           THEN 1
           ELSE 0
           END
           ) * 100.0 / COUNT(*),2
           ) AS INJURY_RATE

    FROM trafficcrashesdata

    GROUP BY STREET_NAME

    HAVING COUNT(*) > 100

    ORDER BY INJURY_RATE DESC

    LIMIT 5;
    """

    df = run_query(query)

    st.subheader("Top Streets with Highest Injury Rate")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: These streets show the greatest likelihood of injury crashes."
    )


elif option == "10. Most Common Crash Type Per Year":

    query = """
    WITH yearly AS
    (
        SELECT
        YEAR(CRASH_DATE) AS YR,

        CRASH_TYPE,

        COUNT(*) AS TOTAL,

        RANK() OVER(
        PARTITION BY YEAR(CRASH_DATE)
        ORDER BY COUNT(*) DESC
        ) AS RNK

        FROM trafficcrashesdata

        GROUP BY YEAR(CRASH_DATE),
                 CRASH_TYPE
    )

    SELECT *
    FROM yearly

    WHERE RNK = 1;
    """

    df = run_query(query)

    st.subheader("Most Common Crash Type Per Year")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Highlights yearly crash trends."
    )


elif option == "11. Highest Average Crashes Day":

    query = """
    SELECT DAYNAME(CRASH_DATE) AS DAY_NAME,

           ROUND(COUNT(*)/24,2)
           AS AVG_CRASHES_PER_HOUR

    FROM trafficcrashesdata

    GROUP BY DAY_NAME

    ORDER BY AVG_CRASHES_PER_HOUR DESC;
    """

    df = run_query(query)

    st.subheader("Average Crashes Per Hour by Day")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Reveals the busiest crash day of the week."
    )

elif option == "12. High Risk Time Buckets":

    query = """
    SELECT

    CASE
    WHEN CRASH_HOUR BETWEEN 6 AND 11
    THEN 'Morning'

    WHEN CRASH_HOUR BETWEEN 12 AND 17
    THEN 'Afternoon'

    WHEN CRASH_HOUR BETWEEN 18 AND 21
    THEN 'Evening'

    ELSE 'Night'
    END AS TIME_BUCKET,

    COUNT(*) AS INJURY_CRASHES

    FROM trafficcrashesdata

    WHERE INJURIES_TOTAL > 0

    GROUP BY TIME_BUCKET

    ORDER BY INJURY_CRASHES DESC;
    """

    df = run_query(query)

    st.subheader("High Risk Time Buckets")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Shows when injury crashes are most frequent."
    )

elif option == "13. Top Causes per Crash Type":

    query = """
    WITH ranked AS
    (
        SELECT

        CRASH_TYPE,

        PRIM_CONTRIBUTORY_CAUSE,

        COUNT(*) AS TOTAL,

        ROW_NUMBER() OVER(
        PARTITION BY CRASH_TYPE
        ORDER BY COUNT(*) DESC
        ) AS RN

        FROM trafficcrashesdata

        GROUP BY CRASH_TYPE,
                 PRIM_CONTRIBUTORY_CAUSE
    )

    SELECT *
    FROM ranked

    WHERE RN <= 3;
    """

    df = run_query(query)

    st.subheader("Top 3 Causes for Each Crash Type")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Identifies leading causes behind each crash category."
    )


elif option == "14. Year Over Year Growth":

    query = """
    WITH yearly AS
    (
        SELECT

        YEAR(CRASH_DATE) AS YR,

        COUNT(*) AS TOTAL_CRASHES

        FROM trafficcrashesdata

        GROUP BY YEAR(CRASH_DATE)
    )

    SELECT

    YR,

    TOTAL_CRASHES,

    ROUND(
    (
    TOTAL_CRASHES -
    LAG(TOTAL_CRASHES)
    OVER(ORDER BY YR)
    )

    /

    LAG(TOTAL_CRASHES)
    OVER(ORDER BY YR)

    *100,2

    ) AS GROWTH_PERCENT

    FROM yearly;
    """

    df = run_query(query)

    st.subheader("Year Over Year Growth Rate")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Displays yearly increase or decrease in crashes."
    )



elif option == "15. Hotspot Zones":

    query = """
    SELECT

    ROUND(LATITUDE,2) AS LAT_ZONE,

    ROUND(LONGITUDE,2) AS LON_ZONE,

    COUNT(*) AS TOTAL_CRASHES

    FROM trafficcrashesdata

    GROUP BY
    ROUND(LATITUDE,2),
    ROUND(LONGITUDE,2)

    ORDER BY TOTAL_CRASHES DESC

    LIMIT 10;
    """

    df = run_query(query)

    st.subheader("Top 10 Hotspot Zones")
    st.dataframe(df, use_container_width=True)

    st.success(
        "Insight: Nearby crash locations are grouped into zones to reveal major accident clusters."
    )

